"""
Delta Sync Engine para PreciosPy:
Calcula las variaciones de precios entre dos ejecuciones nocturnas y genera
un paquete delta liviano (< 80 KB) para que la app móvil no necesite descargar
la base de datos completa todos los días.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import ScrapedOffer


@dataclass
class PriceDeltaItem:
    supermarket_slug: str
    external_sku: str
    ean: str | None
    raw_title: str
    old_regular_price: int | None
    new_regular_price: int
    old_promo_price: int | None
    new_promo_price: int | None
    price_changed: bool


@dataclass
class DeltaSyncBundle:
    generated_at: str
    total_offers_analyzed: int
    total_price_changes: int
    total_new_products: int
    updated_offers: list[dict]


class DeltaSyncEngine:
    def compute_delta(
        self,
        previous_offers: Iterable[ScrapedOffer],
        current_offers: Iterable[ScrapedOffer],
    ) -> DeltaSyncBundle:
        prev_map: dict[tuple[str, str], ScrapedOffer] = {
            (o.supermarket_slug, o.external_sku): o for o in previous_offers
        }

        changes: list[PriceDeltaItem] = []
        new_count = 0
        changed_count = 0

        for cur in current_offers:
            key = (cur.supermarket_slug, cur.external_sku)
            prev = prev_map.get(key)

            if prev is None:
                new_count += 1
                changes.append(
                    PriceDeltaItem(
                        supermarket_slug=cur.supermarket_slug,
                        external_sku=cur.external_sku,
                        ean=cur.ean,
                        raw_title=cur.raw_title,
                        old_regular_price=None,
                        new_regular_price=cur.regular_price,
                        old_promo_price=None,
                        new_promo_price=cur.promo_price,
                        price_changed=True,
                    )
                )
            else:
                has_changed = (
                    prev.regular_price != cur.regular_price
                    or prev.promo_price != cur.promo_price
                )
                if has_changed:
                    changed_count += 1
                    changes.append(
                        PriceDeltaItem(
                            supermarket_slug=cur.supermarket_slug,
                            external_sku=cur.external_sku,
                            ean=cur.ean or prev.ean,
                            raw_title=cur.raw_title,
                            old_regular_price=prev.regular_price,
                            new_regular_price=cur.regular_price,
                            old_promo_price=prev.promo_price,
                            new_promo_price=cur.promo_price,
                            price_changed=True,
                        )
                    )

        return DeltaSyncBundle(
            generated_at=datetime.now().isoformat(),
            total_offers_analyzed=len(list(current_offers)),
            total_price_changes=changed_count,
            total_new_products=new_count,
            updated_offers=[asdict(c) for c in changes],
        )

    def export_delta_json(self, bundle: DeltaSyncBundle, output_path: str | Path) -> None:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(bundle), indent=2, ensure_ascii=False), encoding="utf-8")
