"""
Spider en vivo para Tiendas Tuti (tuti.com.py / app Tuti Paraguay).
Tiendas Tuti es la cadena de tiendas de descuento de mayor crecimiento en Asunción, Gran Asunción y Cordillera.
Se caracteriza por precios bajos directos de góndola, marcas propias exclusivas y líderes del mercado.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider

logger = logging.getLogger(__name__)


class TutiSpider(BaseSupermarketSpider):
    supermarket_slug = "tuti"
    base_url = "https://www.tuti.com.py"
    api_url = "https://api.tuti.com.py/v1/products"

    def parse_catalog_payload(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[ScrapedOffer]:
        items = payload.get("data", payload.get("items", [])) if isinstance(payload, dict) else payload
        offers: list[ScrapedOffer] = []

        for item in items:
            if not isinstance(item, dict):
                continue

            sku = str(item.get("code") or item.get("id") or item.get("sku") or "").strip()
            raw_title = str(item.get("description") or item.get("name") or "").strip()
            if not sku or not raw_title:
                continue

            reg_price = parse_guaranies(item.get("price") or item.get("precio"))
            raw_promo = item.get("discountPrice") or item.get("promoPrice")
            promo_price = parse_guaranies(raw_promo) if raw_promo else None

            if promo_price is not None and promo_price >= reg_price:
                promo_price = None

            ean = item.get("barcode") or item.get("ean")
            if not ean:
                img_url = item.get("image") or ""
                ean = extract_ean_from_text_or_url(f"{img_url} {raw_title}")

            brand = item.get("brand") or ("Tuti" if "tuti" in raw_title.lower() else None)

            offers.append(
                ScrapedOffer(
                    supermarket_slug="tuti",
                    external_sku=f"TUTI-{sku}",
                    raw_title=raw_title,
                    regular_price=reg_price,
                    promo_price=promo_price,
                    ean=str(ean).strip() if ean else None,
                    brand=str(brand).strip() if brand else None,
                )
            )

        return offers

