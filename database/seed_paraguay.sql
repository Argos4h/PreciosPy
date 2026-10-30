-- ============================================================================
-- SEMILLAS INICIALES: SUPERMERCADOS Y PROMOCIONES BANCARIAS DE PARAGUAY
-- ============================================================================

INSERT INTO supermarkets (slug, name, chain_group, website_url, is_wholesale) VALUES
    ('superseis', 'Superseis', 'Retail S.A. (Grupo Vierci)', 'https://www.superseis.com.py', FALSE),
    ('stock', 'Supermercados Stock', 'Retail S.A. (Grupo Vierci)', 'https://www.stock.com.py', FALSE),
    ('biggie', 'Biggie Express', 'Biggie S.A.', 'https://biggie.com.py', FALSE),
    ('casarica', 'Casa Rica', 'Casa Rica S.A.', 'https://www.casarica.com.py', FALSE),
    ('arete', 'Supermercados Areté', 'Areté S.A.', 'https://www.arete.com.py', FALSE),
    ('fortis', 'Fortis Mayorista', 'Grupo Cogorno / Vierci', 'https://www.fortis.com.py', TRUE),
    ('losjardines', 'Los Jardines', 'Los Jardines S.A.', 'https://www.losjardinesonline.com.py', FALSE),
    ('salemma', 'Salemma Super Center', 'Salemma Retail', 'https://www.salemmaonline.com.py', FALSE)
ON CONFLICT (slug) DO NOTHING;

INSERT INTO financial_entities (slug, name, entity_type) VALUES
    ('ueno', 'ueno bank', 'BANK'),
    ('itau', 'Banco Itaú Paraguay', 'BANK'),
    ('continental', 'Banco Continental', 'BANK'),
    ('atlas', 'Banco Atlas', 'BANK'),
    ('sudameris', 'Sudameris Bank', 'BANK'),
    ('familiar', 'Banco Familiar', 'BANK'),
    ('gnb', 'Banco GNB Paraguay', 'BANK'),
    ('bnf', 'Banco Nacional de Fomento (BNF)', 'BANK')
ON CONFLICT (slug) DO NOTHING;

-- Tarjetas representativas del mercado paraguayo
INSERT INTO payment_cards (entity_id, slug, name, card_type, tier_label) VALUES
    ((SELECT id FROM financial_entities WHERE slug = 'ueno'), 'ueno_credito_n1', 'ueno Crédito QR (Nivel 1)', 'CREDIT', 'Nivel 1'),
    ((SELECT id FROM financial_entities WHERE slug = 'ueno'), 'ueno_credito_n2', 'ueno Crédito QR (Nivel 2)', 'CREDIT', 'Nivel 2'),
    ((SELECT id FROM financial_entities WHERE slug = 'ueno'), 'ueno_credito_n3', 'ueno Crédito QR (Nivel 3)', 'CREDIT', 'Nivel 3'),
    ((SELECT id FROM financial_entities WHERE slug = 'ueno'), 'ueno_credito_n4', 'ueno Crédito QR (Nivel 4)', 'CREDIT', 'Nivel 4'),
    ((SELECT id FROM financial_entities WHERE slug = 'ueno'), 'ueno_credito_n5', 'ueno Crédito QR (Nivel 5)', 'CREDIT', 'Nivel 5'),
    ((SELECT id FROM financial_entities WHERE slug = 'itau'), 'itau_credito_clasica', 'Itaú Crédito Clásica / Oro', 'CREDIT', 'General'),
    ((SELECT id FROM financial_entities WHERE slug = 'itau'), 'itau_credito_infinite', 'Itaú Personal Bank (Platinum / Infinite)', 'CREDIT', 'Personal Bank'),
    ((SELECT id FROM financial_entities WHERE slug = 'continental'), 'continental_credito', 'Continental Crédito QR', 'CREDIT', 'General'),
    ((SELECT id FROM financial_entities WHERE slug = 'atlas'), 'atlas_credito', 'Atlas Crédito Supermercados', 'CREDIT', 'General'),
    ((SELECT id FROM financial_entities WHERE slug = 'familiar'), 'familiar_credito', 'Familiar Crédito QR', 'CREDIT', 'General'),
    ((SELECT id FROM financial_entities WHERE slug = 'sudameris'), 'sudameris_credito', 'Sudameris Crédito', 'CREDIT', 'General')
ON CONFLICT (slug) DO NOTHING;

-- Promociones bancarias de ejemplo configuradas con reglas reales de Paraguay
INSERT INTO bank_promotions (
    supermarket_id, card_id, title, discount_pct, mechanism,
    applies_to_promo_price, days_of_week, spending_cap_gs, max_refund_gs, payment_channel, terms_notes
) VALUES
    -- Biggie + ueno bank (Todos los días, reintegro sobre total abonado vía QR según nivel)
    (
        (SELECT id FROM supermarkets WHERE slug = 'biggie'),
        (SELECT id FROM payment_cards WHERE slug = 'ueno_credito_n3'),
        'Reintegro ueno Nivel 3 en Biggie (Todos los días)',
        25.00, 'CASHBACK', TRUE, '{1,2,3,4,5,6,7}', 600000, 150000, 'QR_POS',
        'Aplica pagando con QR desde la app de ueno bank con tarjeta de crédito.'
    ),
    (
        (SELECT id FROM supermarkets WHERE slug = 'biggie'),
        (SELECT id FROM payment_cards WHERE slug = 'ueno_credito_n4'),
        'Reintegro ueno Nivel 4 en Biggie (Todos los días)',
        35.00, 'CASHBACK', TRUE, '{1,2,3,4,5,6,7}', 800000, 280000, 'QR_POS',
        'Aplica pagando con QR desde la app de ueno bank con tarjeta de crédito.'
    ),
    -- Superseis + Itaú (Martes de descuento)
    (
        (SELECT id FROM supermarkets WHERE slug = 'superseis'),
        (SELECT id FROM payment_cards WHERE slug = 'itau_credito_clasica'),
        'Martes de Superseis con Itaú Crédito',
        20.00, 'CASHBACK', FALSE, '{2}', 1000000, 200000, 'QR_POS',
        'No acumulable con otras promociones u ofertas de góndola.'
    ),
    -- Casa Rica + Itaú Personal Bank (Jueves)
    (
        (SELECT id FROM supermarkets WHERE slug = 'casarica'),
        (SELECT id FROM payment_cards WHERE slug = 'itau_credito_infinite'),
        'Jueves Casa Rica Itaú Personal Bank',
        25.00, 'CASHBACK', FALSE, '{4}', 1500000, 375000, 'QR_POS',
        'Exclusivo clientes Personal Bank pagando vía QR Itaú.'
    ),
    -- Stock + Banco Familiar (Viernes)
    (
        (SELECT id FROM supermarkets WHERE slug = 'stock'),
        (SELECT id FROM payment_cards WHERE slug = 'familiar_credito'),
        'Viernes de Ahorro en Stock con Familiar',
        20.00, 'CASHBACK', FALSE, '{5}', 800000, 160000, 'QR_POS',
        'Tope de compra mensual de Gs. 800.000.'
    ),
    -- Areté + Continental (Miércoles)
    (
        (SELECT id FROM supermarkets WHERE slug = 'arete'),
        (SELECT id FROM payment_cards WHERE slug = 'continental_credito'),
        'Miércoles en Areté con Banco Continental',
        20.00, 'CASHBACK', TRUE, '{3}', 1000000, 200000, 'QR_POS',
        'Reintegro en extracto pagando con QR Continental.'
    );

