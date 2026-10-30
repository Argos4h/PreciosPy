"""
Clase base para Spiders de Supermercados en Paraguay.
Gestiona concurrencia con asyncio.Semaphore, reintentos exponenciales y cabeceras HTTP realistas.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from ..models import ScrapedOffer

logger = logging.getLogger(__name__)


class BaseSupermarketSpider(ABC):
    supermarket_slug: str
    base_url: str

    def __init__(self, concurrency: int = 10, timeout_sec: float = 20.0):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout_sec = timeout_sec
        self.default_headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-PY,es;q=0.9,en;q=0.7",
        }

    async def fetch_text(self, client: Any, url: str, retries: int = 3) -> str:
        async with self.semaphore:
            for attempt in range(1, retries + 1):
                try:
                    resp = await client.get(url, headers=self.default_headers, timeout=self.timeout_sec)
                    resp.raise_for_status()
                    return resp.text
                except Exception as exc:
                    if attempt == retries:
                        logger.error("Fallo definitivo al consultar %s: %s", url, exc)
                        raise
                    await asyncio.sleep(0.8 * attempt)
        return ""

    async def fetch_json(self, client: Any, url: str, params: dict | None = None, retries: int = 3) -> Any:
        async with self.semaphore:
            for attempt in range(1, retries + 1):
                try:
                    resp = await client.get(
                        url,
                        params=params,
                        headers={**self.default_headers, "Accept": "application/json"},
                        timeout=self.timeout_sec,
                    )
                    resp.raise_for_status()
                    return resp.json()
                except Exception as exc:
                    if attempt == retries:
                        logger.error("Fallo definitivo al consultar JSON %s: %s", url, exc)
                        raise
                    await asyncio.sleep(0.8 * attempt)
        return {}

    @abstractmethod
    def parse_catalog_payload(self, raw_payload: Any) -> list[ScrapedOffer]:
        """Transforma el HTML o JSON crudo del supermercado en objetos ScrapedOffer normalizados."""
        raise NotImplementedError

