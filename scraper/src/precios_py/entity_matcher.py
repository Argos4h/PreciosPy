"""
Entity Resolution & Fuzzy Matcher para PreciosPy:
Unifica ofertas de distintos supermercados en un único Producto Maestro.
Transfiere automáticamente códigos EAN-13 entre cadenas cuando hay coincidencia de marca,
gramaje/volumen idéntico y alta similitud léxica.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from typing import Iterable

from .models import ScrapedOffer
from .normalizer import extract_unit_info

STOP_WORDS = {
    "de", "del", "la", "el", "los", "las", "un", "una", "unos", "unas",
    "x", "en", "con", "por", "para", "sin", "al", "caja", "paquete",
    "botella", "lata", "sabor", "tipo", "original", "vacio", "vacio.",
    "uni", "uni.", "unidades", "unidad",
    "l", "lt", "lts", "litro", "litros", "ml", "cc", "kg", "kilo", "kilos", "g", "gr", "grs",
}

BRAND_CANONICAL = {
    "coca-cola": "coca cola",
    "pepsi-cola": "pepsi",
    "trebol": "trébol",
    "kurupi": "kurupí",
    "heineken": "heineken",
    "pilsen": "pilsen",
    "brahma": "brahma",
    "ochsi": "ochsi",
    "campesino": "campesino",
    "pajarito": "pajarito",
    "taragui": "taragüi",
    "selecta": "selecta",
    "colon": "colón",
}


def clean_tokens(text: str) -> set[str]:
    """Extrae conjunto de palabras clave significativas sin acentos ni conectores."""
    t = text.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    raw_tokens = t.split()
    tokens = set()
    for tok in raw_tokens:
        tok = tok.strip()
        if not tok or tok in STOP_WORDS or tok.isdigit():
            continue
        tok = BRAND_CANONICAL.get(tok, tok)
        tokens.add(tok)
    return tokens


def calculate_token_similarity(title_a: str, title_b: str) -> float:
    """Calcula similitud de solapamiento de tokens (Overlap) y coeficiente de Jaccard."""
    tokens_a = clean_tokens(title_a)
    tokens_b = clean_tokens(title_b)

    if not tokens_a or not tokens_b:
        return 0.0

    intersection = tokens_a.intersection(tokens_b)
    if not intersection:
        return 0.0

    overlap = len(intersection) / min(len(tokens_a), len(tokens_b))
    jaccard = len(intersection) / len(tokens_a.union(tokens_b))
    return (overlap * 0.65) + (jaccard * 0.35)


@dataclass
class UnifiedProductGroup:
    product_id: int
    canonical_ean: str | None
    canonical_name: str
    brand: str | None
    unit_measure: str
    unit_quantity: float
    base_unit: str
    base_multiplier: float
    offers: list[ScrapedOffer]


class EntityResolver:
    """
    Agrupa ofertas de múltiples supermercados resolviendo duplicados por:
    1. EAN-13 GS1 exacto (Nivel 1 - 100% Determinista)
    2. Gramaje/Volumen exacto + Marca + Similitud léxica >= 0.75 (Nivel 2)
    """

    def __init__(self, fuzzy_threshold: float = 0.75):
        self.fuzzy_threshold = fuzzy_threshold

    def resolve_catalog(self, offers: Iterable[ScrapedOffer]) -> list[UnifiedProductGroup]:
        groups: list[UnifiedProductGroup] = []
        ean_index: dict[str, UnifiedProductGroup] = {}
        next_id = 1

        for offer in offers:
            # 1. Intento por EAN-13 exacto
            if offer.ean and offer.ean in ean_index:
                target_group = ean_index[offer.ean]
                self._add_offer_to_group(target_group, offer)
                continue

            # 2. Intento por coincidencia de tamaño y similitud léxica con grupos existentes
            unit_info = extract_unit_info(offer.raw_title)
            matched_group: UnifiedProductGroup | None = None
            best_score = 0.0

            for group in groups:
                # Regla estricta: nunca unificar productos de diferente tamaño o unidad base
                if (
                    group.base_unit != unit_info.base_unit
                    or abs(group.base_multiplier - unit_info.base_multiplier) > 0.05
                ):
                    continue

                # Si ambos tienen EAN diferente, jamás unificar
                if offer.ean and group.canonical_ean and offer.ean != group.canonical_ean:
                    continue

                score = calculate_token_similarity(group.canonical_name, offer.raw_title)
                if score >= self.fuzzy_threshold and score > best_score:
                    best_score = score
                    matched_group = group

            if matched_group is not None:
                self._add_offer_to_group(matched_group, offer)
                # Si la nueva oferta aportó un EAN que el grupo no tenía, indexarlo
                if matched_group.canonical_ean and matched_group.canonical_ean not in ean_index:
                    ean_index[matched_group.canonical_ean] = matched_group
            else:
                # 3. Crear nuevo grupo de producto
                new_group = UnifiedProductGroup(
                    product_id=next_id,
                    canonical_ean=offer.ean,
                    canonical_name=offer.raw_title.strip(),
                    brand=offer.brand,
                    unit_measure=unit_info.unit_measure,
                    unit_quantity=unit_info.unit_quantity,
                    base_unit=unit_info.base_unit,
                    base_multiplier=unit_info.base_multiplier,
                    offers=[offer],
                )
                next_id += 1
                groups.append(new_group)
                if offer.ean:
                    ean_index[offer.ean] = new_group

        return groups

    def _add_offer_to_group(self, group: UnifiedProductGroup, offer: ScrapedOffer) -> None:
        # Si el grupo no tenía EAN y la oferta entrante sí tiene EAN válido, el grupo lo adopta
        if not group.canonical_ean and offer.ean:
            group.canonical_ean = offer.ean
            # Propagar retroactivamente a todas las ofertas previas del grupo
            for prev_offer in group.offers:
                if not prev_offer.ean:
                    prev_offer.ean = offer.ean

        # Replicar el EAN canónico en la nueva oferta si no lo tenía
        if group.canonical_ean and not offer.ean:
            offer.ean = group.canonical_ean

        if not group.brand and offer.brand:
            group.brand = offer.brand

        group.offers.append(offer)
