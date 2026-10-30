-- ============================================================================
-- ESQUEMA SQLITE LOCAL (OFFLINE-FIRST) PARA EL CLIENTE MÓVIL FLUTTER (DRIFT)
-- Incluye tabla virtual FTS5 con eliminación de tildes para búsqueda < 4 ms
-- ============================================================================

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sync_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS local_supermarkets (
    id INTEGER PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    is_wholesale INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS local_products (
    id INTEGER PRIMARY KEY,
    ean TEXT UNIQUE,
    normalized_name TEXT NOT NULL,
    brand TEXT,
    unit_measure TEXT NOT NULL,
    unit_quantity REAL NOT NULL,
    base_unit TEXT NOT NULL,
    image_url TEXT
);

CREATE INDEX IF NOT EXISTS idx_local_products_ean ON local_products(ean);

-- Tabla Virtual FTS5 para búsqueda instantánea sin conexión y sin acentos
CREATE VIRTUAL TABLE IF NOT EXISTS local_products_fts USING fts5(
    product_id UNINDEXED,
    ean,
    normalized_name,
    brand,
    tokenize = 'unicode61 remove_diacritics 2'
);

CREATE TABLE IF NOT EXISTS local_offers (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES local_products(id) ON DELETE CASCADE,
    supermarket_id INTEGER NOT NULL REFERENCES local_supermarkets(id) ON DELETE CASCADE,
    regular_price INTEGER NOT NULL,
    promo_price INTEGER,
    club_price INTEGER,
    wholesale_price INTEGER,
    wholesale_min_qty INTEGER,
    price_per_base_unit INTEGER NOT NULL,
    in_stock INTEGER NOT NULL DEFAULT 1,
    scraped_at TEXT NOT NULL,
    UNIQUE(supermarket_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_local_offers_product ON local_offers(product_id);

CREATE TABLE IF NOT EXISTS local_payment_cards (
    id INTEGER PRIMARY KEY,
    entity_slug TEXT NOT NULL,
    entity_name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    card_type TEXT NOT NULL,
    tier_label TEXT
);

CREATE TABLE IF NOT EXISTS local_bank_promotions (
    id INTEGER PRIMARY KEY,
    supermarket_id INTEGER NOT NULL REFERENCES local_supermarkets(id) ON DELETE CASCADE,
    card_id INTEGER NOT NULL REFERENCES local_payment_cards(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    discount_pct REAL NOT NULL,
    mechanism TEXT NOT NULL,
    applies_to_promo_price INTEGER NOT NULL DEFAULT 0,
    days_of_week_csv TEXT NOT NULL,          -- Ej: '1,2,3,4,5,6,7' o '2'
    spending_cap_gs INTEGER,
    max_refund_gs INTEGER
);

