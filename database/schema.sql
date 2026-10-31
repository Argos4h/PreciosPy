-- ============================================================================
-- PRECIOSPY - ESQUEMA MAESTRO POSTGRESQL / SUPABASE
-- Optimizado para retail y promociones bancarias de Paraguay (Moneda: PYG entero)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- 1. CATEGORÍAS DE PRODUCTOS
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    parent_id INT REFERENCES categories(id) ON DELETE SET NULL
);

-- 2. CADENAS DE SUPERMERCADOS Y TIENDAS EN PARAGUAY
CREATE TABLE IF NOT EXISTS supermarkets (
    id SMALLSERIAL PRIMARY KEY,
    slug VARCHAR(32) UNIQUE NOT NULL,        -- 'superseis', 'stock', 'biggie', 'casarica', 'arete', 'fortis'
    name VARCHAR(64) NOT NULL,
    chain_group VARCHAR(64),                 -- Ej: 'Retail S.A. (Grupo Vierci)'
    website_url TEXT NOT NULL,
    logo_url TEXT,
    is_wholesale BOOLEAN DEFAULT FALSE,      -- TRUE para Fortis / Box Mayorista
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. CATÁLOGO MAESTRO DE PRODUCTOS (UNIFICADO POR EAN / GTIN)
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    ean VARCHAR(18) UNIQUE,                  -- EAN-13, EAN-8 o GTIN-14 (NULL solo en pesables sin código estándar)
    normalized_name VARCHAR(255) NOT NULL,   -- Ej: 'Leche Entera Trébol UAT Cartón 1 L'
    brand VARCHAR(100),                      -- Ej: 'Trébol'
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    unit_measure VARCHAR(10) NOT NULL DEFAULT 'UN', -- 'KG', 'LT', 'UN', 'GR', 'ML'
    unit_quantity NUMERIC(10,3) NOT NULL DEFAULT 1.000,
    base_unit VARCHAR(10) NOT NULL DEFAULT 'UN',    -- 'KG', 'LT' o 'UN' (para comparar envases de distinto tamaño)
    image_url TEXT,
    is_weighable BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_ean ON products(ean);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_trgm ON products USING gin (normalized_name gin_trgm_ops);

-- 4. OFERTAS VIGENTES POR SUPERMERCADO (1 fila por Producto x Supermercado)
CREATE TABLE IF NOT EXISTS store_offers (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    supermarket_id SMALLINT NOT NULL REFERENCES supermarkets(id) ON DELETE CASCADE,
    external_sku VARCHAR(64) NOT NULL,
    raw_title VARCHAR(255) NOT NULL,
    regular_price INT NOT NULL CHECK (regular_price > 0),  -- Guaraníes (PYG)
    promo_price INT CHECK (promo_price IS NULL OR promo_price > 0),
    club_price INT CHECK (club_price IS NULL OR club_price > 0),
    wholesale_price INT CHECK (wholesale_price IS NULL OR wholesale_price > 0),
    wholesale_min_qty SMALLINT CHECK (wholesale_min_qty IS NULL OR wholesale_min_qty > 1),
    price_per_base_unit INT NOT NULL,        -- Precio por 1 KG, 1 LT o 1 UN en Guaraníes
    in_stock BOOLEAN DEFAULT TRUE,
    product_url TEXT,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (supermarket_id, external_sku),
    UNIQUE (supermarket_id, product_id)
);

CREATE INDEX IF NOT EXISTS idx_offers_product ON store_offers(product_id);
CREATE INDEX IF NOT EXISTS idx_offers_supermarket ON store_offers(supermarket_id);
CREATE INDEX IF NOT EXISTS idx_offers_scraped_at ON store_offers(scraped_at);

-- 5. HISTORIAL DE PRECIOS (SOLO SE REGISTRA CUANDO HAY VARIACIÓN DE PRECIO)
CREATE TABLE IF NOT EXISTS price_history (
    id BIGSERIAL PRIMARY KEY,
    store_offer_id BIGINT NOT NULL REFERENCES store_offers(id) ON DELETE CASCADE,
    recorded_date DATE NOT NULL DEFAULT CURRENT_DATE,
    regular_price INT NOT NULL,
    promo_price INT,
    club_price INT,
    wholesale_price INT,
    UNIQUE (store_offer_id, recorded_date)
);

CREATE INDEX IF NOT EXISTS idx_history_offer_date ON price_history(store_offer_id, recorded_date DESC);

-- 6. ENTIDADES FINANCIERAS / BANCOS / BILLETERAS DE PARAGUAY
CREATE TABLE IF NOT EXISTS financial_entities (
    id SMALLSERIAL PRIMARY KEY,
    slug VARCHAR(32) UNIQUE NOT NULL,        -- 'ueno', 'itau', 'continental', 'atlas', 'sudameris', 'familiar', 'gnb'
    name VARCHAR(64) NOT NULL,
    entity_type VARCHAR(20) NOT NULL DEFAULT 'BANK', -- 'BANK', 'WALLET', 'COOPERATIVE'
    logo_url TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- 7. TARJETAS Y SEGMENTOS DE CLIENTE (EJ: UENO UP NIVELES 1-5, ITAÚ ORO/INFINITE)
CREATE TABLE IF NOT EXISTS payment_cards (
    id SMALLSERIAL PRIMARY KEY,
    entity_id SMALLINT NOT NULL REFERENCES financial_entities(id) ON DELETE CASCADE,
    slug VARCHAR(64) UNIQUE NOT NULL,        -- 'ueno_credito_n3', 'itau_credito_oro', 'continental_credito'
    name VARCHAR(100) NOT NULL,
    card_type VARCHAR(20) NOT NULL,          -- 'CREDIT', 'DEBIT', 'PREPAID', 'QR_WALLET'
    tier_label VARCHAR(40) DEFAULT 'General' -- 'Nivel 1', 'Nivel 3', 'Infinite', 'Black', 'General'
);

-- 8. PROMOCIONES Y DESCUENTOS BANCARIOS EN SUPERMERCADOS
CREATE TABLE IF NOT EXISTS bank_promotions (
    id SERIAL PRIMARY KEY,
    supermarket_id SMALLINT NOT NULL REFERENCES supermarkets(id) ON DELETE CASCADE,
    card_id SMALLINT NOT NULL REFERENCES payment_cards(id) ON DELETE CASCADE,
    title VARCHAR(140) NOT NULL,
    discount_pct NUMERIC(5,2) NOT NULL CHECK (discount_pct > 0 AND discount_pct <= 100),
    mechanism VARCHAR(20) NOT NULL,          -- 'CASHBACK' (reintegro en extracto), 'INSTANT_POS' (descuento en caja), 'MIXED'
    applies_to_promo_price BOOLEAN DEFAULT FALSE, -- TRUE si el reintegro aplica sobre productos ya en oferta
    days_of_week SMALLINT[] NOT NULL,        -- ISO 8601: 1=Lunes ... 7=Domingo
    specific_dates DATE[],                   -- Fechas puntuales (ej. días de cobro fin de mes)
    spending_cap_gs INT,                     -- Tope de compra mensual/diario en Guaraníes (ej: 800000)
    max_refund_gs INT,                       -- Tope máximo de reintegro en Guaraníes (ej: 200000)
    payment_channel VARCHAR(30) DEFAULT 'QR_POS', -- 'QR_POS', 'PHYSICAL_CARD', 'ECOMMERCE_ONLY', 'ANY'
    valid_from DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_until DATE NOT NULL DEFAULT (CURRENT_DATE + INTERVAL '90 days'),
    terms_notes TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_bank_promos_super_card ON bank_promotions(supermarket_id, card_id) WHERE is_active = TRUE;



-- ============================================================================
-- POLÍTICAS DE ROW LEVEL SECURITY (RLS) PARA SUPABASE
-- ============================================================================
-- Se habilita RLS para proteger la base de datos de modificaciones no autorizadas
-- desde clientes anónimos con anon key.
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE supermarkets ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE store_offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE financial_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE bank_promotions ENABLE ROW LEVEL SECURITY;

-- Políticas de lectura pública para datos del retail
CREATE POLICY "Public read on categories" ON categories FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public read on supermarkets" ON supermarkets FOR SELECT TO anon, authenticated USING (is_active = true);
CREATE POLICY "Public read on products" ON products FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public read on store_offers" ON store_offers FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public read on price_history" ON price_history FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public read on financial_entities" ON financial_entities FOR SELECT TO anon, authenticated USING (is_active = true);
CREATE POLICY "Public read on payment_cards" ON payment_cards FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Public read on bank_promotions" ON bank_promotions FOR SELECT TO anon, authenticated USING (is_active = true);

-- Políticas de escritura exclusivas para el Service Role (Spiders / Ingesta de Scraper)
CREATE POLICY "Service role write on categories" ON categories FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on supermarkets" ON supermarkets FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on products" ON products FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on store_offers" ON store_offers FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on price_history" ON price_history FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on financial_entities" ON financial_entities FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on payment_cards" ON payment_cards FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "Service role write on bank_promotions" ON bank_promotions FOR ALL TO service_role USING (true) WITH CHECK (true);
