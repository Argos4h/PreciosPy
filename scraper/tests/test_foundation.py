"""
Suite de pruebas unitarias y de integración para validar las bases de PreciosPy:
1. Limpieza de Guaraníes, validación matemática GS1 de EAN-13 y normalización de unidades (KG/LT).
2. Motor de Promociones Bancarias de Paraguay (acumulables vs. no acumulables y topes de compra en carrito).
3. Spiders de Superseis/Stock y Biggie Express.
4. Exportador SQLite Offline-First y motor de búsqueda instantánea FTS5 sin acentos.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

# Asegurar que src/ esté en el path al ejecutar pytest o unittest directamente
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import unittest

from precios_py.models import BankPromotion, ScrapedOffer
from precios_py.normalizer import (
    calculate_price_per_base_unit,
    extract_ean_from_text_or_url,
    extract_unit_info,
    is_valid_ean,
    parse_guaranies,
)
from precios_py.promo_engine import (
    evaluate_offer_for_wallet,
    simulate_smart_cart_for_supermarket,
)
from precios_py.spiders.biggie import BiggieSpider
from precios_py.spiders.superseis_stock import RetailSaSpider
from precios_py.sqlite_exporter import MobileSqliteExporter


class TestPreciosPyFoundation(unittest.TestCase):
    def test_guaranies_parser(self) -> None:
        self.assertEqual(parse_guaranies("Gs. 18.500"), 18500)
        self.assertEqual(parse_guaranies("₲ 125.000,00"), 125000)
        self.assertEqual(parse_guaranies(9800), 9800)
        self.assertIsNone(parse_guaranies("Agotado"))

    def test_ean_gs1_checksum_and_extraction(self) -> None:
        # 7840000000036 tiene dígito verificador GS1 válido (8)
        self.assertTrue(is_valid_ean("7840000000036"))
        # Cambiar último dígito debe invalidarlo
        self.assertFalse(is_valid_ean("7840000000039"))
        # Extraer desde URL de imagen típica de Superseis/Casa Rica
        url = "https://www.superseis.com.py/images/thumbs/7840000000036_large.jpg"
        self.assertEqual(extract_ean_from_text_or_url(url), "7840000000036")

    def test_unit_extraction_and_price_per_kg_lt(self) -> None:
        # Yerba de 500g a Gs. 14.500 -> Gs. 29.000 por KG
        u_yerba = extract_unit_info("Yerba Mate Kurupí Menta y Boldo 500 g")
        self.assertEqual(u_yerba.base_unit, "KG")
        self.assertAlmostEqual(u_yerba.base_multiplier, 0.5)
        self.assertEqual(calculate_price_per_base_unit(14500, u_yerba), 29000)

        # Pack de 6 x 330 ml = 1.98 Litros
        u_pack = extract_unit_info("Cerveza Pilsen Pack 6x330ml")
        self.assertEqual(u_pack.base_unit, "LT")
        self.assertAlmostEqual(u_pack.base_multiplier, 1.98)

    def test_bank_promo_engine_non_cumulative_vs_cumulative(self) -> None:
        # Caso 1: Superseis tiene oferta de góndola (Reg: 20.000, Oferta: 14.000 -> 30% off directo)
        # Tarjeta Itaú da 20% NO acumulable los martes (20.000 * 0.8 = 16.000).
        # El motor debe elegir Gs. 14.000 (oferta directa) en vez de 16.000.
        offer_s6 = ScrapedOffer(
            supermarket_slug="superseis",
            external_sku="S6-1",
            raw_title="Café Tostado 250g",
            regular_price=20000,
            promo_price=14000,
        )
        promo_itau = BankPromotion(
            id=1,
            supermarket_slug="superseis",
            card_slug="itau_oro",
            card_name="Itaú Oro",
            entity_name="Banco Itaú",
            title="Martes Itaú 20%",
            discount_pct=20.0,
            mechanism="CASHBACK",
            applies_to_promo_price=False,
            days_of_week=(2,),  # Martes
        )
        res_s6 = evaluate_offer_for_wallet(
            offer_s6, [promo_itau], {"itau_oro"}, date(2026, 10, 27)  # Martes
        )
        self.assertEqual(res_s6.effective_final_price, 14000)
        self.assertIsNone(res_s6.applied_promo)
        self.assertIn("No acumulable", res_s6.pricing_note)

        # Caso 2: Biggie con ueno Nivel 4 (35% reintegro acumulable)
        offer_bg = ScrapedOffer(
            supermarket_slug="biggie",
            external_sku="BG-1",
            raw_title="Café Tostado 250g",
            regular_price=20000,
            promo_price=None,
        )
        promo_ueno = BankPromotion(
            id=2,
            supermarket_slug="biggie",
            card_slug="ueno_n4",
            card_name="ueno Nivel 4",
            entity_name="ueno bank",
            title="ueno 35% todos los días",
            discount_pct=35.0,
            mechanism="CASHBACK",
            applies_to_promo_price=True,
            days_of_week=(1, 2, 3, 4, 5, 6, 7),
        )
        res_bg = evaluate_offer_for_wallet(
            offer_bg, [promo_ueno], {"ueno_n4"}, date(2026, 10, 27)
        )
        self.assertEqual(res_bg.effective_final_price, 13000)
        self.assertEqual(res_bg.cash_outflow_at_pos, 20000)
        self.assertEqual(res_bg.cashback_amount, 7000)

    def test_smart_cart_spending_cap(self) -> None:
        # Carrito de Gs. 1.000.000 en Biggie con tope de compra de Gs. 800.000 al 25%
        # Reintegro máximo esperado: 25% de 800.000 = Gs. 200.000 (Costo neto: Gs. 800.000)
        item = ScrapedOffer(
            supermarket_slug="biggie",
            external_sku="BG-99",
            raw_title="Compra Grande",
            regular_price=500000,
        )
        promo = BankPromotion(
            id=10,
            supermarket_slug="biggie",
            card_slug="ueno_n3",
            card_name="ueno Nivel 3",
            entity_name="ueno bank",
            title="25% con tope Gs. 800.000",
            discount_pct=25.0,
            mechanism="CASHBACK",
            applies_to_promo_price=True,
            days_of_week=(1, 2, 3, 4, 5, 6, 7),
            spending_cap_gs=800000,
            max_refund_gs=200000,
        )
        summary = simulate_smart_cart_for_supermarket(
            "biggie",
            [(item, 2)],  # 2 x 500.000 = Gs. 1.000.000
            [promo],
            {"ueno_n3"},
            date(2026, 10, 30),
        )
        self.assertTrue(summary.cap_reached)
        self.assertEqual(summary.total_cash_at_pos_gs, 1000000)
        self.assertEqual(summary.total_cashback_gs, 200000)
        self.assertEqual(summary.net_final_cost_gs, 800000)

    def test_spiders_html_and_json_parsing(self) -> None:
        s6_spider = RetailSaSpider("superseis")
        sample_html = """
        <div class="product-item" data-productid="4412">
          <div class="picture">
            <img src="/images/thumbs/7840000000036.jpg" />
          </div>
          <div class="details">
            <a href="/yerba-kurupi-500g" class="product-title-link">Yerba Mate Kurupí 500 g</a>
            <div class="prices">
              <span class="price-old">Gs. 17.200</span>
              <span class="price-special">Gs. 14.500</span>
            </div>
          </div>
        </div>
        """
        s6_offers = s6_spider.parse_catalog_payload(sample_html)
        self.assertEqual(len(s6_offers), 1)
        self.assertEqual(s6_offers[0].ean, "7840000000036")
        self.assertEqual(s6_offers[0].regular_price, 17200)
        self.assertEqual(s6_offers[0].promo_price, 14500)

        bg_spider = BiggieSpider()
        bg_offers = bg_spider.parse_catalog_payload(
            {
                "items": [
                    {
                        "id": "991",
                        "nombre": "Yerba Kurupi 500g",
                        "precioRegular": "17.500",
                        "codigoBarras": "7840000000036",
                        "marca": "Kurupí",
                    }
                ]
            }
        )
        self.assertEqual(len(bg_offers), 1)
        self.assertEqual(bg_offers[0].regular_price, 17500)
        self.assertEqual(bg_offers[0].ean, "7840000000036")

    def test_sqlite_fts5_accent_insensitive_search(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        schema_path = repo_root / "database" / "mobile_sqlite_schema.sql"
        test_db = repo_root / "dist" / "test_catalog.db"
        if test_db.exists():
            test_db.unlink()

        exporter = MobileSqliteExporter(test_db, schema_path)
        exporter.initialize_schema()
        exporter.export_catalog_and_offers(
            supermarkets=[(1, "superseis", "Superseis", False), (3, "biggie", "Biggie Express", False)],
            offers=[
                ScrapedOffer(
                    supermarket_slug="superseis",
                    external_sku="1",
                    raw_title="Leche Entera Trébol UAT Cartón 1 L",
                    regular_price=9800,
                    promo_price=8900,
                    ean="7840000000106",
                    brand="Trébol",
                ),
                ScrapedOffer(
                    supermarket_slug="biggie",
                    external_sku="2",
                    raw_title="Leche Entera Trébol 1L",
                    regular_price=10000,
                    ean="7840000000106",
                    brand="Trébol",
                ),
            ],
        )

        # Buscar "trebol carton" SIN tilde debe encontrar "Trébol" y "Cartón" y unificar ambas ofertas bajo el mismo product_id
        hits = exporter.search_instant_fts("trebol carton")
        self.assertEqual(len(hits), 2)
        self.assertEqual(hits[0]["supermarket_slug"], "superseis")
        self.assertEqual(hits[0]["promo_price"], 8900)

    def test_entity_resolution_and_fuzzy_matcher(self) -> None:
        from precios_py.entity_matcher import EntityResolver

        resolver = EntityResolver(fuzzy_threshold=0.70)
        offers = [
            # Superseis no tiene EAN en su tarjeta de listado
            ScrapedOffer(
                supermarket_slug="superseis",
                external_sku="s6_coca_2l",
                raw_title="Gaseosa Coca-Cola sabor original 2 L",
                regular_price=13500,
                ean=None,
            ),
            # Biggie sí tiene el EAN en su JSON
            ScrapedOffer(
                supermarket_slug="biggie",
                external_sku="bg_coca_2000",
                raw_title="Coca Cola Original de 2.000 ml.",
                regular_price=14900,
                ean="7840058008084",
            ),
            # Producto de diferente tamaño que NUNCA debe unificarse
            ScrapedOffer(
                supermarket_slug="biggie",
                external_sku="bg_coca_1500",
                raw_title="Coca Cola Original de 1.500 ml.",
                regular_price=12000,
                ean="7840058000675",
            ),
        ]

        groups = resolver.resolve_catalog(offers)
        # Deben crearse 2 grupos: uno para 2L y otro para 1.5L
        self.assertEqual(len(groups), 2)

        # El grupo de 2L debe tener 2 ofertas (Superseis + Biggie)
        group_2l = next(g for g in groups if "2.000" in g.canonical_name or "2 L" in g.canonical_name)
        self.assertEqual(len(group_2l.offers), 2)
        # El EAN de Biggie debe haberse propagado al grupo y a la oferta de Superseis
        self.assertEqual(group_2l.canonical_ean, "7840058008084")
        self.assertEqual(group_2l.offers[0].ean, "7840058008084")

    def test_delta_sync_engine(self) -> None:
        from precios_py.delta_sync import DeltaSyncEngine

        engine = DeltaSyncEngine()
        prev_offers = [
            ScrapedOffer(
                supermarket_slug="superseis",
                external_sku="item1",
                raw_title="Leche 1L",
                regular_price=9500,
                promo_price=None,
                ean="7840000000106",
            )
        ]
        curr_offers = [
            # Precio cambió de 9500 a 9800 y oferta a 8900
            ScrapedOffer(
                supermarket_slug="superseis",
                external_sku="item1",
                raw_title="Leche 1L",
                regular_price=9800,
                promo_price=8900,
                ean="7840000000106",
            ),
            # Nuevo producto
            ScrapedOffer(
                supermarket_slug="biggie",
                external_sku="item2",
                raw_title="Yerba 500g",
                regular_price=17500,
                ean="7840000000036",
            ),
        ]

        delta = engine.compute_delta(prev_offers, curr_offers)
        self.assertEqual(delta.total_price_changes, 1)
        self.assertEqual(delta.total_new_products, 1)
        self.assertEqual(len(delta.updated_offers), 2)
        self.assertEqual(delta.updated_offers[0]["old_regular_price"], 9500)
        self.assertEqual(delta.updated_offers[0]["new_regular_price"], 9800)


if __name__ == "__main__":
    unittest.main()
