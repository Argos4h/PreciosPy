"""
Normalizador de precios en Guaraníes (PYG), validador de códigos de barras EAN-13/EAN-8
y extractor de unidades de medida (KG, LT, UN) para supermercados de Paraguay.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Expresión regular para detectar EAN-13 (especialmente prefijo 784 de Paraguay o 779 Argentina / 789 Brasil)
EAN_IN_TEXT_RE = re.compile(r"(?<!\d)(\d{8}|\d{12,14})(?!\d)")

# Expresión regular para detectar peso/volumen en el nombre del producto (ej: "500 g", "1,5 L", "250ml", "6x330ml")
MULTIPACK_RE = re.compile(
    r"\b(\d{1,2})\s*[xX*]\s*(\d+(?:[.,]\d+)?)\s*(kg|kilos?|grs?|g|lt?s?|litros?|ml|cc)\b",
    re.IGNORECASE,
)
SINGLE_UNIT_RE = re.compile(
    r"\b(\d+(?:[.,]\d+)?)\s*(kg|kilos?|grs?|g|lt?s?|litros?|ml|cc|unid(?:ades)?|un)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class UnitInfo:
    unit_measure: str      # 'KG', 'GR', 'LT', 'ML', 'UN'
    unit_quantity: float   # Cantidad en la medida declarada (ej. 500.0 para 500g)
    base_unit: str         # 'KG', 'LT' o 'UN'
    base_multiplier: float # Factor en unidad base (ej. 0.5 para 500g -> 0.5 KG)


def parse_guaranies(raw_value: str | int | float | None) -> int | None:
    """
    Convierte cualquier representación de precio paraguayo ('Gs. 18.500', '₲ 120.000', '14500,00')
    en un entero exacto en Guaraníes (PYG).
    """
    if raw_value is None:
        return None
    if isinstance(raw_value, int):
        return raw_value if raw_value > 0 else None
    if isinstance(raw_value, float):
        val = int(round(raw_value))
        return val if val > 0 else None

    text = str(raw_value).strip()
    if not text:
        return None

    # Si termina con decimales explícitos tipo ",00" los removemos antes de limpiar puntos de miles
    text = re.sub(r",\d{1,2}$", "", text)
    digits = re.sub(r"[^\d]", "", text)
    if not digits:
        return None

    value = int(digits)
    return value if value > 0 else None


def is_valid_ean(ean: str | None) -> bool:
    """
    Verifica matemáticamente el dígito verificador GS1 (Módulo 10) para códigos EAN-8, UPC-12, EAN-13 y GTIN-14.
    Evita confundir números de teléfono o SKUs internos con códigos de barras reales.
    """
    if not ean:
        return False
    clean = ean.strip()
    if not clean.isdigit() or len(clean) not in (8, 12, 13, 14):
        return False
    # Descartar códigos triviales como "0000000000000"
    if len(set(clean)) == 1:
        return False

    digits = [int(d) for d in clean]
    check_digit = digits[-1]
    payload = digits[:-1]

    # En GS1, empezando desde la derecha del payload, los pesos alternan 3, 1, 3, 1...
    total = 0
    for idx, digit in enumerate(reversed(payload)):
        weight = 3 if idx % 2 == 0 else 1
        total += digit * weight

    calculated_check = (10 - (total % 10)) % 10
    return check_digit == calculated_check


def extract_ean_from_text_or_url( *candidates: str | None) -> str | None:
    """
    Busca en URLs de imágenes, nombres de archivo o atributos un código EAN válido con checksum GS1 correcto.
    Muy útil en Superseis, Stock, Casa Rica y Areté donde la imagen suele ser '.../7840015001124.jpg'.
    """
    for text in candidates:
        if not text:
            continue
        for match in EAN_IN_TEXT_RE.finditer(text):
            candidate = match.group(1)
            if is_valid_ean(candidate):
                return candidate
    return None


def extract_unit_info(product_title: str) -> UnitInfo:
    """
    Extrae la unidad y cantidad de un título de producto paraguayo y calcula su factor base (KG o LT).
    Soporta formatos individuales ('Yerba 500g', 'Gaseosa 2,5 L') y multipacks ('Cerveza 6x330ml').
    """
    title = product_title or ""

    # 1. Verificar si es multipack (ej. "6x330ml")
    multi_match = MULTIPACK_RE.search(title)
    if multi_match:
        count = int(multi_match.group(1))
        raw_num = multi_match.group(2)
        raw_unit = multi_match.group(3).lower()
        if re.match(r"^\d+\.\d{3}$", raw_num) and raw_unit in ("ml", "cc", "g", "gr", "grs"):
            qty = float(raw_num.replace(".", ""))
        else:
            qty = float(raw_num.replace(",", "."))
        total_qty = count * qty
        return _build_unit_info(total_qty, raw_unit)

    # 2. Verificar unidad simple (ej. "500 g", "1.5 L", "2.000 ml")
    single_match = SINGLE_UNIT_RE.search(title)
    if single_match:
        raw_num = single_match.group(1)
        raw_unit = single_match.group(2).lower()
        if re.match(r"^\d+\.\d{3}$", raw_num) and raw_unit in ("ml", "cc", "g", "gr", "grs"):
            qty = float(raw_num.replace(".", ""))
        else:
            qty = float(raw_num.replace(",", "."))
        return _build_unit_info(qty, raw_unit)

    return UnitInfo(unit_measure="UN", unit_quantity=1.0, base_unit="UN", base_multiplier=1.0)


def _build_unit_info(qty: float, raw_unit: str) -> UnitInfo:
    if qty <= 0:
        return UnitInfo(unit_measure="UN", unit_quantity=1.0, base_unit="UN", base_multiplier=1.0)

    if raw_unit in ("kg", "kilo", "kilos"):
        return UnitInfo(unit_measure="KG", unit_quantity=qty, base_unit="KG", base_multiplier=qty)
    if raw_unit in ("g", "gr", "grs"):
        return UnitInfo(unit_measure="GR", unit_quantity=qty, base_unit="KG", base_multiplier=qty / 1000.0)
    if raw_unit in ("l", "lt", "lts", "litro", "litros"):
        return UnitInfo(unit_measure="LT", unit_quantity=qty, base_unit="LT", base_multiplier=qty)
    if raw_unit in ("ml", "cc"):
        return UnitInfo(unit_measure="ML", unit_quantity=qty, base_unit="LT", base_multiplier=qty / 1000.0)

    return UnitInfo(unit_measure="UN", unit_quantity=qty, base_unit="UN", base_multiplier=qty)


def calculate_price_per_base_unit(effective_price_gs: int, unit_info: UnitInfo) -> int:
    """
    Calcula cuánto cuesta 1 KG, 1 LT o 1 UN en Guaraníes para comparar envases de distinto tamaño.
    Ejemplo: Yerba de 500g a Gs. 11.000 -> Precio por KG = Gs. 22.000.
    """
    if unit_info.base_multiplier <= 0:
        return effective_price_gs
    return int(round(effective_price_gs / unit_info.base_multiplier))

