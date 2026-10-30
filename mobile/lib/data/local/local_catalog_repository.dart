import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqlite3/sqlite3.dart';

import '../../domain/models/catalog_models.dart';

/// Repositorio Offline-First que gestiona el catálogo local (SQLite FTS5 / Snapshot en memoria)
/// permitiendo búsquedas sin tildes en < 4 ms y escaneo de códigos EAN-13 sin internet.
class LocalCatalogRepository {
  final Database? _db;

  LocalCatalogRepository({Database? sqliteDb}) : _db = sqliteDb;

  /// Abre o inicializa el repositorio leyendo el archivo SQLite desde los assets de Flutter
  static Future<LocalCatalogRepository> createFromAsset({
    String assetPath = 'assets/db/catalog_latest.db',
  }) async {
    try {
      final docDir = await getApplicationDocumentsDirectory();
      final targetFile = File(p.join(docDir.path, 'catalog_latest.db'));

      // Si no existe localmente, copiamos desde el bundle de assets
      if (!await targetFile.exists()) {
        final byteData = await rootBundle.load(assetPath);
        final bytes = byteData.buffer.asUint8List(
          byteData.offsetInBytes,
          byteData.lengthInBytes,
        );
        await targetFile.writeAsBytes(bytes, flush: true);
      }

      final db = sqlite3.open(targetFile.path);
      return LocalCatalogRepository(sqliteDb: db);
    } catch (e) {
      // Fallback elegante a catálogo en memoria si ocurre un error de permisos o I/O
      return LocalCatalogRepository();
    }
  }

  Map<String, String> get supermarkets {
    if (_db != null) {
      final rows = _db.select('SELECT slug, name FROM local_supermarkets ORDER BY id ASC');
      final map = <String, String>{};
      for (final r in rows) {
        map[r['slug'] as String] = r['name'] as String;
      }
      if (map.isNotEmpty) return map;
    }
    return defaultSupermarkets;
  }

  static const Map<String, String> defaultSupermarkets = {
    'superseis': 'Superseis',
    'stock': 'Supermercados Stock',
    'biggie': 'Biggie Express',
    'casarica': 'Casa Rica',
    'arete': 'Supermercados Areté',
    'fortis': 'Fortis Mayorista',
  };

  List<BankPromotion> get promotions {
    if (_db != null) {
      final rows = _db.select('''
        SELECT bp.id, s.slug AS supermarket_slug, c.slug AS card_slug, c.name AS card_name,
               c.entity_name, bp.title, bp.discount_pct, bp.mechanism, bp.applies_to_promo_price,
               bp.days_of_week_csv, bp.spending_cap_gs, bp.max_refund_gs
        FROM local_bank_promotions bp
        JOIN local_supermarkets s ON s.id = bp.supermarket_id
        JOIN local_payment_cards c ON c.id = bp.card_id
      ''');

      final list = <BankPromotion>[];
      for (final r in rows) {
        final days = (r['days_of_week_csv'] as String)
            .split(',')
            .where((s) => s.isNotEmpty)
            .map((s) => int.parse(s.trim()))
            .toList();

        list.add(
          BankPromotion(
            id: r['id'] as int,
            supermarketSlug: r['supermarket_slug'] as String,
            cardSlug: r['card_slug'] as String,
            cardName: r['card_name'] as String,
            entityName: r['entity_name'] as String,
            title: r['title'] as String,
            discountPct: (r['discount_pct'] as num).toDouble(),
            mechanism: (r['mechanism'] as String) == 'INSTANT_POS'
                ? DiscountMechanism.instantPos
                : DiscountMechanism.cashback,
            appliesToPromoPrice: (r['applies_to_promo_price'] as int) == 1,
            daysOfWeek: days,
            spendingCapGs: r['spending_cap_gs'] as int?,
            maxRefundGs: r['max_refund_gs'] as int?,
          ),
        );
      }
      if (list.isNotEmpty) return list;
    }
    return paraguayPromotions;
  }

