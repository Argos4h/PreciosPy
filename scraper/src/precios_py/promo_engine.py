"""
Motor de Cálculo de Promociones Bancarias Paraguayas y Optimizador de Carrito Inteligente.
Resuelve reglas de acumulación con ofertas de góndola, días de descuento por banco y topes de compra.
"""

from __future__ import annotations

from datetime import date
from typing import Iterable

from .models import (
    BankPromotion,
    CartSupermarketSummary,
    EffectivePriceResult,
    ScrapedOffer,
)
from .normalizer import calculate_price_per_base_unit, extract_unit_info


def evaluate_offer_for_wallet(
    offer: ScrapedOffer,
    promotions: Iterable[BankPromotion],
    user_card_slugs: set[str],
    target_date: date,
) -> EffectivePriceResult:
    """
    Calcula el 'Precio Final Real' de un producto en un supermercado para la fecha indicada,
    cruzando el precio regular, el precio de oferta de góndola y las tarjetas del usuario.
    """
    unit_info = extract_unit_info(offer.raw_title)
    gondola_best = (
        min(offer.regular_price, offer.promo_price)
        if offer.promo_price is not None and offer.promo_price > 0
        else offer.regular_price
    )

    best_final_price = gondola_best
    best_cash_outflow = gondola_best
    best_cashback = 0
    best_promo: BankPromotion | None = None
    pricing_note = (
        "Oferta directa de góndola"
        if offer.promo_price and offer.promo_price < offer.regular_price
        else "Precio regular de góndola"
    )

    # Filtrar promociones activas en este supermercado para las tarjetas que posee el usuario hoy
    eligible_promos = [
        p
        for p in promotions
        if p.supermarket_slug == offer.supermarket_slug
        and p.card_slug in user_card_slugs
        and p.is_valid_on_date(target_date)
    ]

    for promo in eligible_promos:
        # Si la promo bancaria es acumulable con ofertas de góndola, aplica sobre gondola_best;
        # de lo contrario, aplica únicamente sobre regular_price.
        eligible_base = gondola_best if promo.applies_to_promo_price else offer.regular_price
        raw_discount = int(round(eligible_base * (promo.discount_pct / 100.0)))

        # Respetar el tope máximo de reintegro incluso en un producto individual caro (ej. electrodoméstico/bebida premium)
        if promo.max_refund_gs is not None:
            raw_discount = min(raw_discount, promo.max_refund_gs)

        candidate_final_price = eligible_base - raw_discount

        if candidate_final_price < best_final_price:
            best_final_price = candidate_final_price
            best_promo = promo
            if promo.mechanism == "INSTANT_POS":
                best_cash_outflow = candidate_final_price
                best_cashback = 0
                pricing_note = f"{promo.discount_pct:g}% dto. en caja con {promo.card_name}"
            else:
                best_cash_outflow = eligible_base
                best_cashback = raw_discount
                pricing_note = f"{promo.discount_pct:g}% reintegro con {promo.card_name}"
        elif (
            offer.promo_price is not None
            and not promo.applies_to_promo_price
            and candidate_final_price >= gondola_best
            and best_promo is None
        ):
            pricing_note = (
                f"Conviene oferta directa de góndola (No acumulable con {promo.card_name})"
            )

    price_per_base = calculate_price_per_base_unit(best_final_price, unit_info)

    return EffectivePriceResult(
        supermarket_slug=offer.supermarket_slug,
        regular_price=offer.regular_price,
        promo_price=offer.promo_price,
        effective_final_price=best_final_price,
        cash_outflow_at_pos=best_cash_outflow,
        cashback_amount=best_cashback,
        price_per_base_unit=price_per_base,
        base_unit=unit_info.base_unit,
        applied_promo=best_promo,
        pricing_note=pricing_note,
    )


def simulate_smart_cart_for_supermarket(
    supermarket_slug: str,
    cart_items: list[tuple[ScrapedOffer, int]],  # Lista de (ScrapedOffer, cantidad)
    promotions: Iterable[BankPromotion],
    user_card_slugs: set[str],
    target_date: date,
) -> CartSupermarketSummary:
    """
    Simula el costo total de un carrito de compras en un supermercado aplicando las reglas reales
    de topes bancarios de Paraguay (ej. si el tope de compra es Gs. 800.000 y el carrito suma Gs. 1.100.000,
    el descuento se detiene exactamente en el tope y el excedente se cobra a precio de góndola).
    """
    total_regular = 0
    total_gondola = 0
    for offer, qty in cart_items:
        total_regular += offer.regular_price * qty
        gondola_unit = (
            min(offer.regular_price, offer.promo_price)
            if offer.promo_price is not None and offer.promo_price > 0
            else offer.regular_price
        )
        total_gondola += gondola_unit * qty

    eligible_promos = [
        p
        for p in promotions
        if p.supermarket_slug == supermarket_slug
        and p.card_slug in user_card_slugs
        and p.is_valid_on_date(target_date)
    ]

    # Escenario base: pagar sin promoción bancaria (solo ofertas de góndola)
    best_summary = CartSupermarketSummary(
        supermarket_slug=supermarket_slug,
        total_regular_gs=total_regular,
        total_gondola_gs=total_gondola,
        total_cash_at_pos_gs=total_gondola,
        total_cashback_gs=0,
        net_final_cost_gs=total_gondola,
        applied_card_name=None,
        cap_reached=False,
    )

    # Evaluar cada tarjeta disponible del usuario para ver cuál minimiza el costo neto del carrito completo
    for promo in eligible_promos:
        eligible_spend_for_promo = 0
        non_eligible_spend = 0

        for offer, qty in cart_items:
            gondola_unit = (
                min(offer.regular_price, offer.promo_price)
                if offer.promo_price is not None and offer.promo_price > 0
                else offer.regular_price
            )
            if promo.applies_to_promo_price:
                eligible_spend_for_promo += gondola_unit * qty
            else:
                # Si el producto tiene una oferta de góndola mejor que el % de la tarjeta, conviene pagarlo a precio oferta
                card_unit_price = int(round(offer.regular_price * (1.0 - promo.discount_pct / 100.0)))
                if gondola_unit <= card_unit_price:
                    non_eligible_spend += gondola_unit * qty
                else:
                    eligible_spend_for_promo += offer.regular_price * qty

        cap_reached = False
        capped_eligible_spend = eligible_spend_for_promo
        if promo.spending_cap_gs is not None and eligible_spend_for_promo > promo.spending_cap_gs:
            capped_eligible_spend = promo.spending_cap_gs
            cap_reached = True

        discount_gs = int(round(capped_eligible_spend * (promo.discount_pct / 100.0)))
        if promo.max_refund_gs is not None and discount_gs > promo.max_refund_gs:
            discount_gs = promo.max_refund_gs
            cap_reached = True

        gross_ticket_gs = eligible_spend_for_promo + non_eligible_spend
        net_cost_gs = gross_ticket_gs - discount_gs
        cash_at_pos_gs = net_cost_gs if promo.mechanism == "INSTANT_POS" else gross_ticket_gs
        cashback_gs = 0 if promo.mechanism == "INSTANT_POS" else discount_gs

        if net_cost_gs < best_summary.net_final_cost_gs:
            best_summary = CartSupermarketSummary(
                supermarket_slug=supermarket_slug,
                total_regular_gs=total_regular,
                total_gondola_gs=total_gondola,
                total_cash_at_pos_gs=cash_at_pos_gs,
                total_cashback_gs=cashback_gs,
                net_final_cost_gs=net_cost_gs,
                applied_card_name=promo.card_name,
                cap_reached=cap_reached,
            )

    return best_summary

