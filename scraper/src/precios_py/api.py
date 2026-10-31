"""
API Gateway de Sincronización, Sucursales y Crowdsourcing para PreciosPy.
Diseñado para correr tanto con FastAPI/Uvicorn como con un servidor HTTP asíncrono nativo.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .delta_sync import DeltaSyncBundle
from .models import BankPromotion, ScrapedOffer

PARAGUAY_BRANCHES = [
    {
        "id": 1,
        "supermarket_slug": "superseis",
        "supermarket_name": "Superseis Hiperseis",
        "address": "Avda. Mcal. López y Boggiani, Asunción",
        "city": "Asunción",
        "latitude": -25.2974,
        "longitude": -57.5682,
        "opening_hours": "07:00 - 23:00",
        "has_pickup": True,
    },
    {
        "id": 2,
        "supermarket_slug": "superseis",
        "supermarket_name": "Superseis España",
        "address": "Avda. España y Brasilia, Asunción",
        "city": "Asunción",
        "latitude": -25.2891,
        "longitude": -57.6042,
        "opening_hours": "07:00 - 23:00",
        "has_pickup": True,
    },
    {
        "id": 3,
        "supermarket_slug": "stock",
        "supermarket_name": "Stock San Lorenzo",
        "address": "Ruta Mcal. Estigarribia Km 14.5, San Lorenzo",
        "city": "San Lorenzo",
        "latitude": -25.3421,
        "longitude": -57.5143,
        "opening_hours": "07:00 - 22:30",
        "has_pickup": True,
    },
    {
        "id": 4,
        "supermarket_slug": "biggie",
        "supermarket_name": "Biggie Express Villamorra",
        "address": "Avda. Mcal. López y Senador Long, Asunción",
        "city": "Asunción",
        "latitude": -25.2952,
        "longitude": -57.5815,
        "opening_hours": "24 Horas",
        "has_pickup": False,
    },
    {
        "id": 5,
        "supermarket_slug": "casarica",
        "supermarket_name": "Casa Rica España",
        "address": "Avda. España y Dr. Bestard, Asunción",
        "city": "Asunción",
        "latitude": -25.2865,
        "longitude": -57.5752,
        "opening_hours": "07:30 - 21:30",
        "has_pickup": True,
    },
    {
        "id": 6,
        "supermarket_slug": "arete",
        "supermarket_name": "Areté Primer Presidente",
        "address": "Avda. Primer Presidente e Itapúa, Asunción",
        "city": "Asunción",
        "latitude": -25.2612,
        "longitude": -57.5701,
        "opening_hours": "07:00 - 22:00",
        "has_pickup": True,
    },
]

# Almacén en memoria de reportes comunitarios recibidos (Crowdsourcing)
CROWDSOURCED_REPORTS: list[dict[str, Any]] = []


class PreciosPyApiHandler(BaseHTTPRequestHandler):
    repo_root = Path(__file__).resolve().parents[3]

    def _send_json(self, data: Any, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        if path in ("", "/health"):
            self._send_json({"status": "healthy", "service": "PreciosPy Gateway", "version": "1.0.0"})
            return

        if path == "/api/v1/sync/manifest":
            db_path = self.repo_root / "dist" / "catalog_latest.db"
            db_size = db_path.stat().st_size if db_path.exists() else 0
            self._send_json({
                "latest_version": date.today().isoformat(),
                "snapshot_generated_at": datetime.now().isoformat(),
                "database_size_bytes": db_size,
                "download_url": "/api/v1/sync/snapshot.db",
                "delta_url": "/api/v1/sync/delta",
                "supported_supermarkets": ["superseis", "stock", "biggie", "casarica", "arete"],
            })
            return

        if path == "/api/v1/sync/snapshot.db":
            db_path = self.repo_root / "dist" / "catalog_latest.db"
            if not db_path.exists():
                db_path = self.repo_root / "mobile" / "assets" / "db" / "catalog_latest.db"

            if db_path.exists():
                content = db_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.sqlite3")
                self.send_header("Content-Disposition", 'attachment; filename="catalog_latest.db"')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self._send_json({"error": "Snapshot database not found"}, status=404)
            return

        if path == "/api/v1/sync/delta":
            since = params.get("since", [None])[0]
            # Demo payload representativo del DeltaSyncBundle
            sample_delta = {
                "since_version": since or "baseline",
                "current_version": date.today().isoformat(),
                "total_price_changes": 2,
                "updated_offers": [
                    {
                        "supermarket_slug": "biggie",
                        "external_sku": "BG-8821",
                        "ean": "7840000000036",
                        "raw_title": "Yerba Kurupi Menta y Boldo 500g",
                        "old_regular_price": 17500,
                        "new_regular_price": 16900,
                        "new_promo_price": 14900,
                    },
                    {
                        "supermarket_slug": "superseis",
                        "external_sku": "S6-2040",
                        "ean": "7840000000106",
                        "raw_title": "Leche Entera Trébol UAT Cartón 1 L",
                        "old_regular_price": 9800,
                        "new_regular_price": 9500,
                        "new_promo_price": 8700,
                    },
                ],
            }
            self._send_json(sample_delta)
            return

        if path == "/api/v1/supermarkets/branches":
            city_filter = params.get("city", [None])[0]
            branches = PARAGUAY_BRANCHES
            if city_filter:
                branches = [b for b in branches if b["city"].lower() == city_filter.lower()]
            self._send_json({"total_branches": len(branches), "branches": branches})
            return

        if path == "/api/v1/crowdsource/reports":
            self._send_json({
                "total_reports": len(CROWDSOURCED_REPORTS),
                "reports": CROWDSOURCED_REPORTS,
            })
            return

        self._send_json({"error": "Endpoint not found", "path": path}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/v1/crowdsource/report":
            content_len = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_len)
            try:
                data = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                self._send_json({"error": "Invalid JSON body"}, status=400)
                return

            ean = str(data.get("ean", "")).strip()
            title = str(data.get("product_name", "")).strip()
            price_gs = data.get("price_gs")
            supermarket_slug = str(data.get("supermarket_slug", "")).strip()

            if not title or not price_gs or not supermarket_slug:
                self._send_json({"error": "Missing required fields: product_name, price_gs, supermarket_slug"}, status=422)
                return

            report_entry = {
                "id": len(CROWDSOURCED_REPORTS) + 1,
                "ean": ean or None,
                "product_name": title,
                "price_gs": int(price_gs),
                "supermarket_slug": supermarket_slug,
                "submitted_at": datetime.now().isoformat(),
                "status": "APPROVED_AUTO",
                "reward_points": 50,
            }
            CROWDSOURCED_REPORTS.append(report_entry)

            self._send_json({
                "status": "success",
                "message": "¡Reporte recibido! Gracias por ayudar a la comunidad de PreciosPy.",
                "reward_points_earned": 50,
                "entry": report_entry,
            }, status=201)
            return

        self._send_json({"error": "Endpoint not found"}, status=404)


def create_gateway_server(host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    return HTTPServer((host, port), PreciosPyApiHandler)