  static const List<BankPromotion> paraguayPromotions = [
    BankPromotion(
      id: 1,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n4',
      cardName: 'ueno Crédito QR (Nivel 4)',
      entityName: 'ueno bank',
      title: '35% reintegro todos los días con QR ueno',
      discountPct: 35.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 800000,
      maxRefundGs: 280000,
    ),
    BankPromotion(
      id: 2,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n3',
      cardName: 'ueno Crédito QR (Nivel 3)',
      entityName: 'ueno bank',
      title: '25% reintegro todos los días con QR ueno',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 600000,
      maxRefundGs: 150000,
    ),
    BankPromotion(
      id: 3,
      supermarketSlug: 'superseis',
      cardSlug: 'itau_credito_clasica',
      cardName: 'Itaú Crédito Clásica / Oro',
      entityName: 'Banco Itaú',
      title: 'Martes de Superseis con Itaú 20%',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [2], // Martes
      spendingCapGs: 1000000,
      maxRefundGs: 200000,
    ),
    BankPromotion(
      id: 4,
      supermarketSlug: 'casarica',
      cardSlug: 'itau_credito_infinite',
      cardName: 'Itaú Personal Bank (Infinite)',
      entityName: 'Banco Itaú',
      title: 'Jueves en Casa Rica 25% Itaú Personal Bank',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [4], // Jueves
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),
    BankPromotion(
      id: 5,
      supermarketSlug: 'stock',
      cardSlug: 'familiar_credito',
      cardName: 'Familiar Crédito QR',
      entityName: 'Banco Familiar',
      title: 'Viernes de Ahorro en Stock 20%',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [5], // Viernes
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),
    BankPromotion(
      id: 6,
      supermarketSlug: 'arete',
      cardSlug: 'continental_credito',
      cardName: 'Continental Crédito QR',
      entityName: 'Banco Continental',
      title: 'Miércoles en Areté 20% Continental',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [3], // Miércoles
      spendingCapGs: 1000000,
      maxRefundGs: 200000,
    ),
  ];

