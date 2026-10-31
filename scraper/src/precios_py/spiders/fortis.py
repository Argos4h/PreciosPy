"""
Spider en vivo para Fortis Mayorista (fortis.com.py) y Box Mayorista (boxmayorista.com.py).
Maneja precios minoristas (por unidad) y mayoristas (por caja/fardo a partir de X unidades),
así como extracción de códigos de barras EAN-13 para el comparador de precios de Paraguay.
"""

from __future__ import annotations

import json
import logging
import re
import urllib.parse
import urllib.request
from typing import Any

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider

logger = logging.getLogger(__name__)


class FortisMayoristaSpider(BaseSupermarketSpider):
    """
    Spider para Fortis Mayorista y Box Mayorista.
    Extrae ofertas minoristas y calcula el descuento mayorista.
    """

    def __init__(self, target: str = "fortis", concurrency: int = 10):
        super().__init__(concurrency=concurrency)
        if target not in ("fortis", "box"):
            raise ValueError("target debe ser 'fortis' o 'box'")
        self.supermarket_slug = target
        self.base_url = (
            "https://www.fortis.com.py"
            if target == "fortis"
            else "https://www.boxmayorista.com.py"
        )
        self.api_url = f"{self.base_url}/api/v1/catalog/products"

    def parse_catalog_payload(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[ScrapedOffer]:
        items = payload.get("products", payload.get("data", [])) if isinstance(payload, dict) else payload
        offers: list[ScrapedOffer] = []

        for item in items:
            if not isinstance(item, dict):
                continue

            sku = str(item.get("sku") or item.get("id") or item.get("code") or "").strip()
            raw_title = str(item.get("name") or item.get("title") or item.get("description") or "").strip()
            if not sku or not raw_title:
                continue

            # Precio minorista regular
            reg_price = parse_guaranies(
                item.get("price") or item.get("regular_price") or item.get("retail_price") or item.get("precio")
            )
            # Precio promo o mayorista por bulto
            raw_promo = item.get("promo_price") or item.get("sale_price") or item.get("wholesale_price")
            promo_price = parse_guaranies(raw_promo) if raw_promo else None

            # Si el precio de oferta es igual o mayor al regular, no es oferta
            if promo_price is not None and promo_price >= reg_price:
                promo_price = None

            # EAN-13
            ean = item.get("barcode") or item.get("ean") or item.get("cbaCode") or item.get("upc")
            if not ean:
                # Buscar en URL de imagen o atributos adicionales
                img_url = item.get("image") or item.get("imageUrl") or item.get("thumbnail") or ""
                ean = extract_ean_from_text_or_url(f"{img_url} {raw_title}")

            brand = item.get("brand") or item.get("brandName")
            if isinstance(brand, dict):
                brand = brand.get("name")

            offers.append(
                ScrapedOffer(
                    supermarket_slug=self.supermarket_slug,
                    external_sku=f"{self.supermarket_slug.upper()}-{sku}",
                    raw_title=raw_title,
                    regular_price=reg_price,
                    promo_price=promo_price,
                    ean=str(ean).strip() if ean else None,
                    brand=str(brand).strip() if brand else None,
                )
            )

        return offers

