"""
Interfaz de Línea de Comandos (CLI) para PreciosPy:
1. `scrape-live`: Extrae productos reales en vivo desde Biggie Express, Superseis, Casa Rica y Areté,
   unifica por EAN-13 y compila el archivo SQLite Offline-First (FTS5) tanto en `dist/` como en `mobile/assets/db/`.
2. `export-sqlite`: Genera el archivo SQLite desde el dataset semilla.
3. `simulate-wallet`: Ejecuta la simulación de precios con tarjetas paraguayas y búsqueda instantánea FTS5.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from pathlib import Path

from .models import BankPromotion, ScrapedOffer
from .promo_engine import evaluate_offer_for_wallet
from .spiders.biggie import BiggieSpider
from .spiders.dattamax import DattamaxSpider
from .spiders.superseis_stock import RetailSaSpider
from .sqlite_exporter import MobileSqliteExporter


def get_paraguay_metadata_and_baseline() -> tuple[
    list[tuple[int, str, str, bool]],
    list[ScrapedOffer],
    list[BankPromotion],
]:
    supermarkets = [
        (1, "superseis", "Superseis", False),
        (2, "stock", "Supermercados Stock", False),
        (3, "biggie", "Biggie Express", False),
        (4, "casarica", "Casa Rica", False),
        (5, "arete", "Supermercados Areté", False),
    ]

    baseline_offers = [
        ScrapedOffer(
            supermarket_slug="superseis",
            external_sku="S6-1001",
            raw_title="Yerba Mate Kurupí Compuesta Menta y Boldo 500 g",
            regular_price=17200,
            promo_price=14500,
            ean="7840000000036",
            brand="Kurupí",
        ),
        ScrapedOffer(
            supermarket_slug="stock",
            external_sku="ST-1001",
            raw_title="YERBA MATE KURUPI MENTA Y BOLDO 500GR",
            regular_price=17000,
            promo_price=None,
            ean="7840000000036",
            brand="Kurupí",
        ),
        ScrapedOffer(
            supermarket_slug="biggie",
            external_sku="BG-8821",
            raw_title="Yerba Kurupi Menta y Boldo 500g",
            regular_price=17500,
            promo_price=None,
            ean="7840000000036",
            brand="Kurupí",
        ),
        ScrapedOffer(
            supermarket_slug="superseis",
            external_sku="S6-2040",
            raw_title="Leche Entera Trébol UAT Cartón 1 L",
            regular_price=9800,
            promo_price=8900,
            ean="7840000000106",
            brand="Trébol",
        ),
        ScrapedOffer(
            supermarket_slug="biggie",
            external_sku="BG-3099",
            raw_title="Leche UAT Entera Trebol 1000ml",
            regular_price=10000,
            promo_price=None,
            ean="7840000000106",
            brand="Trébol",
        ),
    ]

    promotions = [
        BankPromotion(
            id=1,
            supermarket_slug="biggie",
            card_slug="ueno_credito_n4",
            card_name="ueno Crédito QR (Nivel 4)",
            entity_name="ueno bank",
            title="Reintegro ueno Nivel 4 en Biggie 35%",
            discount_pct=35.0,
            mechanism="CASHBACK",
            applies_to_promo_price=True,
            days_of_week=(1, 2, 3, 4, 5, 6, 7),
            spending_cap_gs=800000,
            max_refund_gs=280000,
        ),
        BankPromotion(
            id=2,
            supermarket_slug="superseis",
            card_slug="itau_credito_clasica",
            card_name="Itaú Crédito Clásica / Oro",
            entity_name="Banco Itaú",
            title="Martes de Superseis con Itaú 20%",
            discount_pct=20.0,
            mechanism="CASHBACK",
            applies_to_promo_price=False,
            days_of_week=(2,),
            spending_cap_gs=1000000,
            max_refund_gs=200000,
        ),
        BankPromotion(
            id=3,
            supermarket_slug="casarica",
            card_slug="itau_credito_infinite",
            card_name="Itaú Personal Bank (Infinite)",
            entity_name="Banco Itaú",
            title="Jueves Casa Rica Itaú Personal Bank 25%",
            discount_pct=25.0,
            mechanism="CASHBACK",
            applies_to_promo_price=False,
            days_of_week=(4,),
            spending_cap_gs=1500000,
            max_refund_gs=375000,
        ),
        BankPromotion(
            id=4,
            supermarket_slug="arete",
            card_slug="continental_credito",
            card_name="Continental Crédito QR",
            entity_name="Banco Continental",
            title="Miércoles en Areté con Continental 20%",
            discount_pct=20.0,
            mechanism="CASHBACK",
            applies_to_promo_price=True,
            days_of_week=(3,),
            spending_cap_gs=1000000,
            max_refund_gs=200000,
        ),
    ]

    return supermarkets, baseline_offers, promotions


def run_live_scraping() -> tuple[list[ScrapedOffer], dict[str, int]]:
    """
    Ejecuta scraping en tiempo real contra:
    1. Biggie Express API REST (`api.app.biggie.com.py/api/articles`)
    2. Superseis (`superseis.com.py/catalog/almacen/yerbas` + portada)
    3. Casa Rica (`casarica.com.py/catalogo/almacen-c254` + portada)
    4. Supermercados Areté (`arete.com.py/catalogo/almacen-c273` + portada)
    """
    all_live_offers: list[ScrapedOffer] = []
    per_store_counts: dict[str, int] = {}

    # 1. Biggie Express en vivo
    biggie = BiggieSpider()
    bg_offers: list[ScrapedOffer] = []
    for skip in (0, 120):
        try:
            bg_offers.extend(biggie.fetch_live_articles(take=60, skip=skip))
        except Exception as exc:
            print(f"[WARN] Biggie skip={skip}: {exc}")
    per_store_counts["biggie"] = len(bg_offers)
    all_live_offers.extend(bg_offers)

    # 2. Superseis en vivo (incluyendo enriquecimiento de EAN-13 en los primeros 6 productos de yerbas)
    s6 = RetailSaSpider("superseis")
    s6_offers: list[ScrapedOffer] = []
    for url, enrich in [
        ("https://www.superseis.com.py/catalog/almacen/yerbas", 6),
        ("https://www.superseis.com.py/", 0),
    ]:
        try:
            s6_offers.extend(s6.fetch_live_url(url, enrich_eans_limit=enrich))
        except Exception as exc:
            print(f"[WARN] Superseis url={url}: {exc}")
    per_store_counts["superseis"] = len(s6_offers)
    all_live_offers.extend(s6_offers)

    # 3. Casa Rica en vivo
    casarica = DattamaxSpider("casarica")
    cr_offers: list[ScrapedOffer] = []
    for path in ("", "catalogo/alimentos-para-bebe-c289"):
        try:
            cr_offers.extend(casarica.fetch_live_url(path))
        except Exception as exc:
            print(f"[WARN] Casa Rica path={path}: {exc}")
    per_store_counts["casarica"] = len(cr_offers)
    all_live_offers.extend(cr_offers)

    # 4. Areté en vivo
    arete = DattamaxSpider("arete")
    ar_offers: list[ScrapedOffer] = []
    for path in ("", "catalogo/almacen-c273"):
        try:
            ar_offers.extend(arete.fetch_live_url(path))
        except Exception as exc:
            print(f"[WARN] Arete path={path}: {exc}")
    per_store_counts["arete"] = len(ar_offers)
    all_live_offers.extend(ar_offers)

    return all_live_offers, per_store_counts


def main() -> None:
    parser = argparse.ArgumentParser(description="PreciosPy CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    export_cmd = sub.add_parser("export-sqlite", help="Genera el archivo SQLite Offline-First con FTS5")
    export_cmd.add_argument(
        "--output",
        default="../dist/catalog_latest.db",
        help="Ruta de salida para la base SQLite móvil",
    )

    live_cmd = sub.add_parser(
        "scrape-live",
        help="Extrae catálogo real en vivo (Biggie, Superseis, Casa Rica, Areté) y actualiza el SQLite de Flutter",
    )
    live_cmd.add_argument(
        "--query",
        default="yerba",
        help="Consulta FTS5 para verificar los productos reales descargados",
    )

    demo_cmd = sub.add_parser("simulate-wallet", help="Ejecuta una simulación de precios y carrito con tarjetas PY")
    demo_cmd.add_argument("--query", default="trebol", help="Consulta FTS5 sin acentos para probar velocidad")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    schema_path = repo_root / "database" / "mobile_sqlite_schema.sql"
    supermarkets, baseline_offers, promotions = get_paraguay_metadata_and_baseline()

    if args.command == "export-sqlite":
        exporter = MobileSqliteExporter(args.output, schema_path)
        exporter.initialize_schema()
        stats = exporter.export_catalog_and_offers(supermarkets, baseline_offers, promotions)
        print(json.dumps({"status": "ok", "output": str(Path(args.output).resolve()), "stats": stats}, indent=2))

    elif args.command == "scrape-live":
        live_offers, per_store = run_live_scraping()
        combined_offers = baseline_offers + live_offers

        dist_db = repo_root / "dist" / "catalog_latest.db"
        mobile_asset_db = repo_root / "mobile" / "assets" / "db" / "catalog_latest.db"

        exporter = MobileSqliteExporter(dist_db, schema_path)
        exporter.initialize_schema()
        stats = exporter.export_catalog_and_offers(supermarkets, combined_offers, promotions)

        mobile_asset_db.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dist_db, mobile_asset_db)

        sample_with_ean = [
            {
                "supermarket": o.supermarket_slug,
                "ean": o.ean,
                "title": o.raw_title,
                "regular_gs": o.regular_price,
                "promo_gs": o.promo_price,
            }
            for o in live_offers
            if o.ean
        ][:10]

        fts_results = exporter.search_instant_fts(args.query, limit=8)

        print(
            json.dumps(
                {
                    "status": "live_scrape_completed",
                    "scraped_per_supermarket": per_store,
                    "sqlite_bundle_stats": stats,
                    "mobile_asset_updated": str(mobile_asset_db),
                    "sample_live_products_with_ean13": sample_with_ean,
                    "fts5_live_search_sample": fts_results,
                },
                indent=2,
                ensure_ascii=False,
            )
        )

    elif args.command == "simulate-wallet":
        db_out = repo_root / "dist" / "catalog_latest.db"
        exporter = MobileSqliteExporter(db_out, schema_path)
        exporter.initialize_schema()
        exporter.export_catalog_and_offers(supermarkets, baseline_offers, promotions)

        wallet = {"ueno_credito_n4", "itau_credito_clasica"}
        sim_date = date(2026, 10, 27)

        results = []
        for offer in baseline_offers:
            if offer.ean == "7840000000036":
                res = evaluate_offer_for_wallet(offer, promotions, wallet, sim_date)
                results.append(
                    {
                        "supermarket": res.supermarket_slug,
                        "regular_gs": res.regular_price,
                        "promo_gondola_gs": res.promo_price,
                        "effective_final_gs": res.effective_final_price,
                        "cash_at_pos_gs": res.cash_outflow_at_pos,
                        "cashback_gs": res.cashback_amount,
                        "price_per_kg_gs": res.price_per_base_unit,
                        "note": res.pricing_note,
                    }
                )

        fts_hits = exporter.search_instant_fts(args.query)
        print(
            json.dumps(
                {
                    "comparison_product": "Yerba Mate Kurupí Compuesta Menta y Boldo 500 g",
                    "wallet": sorted(wallet),
                    "offers_ranked": sorted(results, key=lambda x: x["effective_final_gs"]),
                    "fts5_instant_search_results": fts_hits,
                },
                indent=2,
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