  static const List<ProductItem> initialCatalog = [
    ProductItem(
      id: 1,
      ean: '7840000000036',
      normalizedName: 'Yerba Mate Kurupí Compuesta Menta y Boldo 500 g',
      brand: 'Kurupí',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      offers: [
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 17200,
          promoPriceGs: 14500,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 17000,
        ),
        StoreOffer(
          supermarketSlug: 'biggie',
          supermarketName: 'Biggie Express',
          regularPriceGs: 17500,
        ),
        StoreOffer(
          supermarketSlug: 'arete',
          supermarketName: 'Supermercados Areté',
          regularPriceGs: 16900,
          promoPriceGs: 15200,
        ),
      ],
    ),
    ProductItem(
      id: 2,
      ean: '7840000000106',
      normalizedName: 'Leche Entera Trébol UAT Cartón 1 L',
      brand: 'Trébol',
      unitMeasure: 'LT',
      unitQuantity: 1.0,
      baseUnit: 'LT',
      baseMultiplier: 1.0,
      offers: [
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 9800,
          promoPriceGs: 8900,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 9700,
          promoPriceGs: 8850,
        ),
        StoreOffer(
          supermarketSlug: 'biggie',
          supermarketName: 'Biggie Express',
          regularPriceGs: 10000,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica',
          regularPriceGs: 10200,
        ),
      ],
    ),
    ProductItem(
      id: 3,
      ean: '7840058000122',
      normalizedName: 'Gaseosa Coca-Cola Sabor Original Retornable 2 L',
      brand: 'Coca-Cola',
      unitMeasure: 'LT',
      unitQuantity: 2.0,
      baseUnit: 'LT',
      baseMultiplier: 2.0,
      offers: [
        StoreOffer(
          supermarketSlug: 'biggie',
          supermarketName: 'Biggie Express',
          regularPriceGs: 13000,
        ),
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 13500,
          promoPriceGs: 12000,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 13000,
        ),
      ],
    ),
    ProductItem(
      id: 4,
      ean: '7840112233441',
      normalizedName: 'Cerveza Pilsen Pack 6 x 330 ml Botella',
      brand: 'Pilsen',
      unitMeasure: 'ML',
      unitQuantity: 1980,
      baseUnit: 'LT',
      baseMultiplier: 1.98,
      offers: [
        StoreOffer(
          supermarketSlug: 'biggie',
          supermarketName: 'Biggie Express',
          regularPriceGs: 42000,
          promoPriceGs: 36000,
        ),
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 43500,
          promoPriceGs: 37500,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica',
          regularPriceGs: 44000,
        ),
      ],
    ),
  ];

  static String normalizeDiacritics(String input) {
    return input
        .toLowerCase()
        .replaceAll('á', 'a')
        .replaceAll('é', 'e')
        .replaceAll('í', 'i')
        .replaceAll('ó', 'o')
        .replaceAll('ú', 'u')
        .replaceAll('ü', 'u');
  }

  /// Búsqueda instantánea FTS5 (< 4 ms) en SQLite local o filtro en memoria como fallback
  List<ProductItem> searchInstant(String rawQuery, {int limit = 30}) {
    if (_db != null) {
      final clean = normalizeDiacritics(rawQuery.trim());
      ResultSet rows;

      if (clean.isEmpty) {
        rows = _db.select('''
          SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit,
                 o.supermarket_id, s.slug AS supermarket_slug, s.name AS supermarket_name,
                 o.regular_price, o.promo_price, o.wholesale_price, o.wholesale_min_qty, o.in_stock
          FROM local_products p
          JOIN local_offers o ON o.product_id = p.id
          JOIN local_supermarkets s ON s.id = o.supermarket_id
          ORDER BY p.id ASC
          LIMIT ?
        ''', [limit * 4]);
      } else {
        final tokens = clean.split(RegExp(r'\s+')).where((t) => t.isNotEmpty).toList();
        final ftsMatch = tokens.map((t) => '"$t"*').join(' AND ');

        rows = _db.select('''
          SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit,
                 o.supermarket_id, s.slug AS supermarket_slug, s.name AS supermarket_name,
                 o.regular_price, o.promo_price, o.wholesale_price, o.wholesale_min_qty, o.in_stock
          FROM local_products_fts fts
          JOIN local_products p ON p.id = fts.product_id
          JOIN local_offers o ON o.product_id = p.id
          JOIN local_supermarkets s ON s.id = o.supermarket_id
          WHERE local_products_fts MATCH ?
          ORDER BY p.id ASC
          LIMIT ?
        ''', [ftsMatch, limit * 4]);
      }

      return _groupRowsIntoProducts(rows);
    }

    // Fallback en memoria
    final clean = normalizeDiacritics(rawQuery.trim());
    if (clean.isEmpty) {
      return initialCatalog;
    }

    final tokens = clean.split(RegExp(r'\s+')).where((t) => t.isNotEmpty).toList();
    return initialCatalog.where((product) {
      final haystack = normalizeDiacritics(
        '${product.normalizedName} ${product.brand ?? ''} ${product.ean ?? ''}',
      );
      return tokens.every((token) => haystack.contains(token));
    }).toList();
  }

  /// Búsqueda ultra rápida por EAN-13 para el Escáner de Pasillo (< 2 ms)
  ProductItem? findByBarcode(String ean) {
    final trimmed = ean.trim();
    if (_db != null) {
      final rows = _db.select('''
        SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit,
               o.supermarket_id, s.slug AS supermarket_slug, s.name AS supermarket_name,
               o.regular_price, o.promo_price, o.wholesale_price, o.wholesale_min_qty, o.in_stock
        FROM local_products p
        JOIN local_offers o ON o.product_id = p.id
        JOIN local_supermarkets s ON s.id = o.supermarket_id
        WHERE p.ean = ?
      ''', [trimmed]);

      final products = _groupRowsIntoProducts(rows);
      return products.isNotEmpty ? products.first : null;
    }

    // Fallback en memoria
    for (final product in initialCatalog) {
      if (product.ean == trimmed) {
        return product;
      }
    }
    return null;
  }

  List<ProductItem> _groupRowsIntoProducts(ResultSet rows) {
    final map = <int, ProductItem>{};
    final offersMap = <int, List<StoreOffer>>{};

    for (final r in rows) {
      final id = r['id'] as int;
      if (!map.containsKey(id)) {
        final uMeasure = (r['unit_measure'] as String?) ?? 'UN';
        final uQty = (r['unit_quantity'] as num?)?.toDouble() ?? 1.0;
        final bUnit = (r['base_unit'] as String?) ?? 'UN';

        var multiplier = uQty;
        if (uMeasure == 'GR' || uMeasure == 'ML') {
          multiplier = uQty / 1000.0;
        }

        map[id] = ProductItem(
          id: id,
          ean: r['ean'] as String?,
          normalizedName: r['normalized_name'] as String,
          brand: r['brand'] as String?,
          unitMeasure: uMeasure,
          unitQuantity: uQty,
          baseUnit: bUnit,
          baseMultiplier: multiplier > 0 ? multiplier : 1.0,
          offers: const [],
        );
        offersMap[id] = [];
      }

      offersMap[id]!.add(
        StoreOffer(
          supermarketSlug: r['supermarket_slug'] as String,
          supermarketName: r['supermarket_name'] as String,
          regularPriceGs: r['regular_price'] as int,
          promoPriceGs: r['promo_price'] as int?,
          wholesalePriceGs: r['wholesale_price'] as int?,
          wholesaleMinQty: r['wholesale_min_qty'] as int?,
          inStock: (r['in_stock'] as int?) == 1,
        ),
      );
    }

    final result = <ProductItem>[];
    for (final entry in map.entries) {
      final p = entry.value;
      result.add(
        ProductItem(
          id: p.id,
          ean: p.ean,
          normalizedName: p.normalizedName,
          brand: p.brand,
          unitMeasure: p.unitMeasure,
          unitQuantity: p.unitQuantity,
          baseUnit: p.baseUnit,
          baseMultiplier: p.baseMultiplier,
          offers: offersMap[p.id] ?? const [],
        ),
      );
    }
    return result;
  }

  /// Aplica el paquete delta diario (< 80 KB) de cambios de precios en la base SQLite local
  int applyDeltaSync(List<Map<String, dynamic>> updatedOffers) {
    if (_db == null || updatedOffers.isEmpty) return 0;

    var applied = 0;
    _db.execute('BEGIN TRANSACTION;');
    try {
      final stmt = _db.prepare('''
        UPDATE local_offers
        SET regular_price = ?,
            promo_price = ?,
            scraped_at = CURRENT_TIMESTAMP
        WHERE supermarket_id = (SELECT id FROM local_supermarkets WHERE slug = ?)
          AND product_id = (
            SELECT p.id FROM local_products p
            WHERE (p.ean IS NOT NULL AND p.ean = ?)
               OR p.normalized_name = ?
            LIMIT 1
          );
      ''');

      for (final item in updatedOffers) {
        final supSlug = item['supermarket_slug'] as String?;
        final regPrice = item['new_regular_price'] as int?;
        final promoPrice = item['new_promo_price'] as int?;
        final ean = item['ean'] as String?;
        final title = item['raw_title'] as String?;

        if (supSlug == null || regPrice == null) continue;

        stmt.execute([regPrice, promoPrice, supSlug, ean ?? '', title ?? '']);
        applied++;
      }
      stmt.dispose();
      _db.execute('COMMIT;');
    } catch (_) {
      _db.execute('ROLLBACK;');
      rethrow;
    }
    return applied;
  }

  /// Permite a la comunidad registrar un producto no catalogado (Modo Cazador de Precios)
  ProductItem addCrowdsourcedProduct({
    required String ean,
    required String productName,
    required String supermarketSlug,
    required int priceGs,
    String? brand,
  }) {
    final now = DateTime.now();
    final newProd = ProductItem(
      id: DateTime.now().millisecondsSinceEpoch % 1000000,
      ean: ean.trim(),
      normalizedName: productName.trim(),
      brand: brand,
      unitMeasure: 'UN',
      unitQuantity: 1.0,
      baseUnit: 'UN',
      baseMultiplier: 1.0,
      offers: [
        StoreOffer(
          supermarketSlug: supermarketSlug,
          supermarketName: supermarkets[supermarketSlug] ?? supermarketSlug,
          regularPriceGs: priceGs,
          promoPriceGs: null,
        ),
      ],
    );

    if (_db != null) {
      _db.execute('''
        INSERT OR REPLACE INTO local_products
        (id, ean, normalized_name, brand, unit_measure, unit_quantity, base_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?);
      ''', [newProd.id, newProd.ean, newProd.normalizedName, newProd.brand, 'UN', 1.0, 'UN']);

      _db.execute('''
        INSERT INTO local_products_fts (product_id, ean, normalized_name, brand)
        VALUES (?, ?, ?, ?);
      ''', [newProd.id, newProd.ean ?? '', newProd.normalizedName, newProd.brand ?? '']);

      final supId = _db.select(
        'SELECT id FROM local_supermarkets WHERE slug = ?',
        [supermarketSlug],
      );
      if (supId.isNotEmpty) {
        _db.execute('''
          INSERT OR REPLACE INTO local_offers
          (product_id, supermarket_id, regular_price, promo_price, price_per_base_unit, scraped_at)
          VALUES (?, ?, ?, ?, ?, ?);
        ''', [newProd.id, supId.first['id'], priceGs, null, priceGs, now.toIso8601String()]);
      }
    }

    return newProd;
  }
}
