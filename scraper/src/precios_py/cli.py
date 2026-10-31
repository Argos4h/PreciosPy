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

from .bank_promos_sync import get_all_bank_promotions
from .models import BankPromotion, ScrapedOffer
from .promo_engine import evaluate_offer_for_wallet
from .spiders.biggie import BiggieSpider
from .spiders.dattamax import DattamaxSpider
from .spiders.fortis import FortisMayoristaSpider
from .spiders.salemma_real import SalemmaRealSpider
from .spiders.superseis_stock import RetailSaSpider
from .spiders.tuti import TutiSpider
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
        (4, "casarica", "Casa Rica Gourmet", False),
        (5, "arete", "Supermercados Areté", False),
        (6, "fortis", "Fortis Mayorista", False),
        (7, "box", "Box Mayorista", False),
        (8, "real", "Cadena Real", False),
        (9, "salemma", "Supermercados Salemma", False),
        (10, "losjardines", "Los Jardines (Luque)", False),
        (11, "labomba", "Supermercados La Bomba", False),
        (12, "granvia", "Cadena Gran Vía", False),
        (13, "delimarket", "Delimarket Shopping del Sol", False),
        (14, "tuti", "Tiendas Tuti", False),
    ]

    baseline_offers = [
        # 1. YERBA MATE KURUPI MENTA Y BOLDO 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-1001", raw_title="Yerba Mate Kurupí Compuesta Menta y Boldo 500 g", regular_price=17200, promo_price=14500, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-1001", raw_title="YERBA MATE KURUPI MENTA Y BOLDO 500GR", regular_price=17000, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-8821", raw_title="Yerba Kurupi Menta y Boldo 500g", regular_price=17500, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-1001", raw_title="Yerba Kurupi Menta y Boldo 500g", regular_price=15900, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-1001", raw_title="Yerba Mate Kurupí Menta y Boldo 500g", regular_price=15500, promo_price=14200, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="real", external_sku="RL-1001", raw_title="Yerba Mate Kurupí Menta y Boldo 500 gr", regular_price=16800, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="salemma", external_sku="SL-1001", raw_title="Yerba Mate Kurupi Menta Boldo 500g", regular_price=16900, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="casarica", external_sku="CR-1001", raw_title="Yerba Kurupí Compuesta 500g", regular_price=18200, promo_price=None, ean="7840000000036", brand="Kurupí"),
        ScrapedOffer(supermarket_slug="arete", external_sku="AR-1001", raw_title="Yerba Kurupi Menta y Boldo 500g", regular_price=16900, promo_price=15200, ean="7840000000036", brand="Kurupí"),

        # 2. YERBA MATE CAMPESINO MENTA Y LIMON 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-1002", raw_title="Yerba Mate Campesino Menta y Limón 500 g", regular_price=16800, promo_price=13900, ean="7840003001016", brand="Campesino"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-1002", raw_title="Yerba Campesino Refrescante Menta Limon 500g", regular_price=16500, promo_price=None, ean="7840003001016", brand="Campesino"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-1002", raw_title="Yerba Mate Campesino Menta Limon 500g", regular_price=17000, promo_price=None, ean="7840003001016", brand="Campesino"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-1002", raw_title="Yerba Campesino Menta y Limon 500g", regular_price=15200, promo_price=None, ean="7840003001016", brand="Campesino"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-1002", raw_title="Yerba Mate Campesino 500g Menta Limon", regular_price=14900, promo_price=None, ean="7840003001016", brand="Campesino"),

        # 3. YERBA MATE PAJARITO COMPUESTA 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-1003", raw_title="Yerba Mate Pajarito Compuesta con Hierbas 500 g", regular_price=16500, promo_price=None, ean="7840013000030", brand="Pajarito"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-1003", raw_title="Yerba Pajarito Compuesta 500g", regular_price=16200, promo_price=None, ean="7840013000030", brand="Pajarito"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-1003", raw_title="Yerba Mate Pajarito Hierbas 500g", regular_price=14800, promo_price=None, ean="7840013000030", brand="Pajarito"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-1003", raw_title="Yerba Pajarito Compuesta 500g", regular_price=14900, promo_price=None, ean="7840013000030", brand="Pajarito"),

        # 4. LECHE ENTERA TREBOL UAT 1L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-2040", raw_title="Leche Entera Trébol UAT Cartón 1 L", regular_price=9800, promo_price=8900, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-2040", raw_title="Leche UAT Entera Trebol 1L", regular_price=9700, promo_price=8850, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-3099", raw_title="Leche UAT Entera Trebol 1000ml", regular_price=10000, promo_price=None, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-2040", raw_title="Leche Entera Trebol 1L Tetra", regular_price=8700, promo_price=None, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-2040", raw_title="Leche Entera Trébol Larga Vida 1L", regular_price=8900, promo_price=8350, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="real", external_sku="RL-2040", raw_title="Leche Trebol Entera 1L", regular_price=9650, promo_price=None, ean="7840000000106", brand="Trébol"),
        ScrapedOffer(supermarket_slug="salemma", external_sku="SL-2040", raw_title="Leche Entera Trebol 1L Tetra", regular_price=9600, promo_price=None, ean="7840000000106", brand="Trébol"),

        # 5. LECHE DESCREMADA LACTOLANDA 1L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-2041", raw_title="Leche Descremada Lactolanda 1 L Tetra", regular_price=9500, promo_price=None, ean="7840024001156", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-2041", raw_title="Leche UAT Descremada Lactolanda 1L", regular_price=9400, promo_price=None, ean="7840024001156", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-2041", raw_title="Leche Descremada Lactolanda 1000ml", regular_price=9900, promo_price=None, ean="7840024001156", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-2041", raw_title="Leche Descremada Lactolanda 1L", regular_price=8500, promo_price=None, ean="7840024001156", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-2041", raw_title="Leche Descremada Lactolanda 1L", regular_price=8600, promo_price=None, ean="7840024001156", brand="Lactolanda"),

        # 6. YOGUR FRUTILLA TREBOL SACHET 1L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-2042", raw_title="Yogur Frutilla Trébol Sachet 1 L", regular_price=11200, promo_price=9900, ean="7840000000519", brand="Trébol"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-2042", raw_title="Yogur Trébol Sabor Frutilla 1L Sachet", regular_price=10900, promo_price=None, ean="7840000000519", brand="Trébol"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-2042", raw_title="Yogur Sachet Frutilla Trebol 1L", regular_price=11500, promo_price=None, ean="7840000000519", brand="Trébol"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-2042", raw_title="Yogur Entero Frutilla Trebol 1L", regular_price=9800, promo_price=None, ean="7840000000519", brand="Trébol"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-2042", raw_title="Yogur Frutilla Sachet Trebol 1L", regular_price=9500, promo_price=None, ean="7840000000519", brand="Trébol"),

        # 7. QUESO PARAGUAY TRADICIONAL 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-2043", raw_title="Queso Paraguay Tradicional por Kilo", regular_price=42000, promo_price=None, ean="2000000001018", brand="Nacional"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-2043", raw_title="Queso Paraguay Artesanal al Kilo", regular_price=39500, promo_price=None, ean="2000000001018", brand="Nacional"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-2043", raw_title="Queso Paraguay Criollo Kg", regular_price=36900, promo_price=None, ean="2000000001018", brand="Nacional"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-2043", raw_title="Queso Paraguay Envasado 1kg", regular_price=37000, promo_price=None, ean="2000000001018", brand="Nacional"),

        # 8. GASEOSA COCA-COLA ORIGINAL 2L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-3001", raw_title="Gaseosa Coca-Cola Sabor Original 2 L", regular_price=13500, promo_price=12000, ean="7840058000122", brand="Coca-Cola"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-3001", raw_title="Gaseosa Coca-Cola 2 Litros", regular_price=13000, promo_price=None, ean="7840058000122", brand="Coca-Cola"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-1020", raw_title="Coca Cola 2L Descartable", regular_price=13000, promo_price=None, ean="7840058000122", brand="Coca-Cola"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-3001", raw_title="Coca Cola Original 2 Litros", regular_price=12200, promo_price=None, ean="7840058000122", brand="Coca-Cola"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-3001", raw_title="Coca Cola Sabor Original 2L PET", regular_price=12500, promo_price=11800, ean="7840058000122", brand="Coca-Cola"),
        ScrapedOffer(supermarket_slug="real", external_sku="RL-3001", raw_title="Coca Cola 2L Botella", regular_price=12900, promo_price=None, ean="7840058000122", brand="Coca-Cola"),

        # 9. GASEOSA PULP POMELO 1.5L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-3002", raw_title="Gaseosa Pulp Sabor Pomelo 1.5 L", regular_price=10500, promo_price=None, ean="7840032000155", brand="Pulp"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-3002", raw_title="Gaseosa Pulp Pomelo 1.5L PET", regular_price=10200, promo_price=None, ean="7840032000155", brand="Pulp"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-3002", raw_title="Pulp Pomelo 1.5 Litros", regular_price=10800, promo_price=None, ean="7840032000155", brand="Pulp"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-3002", raw_title="Pulp Pomelo 1.5L Descartable", regular_price=9500, promo_price=None, ean="7840032000155", brand="Pulp"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-3002", raw_title="Gaseosa Pulp Pomelo 1.5L", regular_price=9200, promo_price=None, ean="7840032000155", brand="Pulp"),

        # 10. CERVEZA PILSEN 940ML
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-4001", raw_title="Cerveza Pilsen 940 ml Retornable", regular_price=11000, promo_price=9900, ean="7840000000205", brand="Pilsen"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-4001", raw_title="Cerveza Pilsen Retornable 940cc", regular_price=10800, promo_price=None, ean="7840000000205", brand="Pilsen"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-4001", raw_title="Cerveza Pilsen 940 ml", regular_price=11500, promo_price=None, ean="7840000000205", brand="Pilsen"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-4001", raw_title="Cerveza Pilsen Botella 940ml", regular_price=9800, promo_price=None, ean="7840000000205", brand="Pilsen"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-4001", raw_title="Cerveza Pilsen 940ml Botella", regular_price=9600, promo_price=None, ean="7840000000205", brand="Pilsen"),

        # 11. CERVEZA BRAHMA CHOPP LATA 354ML PACK X6
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-4002", raw_title="Cerveza Brahma Chopp Lata 354 ml Pack x 6", regular_price=32500, promo_price=28900, ean="7840018001048", brand="Brahma"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-4002", raw_title="Brahma Chopp 354ml Sixpack", regular_price=31900, promo_price=None, ean="7840018001048", brand="Brahma"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-4002", raw_title="Brahma Chopp Lata 354ml Pack 6", regular_price=33000, promo_price=None, ean="7840018001048", brand="Brahma"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-4002", raw_title="Cerveza Brahma Chopp Sixpack Latas", regular_price=27500, promo_price=None, ean="7840018001048", brand="Brahma"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-4002", raw_title="Brahma Chopp Pack 6 Latas", regular_price=27000, promo_price=None, ean="7840018001048", brand="Brahma"),

        # 12. ACEITE DE GIRASOL SIGLO DE ORO 900ML
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-5001", raw_title="Aceite de Girasol Siglo de Oro 900 ml", regular_price=14500, promo_price=12900, ean="7840000000212", brand="Siglo de Oro"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-5001", raw_title="Aceite Siglo de Oro 900ml Botella", regular_price=14200, promo_price=None, ean="7840000000212", brand="Siglo de Oro"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-5001", raw_title="Aceite Siglo de Oro Girasol 900ml", regular_price=12900, promo_price=11950, ean="7840000000212", brand="Siglo de Oro"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-5001", raw_title="Aceite Siglo de Oro 900ml", regular_price=12500, promo_price=None, ean="7840000000212", brand="Siglo de Oro"),

        # 13. ARROZ BLANCO TIO NICO 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6001", raw_title="Arroz Blanco Tipo 1 Tío Nico 1 kg", regular_price=8500, promo_price=None, ean="7840000000304", brand="Tío Nico"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6001", raw_title="Arroz Tipo 1 Tio Nico 1kg", regular_price=8400, promo_price=None, ean="7840000000304", brand="Tío Nico"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6001", raw_title="Arroz Tío Nico Tipo 1 1kg", regular_price=7450, promo_price=6900, ean="7840000000304", brand="Tío Nico"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-6001", raw_title="Arroz Blanco Tio Nico 1kg", regular_price=7200, promo_price=None, ean="7840000000304", brand="Tío Nico"),

        # 14. FIDEOS SPAGHETTI ANITA 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6002", raw_title="Fideos Spaghetti Anita 500 g", regular_price=5800, promo_price=None, ean="7840045000058", brand="Anita"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6002", raw_title="Fideo Anita Spaghetti 500g", regular_price=5600, promo_price=None, ean="7840045000058", brand="Anita"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6002", raw_title="Fideos Anita Spaghetti 500g Paquete", regular_price=4900, promo_price=None, ean="7840045000058", brand="Anita"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-6002", raw_title="Fideo Spaghetti Anita 500g", regular_price=4700, promo_price=None, ean="7840045000058", brand="Anita"),

        # 15. HARINA DE TRIGO 0000 HILDEBRAND 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6003", raw_title="Harina de Trigo 0000 Hildebrand 1 kg", regular_price=7900, promo_price=None, ean="7840051000104", brand="Hildebrand"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6003", raw_title="Harina 0000 Hildebrand 1kg", regular_price=7700, promo_price=None, ean="7840051000104", brand="Hildebrand"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6003", raw_title="Harina Hildebrand 0000 1kg", regular_price=6800, promo_price=None, ean="7840051000104", brand="Hildebrand"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-6003", raw_title="Harina Especial Hildebrand 0000 1kg", regular_price=6500, promo_price=None, ean="7840051000104", brand="Hildebrand"),

        # 16. COSTILLA DE PRIMERA AL VACIO 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-7001", raw_title="Costilla de Primera para Asado al Vacío 1 kg", regular_price=42500, promo_price=36900, ean="2000000000403", brand="Chortitzer"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-7001", raw_title="Costilla Vacuna de Primera al Vacío Kg", regular_price=41900, promo_price=35900, ean="2000000000403", brand="Chortitzer"),
        ScrapedOffer(supermarket_slug="real", external_sku="RL-7001", raw_title="Costilla de Primera Asado Kg", regular_price=39900, promo_price=None, ean="2000000000403", brand="Chortitzer"),
        ScrapedOffer(supermarket_slug="labomba", external_sku="LB-7001", raw_title="Costilla Primera Vacuno Kg", regular_price=34500, promo_price=None, ean="2000000000403", brand="Chortitzer"),

        # 17. PAN FELIPE FRANCES TRADICIONAL 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-8001", raw_title="Pan Felipe Francés Tradicional por Kilo", regular_price=8900, promo_price=None, ean="2000000000601", brand="Panadería"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-8001", raw_title="Pan Francés Felipe al Kilo", regular_price=8500, promo_price=None, ean="2000000000601", brand="Panadería"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-8001", raw_title="Pan Felipe Artesanal 1kg", regular_price=7500, promo_price=None, ean="2000000000601", brand="Panadería"),

        # 18. JABON LIQUIDO OMO MATIC 3L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-9001", raw_title="Jabón Líquido Omo Matic Concentrado 3 L", regular_price=64000, promo_price=54000, ean="7891150043878", brand="Omo"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-9001", raw_title="Jabon Liquido Omo Matic 3L Botella", regular_price=63500, promo_price=None, ean="7891150043878", brand="Omo"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-9001", raw_title="Jabón Líquido Omo Matic 3 Litros", regular_price=58000, promo_price=52900, ean="7891150043878", brand="Omo"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-9001", raw_title="Jabon Liquido Para Ropa Omo 3L", regular_price=55000, promo_price=None, ean="7891150043878", brand="Omo"),

        # 19. GALLETITAS OREO RELLENAS 108G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-9501", raw_title="Galletitas Oreo Rellenas con Vainilla 108 g", regular_price=7500, promo_price=6200, ean="7622300744663", brand="Oreo"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-9501", raw_title="Galletita Oreo Original 108g", regular_price=7200, promo_price=None, ean="7622300744663", brand="Oreo"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-9501", raw_title="Oreo Galletita Rellena 108g", regular_price=7800, promo_price=None, ean="7622300744663", brand="Oreo"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-9501", raw_title="Galletitas Oreo Vainilla 108g", regular_price=5900, promo_price=None, ean="7622300744663", brand="Oreo"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-9501", raw_title="Oreo Original 108g Paquete", regular_price=5500, promo_price=None, ean="7622300744663", brand="Oreo"),

        # 20. YERBA MATE SELECTA TRADICIONAL 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-1004", raw_title="Yerba Mate Selecta Tradicional 500 g", regular_price=16200, promo_price=13800, ean="7840006000016", brand="Selecta"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-1004", raw_title="Yerba Selecta 500g Paquete", regular_price=15900, promo_price=None, ean="7840006000016", brand="Selecta"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-1004", raw_title="Yerba Mate Selecta 500g", regular_price=14500, promo_price=None, ean="7840006000016", brand="Selecta"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-1004", raw_title="Yerba Selecta Tradicional 500g", regular_price=14200, promo_price=None, ean="7840006000016", brand="Selecta"),

        # 21. MANTECA LACTOLANDA CON SAL 200G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-2044", raw_title="Manteca Lactolanda con Sal Pan 200 g", regular_price=14800, promo_price=12900, ean="7840024001309", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-2044", raw_title="Manteca con Sal Lactolanda 200g", regular_price=14500, promo_price=None, ean="7840024001309", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-2044", raw_title="Manteca Lactolanda 200g", regular_price=15200, promo_price=None, ean="7840024001309", brand="Lactolanda"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-2044", raw_title="Manteca Lactolanda Pan 200g", regular_price=13400, promo_price=None, ean="7840024001309", brand="Lactolanda"),

        # 22. GASEOSA SPRITE LIMA LIMON 2L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-3003", raw_title="Gaseosa Sprite Sabor Lima-Limón 2 L", regular_price=13500, promo_price=12000, ean="7840058000214", brand="Sprite"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-3003", raw_title="Sprite Sabor Lima Limon 2L PET", regular_price=13000, promo_price=None, ean="7840058000214", brand="Sprite"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-3003", raw_title="Sprite 2L Botella", regular_price=13000, promo_price=None, ean="7840058000214", brand="Sprite"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-3003", raw_title="Gaseosa Sprite 2L Descartable", regular_price=12500, promo_price=11800, ean="7840058000214", brand="Sprite"),

        # 23. JUGO PURO SOL NARANJA 1L
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-3004", raw_title="Jugo Puro Sol Naranja 100% 1 L Tetra", regular_price=11900, promo_price=9900, ean="7840015000112", brand="Puro Sol"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-3004", raw_title="Jugo Naranja Puro Sol 1L", regular_price=11500, promo_price=None, ean="7840015000112", brand="Puro Sol"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-3004", raw_title="Puro Sol Naranja 1 Litro", regular_price=12000, promo_price=None, ean="7840015000112", brand="Puro Sol"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-3004", raw_title="Jugo Puro Sol Sabor Naranja 1L", regular_price=10500, promo_price=None, ean="7840015000112", brand="Puro Sol"),

        # 24. VINO TINTO SANTA HELENA CABERNET SAUVIGNON 750ML
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-4003", raw_title="Vino Tinto Santa Helena Cabernet Sauvignon 750 ml", regular_price=27500, promo_price=22900, ean="7804300100125", brand="Santa Helena"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-4003", raw_title="Vino Santa Helena Cabernet 750ml", regular_price=26900, promo_price=None, ean="7804300100125", brand="Santa Helena"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-4003", raw_title="Vino Santa Helena Varietal Cabernet 750ml", regular_price=28000, promo_price=None, ean="7804300100125", brand="Santa Helena"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-4003", raw_title="Vino Santa Helena Cabernet Sauvignon 750ml", regular_price=23500, promo_price=None, ean="7804300100125", brand="Santa Helena"),

        # 25. AZUCAR BLANCO BELLA VISTA 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6004", raw_title="Azúcar Blanco Común Bella Vista 1 kg", regular_price=6900, promo_price=None, ean="7840000000311", brand="Bella Vista"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6004", raw_title="Azúcar Bella Vista 1kg Paquete", regular_price=6800, promo_price=None, ean="7840000000311", brand="Bella Vista"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6004", raw_title="Azúcar Bella Vista Común 1kg", regular_price=5950, promo_price=None, ean="7840000000311", brand="Bella Vista"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-6004", raw_title="Azucar Blanco Bella Vista 1kg", regular_price=5800, promo_price=None, ean="7840000000311", brand="Bella Vista"),

        # 26. SAL FINA YODADA DOS ANCLAS 500G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6005", raw_title="Sal Fina Yodada Dos Anclas Salero 500 g", regular_price=4800, promo_price=None, ean="7790070012053", brand="Dos Anclas"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6005", raw_title="Sal Dos Anclas Fina 500g", regular_price=4700, promo_price=None, ean="7790070012053", brand="Dos Anclas"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6005", raw_title="Sal Fina Dos Anclas Paquete 500g", regular_price=3900, promo_price=None, ean="7790070012053", brand="Dos Anclas"),

        # 27. CAFE SOLUBLE NESCAFE DOLCA 100G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-6006", raw_title="Café Soluble Nescafé Dolca Suave Frasco 100 g", regular_price=24500, promo_price=19900, ean="7613035345678", brand="Nescafé"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-6006", raw_title="Café Nescafé Dolca 100g Frasco", regular_price=23900, promo_price=None, ean="7613035345678", brand="Nescafé"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-6006", raw_title="Nescafé Dolca Frasco 100g", regular_price=25000, promo_price=None, ean="7613035345678", brand="Nescafé"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-6006", raw_title="Café Soluble Nescafé Dolca 100g", regular_price=20900, promo_price=None, ean="7613035345678", brand="Nescafé"),

        # 28. PECHUGA DE POLLO PECHUGON AL VACIO 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-7002", raw_title="Pechuga de Pollo Deshuesada Pechugon al Vacío 1 kg", regular_price=31900, promo_price=26500, ean="2000000000502", brand="Pechugon"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-7002", raw_title="Pechuga Pollo Pechugon al Vacío Kg", regular_price=31500, promo_price=25900, ean="2000000000502", brand="Pechugon"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-7002", raw_title="Pechuga de Pollo Pechugon Kg", regular_price=27900, promo_price=None, ean="2000000000502", brand="Pechugon"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-7002", raw_title="Pechuga Pollo Pechugon 1kg", regular_price=26900, promo_price=None, ean="2000000000502", brand="Pechugon"),

        # 29. GALLETA CUARTEL TRADICIONAL 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-8002", raw_title="Galleta Cuartel Tradicional por Kilo", regular_price=9200, promo_price=None, ean="2000000000618", brand="Panadería"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-8002", raw_title="Galleta Cuartel al Kilo", regular_price=8900, promo_price=None, ean="2000000000618", brand="Panadería"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-8002", raw_title="Galleta Cuartel Tradicional 1kg", regular_price=7800, promo_price=None, ean="2000000000618", brand="Panadería"),

        # 30. TOMATE SANTA CRUZ SELECCION 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-8501", raw_title="Tomate Santa Cruz Seleccionado por Kilo", regular_price=12500, promo_price=8900, ean="2000000000700", brand="Verdulería"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-8501", raw_title="Tomate Santa Cruz Kg", regular_price=12200, promo_price=8500, ean="2000000000700", brand="Verdulería"),
        ScrapedOffer(supermarket_slug="real", external_sku="RL-8501", raw_title="Tomate Santa Cruz al Kilo", regular_price=10900, promo_price=None, ean="2000000000700", brand="Verdulería"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-8501", raw_title="Tomate Santa Cruz 1kg", regular_price=9500, promo_price=None, ean="2000000000700", brand="Verdulería"),

        # 31. BANANA KARAPE 1KG
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-8502", raw_title="Banana Karape Nacional de Primera por Kilo", regular_price=6500, promo_price=4900, ean="2000000000717", brand="Frutería"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-8502", raw_title="Banana Karape Kg", regular_price=6300, promo_price=4800, ean="2000000000717", brand="Frutería"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-8502", raw_title="Banana Karape al Kilo", regular_price=5200, promo_price=None, ean="2000000000717", brand="Frutería"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-8502", raw_title="Banana Karape Nacional 1kg", regular_price=4900, promo_price=None, ean="2000000000717", brand="Frutería"),

        # 32. DETERGENTE ZORRO CONCENTRADO MANZANA 500ML
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-9002", raw_title="Detergente Vajilla Zorro Concentrado Manzana 500 ml", regular_price=6800, promo_price=None, ean="7840000000908", brand="Zorro"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-9002", raw_title="Detergente Zorro Manzana 500ml", regular_price=6700, promo_price=None, ean="7840000000908", brand="Zorro"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-9002", raw_title="Detergente Zorro 500ml", regular_price=7200, promo_price=None, ean="7840000000908", brand="Zorro"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-9002", raw_title="Detergente Zorro Manzana 500ml Botella", regular_price=5600, promo_price=None, ean="7840000000908", brand="Zorro"),
        ScrapedOffer(supermarket_slug="tuti", external_sku="TU-9002", raw_title="Detergente Zorro Manzana 500ml", regular_price=5400, promo_price=None, ean="7840000000908", brand="Zorro"),

        # 33. PAPAS FRITAS LAYS CLASICAS 85G
        ScrapedOffer(supermarket_slug="superseis", external_sku="S6-9502", raw_title="Papas Fritas Lay's Clásicas Paquete 85 g", regular_price=10500, promo_price=8900, ean="7840058001013", brand="Lays"),
        ScrapedOffer(supermarket_slug="stock", external_sku="ST-9502", raw_title="Papas Fritas Lays Clasicas 85g", regular_price=10200, promo_price=None, ean="7840058001013", brand="Lays"),
        ScrapedOffer(supermarket_slug="biggie", external_sku="BG-9502", raw_title="Papas Fritas Lay's 85g", regular_price=11000, promo_price=None, ean="7840058001013", brand="Lays"),
        ScrapedOffer(supermarket_slug="fortis", external_sku="FT-9502", raw_title="Papas Lays Clásicas 85g Bolsa", regular_price=8900, promo_price=None, ean="7840058001013", brand="Lays"),
    ]

    promotions = get_all_bank_promotions()
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

    serve_cmd = sub.add_parser("serve", help="Inicia el servidor API Gateway REST para PreciosPy")
    serve_cmd.add_argument("--port", type=int, default=8080, help="Puerto HTTP (por defecto 8080)")
    serve_cmd.add_argument("--host", default="127.0.0.1", help="Host IP")

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

    elif args.command == "serve":
        from .api import create_gateway_server

        server = create_gateway_server(host=args.host, port=args.port)
        print(f"PreciosPy API Gateway activo en http://{args.host}:{args.port}")
        print("Endpoints disponibles:")
        print(" - GET  /health")
        print(" - GET  /api/v1/sync/manifest")
        print(" - GET  /api/v1/sync/snapshot.db")
        print(" - GET  /api/v1/sync/delta")
        print(" - GET  /api/v1/supermarkets/branches")
        print(" - POST /api/v1/crowdsource/report")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            server.server_close()


if __name__ == "__main__":
    main()
