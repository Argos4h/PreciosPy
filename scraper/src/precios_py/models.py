"""
Modelos de dominio para Productos, Ofertas de Supermercados y Promociones Bancarias de Paraguay.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class ScrapedOffer:
    supermarket_slug: str
    external_sku: str
    raw_title: str
    regular_price: int                  # Guaraníes (PYG)
    promo_price: int | None = None      # Precio oferta directa en góndola
    club_price: int | None = None       # Precio fidelidad gratuita (ej. Socio Stock)
    wholesale_price: int | None = None  # Precio mayorista (Fortis / Box)
    wholesale_min_qty: int | None = None
    ean: str | None = None
    brand: str | None = None
    in_stock: bool = True
    product_url: str = ""
    image_url: str | None = None
    scraped_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class BankPromotion:
    id: int
    supermarket_slug: str
    card_slug: str
    card_name: str
    entity_name: str
    title: str
    discount_pct: float                 # Ej: 25.0 o 35.0
    mechanism: str                      # 'CASHBACK' o 'INSTANT_POS'
    applies_to_promo_price: bool        # Si se acumula sobre productos ya rebajados
    days_of_week: tuple[int, ...]       # ISO 1=Lunes ... 7=Domingo
    spending_cap_gs: int | None = None  # Tope de compra en Gs (ej. 800000)
    max_refund_gs: int | None = None    # Tope de reintegro en Gs (ej. 280000)

    def is_valid_on_date(self, target_date: date) -> bool:
        return target_date.isoweekday() in self.days_of_week


@dataclass(frozen=True)
class EffectivePriceResult:
    supermarket_slug: str
    regular_price: int
    promo_price: int | None
    effective_final_price: int          # Precio real final considerando la mejor opción hoy
    cash_outflow_at_pos: int            # Lo que el usuario paga efectivamente en la caja registradora
    cashback_amount: int                # Reintegro que acredita el banco luego
    price_per_base_unit: int            # Precio final normalizado por 1 KG / 1 LT / 1 UN
    base_unit: str                      # 'KG', 'LT', 'UN'
    applied_promo: BankPromotion | None
    pricing_note: str                   # Explicación clara para la UI móvil


@dataclass(frozen=True)
class CartSupermarketSummary:
    supermarket_slug: str
    total_regular_gs: int
    total_gondola_gs: int               # Total sin tarjetas (solo ofertas de góndola)
    total_cash_at_pos_gs: int           # Desembolso en caja
    total_cashback_gs: int              # Reintegro real (respetando el tope spending_cap_gs del banco)
    net_final_cost_gs: int              # Costo neto final real para el bolsillo del usuario
    applied_card_name: str | None
    cap_reached: bool                   # True si el carrito superó el tope de compra de la tarjeta

