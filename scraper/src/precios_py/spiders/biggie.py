"""
Spider en vivo para Biggie Express (api.app.biggie.com.py).
Consume la API REST JSON oficial de artículos y extrae precios regulares, ofertas y códigos EAN-13.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider


class BiggieSpider(BaseSupermarketSpider):
    supermarket_slug = "biggie"
    base_url = "https://biggie.com.py"
    api_url = "https://api.app.biggie.com.py/api/articles"

    def fetch_live_articles(self, take: int = 80, skip: int = 0, query: str | None = None) -> list[ScrapedOffer]:
        params: dict[str, str | int] = {"take": take, "skip": skip}
        if query:
            params["query"] = query
        url = f"{self.api_url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={**self.default_headers, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
        return self.parse_catalog_payload(payload)

    def parse_catalog_payload(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[ScrapedOffer]:
        """
        Soporta tanto el esquema real en producción de `api.app.biggie.com.py/api/articles`
        (`code`, `cbaCode`, `name`, `price`, `priceSaleOffer`, `isOnOffer`, `brand`, `images`)
        como esquemas simplificados de pruebas.
        """
        items = payload.get("items", payload.get("data", [])) if isinstance(payload, dict) else payload
        offers: list[ScrapedOffer] = []

        for item in items:
            if not isinstance(item, dict):
                continue

            sku = str(
                item.get("code") or item.get("id") or item.get("codigo") or item.get("sku") or ""
            ).strip()
            raw_title = str(
                item.get("name") or item.get("nombre") or item.get("descripcion") or ""
            ).strip()
            if not sku or not raw_title:
                continue

            reg_price = parse_guaranies(
                item.get("price") or item.get("precioRegular") or item.get("precio")
            )
            raw_promo = (
                item.get("priceSaleOffer")
                or item.get("precioOferta")
                or item.get("precioPromocional")
                or item.get("promoPrice")
            )
            promo_price = parse_guaranies(raw_promo)

            if not reg_price:
                continue
            if promo_price and promo_price >= reg_price:
                promo_price = None

            # En Biggie, `cbaCode` y `code` contienen el EAN-13 real en productos envasados
            raw_ean = str(
                item.get("cbaCode")
                or item.get("code")
                or item.get("codigoBarras")
                or item.get("ean")
                or ""
            ).strip()

            image_url = item.get("imagenUrl") or item.get("image")
            if not image_url and isinstance(item.get("images"), list) and item["images"]:
                first_img = item["images"][0]
                if isinstance(first_img, dict):
                    image_url = first_img.get("src")

            ean = extract_ean_from_text_or_url(raw_ean, image_url)

            brand_val = item.get("brand") or item.get("marca")
            if isinstance(brand_val, dict):
                brand_name = str(brand_val.get("name") or "").strip() or None
            elif isinstance(brand_val, str):
                brand_name = brand_val.strip() or None
            else:
                brand_name = None

            slug_or_id = item.get("slug") or sku
            offers.append(
                ScrapedOffer(
                    supermarket_slug=self.supermarket_slug,
                    external_sku=sku,
                    raw_title=raw_title,
                    regular_price=reg_price,
                    promo_price=promo_price,
                    ean=ean,
                    brand=brand_name,
                    in_stock=not bool(item.get("isDeleted", False)),
                    product_url=f"{self.base_url}/item/{slug_or_id}",
                    image_url=image_url,
                )
            )

        return offers
