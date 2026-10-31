"""
Módulo de Sincronización y Normalización de Beneficios y Promociones Bancarias de Paraguay.
Modela y actualiza las alianzas activas de:
- ueno bank (Nivel 1 al 5, Tarjetas Dúo Crédito QR y Débito).
- Banco Itaú (Clásica/Oro, Platinum, Black/Infinite, Pagos QR).
- Banco Continental (Conticredit, MasterCard, Visa).
- Banco Atlas (Visa/MasterCard Clásica, Oro, Platinum).
- Sudameris Bank (Visa Infinite, Platinum, Signature).
- Banco Familiar (Tarjetas Familiar y Credicard).
- Banco GNB (Tarjetas de Crédito GNB y QR).
- Tarjeta Zeta (Financiera Zeta).
- Banco Basa (Crédito y Débito Basa).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from .models import BankPromotion

logger = logging.getLogger(__name__)

# Catálogo maestro de convenios bancarios vigentes en Paraguay
PARAGUAY_BANK_PROMOTIONS_MASTER: list[dict[str, Any]] = [
    # ueno bank
    {
        "id": 1,
        "supermarket_slug": "biggie",
        "card_slug": "ueno_credito_n4",
        "card_name": "ueno Crédito QR (Nivel 4)",
        "entity_name": "ueno bank",
        "title": "35% de Reintegro ueno Nivel 4 en Biggie 24hs",
        "discount_pct": 35.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": True,
        "days_of_week": (1, 2, 3, 4, 5, 6, 7),
        "spending_cap_gs": 800000,
        "max_refund_gs": 280000,
    },
    {
        "id": 2,
        "supermarket_slug": "superseis",
        "card_slug": "ueno_credito_n4",
        "card_name": "ueno Crédito QR (Nivel 4)",
        "entity_name": "ueno bank",
        "title": "30% Reintegro ueno en Superseis",
        "discount_pct": 30.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": True,
        "days_of_week": (2, 4),
        "spending_cap_gs": 600000,
        "max_refund_gs": 180000,
    },
    {
        "id": 3,
        "supermarket_slug": "stock",
        "card_slug": "ueno_credito_n4",
        "card_name": "ueno Crédito QR (Nivel 4)",
        "entity_name": "ueno bank",
        "title": "30% Reintegro ueno en Stock",
        "discount_pct": 30.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": True,
        "days_of_week": (1, 3, 5),
        "spending_cap_gs": 600000,
        "max_refund_gs": 180000,
    },
    {
        "id": 4,
        "supermarket_slug": "tuti",
        "card_slug": "ueno_debito",
        "card_name": "ueno Débito / QR",
        "entity_name": "ueno bank",
        "title": "15% Reintegro ueno Débito en Tuti",
        "discount_pct": 15.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": True,
        "days_of_week": (1, 2, 3, 4, 5, 6, 7),
        "spending_cap_gs": 400000,
        "max_refund_gs": 60000,
    },
    # Banco Itaú
    {
        "id": 5,
        "supermarket_slug": "superseis",
        "card_slug": "itau_credito_clasica",
        "card_name": "Itaú Crédito Clásica / Oro",
        "entity_name": "Banco Itaú",
        "title": "Martes de Superseis con Itaú 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (2,),
        "spending_cap_gs": 1000000,
        "max_refund_gs": 200000,
    },
    {
        "id": 6,
        "supermarket_slug": "stock",
        "card_slug": "itau_credito_clasica",
        "card_name": "Itaú Crédito Clásica / Oro",
        "entity_name": "Banco Itaú",
        "title": "Jueves de Stock con Itaú 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (4,),
        "spending_cap_gs": 1000000,
        "max_refund_gs": 200000,
    },
    {
        "id": 7,
        "supermarket_slug": "casarica",
        "card_slug": "itau_credito_infinite",
        "card_name": "Itaú Personal Bank (Infinite)",
        "entity_name": "Banco Itaú",
        "title": "25% Reintegro Casa Rica con Itaú Personal Bank",
        "discount_pct": 25.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": True,
        "days_of_week": (3, 5),
        "spending_cap_gs": 1500000,
        "max_refund_gs": 375000,
    },
    # Banco Continental
    {
        "id": 8,
        "supermarket_slug": "stock",
        "card_slug": "continental_credito",
        "card_name": "Continental Conticredit",
        "entity_name": "Banco Continental",
        "title": "Miércoles de Supermercados con Continental 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (3,),
        "spending_cap_gs": 800000,
        "max_refund_gs": 160000,
    },
    {
        "id": 9,
        "supermarket_slug": "superseis",
        "card_slug": "continental_credito",
        "card_name": "Continental Conticredit",
        "entity_name": "Banco Continental",
        "title": "Miércoles de Continental en Superseis 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (3,),
        "spending_cap_gs": 800000,
        "max_refund_gs": 160000,
    },
    # Banco Atlas
    {
        "id": 10,
        "supermarket_slug": "superseis",
        "card_slug": "atlas_credito",
        "card_name": "Atlas Crédito / QR",
        "entity_name": "Banco Atlas",
        "title": "Lunes de Atlas en Superseis 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (1,),
        "spending_cap_gs": 750000,
        "max_refund_gs": 150000,
    },
    {
        "id": 11,
        "supermarket_slug": "arete",
        "card_slug": "atlas_credito",
        "card_name": "Atlas Crédito / QR",
        "entity_name": "Banco Atlas",
        "title": "Jueves de Areté con Banco Atlas 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (4,),
        "spending_cap_gs": 750000,
        "max_refund_gs": 150000,
    },
    # Sudameris Bank
    {
        "id": 12,
        "supermarket_slug": "stock",
        "card_slug": "sudameris_credito",
        "card_name": "Sudameris Club",
        "entity_name": "Sudameris Bank",
        "title": "Jueves de Sudameris en Stock 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (4,),
        "spending_cap_gs": 1000000,
        "max_refund_gs": 200000,
    },
    {
        "id": 13,
        "supermarket_slug": "casarica",
        "card_slug": "sudameris_credito",
        "card_name": "Sudameris Club",
        "entity_name": "Sudameris Bank",
        "title": "Viernes de Sudameris en Casa Rica 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (5,),
        "spending_cap_gs": 1000000,
        "max_refund_gs": 200000,
    },
    # Banco Familiar
    {
        "id": 14,
        "supermarket_slug": "stock",
        "card_slug": "familiar_credito",
        "card_name": "Familiar Crédito",
        "entity_name": "Banco Familiar",
        "title": "Viernes de Banco Familiar en Stock 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (5,),
        "spending_cap_gs": 700000,
        "max_refund_gs": 140000,
    },
    # Banco GNB
    {
        "id": 15,
        "supermarket_slug": "real",
        "card_slug": "gnb_credito",
        "card_name": "GNB Mastercard",
        "entity_name": "Banco GNB",
        "title": "Miércoles de Banco GNB en Cadena Real 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (3,),
        "spending_cap_gs": 800000,
        "max_refund_gs": 160000,
    },
    {
        "id": 16,
        "supermarket_slug": "salemma",
        "card_slug": "gnb_credito",
        "card_name": "GNB Mastercard",
        "entity_name": "Banco GNB",
        "title": "Domingos de Banco GNB en Salemma 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (7,),
        "spending_cap_gs": 800000,
        "max_refund_gs": 160000,
    },
    # Tarjeta Zeta
    {
        "id": 17,
        "supermarket_slug": "stock",
        "card_slug": "zeta_credito",
        "card_name": "Tarjeta Zeta",
        "entity_name": "Financiera Zeta",
        "title": "Viernes de Tarjeta Zeta en Stock 15%",
        "discount_pct": 15.0,
        "mechanism": "INSTANT_POS",
        "applies_to_promo_price": True,
        "days_of_week": (5,),
        "spending_cap_gs": 500000,
        "max_refund_gs": 75000,
    },
    # Banco Basa
    {
        "id": 18,
        "supermarket_slug": "superseis",
        "card_slug": "basa_credito",
        "card_name": "Banco Basa Crédito",
        "entity_name": "Banco Basa",
        "title": "Sábados de Banco Basa en Superseis 20%",
        "discount_pct": 20.0,
        "mechanism": "CASHBACK",
        "applies_to_promo_price": False,
        "days_of_week": (6,),
        "spending_cap_gs": 800000,
        "max_refund_gs": 160000,
    },
]


def get_all_bank_promotions() -> list[BankPromotion]:
    """Retorna todas las promociones bancarias vigentes mapeadas a objetos Pydantic."""
    return [BankPromotion(**p) for p in PARAGUAY_BANK_PROMOTIONS_MASTER]

