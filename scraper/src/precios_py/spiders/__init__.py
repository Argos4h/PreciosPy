"""Módulo de Spiders de PreciosPy para Supermercados de Paraguay."""

from .base import BaseSupermarketSpider
from .biggie import BiggieSpider
from .dattamax import DattamaxSpider
from .fortis import FortisMayoristaSpider
from .salemma_real import SalemmaRealSpider
from .superseis_stock import RetailSaSpider
from .tuti import TutiSpider

__all__ = [
    "BaseSupermarketSpider",
    "BiggieSpider",
    "DattamaxSpider",
    "FortisMayoristaSpider",
    "RetailSaSpider",
    "SalemmaRealSpider",
    "TutiSpider",
]
