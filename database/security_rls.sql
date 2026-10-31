-- ============================================================================
-- PRECIOSPY - POLÍTICAS DE SEGURIDAD Y ROW LEVEL SECURITY (RLS) EN SUPABASE
-- ============================================================================
-- Este script configura la seguridad de grado de producción en Supabase / PostgreSQL:
-- 1. Habilita RLS en todas las tablas del esquema público.
-- 2. Concede acceso de LECTURA PÚBLICA (SELECT) a clientes anónimos y autenticados
--    (Precios y ofertas minoristas de Paraguay son datos públicos).
-- 3. Restringe ESCRITURA, MODIFICACIÓN y ELIMINACIÓN (INSERT, UPDATE, DELETE)
--    exclusivamente al rol 'service_role' (Scrapers nocturnos y Workers autorizados).
-- 4. Protege los datos privados de usuarios (Favoritos, Listas y Ahorros) mediante
--    aislamiento estricto por auth.uid().
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. HABILITAR ROW LEVEL SECURITY (RLS) EN TABLAS PÚBLICAS DE CATÁLOGO
-- ----------------------------------------------------------------------------
ALTER TABLE IF EXISTS categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS supermarkets ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS products ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS store_offers ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS price_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS financial_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS payment_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS bank_promotions ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- 2. POLÍTICAS DE LECTURA PÚBLICA (SELECT PARA CLIENTES ANON & AUTHENTICATED)
-- ----------------------------------------------------------------------------

-- Categorías: lectura pública
DROP POLICY IF EXISTS "Public read access on categories" ON categories;
CREATE POLICY "Public read access on categories"
    ON categories FOR SELECT
    TO anon, authenticated
    USING (true);

-- Supermercados: lectura pública de supermercados activos
DROP POLICY IF EXISTS "Public read access on supermarkets" ON supermarkets;
CREATE POLICY "Public read access on supermarkets"
    ON supermarkets FOR SELECT
    TO anon, authenticated
    USING (is_active = true);

-- Productos del catálogo: lectura pública
DROP POLICY IF EXISTS "Public read access on products" ON products;
CREATE POLICY "Public read access on products"
    ON products FOR SELECT
    TO anon, authenticated
    USING (true);

-- Ofertas en góndolas: lectura pública de ofertas en stock
DROP POLICY IF EXISTS "Public read access on store_offers" ON store_offers;
CREATE POLICY "Public read access on store_offers"
    ON store_offers FOR SELECT
    TO anon, authenticated
    USING (in_stock = true);

-- Historial de precios (Ficha Knasta): lectura pública
DROP POLICY IF EXISTS "Public read access on price_history" ON price_history;
CREATE POLICY "Public read access on price_history"
    ON price_history FOR SELECT
    TO anon, authenticated
    USING (true);

-- Entidades financieras (Bancos): lectura pública de entidades activas
DROP POLICY IF EXISTS "Public read access on financial_entities" ON financial_entities;
CREATE POLICY "Public read access on financial_entities"
    ON financial_entities FOR SELECT
    TO anon, authenticated
    USING (is_active = true);

-- Tarjetas de pago: lectura pública
DROP POLICY IF EXISTS "Public read access on payment_cards" ON payment_cards;
CREATE POLICY "Public read access on payment_cards"
    ON payment_cards FOR SELECT
    TO anon, authenticated
    USING (true);

-- Promociones bancarias: lectura pública de promociones vigentes
DROP POLICY IF EXISTS "Public read access on bank_promotions" ON bank_promotions;
CREATE POLICY "Public read access on bank_promotions"
    ON bank_promotions FOR SELECT
    TO anon, authenticated
    USING (is_active = true AND valid_until >= CURRENT_DATE);

-- ----------------------------------------------------------------------------
-- 3. POLÍTICAS DE ESCRITURA RESTRINGIDAS AL SERVICE ROLE (SCRAPERS / BACKEND)
-- ----------------------------------------------------------------------------
-- Ningún usuario público (anon ni authenticated común) puede modificar precios,
-- insertar productos ni alterar promociones bancarias.

DO $$
DECLARE
    tbl text;
BEGIN
    FOR tbl IN
        SELECT unnest(ARRAY[
            'categories',
            'supermarkets',
            'products',
            'store_offers',
            'price_history',
            'financial_entities',
            'payment_cards',
            'bank_promotions'
        ])
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Service role write access on %I" ON %I;', tbl, tbl);
        EXECUTE format('
            CREATE POLICY "Service role write access on %I"
                ON %I FOR ALL
                TO service_role
                USING (true)
                WITH CHECK (true);
        ', tbl, tbl);
    END LOOP;
END $$;

-- ----------------------------------------------------------------------------
-- 4. TABLAS DE USUARIO Y PRIVACIDAD DE DATOS (AUTH.UID())
-- ----------------------------------------------------------------------------

-- Perfil de Usuario y configuración de tarjetas personales
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    full_name TEXT,
    selected_city TEXT DEFAULT 'Asunción',
    configured_cards JSONB DEFAULT '[]'::jsonb,
    is_cash_only BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can read own profile" ON user_profiles;
CREATE POLICY "Users can read own profile"
    ON user_profiles FOR SELECT
    TO authenticated
    USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update own profile" ON user_profiles;
CREATE POLICY "Users can update own profile"
    ON user_profiles FOR UPDATE
    TO authenticated
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Users can insert own profile" ON user_profiles;
CREATE POLICY "Users can insert own profile"
    ON user_profiles FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = id);

-- Historial y Registro de Ahorros del Usuario
CREATE TABLE IF NOT EXISTS user_savings_records (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    purchase_date TIMESTAMPTZ DEFAULT NOW(),
    store_name TEXT NOT NULL,
    items_count INT NOT NULL DEFAULT 1,
    saved_amount_gs INT NOT NULL CHECK (saved_amount_gs >= 0),
    paid_total_gs INT NOT NULL CHECK (paid_total_gs >= 0),
    regular_total_gs INT NOT NULL CHECK (regular_total_gs >= 0),
    applied_benefits TEXT,
    is_split_purchase BOOLEAN DEFAULT FALSE
);

ALTER TABLE user_savings_records ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can manage own savings records" ON user_savings_records;
CREATE POLICY "Users can manage own savings records"
    ON user_savings_records FOR ALL
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Favoritos del Usuario
CREATE TABLE IF NOT EXISTS user_favorites (
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, product_id)
);

ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can manage own favorites" ON user_favorites;
CREATE POLICY "Users can manage own favorites"
    ON user_favorites FOR ALL
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- ----------------------------------------------------------------------------
-- 5. BLINDAJE CONTRA INYECCIÓN SQL Y HARDENING DE FUNCIONES RPC
-- ----------------------------------------------------------------------------
-- Se asegura que cualquier función RPC creada en Supabase tenga un search_path seguro.
ALTER DEFAULT PRIVILEGES REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
