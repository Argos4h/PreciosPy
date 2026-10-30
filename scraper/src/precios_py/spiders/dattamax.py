"""
Spider unificado en vivo para Casa Rica (casarica.com.py) y Supermercados Areté (arete.com.py).
Ambos utilizan el motor Dattamax EcommercePro y exponen el código de barras EAN-13 directamente
en la URL de la imagen del producto (`.../userfiles/images/productos/448/7840369041046.jpg`).
"""

from __future__ import annotations

import html as html_lib
import re
import urllib.request
from urllib.parse import urljoin

from ..models import ScrapedOffer
from ..normalizer import extract_ean_from_text_or_url, parse_guaranies
from .base import BaseSupermarketSpider

PRODUCT_CARD_RE = re.compile(
    r'<div class="product">(?P<body>.*?)<div class="hover-area">',
    re.DOTALL | re.IGNORECASE,
)
PRODUCT_ID_RE = re.compile(r'data-product_id="(?P<sku>\d+)"', re.IGNORECASE)
LINK_RE = re.compile(
    r'<a href="(?P<href>[^"]+)" class="ecommercepro-LoopProduct-link">',
    re.IGNORECASE,
)
IMG_DATA_SRC_RE = re.compile(r'data-src="(?P<src>[^"]+)"', re.IGNORECASE)
TITLE_RE = re.compile(
    r'<h2 class="ecommercepro-loop-product__title">(?P<title>.*?)</h2>',
    re.DOTALL | re.IGNORECASE,
)
INS_PRICE_RE = re.compile(
    r'<ins>\s*<span class="amount">(?P<price>.*?)</span>\s*</ins>',
    re.DOTALL | re.IGNORECASE,
)
DEL_PRICE_RE = re.compile(
    r'<del>\s*<span class="amount">(?P<price>.*?)</span>\s*</del>',
    re.DOTALL | re.IGNORECASE,
)
ALL_AMOUNTS_RE = re.compile(
    r'<span class="amount">(?P<price>[^<]+)</span>',
    re.DOTALL | re.IGNORECASE,
)


class DattamaxSpider(BaseSupermarketSpider):
    """Soporta 'casarica' y 'arete'."""

    def __init__(self, target: str = "casarica", concurrency: int = 10):
        super().__init__(concurrency=concurrency)
        if target not in ("casarica", "arete"):
            raise ValueError("target debe ser 'casarica' o 'arete'")
        self.supermarket_slug = target
        self.base_url = (
            "https://www.casarica.com.py/"
            if target == "casarica"
            else "https://www.arete.com.py/"
        )

    def fetch_live_url(self, relative_or_full_url: str = "") -> list[ScrapedOffer]:
        target_url = urljoin(self.base_url, relative_or_full_url)
        req = urllib.request.Request(target_url, headers=self.default_headers)
        with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")
        return self.parse_catalog_payload(raw_html)

    def parse_catalog_payload(self, html: str) -> list[ScrapedOffer]:
        offers: list[ScrapedOffer] = []
        seen_skus: set[str] = set()

        for match in PRODUCT_CARD_RE.finditer(html):
            body = match.group("body")
            sku_m = PRODUCT_ID_RE.search(body)
            title_m = TITLE_RE.search(body)
            link_m = LINK_RE.search(body)

            if not sku_m or not title_m:
                continue

            sku = sku_m.group("sku").strip()
            if sku in seen_skus:
                continue

            raw_title = html_lib.unescape(re.sub(r"<[^>]+>", "", title_m.group("title"))).strip()
            product_url = urljoin(self.base_url, link_m.group("href")) if link_m else self.base_url

            ins_m = INS_PRICE_RE.search(body)
            del_m = DEL_PRICE_RE.search(body)

            promo_candidate = parse_guaranies(ins_m.group("price")) if ins_m else None
            old_candidate = parse_guaranies(del_m.group("price")) if del_m else None

            regular_price: int | None = None
            promo_price: int | None = None

            if old_candidate and promo_candidate and promo_candidate < old_candidate:
                regular_price = old_candidate
                promo_price = promo_candidate
            else:
                for amt_m in ALL_AMOUNTS_RE.finditer(body):
                    val = parse_guaranies(amt_m.group("price"))
                    if val:
                        regular_price = val
                        break

            if not regular_price:
                continue

            img_m = IMG_DATA_SRC_RE.search(body)
            img_url = urljoin(self.base_url, img_m.group("src")) if img_m else None
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

        return offers

