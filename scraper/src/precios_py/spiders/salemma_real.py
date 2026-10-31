"""
Spider unificado para cadenas regionales clave del Gran Asunción:
- Salemma Online (salemmaonline.com.py)
- Supermercados Real (realonline.com.py)
- Los Jardines Supermercado (losjardinesonline.com.py)
"""

from __future__ import annotations

import logging
import re
from typing import Any

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider

logger = logging.getLogger(__name__)


class SalemmaRealSpider(BaseSupermarketSpider):
    """Soporta 'salemma', 'real' y 'losjardines'."""

    def __init__(self, target: str = "salemma", concurrency: int = 10):
        super().__init__(concurrency=concurrency)
        if target not in ("salemma", "real", "losjardines"):
            raise ValueError("target debe ser 'salemma', 'real' o 'losjardines'")
        self.supermarket_slug = target
        if target == "salemma":
            self.base_url = "https://salemmaonline.com.py"
        elif target == "real":
            self.base_url = "https://realonline.com.py"
        else:
            self.base_url = "https://losjardinesonline.com.py"

    def parse_catalog_payload(self, payload: dict[str, Any] | list[dict[str, Any]]) -> list[ScrapedOffer]:
        items = payload.get("data", payload.get("articles", [])) if isinstance(payload, dict) else payload
        offers: list[ScrapedOffer] = []

        for item in items:
            if not isinstance(item, dict):
                continue

            sku = str(item.get("sku") or item.get("id") or item.get("code") or "").strip()
            raw_title = str(item.get("name") or item.get("title") or item.get("description") or "").strip()
            if not sku or not raw_title:
                continue

            reg_price = parse_guaranies(item.get("regular_price") or item.get("price") or item.get("precio"))
            raw_promo = item.get("sale_price") or item.get("promo_price")
            promo_price = parse_guaranies(raw_promo) if raw_promo else None

            if promo_price is not None and promo_price >= reg_price:
                promo_price = None

            ean = item.get("ean") or item.get("barcode")
            if not ean:
                img_url = item.get("imageUrl") or item.get("image") or ""
                ean = extract_ean_from_text_or_url(f"{img_url} {raw_title}")

            brand = item.get("brand") or item.get("brandName")

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

