"""
Spider para Superseis (superseis.com.py) y Stock (stock.com.py).
Soporta tanto el nuevo DOM en vivo de Superseis (`div.product-thumb`, `span.price-normal`, `span.price-new`, `span.price-old`)
como la plantilla clásica (`div.product-item`).
"""

from __future__ import annotations

import html as html_lib
import re
import urllib.request
from urllib.parse import urljoin

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider

# 1. Selectores para el DOM actual en producción de Superseis (`div.product-thumb`)
LIVE_THUMB_RE = re.compile(
    r'<div[^>]+class="[^"]*product-thumb[^"]*"[^>]*data-product-id="(?P<sku>\d+)"[^>]*>(?P<body>.*?)</form>\s*</div>',
    re.DOTALL | re.IGNORECASE,
)
LIVE_LINK_RE = re.compile(
    r'<a[^>]+href="(?P<href>https?://[^"]+/product/[^"]+)"[^>]*data-product-name="(?P<title>[^"]+)"',
    re.DOTALL | re.IGNORECASE,
)
LIVE_PRICE_NEW_RE = re.compile(
    r'<span[^>]+class="[^"]*price-new[^"]*"[^>]*>(?P<price>.*?)</span>',
    re.DOTALL | re.IGNORECASE,
)
LIVE_PRICE_OLD_RE = re.compile(
    r'<span[^>]+class="[^"]*price-old[^"]*"[^>]*>(?P<price>.*?)</span>',
    re.DOTALL | re.IGNORECASE,
)
LIVE_PRICE_NORMAL_RE = re.compile(
    r'<span[^>]+class="[^"]*price-normal[^"]*"[^>]*>(?P<price>.*?)</span>',
    re.DOTALL | re.IGNORECASE,
)

# 2. Selectores para la estructura clásica (`div.product-item`)
LEGACY_BLOCK_RE = re.compile(
    r'<div[^>]+class="[^"]*product-item[^"]*"[^>]*data-productid="(?P<sku>[^"]+)"[^>]*>(?P<body>.*?)</div>\s*</div>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_TITLE_RE = re.compile(
    r'<a[^>]+href="(?P<href>[^"]+)"[^>]*class="[^"]*product-title-link[^"]*"[^>]*>(?P<title>.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_OLD_PRICE_RE = re.compile(
    r'<span[^>]+class="[^"]*(?:price-old|old-price)[^"]*"[^>]*>(?P<price>.*?)</span>',
    re.DOTALL | re.IGNORECASE,
)
LEGACY_SPECIAL_PRICE_RE = re.compile(
    r'<span[^>]+class="[^"]*(?:price-special|actual-price|price-label)[^"]*"[^>]*>(?P<price>.*?)</span>',
    re.DOTALL | re.IGNORECASE,
)

IMG_SRC_RE = re.compile(r'<img[^>]+src="(?P<src>[^"]+)"', re.IGNORECASE)
DATA_EAN_RE = re.compile(r'data-ean="(?P<ean>[^"]+)"', re.IGNORECASE)
ANY_EAN13_RE = re.compile(r"\b((?:779|784|789|750|780|841)\d{10})\b")


