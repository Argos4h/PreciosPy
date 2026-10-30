"""
Generador y Motor de Búsqueda Local para el Snapshot SQLite Offline-First (FTS5).
Este módulo compila el archivo `.db` que descarga la app móvil Flutter para hacer búsquedas
en menos de 4 milisegundos sin conexión a internet dentro del supermercado.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .entity_matcher import EntityResolver
from .models import BankPromotion, ScrapedOffer
from .normalizer import calculate_price_per_base_unit, extract_unit_info


class MobileSqliteExporter:
    def __init__(self, db_path: str | Path, schema_sql_path: str | Path):
        self.db_path = Path(db_path)
        self.schema_sql_path = Path(schema_sql_path)
        self.resolver = EntityResolver()

    def initialize_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        schema_sql = self.schema_sql_path.read_text(encoding="utf-8")
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema_sql)
            conn.execute(
                "INSERT OR REPLACE INTO sync_metadata (key, value) VALUES (?, ?)",
                ("snapshot_generated_at", datetime.now().isoformat()),
            )

    def export_catalog_and_offers(
        self,
        supermarkets: list[tuple[int, str, str, bool]],
        offers: Iterable[ScrapedOffer],
        promotions: Iterable[BankPromotion] = (),
    ) -> dict[str, int]:
        """
        Unifica las ofertas mediante Entity Resolution (EAN-13 exacto + Fuzzy Matcher por volumen/marca),
        inserta el catálogo en el SQLite local y reconstruye el índice de búsqueda instantánea FTS5.
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # 1. Insertar supermercados
            supermarket_id_by_slug: dict[str, int] = {}
            for sup_id, slug, name, is_wholesale in supermarkets:
                cur.execute(
                    """
                    INSERT OR REPLACE INTO local_supermarkets (id, slug, name, is_wholesale)
                    VALUES (?, ?, ?, ?)
                    """,
                    (sup_id, slug, name, 1 if is_wholesale else 0),
                )
                supermarket_id_by_slug[slug] = sup_id

            # 2. Resolver entidades cruzadas entre supermercados
            valid_offers = [o for o in offers if o.supermarket_slug in supermarket_id_by_slug]
            unified_groups = self.resolver.resolve_catalog(valid_offers)

            cur.execute("DELETE FROM local_products_fts;")
            cur.execute("DELETE FROM local_products;")
            cur.execute("DELETE FROM local_offers;")

            offers_count = 0

            for group in unified_groups:
                prod_id = group.product_id

                cur.execute(
                    """
                    INSERT OR REPLACE INTO local_products
                    (id, ean, normalized_name, brand, unit_measure, unit_quantity, base_unit, image_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        prod_id,
                        group.canonical_ean,
                        group.canonical_name,
                        group.brand,
                        group.unit_measure,
                        group.unit_quantity,
                        group.base_unit,
                        group.offers[0].image_url if group.offers else None,
                    ),
                )

                cur.execute(
                    """
                    INSERT INTO local_products_fts (product_id, ean, normalized_name, brand)
                    VALUES (?, ?, ?, ?)
                    """,
                    (prod_id, group.canonical_ean or "", group.canonical_name, group.brand or ""),
                )

                for offer in group.offers:
                    sup_id = supermarket_id_by_slug[offer.supermarket_slug]
                    unit_info = extract_unit_info(offer.raw_title)

                    effective_gondola = (
                        min(offer.regular_price, offer.promo_price)
                        if offer.promo_price
                        else offer.regular_price
                    )
                    price_per_base = calculate_price_per_base_unit(effective_gondola, unit_info)

                    cur.execute(
                        """
                        INSERT OR REPLACE INTO local_offers
                        (product_id, supermarket_id, regular_price, promo_price, club_price,
                         wholesale_price, wholesale_min_qty, price_per_base_unit, in_stock, scraped_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            prod_id,
                            sup_id,
                            offer.regular_price,
                            offer.promo_price,
                            offer.club_price,
                            offer.wholesale_price,
                            offer.wholesale_min_qty,
                            price_per_base,
                            1 if offer.in_stock else 0,
                            offer.scraped_at.isoformat(),
                        ),
                    )
                    offers_count += 1

            # 3. Insertar tarjetas y promociones bancarias
            card_id_by_slug: dict[str, int] = {}
            next_card_id = 1
            promos_count = 0
            for promo in promotions:
                if promo.card_slug not in card_id_by_slug:
                    c_id = next_card_id
                    next_card_id += 1
                    card_id_by_slug[promo.card_slug] = c_id
                    cur.execute(
                        """
                        INSERT OR REPLACE INTO local_payment_cards
                        (id, entity_slug, entity_name, slug, name, card_type, tier_label)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            c_id,
                            promo.entity_name.lower().split()[0],
                            promo.entity_name,
                            promo.card_slug,
                            promo.card_name,
                            "CREDIT",
                            "General",
                        ),
                    )
                else:
                    c_id = card_id_by_slug[promo.card_slug]

                sup_id = supermarket_id_by_slug.get(promo.supermarket_slug)
                if sup_id is not None:
                    cur.execute(
                        """
                        INSERT OR REPLACE INTO local_bank_promotions
                        (id, supermarket_id, card_id, title, discount_pct, mechanism,
                         applies_to_promo_price, days_of_week_csv, spending_cap_gs, max_refund_gs)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            promo.id,
                            sup_id,
                            c_id,
                            promo.title,
                            promo.discount_pct,
                            promo.mechanism,
                            1 if promo.applies_to_promo_price else 0,
                            ",".join(str(d) for d in promo.days_of_week),
                            promo.spending_cap_gs,
                            promo.max_refund_gs,
                        ),
                    )
                    promos_count += 1

            conn.commit()

        return {
            "unique_products": len(unified_groups),
            "store_offers": offers_count,
            "bank_promotions": promos_count,
        }

    def search_instant_fts(self, query: str, limit: int = 15) -> list[dict]:
        """
        Ejecuta la misma consulta FTS5 que correrá dentro de Flutter en el teléfono.
        Soporta prefijos ('yerb* kur*') e ignora tildes ('trebol' encuentra 'Trébol').
        """
        tokens = [t.strip() for t in query.split() if t.strip()]
        if not tokens:
            return []
        fts_query = " AND ".join(f'{t}*' for t in tokens)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT
                    p.id AS product_id,
                    p.ean,
                    p.normalized_name,
                    p.brand,
                    p.base_unit,
                    s.slug AS supermarket_slug,
                    s.name AS supermarket_name,
                    o.regular_price,
                    o.promo_price,
                    o.price_per_base_unit
                FROM local_products_fts fts
                JOIN local_products p ON p.id = fts.product_id
                JOIN local_offers o ON o.product_id = p.id
                JOIN local_supermarkets s ON s.id = o.supermarket_id
                WHERE local_products_fts MATCH ?
                ORDER BY COALESCE(o.promo_price, o.regular_price) ASC
                LIMIT ?
                """,
                (fts_query, limit),
            ).fetchall()
            return [dict(r) for r in rows]