class RetailSaSpider(BaseSupermarketSpider):
    """Soporta tanto 'superseis' como 'stock'."""

    def __init__(self, target: str = "superseis", concurrency: int = 12):
        super().__init__(concurrency=concurrency)
        if target not in ("superseis", "stock"):
            raise ValueError("target debe ser 'superseis' o 'stock'")
        self.supermarket_slug = target
        self.base_url = (
            "https://www.superseis.com.py"
            if target == "superseis"
            else "https://www.stock.com.py"
        )

    def fetch_live_url(self, url: str, enrich_eans_limit: int = 0) -> list[ScrapedOffer]:
        req = urllib.request.Request(url, headers=self.default_headers)
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")
        offers = self.parse_catalog_payload(raw_html)

        # Opcionalmente enriquecer EAN-13 desde la ficha de producto para los primeros N ítems
        for idx, offer in enumerate(offers):
            if idx >= enrich_eans_limit:
                break
            if not offer.ean and offer.product_url.startswith("http"):
                try:
                    detail_req = urllib.request.Request(offer.product_url, headers=self.default_headers)
                    with urllib.request.urlopen(detail_req, timeout=10.0) as d_resp:
                        d_html = d_resp.read().decode("utf-8", errors="ignore")
                        m = ANY_EAN13_RE.search(d_html)
                        if m:
                            offer.ean = extract_ean_from_text_or_url(m.group(1))
                except Exception:
                    pass
        return offers

    def parse_catalog_payload(self, html: str) -> list[ScrapedOffer]:
        offers: list[ScrapedOffer] = []
        seen_skus: set[str] = set()

        # 1. Intentar parsear con el nuevo DOM en vivo (`div.product-thumb`)
        for match in LIVE_THUMB_RE.finditer(html):
            sku = match.group("sku").strip()
            if sku in seen_skus:
                continue
            body = match.group("body")

            link_match = LIVE_LINK_RE.search(body)
            if not link_match:
                continue

            raw_title = html_lib.unescape(link_match.group("title")).strip()
            product_url = urljoin(self.base_url, link_match.group("href").strip())

            p_new_m = LIVE_PRICE_NEW_RE.search(body)
            p_old_m = LIVE_PRICE_OLD_RE.search(body)
            p_norm_m = LIVE_PRICE_NORMAL_RE.search(body)

            p_new = parse_guaranies(p_new_m.group("price")) if p_new_m else None
            p_old = parse_guaranies(p_old_m.group("price")) if p_old_m else None
            p_norm = parse_guaranies(p_norm_m.group("price")) if p_norm_m else None

            if p_old and p_new and p_new < p_old:
                regular_price = p_old
                promo_price = p_new
            else:
                regular_price = p_norm or p_new or p_old
                promo_price = None

            if not regular_price:
                continue

            img_match = IMG_SRC_RE.search(body)
            img_url = urljoin(self.base_url, img_match.group("src")) if img_match else None
            ean = extract_ean_from_text_or_url(img_url, product_url)

            seen_skus.add(sku)
            offers.append(
                ScrapedOffer(
                    supermarket_slug=self.supermarket_slug,
                    external_sku=sku,
                    raw_title=raw_title,
                    regular_price=regular_price,
                    promo_price=promo_price,
                    ean=ean,
                    product_url=product_url,
                    image_url=img_url,
                )
            )

        # 2. Fallback / soporte para DOM clásico (`div.product-item`)
        for match in LEGACY_BLOCK_RE.finditer(html):
            sku = match.group("sku").strip()
            if sku in seen_skus:
                continue
            body = match.group("body")

            title_match = LEGACY_TITLE_RE.search(body)
            if not title_match:
                continue

            raw_title = re.sub(r"<[^>]+>", "", title_match.group("title")).strip()
            href = title_match.group("href").strip()
            product_url = urljoin(self.base_url, href)

            old_price_match = LEGACY_OLD_PRICE_RE.search(body)
            special_price_match = LEGACY_SPECIAL_PRICE_RE.search(body)

            old_price = parse_guaranies(old_price_match.group("price")) if old_price_match else None
            special_price = (
                parse_guaranies(special_price_match.group("price")) if special_price_match else None
            )

            if old_price and special_price and special_price < old_price:
                regular_price = old_price
                promo_price = special_price
            else:
                regular_price = special_price or old_price
                promo_price = None

            if not regular_price:
                continue

            img_match = IMG_SRC_RE.search(body)
            img_url = urljoin(self.base_url, img_match.group("src")) if img_match else None

            ean_attr_match = DATA_EAN_RE.search(match.group(0))
            explicit_ean = ean_attr_match.group("ean") if ean_attr_match else None
            ean = extract_ean_from_text_or_url(explicit_ean, img_url, href)

            seen_skus.add(sku)
            offers.append(
                ScrapedOffer(
                    supermarket_slug=self.supermarket_slug,
                    external_sku=sku,
                    raw_title=raw_title,
                    regular_price=regular_price,
                    promo_price=promo_price,
                    ean=ean,
                    product_url=product_url,
                    image_url=img_url,
                )
            )

        return offers
