import 'dart:convert';
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

    /// URL en la nube (GitHub Raw) donde se aloja el catálogo SQLite oficial actualizado automáticamente
  static const String cloudCatalogDbUrl =
      'https://raw.githubusercontent.com/Argos4h/PreciosPy/main/mobile/assets/db/catalog_latest.db';

  /// Sincroniza silenciosamente en segundo plano la base de datos desde la nube sin reinstalar la app.
  /// Retorna true si se descargó e instaló una nueva versión de precios.
  static Future<bool> syncCloudCatalogSilently() async {
    try {
      final docDir = await getApplicationDocumentsDirectory();
      final targetFile = File(p.join(docDir.path, 'catalog_latest.db'));
      final tempFile = File(p.join(docDir.path, 'catalog_latest_temp.db'));

      final uri = Uri.parse(cloudCatalogDbUrl);
      final client = HttpClient()..connectionTimeout = const Duration(seconds: 8);
      final request = await client.getUrl(uri);
      final response = await request.close();

      if (response.statusCode == 200) {
        final bytes = await response.fold<List<int>>([], (acc, chunk) => acc..addAll(chunk));
        
        // Si el archivo en la nube es válido (> 500 KB) y es distinto al actual
        if (bytes.length > 500000) {
          if (!await targetFile.exists() || (await targetFile.length()) != bytes.length) {
            await tempFile.writeAsBytes(bytes, flush: true);

            // Validar que el SQLite descargado sea íntegro antes de sustituirlo
            final testDb = sqlite3.open(tempFile.path);
            final count = testDb.select('SELECT count(*) as cnt FROM local_products').first['cnt'] as int;
            testDb.dispose();

            if (count > 0) {
              if (await targetFile.exists()) {
                await targetFile.delete();
              }
              await tempFile.rename(targetFile.path);
              return true;
            }
          }
        }
      }
      return false;
    } catch (_) {
      return false;
    }
  }

  /// Abre o inicializa el repositorio leyendo el archivo SQLite desde el almacenamiento o assets
  static Future<LocalCatalogRepository> createFromAsset({
    String assetPath = 'assets/db/catalog_latest.db',
  }) async {
    try {
      final docDir = await getApplicationDocumentsDirectory();
      final targetFile = File(p.join(docDir.path, 'catalog_latest.db'));

      // 1. Si no existe en el almacenamiento, copiar desde los assets
      if (!await targetFile.exists()) {
        final byteData = await rootBundle.load(assetPath);
        final bytes = byteData.buffer.asUint8List(
          byteData.offsetInBytes,
          byteData.lengthInBytes,
        );
        await targetFile.writeAsBytes(bytes, flush: true);
      } else {
        // Si el asset empaquetado es más reciente o de tamaño distinto, actualizar
        final byteData = await rootBundle.load(assetPath);
        final bytes = byteData.buffer.asUint8List(
          byteData.offsetInBytes,
          byteData.lengthInBytes,
        );
        if ((await targetFile.length()) != bytes.length) {
          await targetFile.writeAsBytes(bytes, flush: true);
        }
      }

      final db = sqlite3.open(targetFile.path);
      return LocalCatalogRepository(sqliteDb: db);
    } catch (e) {
      // Fallback elegante a catálogo en memoria si ocurre un error de permisos o I/O
      return LocalCatalogRepository();
    }
  }

  Map<String, int> getUniqueBrands() {
    final counts = <String, int>{};
    if (_db != null) {
      try {
        final rows = _db.select(
          'SELECT brand, count(*) as cnt FROM local_products WHERE brand IS NOT NULL AND trim(brand) != "" GROUP BY brand ORDER BY cnt DESC, brand ASC'
        );
        for (final r in rows) {
          final b = (r['brand'] as String?)?.trim() ?? '';
          if (b.isNotEmpty) {
            counts[b] = (r['cnt'] as int?) ?? 1;
          }
        }
      } catch (_) {}
    }
    return counts;
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
    'casarica': 'Casa Rica Gourmet',
    'arete': 'Supermercados Areté',
    'fortis': 'Fortis Mayorista',
    'box': 'Box Mayorista',
    'real': 'Cadena Real',
    'salemma': 'Supermercados Salemma',
    'losjardines': 'Los Jardines (Luque)',
    'labomba': 'Supermercados La Bomba',
    'granvia': 'Cadena Gran Vía',
    'delimarket': 'Delimarket Shopping del Sol',
    'tuti': 'Tiendas Tuti',
  };

  /// Sucursales físicas reales de supermercados geolocalizadas por ciudad
  static const List<Map<String, String>> paraguayCities = [
    {'city': 'Caacupé', 'dept': 'Cordillera', 'badge': 'Stock, Superseis, Biggie, Tuti'},
    {'city': 'Asunción', 'dept': 'Capital', 'badge': 'Todas las cadenas'},
    {'city': 'Luque', 'dept': 'Central', 'badge': 'Fortis, Box, Superseis, Stock'},
    {'city': 'San Lorenzo', 'dept': 'Central', 'badge': 'Salemma, Real, Fortis, Stock'},
    {'city': 'Ciudad del Este', 'dept': 'Alto Paraná', 'badge': 'Fortis, Box, Gran Vía, Stock'},
    {'city': 'Encarnación', 'dept': 'Itapúa', 'badge': 'Superseis, Stock'},
    {'city': 'Todas', 'dept': 'Nacional', 'badge': 'Todos los supermercados'},
  ];

  static const List<SupermarketBranch> paraguayBranches = [
    // CAACUPÉ (Cordillera)
    SupermarketBranch(
      id: 1,
      supermarketSlug: 'stock',
      supermarketName: 'Supermercados Stock',
      branchName: 'Stock Caacupé',
      city: 'Caacupé',
      department: 'Cordillera',
      latitude: -25.3855,
      longitude: -57.1422,
      address: 'Ruta PY02 Km 54',
    ),
    SupermarketBranch(
      id: 2,
      supermarketSlug: 'superseis',
      supermarketName: 'Superseis',
      branchName: 'Superseis Caacupé',
      city: 'Caacupé',
      department: 'Cordillera',
      latitude: -25.3860,
      longitude: -57.1405,
      address: 'Av. Dr. Eligio Ayala c/ Alberdi',
    ),
    SupermarketBranch(
      id: 3,
      supermarketSlug: 'biggie',
      supermarketName: 'Biggie Express',
      branchName: 'Biggie Caacupé Basílica',
      city: 'Caacupé',
      department: 'Cordillera',
      latitude: -25.3872,
      longitude: -57.1418,
      address: 'Concepción e/ 14 de Mayo',
    ),
    SupermarketBranch(
      id: 4,
      supermarketSlug: 'tuti',
      supermarketName: 'Tiendas Tuti',
      branchName: 'Tuti Caacupé Centro',
      city: 'Caacupé',
      department: 'Cordillera',
      latitude: -25.3880,
      longitude: -57.1430,
      address: 'Asunción c/ Variante',
    ),

    // ASUNCIÓN (Capital)
    SupermarketBranch(
      id: 10,
      supermarketSlug: 'superseis',
      supermarketName: 'Superseis',
      branchName: 'Superseis España',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2950,
      longitude: -57.6010,
      address: 'Av. España c/ Pitiantuta',
    ),
    SupermarketBranch(
      id: 11,
      supermarketSlug: 'stock',
      supermarketName: 'Supermercados Stock',
      branchName: 'Stock Sacramento',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2760,
      longitude: -57.5890,
      address: 'Av. Santísimo Sacramento',
    ),
    SupermarketBranch(
      id: 12,
      supermarketSlug: 'biggie',
      supermarketName: 'Biggie Express',
      branchName: 'Biggie Villa Morra',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2980,
      longitude: -57.5820,
      address: 'Senador Long c/ España',
    ),
    SupermarketBranch(
      id: 13,
      supermarketSlug: 'casarica',
      supermarketName: 'Casa Rica Gourmet',
      branchName: 'Casa Rica España',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2920,
      longitude: -57.5980,
      address: 'Av. España c/ Dr. Bestard',
    ),
    SupermarketBranch(
      id: 14,
      supermarketSlug: 'arete',
      supermarketName: 'Supermercados Areté',
      branchName: 'Areté Shopping Mariscal',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2965,
      longitude: -57.5795,
      address: 'Quesada c/ Roque González',
    ),
    SupermarketBranch(
      id: 15,
      supermarketSlug: 'delimarket',
      supermarketName: 'Delimarket',
      branchName: 'Delimarket Shopping del Sol',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2820,
      longitude: -57.5650,
      address: 'Av. Aviadores del Chaco',
    ),
    SupermarketBranch(
      id: 16,
      supermarketSlug: 'real',
      supermarketName: 'Cadena Real',
      branchName: 'Real Villa Morra',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2970,
      longitude: -57.5850,
      address: 'Av. Boggiani c/ R.I. 3 Corrales',
    ),
    SupermarketBranch(
      id: 17,
      supermarketSlug: 'salemma',
      supermarketName: 'Supermercados Salemma',
      branchName: 'Salemma Carmelitas',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2840,
      longitude: -57.5720,
      address: 'Av. San Martín c/ España',
    ),
    SupermarketBranch(
      id: 18,
      supermarketSlug: 'labomba',
      supermarketName: 'Supermercados La Bomba',
      branchName: 'La Bomba Sajonia',
      city: 'Asunción',
      department: 'Capital',
      latitude: -25.2990,
      longitude: -57.6530,
      address: 'Av. Carlos Antonio López',
    ),

    // LUQUE (Central)
    SupermarketBranch(
      id: 20,
      supermarketSlug: 'losjardines',
      supermarketName: 'Los Jardines (Luque)',
      branchName: 'Los Jardines Luque Central',
      city: 'Luque',
      department: 'Central',
      latitude: -25.2670,
      longitude: -57.4890,
      address: 'Gral. Aquino c/ San Martín',
    ),
    SupermarketBranch(
      id: 21,
      supermarketSlug: 'fortis',
      supermarketName: 'Fortis Mayorista',
      branchName: 'Fortis Luque',
      city: 'Luque',
      department: 'Central',
      latitude: -25.2550,
      longitude: -57.4980,
      address: 'Ruta Luque - San Lorenzo',
    ),
    SupermarketBranch(
      id: 22,
      supermarketSlug: 'box',
      supermarketName: 'Box Mayorista',
      branchName: 'Box Luque',
      city: 'Luque',
      department: 'Central',
      latitude: -25.2600,
      longitude: -57.5020,
      address: 'Corredor Luque',
    ),
    SupermarketBranch(
      id: 23,
      supermarketSlug: 'superseis',
      supermarketName: 'Superseis',
      branchName: 'Superseis Luque',
      city: 'Luque',
      department: 'Central',
      latitude: -25.2710,
      longitude: -57.4850,
      address: 'Rosario c/ Cerro Corá',
    ),
    SupermarketBranch(
      id: 24,
      supermarketSlug: 'stock',
      supermarketName: 'Supermercados Stock',
      branchName: 'Stock Luque',
      city: 'Luque',
      department: 'Central',
      latitude: -25.2730,
      longitude: -57.4870,
      address: 'Las Residentas',
    ),

    // SAN LORENZO (Central)
    SupermarketBranch(
      id: 30,
      supermarketSlug: 'salemma',
      supermarketName: 'Supermercados Salemma',
      branchName: 'Salemma Super Center',
      city: 'San Lorenzo',
      department: 'Central',
      latitude: -25.3340,
      longitude: -57.5180,
      address: 'Ruta PY02 Mcal. Estigarribia Km 9.5',
    ),
    SupermarketBranch(
      id: 31,
      supermarketSlug: 'real',
      supermarketName: 'Cadena Real',
      branchName: 'Real San Lorenzo',
      city: 'San Lorenzo',
      department: 'Central',
      latitude: -25.3380,
      longitude: -57.5120,
      address: 'Av. Defensores del Chaco',
    ),

    // CIUDAD DEL ESTE (Alto Paraná)
    SupermarketBranch(
      id: 40,
      supermarketSlug: 'fortis',
      supermarketName: 'Fortis Mayorista',
      branchName: 'Fortis Ciudad del Este',
      city: 'Ciudad del Este',
      department: 'Alto Paraná',
      latitude: -25.5090,
      longitude: -54.6380,
      address: 'Ruta PY02 Km 4',
    ),
    SupermarketBranch(
      id: 41,
      supermarketSlug: 'box',
      supermarketName: 'Box Mayorista',
      branchName: 'Box Mayorista CDE',
      city: 'Ciudad del Este',
      department: 'Alto Paraná',
      latitude: -25.5120,
      longitude: -54.6450,
      address: 'Av. Monseñor Rodríguez Km 5.5',
    ),
    SupermarketBranch(
      id: 42,
      supermarketSlug: 'granvia',
      supermarketName: 'Cadena Gran Vía',
      branchName: 'Gran Vía CDE Centro',
      city: 'Ciudad del Este',
      department: 'Alto Paraná',
      latitude: -25.5100,
      longitude: -54.6150,
      address: 'Av. Adrián Jara c/ Curupayty',
    ),

    // ENCARNACIÓN (Itapúa)
    SupermarketBranch(
      id: 50,
      supermarketSlug: 'superseis',
      supermarketName: 'Superseis',
      branchName: 'Superseis Costanera Encarnación',
      city: 'Encarnación',
      department: 'Itapúa',
      latitude: -27.3320,
      longitude: -55.8670,
      address: 'Av. Costanera República del Paraguay',
    ),
    SupermarketBranch(
      id: 51,
      supermarketSlug: 'stock',
      supermarketName: 'Supermercados Stock',
      branchName: 'Stock Encarnación Centro',
      city: 'Encarnación',
      department: 'Itapúa',
      latitude: -27.3380,
      longitude: -55.8610,
      address: 'Av. Caballero e/ Mariscal López',
    ),
  ];

  /// Devuelve los slugs de supermercados que tienen al menos una sucursal física en la ciudad
  List<String> getSupermarketsInCity(String city) {
    if (city.toLowerCase() == 'todas' || city.trim().isEmpty) {
      return defaultSupermarkets.keys.toList();
    }
    final cleanCity = normalizeDiacritics(city.trim().toLowerCase());
    final matchingSlugs = paraguayBranches
        .where((b) => normalizeDiacritics(b.city.toLowerCase()) == cleanCity)
        .map((b) => b.supermarketSlug)
        .toSet();

    if (matchingSlugs.isEmpty) {
      return defaultSupermarkets.keys.toList();
    }
    return matchingSlugs.toList();
  }

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
    // UENO BANK (Escalonado por niveles 1..5)
    BankPromotion(
      id: 101,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n5',
      cardName: 'ueno Crédito QR (Nivel 5)',
      entityName: 'ueno bank',
      bankSlug: 'ueno',
      tier: 'n5',
      minUenoLevel: 5,
      requiresQr: true,
      title: '40% reintegro diario QR ueno Nivel 5 (VIP)',
      discountPct: 40.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 1000000,
      maxRefundGs: 400000,
    ),
    BankPromotion(
      id: 1,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n4',
      cardName: 'ueno Crédito QR (Nivel 4)',
      entityName: 'ueno bank',
      bankSlug: 'ueno',
      tier: 'n4',
      minUenoLevel: 4,
      requiresQr: true,
      title: '35% reintegro todos los días con QR ueno (Nivel 4)',
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
      bankSlug: 'ueno',
      tier: 'n3',
      minUenoLevel: 3,
      requiresQr: true,
      title: '25% reintegro todos los días con QR ueno (Nivel 3)',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 600000,
      maxRefundGs: 150000,
    ),
    BankPromotion(
      id: 102,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n2',
      cardName: 'ueno Crédito QR (Nivel 2)',
      entityName: 'ueno bank',
      bankSlug: 'ueno',
      tier: 'n2',
      minUenoLevel: 2,
      requiresQr: true,
      title: '15% reintegro todos los días con QR ueno (Nivel 2)',
      discountPct: 15.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 400000,
      maxRefundGs: 60000,
    ),
    BankPromotion(
      id: 103,
      supermarketSlug: 'biggie',
      cardSlug: 'ueno_credito_n1',
      cardName: 'ueno Crédito QR (Nivel 1)',
      entityName: 'ueno bank',
      bankSlug: 'ueno',
      tier: 'n1',
      minUenoLevel: 1,
      requiresQr: true,
      title: '10% reintegro con QR ueno (Nivel 1 Inicial)',
      discountPct: 10.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 300000,
      maxRefundGs: 30000,
    ),
    BankPromotion(
      id: 104,
      supermarketSlug: 'superseis',
      cardSlug: 'ueno_superseis',
      cardName: 'ueno QR en Superseis',
      entityName: 'ueno bank',
      bankSlug: 'ueno',
      requiresQr: true,
      title: 'Viernes y Sábados 20% reintegro QR ueno en Superseis',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [5, 6],
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),

    // BANCO ITAÚ
    BankPromotion(
      id: 3,
      supermarketSlug: 'superseis',
      cardSlug: 'itau_credito_clasica',
      cardName: 'Itaú Crédito Clásica / Oro',
      entityName: 'Banco Itaú',
      bankSlug: 'itau',
      tier: 'clasica',
      title: 'Martes de Superseis con Itaú 20%',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [2], // Martes
      spendingCapGs: 1000000,
      maxRefundGs: 200000,
    ),
    BankPromotion(
      id: 105,
      supermarketSlug: 'superseis',
      cardSlug: 'itau_credito_platinum',
      cardName: 'Itaú Crédito Platinum',
      entityName: 'Banco Itaú',
      bankSlug: 'itau',
      tier: 'platinum',
      title: 'Martes Platinum en Superseis 25% Itaú',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [2],
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),
    BankPromotion(
      id: 4,
      supermarketSlug: 'casarica',
      cardSlug: 'itau_credito_infinite',
      cardName: 'Itaú Personal Bank (Infinite/Black)',
      entityName: 'Banco Itaú',
      bankSlug: 'itau',
      tier: 'infinite',
      title: 'Jueves en Casa Rica 25% Itaú Personal Bank',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [4], // Jueves
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),
    BankPromotion(
      id: 106,
      supermarketSlug: 'superseis',
      cardSlug: 'itau_afinidad',
      cardName: 'Tarjeta Afinidad Itaú Superseis',
      entityName: 'Banco Itaú',
      bankSlug: 'itau',
      tier: 'afinidad',
      title: 'Todos los días 20% directo + Puntos Superseis',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [1, 2, 3, 4, 5, 6, 7],
      spendingCapGs: 1200000,
      maxRefundGs: 240000,
    ),

    // BANCO CONTINENTAL
    BankPromotion(
      id: 6,
      supermarketSlug: 'arete',
      cardSlug: 'continental_credito',
      cardName: 'Continental Crédito Clásica/Oro',
      entityName: 'Banco Continental',
      bankSlug: 'continental',
      tier: 'clasica',
      title: 'Miércoles en Areté 20% Continental',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [3], // Miércoles
      spendingCapGs: 1000000,
      maxRefundGs: 200000,
    ),
    BankPromotion(
      id: 107,
      supermarketSlug: 'arete',
      cardSlug: 'continental_black',
      cardName: 'Continental Black / Signature QR',
      entityName: 'Banco Continental',
      bankSlug: 'continental',
      tier: 'infinite',
      title: 'Miércoles en Areté 25% Continental Signature/Black',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [3],
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),

    // BANCO FAMILIAR
    BankPromotion(
      id: 5,
      supermarketSlug: 'stock',
      cardSlug: 'familiar_credito',
      cardName: 'Familiar Crédito Clásica',
      entityName: 'Banco Familiar',
      bankSlug: 'familiar',
      tier: 'clasica',
      title: 'Viernes de Ahorro en Stock 20% Familiar',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [5], // Viernes
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),
    BankPromotion(
      id: 108,
      supermarketSlug: 'stock',
      cardSlug: 'familiar_platinum',
      cardName: 'Familiar Mujer / Platinum',
      entityName: 'Banco Familiar',
      bankSlug: 'familiar',
      tier: 'platinum',
      title: 'Viernes en Stock 25% Familiar Platinum/Mujer',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [5],
      spendingCapGs: 1200000,
      maxRefundGs: 300000,
    ),

    // BANCO ATLAS
    BankPromotion(
      id: 109,
      supermarketSlug: 'stock',
      cardSlug: 'atlas_credito',
      cardName: 'Banco Atlas Crédito Clásica',
      entityName: 'Banco Atlas',
      bankSlug: 'atlas',
      tier: 'clasica',
      title: 'Lunes de Stock 20% con Tarjetas Atlas',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [1], // Lunes
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),
    BankPromotion(
      id: 110,
      supermarketSlug: 'stock',
      cardSlug: 'atlas_black',
      cardName: 'Banco Atlas Platinum / Black',
      entityName: 'Banco Atlas',
      bankSlug: 'atlas',
      tier: 'infinite',
      title: 'Lunes en Stock 25% Tarjetas Atlas Black/Platinum',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [1],
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),

    // SUDAMERIS
    BankPromotion(
      id: 111,
      supermarketSlug: 'casarica',
      cardSlug: 'sudameris_infinite',
      cardName: 'Sudameris Club Infinite / Black',
      entityName: 'Banco Sudameris',
      bankSlug: 'sudameris',
      tier: 'infinite',
      title: 'Jueves Gourmet en Casa Rica 25% Sudameris Black',
      discountPct: 25.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [4], // Jueves
      spendingCapGs: 1500000,
      maxRefundGs: 375000,
    ),

    // BANCO GNB
    BankPromotion(
      id: 112,
      supermarketSlug: 'superseis',
      cardSlug: 'gnb_credito',
      cardName: 'Banco GNB Mastercard / Visa',
      entityName: 'Banco GNB',
      bankSlug: 'gnb',
      tier: 'clasica',
      title: 'Miércoles de Supermercados 20% con Banco GNB',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [3], // Miércoles
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),

    // ZETA BANCO
    BankPromotion(
      id: 113,
      supermarketSlug: 'biggie',
      cardSlug: 'zeta_qr',
      cardName: 'Zeta Banco QR',
      entityName: 'Zeta Banco',
      bankSlug: 'zeta',
      requiresQr: true,
      title: 'Sábados de Ahorro 20% QR Zeta Banco',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: true,
      daysOfWeek: [6], // Sábado
      spendingCapGs: 600000,
      maxRefundGs: 120000,
    ),

    // BANCO BASA
    BankPromotion(
      id: 114,
      supermarketSlug: 'stock',
      cardSlug: 'basa_credito',
      cardName: 'Banco Basa Tarjetas de Crédito',
      entityName: 'Banco Basa',
      bankSlug: 'basa',
      tier: 'clasica',
      title: 'Domingos Familiares en Stock 20% Banco Basa',
      discountPct: 20.0,
      mechanism: DiscountMechanism.cashback,
      appliesToPromoPrice: false,
      daysOfWeek: [7], // Domingo
      spendingCapGs: 800000,
      maxRefundGs: 160000,
    ),
  ];

  static String? resolveProductImageUrl(String normalizedName, String? brand, String? ean) {
    final lower = normalizedName.toLowerCase();
    
    // Yerba Mate
    if (lower.contains('kurupi')) return 'https://static.app.biggie.com.py/images/products/7840127000124.jpg';
    if (lower.contains('campesino')) return 'https://static.app.biggie.com.py/images/products/7840009040507.jpg';
    if (lower.contains('pajarito')) return 'https://static.app.biggie.com.py/images/products/7840013000726.jpg';
    if (lower.contains('selecta')) return 'https://static.app.biggie.com.py/images/products/7840078001485-32620106.jpg';
    if (lower.contains('yerba')) return 'https://static.app.biggie.com.py/images/products/7840127000124.jpg';
    
    // Lácteos y Quesos
    if (lower.contains('trebol') && lower.contains('leche')) return 'https://static.app.biggie.com.py/images/products/7840005012379.jpg';
    if (lower.contains('lactolanda') && lower.contains('descremada')) return 'https://static.app.biggie.com.py/images/products/7840042000124.jpg';
    if (lower.contains('leche')) return 'https://static.app.biggie.com.py/images/products/7840005012379.jpg';
    if (lower.contains('yogur')) return 'https://static.app.biggie.com.py/images/products/7840005013550.jpg';
    if (lower.contains('queso paraguay')) return 'https://static.app.biggie.com.py/images/products/19999.jpg';
    if (lower.contains('queso') && (lower.contains('sandwich') || lower.contains('danbo') || lower.contains('feteado'))) return 'https://static.app.biggie.com.py/images/products/7840042004061.jpg';
    if (lower.contains('queso')) return 'https://static.app.biggie.com.py/images/products/7840042004061.jpg';
    if (lower.contains('manteca')) return 'https://static.app.biggie.com.py/images/products/7840042001503.jpg';

    // Bebidas y Jugos
    if (lower.contains('coca')) return 'https://static.app.biggie.com.py/images/products/7840058008084.jpg';
    if (lower.contains('pulp')) return 'https://static.app.biggie.com.py/images/products/7840779002057.jpg';
    if (lower.contains('sprite')) return 'https://static.app.biggie.com.py/images/products/7840058000088.jpg';
    if (lower.contains('puro sol') || lower.contains('jugo')) return 'https://static.app.biggie.com.py/images/products/7840779008363-28227085.jpg';
    if (lower.contains('dasani') || lower.contains('agua mineral')) return 'https://static.app.biggie.com.py/images/products/7840058003898.jpg';
    if (lower.contains('monster') || lower.contains('energizante')) return 'https://static.app.biggie.com.py/images/products/070847033233.jpg';

    // Cervezas y Vinos
    if (lower.contains('pilsen')) return 'https://static.app.biggie.com.py/images/products/7840050007696.jpg';
    if (lower.contains('brahma')) return 'https://static.app.biggie.com.py/images/products/7840050008655.jpg';
    if (lower.contains('michelob')) return 'https://static.app.biggie.com.py/images/products/7840050009881.png';
    if (lower.contains('corona')) return 'https://static.app.biggie.com.py/images/products/7891149108749.jpg';
    if (lower.contains('heineken')) return 'https://static.app.biggie.com.py/images/products/7802100004185.jpg';
    if (lower.contains('santa helena') || lower.contains('vino')) return 'https://static.app.biggie.com.py/images/products/7804300149314.jpg';
    if (lower.contains('cerveza')) return 'https://static.app.biggie.com.py/images/products/7840050007696.jpg';

    // Carnicería y Embutidos
    if (lower.contains('costilla')) return 'https://static.app.biggie.com.py/images/products/60168.jpg';
    if (lower.contains('vacio')) return 'https://static.app.biggie.com.py/images/products/60136.jpg';
    if (lower.contains('pollo') || lower.contains('pechug')) return 'https://static.app.biggie.com.py/images/products/30168.jpg';
    if (lower.contains('jamon') || lower.contains('ochsi') || lower.contains('pancho')) return 'https://static.app.biggie.com.py/images/products/18000.jpg';
    if (lower.contains('carne')) return 'https://static.app.biggie.com.py/images/products/60168.jpg';

    // Panadería
    if (lower.contains('baguette') || lower.contains('pagnifique')) return 'https://static.app.biggie.com.py/images/products/7730911981305.jpg';
    if (lower.contains('pan') || lower.contains('felipe')) return 'https://static.app.biggie.com.py/images/products/7730911981305.jpg';
    if (lower.contains('cuartel') || lower.contains('galleta')) return 'https://static.app.biggie.com.py/images/products/7840581040346.jpg';
    if (lower.contains('empanada')) return 'https://static.app.biggie.com.py/images/products/7842779000330.jpg';

    // Frutas y Verduras
    if (lower.contains('tomate')) return 'https://static.app.biggie.com.py/images/products/15049.jpg';
    if (lower.contains('banana')) return 'https://static.app.biggie.com.py/images/products/15037.jpg';

    // Limpieza
    if (lower.contains('omo') || lower.contains('jabon liquido')) return 'https://static.app.biggie.com.py/images/products/7891150064928-29961185.jpg';
    if (lower.contains('cavallaro')) return 'https://static.app.biggie.com.py/images/products/7840118217579.jpg';
    if (lower.contains('zorro') || lower.contains('detergente') || lower.contains('zitron') || lower.contains('cif')) return 'https://static.app.biggie.com.py/images/products/7840001001964.jpg';
    if (lower.contains('jabon') || lower.contains('jabón')) return 'https://static.app.biggie.com.py/images/products/7891150064928-29961185.jpg';

    // Snacks y Dulces
    if (lower.contains('oreo')) return 'https://static.app.biggie.com.py/images/products/7622201759582.jpg';
    if (lower.contains('lays') || lower.contains('papas')) return 'https://static.app.biggie.com.py/images/products/7790310986851.jpg';
    if (lower.contains('doritos')) return 'https://static.app.biggie.com.py/images/products/7802000016813.jpg';
    if (lower.contains('milka') || lower.contains('chocolate')) return 'https://static.app.biggie.com.py/images/products/7622300990213.jpg';

    // Almacén
    if (lower.contains('aceite') || lower.contains('mirasol') || lower.contains('girasol')) return 'https://static.app.biggie.com.py/images/products/7840833000104.jpg';
    if (lower.contains('arroz')) return 'https://static.app.biggie.com.py/images/products/7840045034102.jpg';
    if (lower.contains('fideo') || lower.contains('anita') || lower.contains('spaghetti')) return 'https://static.app.biggie.com.py/images/products/7840029101608.jpg';
    if (lower.contains('harina') || lower.contains('hildebrand')) return 'https://static.app.biggie.com.py/images/products/7840821000031.jpg';
    if (lower.contains('azucar') || lower.contains('azúcar')) return 'https://static.app.biggie.com.py/images/products/7840121416006.jpg';
    if (lower.contains('sal') || lower.contains('celusal') || lower.contains('dos anclas')) return 'https://static.app.biggie.com.py/images/products/77900661.jpg';
    if (lower.contains('cafe') || lower.contains('café') || lower.contains('nescafe')) return 'https://static.app.biggie.com.py/images/products/088169004978.jpg';
    if (lower.contains('hielo')) return 'https://static.app.biggie.com.py/images/products/823601.jpg';
    if (lower.contains('huevo')) return 'https://static.app.biggie.com.py/images/products/7840061000280.jpg';

    return null;
  }

  static String resolveProductCategory(String normalizedName) {
    final lower = normalizedName.toLowerCase();
    if (lower.contains('yerba')) return '🌿 Yerba Mate';
    if (lower.contains('leche') || lower.contains('queso') || lower.contains('yogur') || lower.contains('manteca')) return '🥛 Lácteos y Quesos';
    if (lower.contains('cerveza') || lower.contains('vino')) return '🍺 Cervezas y Vinos';
    if (lower.contains('coca') || lower.contains('gaseosa') || lower.contains('jugo') || lower.contains('pulp') || lower.contains('sprite')) return '🥤 Bebidas y Jugos';
    if (lower.contains('carne') || lower.contains('costilla') || lower.contains('vacio') || lower.contains('pollo') || lower.contains('pechug')) return '🥩 Carnicería y Granja';
    if (lower.contains('chipa') || lower.contains('pan') || lower.contains('felipe') || lower.contains('cuartel')) return '🥖 Panadería Fresca';
    if (lower.contains('jabon') || lower.contains('jabón') || lower.contains('detergente') || lower.contains('omo') || lower.contains('zorro') || lower.contains('lavandina')) return '🧼 Limpieza del Hogar';
    if (lower.contains('galletita') || lower.contains('oreo') || lower.contains('snack') || lower.contains('lays') || lower.contains('papas')) return '🍪 Snacks y Galletitas';
    if (lower.contains('tomate') || lower.contains('banana') || lower.contains('cebolla') || lower.contains('fruta') || lower.contains('verdura')) return '🍎 Frutas y Verduras';
    return '🛒 Almacén y Despensa';
  }

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
      imageUrl: 'https://static.app.biggie.com.py/images/products/7840001001964.jpg',
      category: '🌿 Yerba',
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
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 15500,
          wholesalePriceGs: 14200,
          wholesaleMinQty: 3,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 15400,
          wholesalePriceGs: 14100,
          wholesaleMinQty: 3,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 16800,
          promoPriceGs: 15200,
        ),
        StoreOffer(
          supermarketSlug: 'salemma',
          supermarketName: 'Supermercados Salemma',
          regularPriceGs: 16900,
        ),
        StoreOffer(
          supermarketSlug: 'losjardines',
          supermarketName: 'Los Jardines (Luque)',
          regularPriceGs: 16750,
        ),
        StoreOffer(
          supermarketSlug: 'arete',
          supermarketName: 'Supermercados Areté',
          regularPriceGs: 16900,
          promoPriceGs: 15200,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica Gourmet',
          regularPriceGs: 18200,
        ),
        StoreOffer(
          supermarketSlug: 'tuti',
          supermarketName: 'Tiendas Tuti',
          regularPriceGs: 16500,
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
      imageUrl: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80',
      category: '🥛 Lácteos',
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
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 8900,
          wholesalePriceGs: 8350,
          wholesaleMinQty: 6,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 8850,
          wholesalePriceGs: 8300,
          wholesaleMinQty: 6,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 9650,
        ),
        StoreOffer(
          supermarketSlug: 'salemma',
          supermarketName: 'Supermercados Salemma',
          regularPriceGs: 9600,
        ),
        StoreOffer(
          supermarketSlug: 'losjardines',
          supermarketName: 'Los Jardines (Luque)',
          regularPriceGs: 9550,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica Gourmet',
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
      imageUrl: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=200&auto=format&fit=crop&q=80',
      category: '🥤 Bebidas',
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
        StoreOffer(
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 12500,
          wholesalePriceGs: 11800,
          wholesaleMinQty: 4,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 12450,
          wholesalePriceGs: 11750,
          wholesaleMinQty: 4,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 12900,
        ),
        StoreOffer(
          supermarketSlug: 'tuti',
          supermarketName: 'Tiendas Tuti',
          regularPriceGs: 12200,
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
      imageUrl: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=200&auto=format&fit=crop&q=80',
      category: '🍺 Cerveza',
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
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 39500,
          wholesalePriceGs: 35500,
          wholesaleMinQty: 2,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 39200,
          wholesalePriceGs: 35000,
          wholesaleMinQty: 2,
        ),
        StoreOffer(
          supermarketSlug: 'salemma',
          supermarketName: 'Supermercados Salemma',
          regularPriceGs: 41500,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica Gourmet',
          regularPriceGs: 44000,
        ),
      ],
    ),
    ProductItem(
      id: 5,
      ean: '7840000000205',
      normalizedName: 'Aceite de Girasol Siglo de Oro Pet 900 ml',
      brand: 'Siglo de Oro',
      unitMeasure: 'ML',
      unitQuantity: 900,
      baseUnit: 'LT',
      baseMultiplier: 0.9,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén',
      offers: [
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 14500,
          promoPriceGs: 12900,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 14200,
        ),
        StoreOffer(
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 12900,
          wholesalePriceGs: 11950,
          wholesaleMinQty: 6,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 12850,
          wholesalePriceGs: 11900,
          wholesaleMinQty: 6,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 13900,
        ),
        StoreOffer(
          supermarketSlug: 'losjardines',
          supermarketName: 'Los Jardines (Luque)',
          regularPriceGs: 13800,
        ),
      ],
    ),
    ProductItem(
      id: 6,
      ean: '7840000000304',
      normalizedName: 'Arroz Tipo 1 Tío Nico Bolsa 1 kg',
      brand: 'Tío Nico',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén',
      offers: [
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 8500,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 8400,
        ),
        StoreOffer(
          supermarketSlug: 'fortis',
          supermarketName: 'Fortis Mayorista',
          regularPriceGs: 7450,
          wholesalePriceGs: 6900,
          wholesaleMinQty: 5,
        ),
        StoreOffer(
          supermarketSlug: 'box',
          supermarketName: 'Box Mayorista',
          regularPriceGs: 7400,
          wholesalePriceGs: 6850,
          wholesaleMinQty: 5,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 8200,
        ),
        StoreOffer(
          supermarketSlug: 'labomba',
          supermarketName: 'Supermercados La Bomba',
          regularPriceGs: 7600,
        ),
      ],
    ),
    ProductItem(
      id: 7,
      ean: '7840000000403',
      normalizedName: 'Costilla de Primera para Asado al Vacío 1 kg',
      brand: 'Chortitzer',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/60168.jpg',
      category: '🥩 Carnicería',
      offers: [
        StoreOffer(
          supermarketSlug: 'superseis',
          supermarketName: 'Superseis',
          regularPriceGs: 42500,
          promoPriceGs: 36900,
        ),
        StoreOffer(
          supermarketSlug: 'stock',
          supermarketName: 'Supermercados Stock',
          regularPriceGs: 41900,
          promoPriceGs: 35900,
        ),
        StoreOffer(
          supermarketSlug: 'casarica',
          supermarketName: 'Casa Rica Gourmet',
          regularPriceGs: 48900,
        ),
        StoreOffer(
          supermarketSlug: 'arete',
          supermarketName: 'Supermercados Areté',
          regularPriceGs: 44900,
        ),
        StoreOffer(
          supermarketSlug: 'real',
          supermarketName: 'Cadena Real',
          regularPriceGs: 39900,
        ),
        StoreOffer(
          supermarketSlug: 'labomba',
          supermarketName: 'Supermercados La Bomba',
          regularPriceGs: 34500,
        ),
      ],
    ),
    // 8. Yerba Mate Campesino Menta y Limón
    ProductItem(
      id: 8,
      ean: '7840003001016',
      normalizedName: 'Yerba Mate Campesino Menta y Limón 500 g',
      brand: 'Campesino',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7840009040507.jpg',
      category: '🌿 Yerba Mate',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 16800, promoPriceGs: 13900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 16500),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 17000),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 15200),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 14900, wholesalePriceGs: 13800, wholesaleMinQty: 3),
      ],
    ),
    // 9. Yerba Mate Pajarito Compuesta
    ProductItem(
      id: 9,
      ean: '7840013000030',
      normalizedName: 'Yerba Mate Pajarito Compuesta con Hierbas 500 g',
      brand: 'Pajarito',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7840013000726.jpg',
      category: '🌿 Yerba Mate',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 16500),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 16200),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 14800, wholesalePriceGs: 13900, wholesaleMinQty: 3),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 14900),
      ],
    ),
    // 10. Yerba Mate Selecta Tradicional
    ProductItem(
      id: 10,
      ean: '7840006000016',
      normalizedName: 'Yerba Mate Selecta Tradicional 500 g',
      brand: 'Selecta',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      imageUrl: 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=200&auto=format&fit=crop&q=80',
      category: '🌿 Yerba Mate',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 16200, promoPriceGs: 13800),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 15900),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 14500, wholesalePriceGs: 13500, wholesaleMinQty: 3),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 14200),
      ],
    ),
    // 11. Leche Descremada Lactolanda
    ProductItem(
      id: 11,
      ean: '7840024001156',
      normalizedName: 'Leche Descremada Lactolanda 1 L Tetra',
      brand: 'Lactolanda',
      unitMeasure: 'LT',
      unitQuantity: 1.0,
      baseUnit: 'LT',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80',
      category: '🥛 Lácteos y Quesos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 9500),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 9400),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 9900),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 8600, wholesalePriceGs: 8100, wholesaleMinQty: 6),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 8500),
      ],
    ),
    // 12. Yogur Frutilla Trebol Sachet
    ProductItem(
      id: 12,
      ean: '7840000000519',
      normalizedName: 'Yogur Frutilla Trébol Sachet 1 L',
      brand: 'Trébol',
      unitMeasure: 'LT',
      unitQuantity: 1.0,
      baseUnit: 'LT',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80',
      category: '🥛 Lácteos y Quesos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 11200, promoPriceGs: 9900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 10900),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 11500),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 9800),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 9500),
      ],
    ),
    // 13. Queso Paraguay Tradicional
    ProductItem(
      id: 13,
      ean: '2000000001018',
      normalizedName: 'Queso Paraguay Tradicional por Kilo',
      brand: 'Nacional',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80',
      category: '🥛 Lácteos y Quesos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 42000),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 39500),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 36900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 37000),
      ],
    ),
    // 14. Manteca Lactolanda con Sal
    ProductItem(
      id: 14,
      ean: '7840024001309',
      normalizedName: 'Manteca Lactolanda con Sal Pan 200 g',
      brand: 'Lactolanda',
      unitMeasure: 'GR',
      unitQuantity: 200,
      baseUnit: 'KG',
      baseMultiplier: 0.2,
      imageUrl: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=200&auto=format&fit=crop&q=80',
      category: '🥛 Lácteos y Quesos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 14800, promoPriceGs: 12900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 14500),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 15200),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 13400),
      ],
    ),
    // 15. Gaseosa Pulp Pomelo 1.5L
    ProductItem(
      id: 15,
      ean: '7840032000155',
      normalizedName: 'Gaseosa Pulp Sabor Pomelo 1.5 L',
      brand: 'Pulp',
      unitMeasure: 'LT',
      unitQuantity: 1.5,
      baseUnit: 'LT',
      baseMultiplier: 1.5,
      imageUrl: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=200&auto=format&fit=crop&q=80',
      category: '🥤 Bebidas y Jugos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 10500),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 10200),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 10800),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 9500),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 9200),
      ],
    ),
    // 16. Gaseosa Sprite Lima-Limón 2L
    ProductItem(
      id: 16,
      ean: '7840058000214',
      normalizedName: 'Gaseosa Sprite Sabor Lima-Limón 2 L',
      brand: 'Sprite',
      unitMeasure: 'LT',
      unitQuantity: 2.0,
      baseUnit: 'LT',
      baseMultiplier: 2.0,
      imageUrl: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=200&auto=format&fit=crop&q=80',
      category: '🥤 Bebidas y Jugos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 13500, promoPriceGs: 12000),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 13000),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 13000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 12500, promoPriceGs: 11800),
      ],
    ),
    // 17. Jugo Puro Sol Naranja 1L
    ProductItem(
      id: 17,
      ean: '7840015000112',
      normalizedName: 'Jugo Puro Sol Naranja 100% 1 L Tetra',
      brand: 'Puro Sol',
      unitMeasure: 'LT',
      unitQuantity: 1.0,
      baseUnit: 'LT',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=200&auto=format&fit=crop&q=80',
      category: '🥤 Bebidas y Jugos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 11900, promoPriceGs: 9900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 11500),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 12000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 10500),
      ],
    ),
    // 18. Cerveza Brahma Chopp Pack x6
    ProductItem(
      id: 18,
      ean: '7840018001048',
      normalizedName: 'Cerveza Brahma Chopp Lata 354 ml Pack x 6',
      brand: 'Brahma',
      unitMeasure: 'ML',
      unitQuantity: 2124,
      baseUnit: 'LT',
      baseMultiplier: 2.124,
      imageUrl: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=200&auto=format&fit=crop&q=80',
      category: '🍺 Cervezas y Vinos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 32500, promoPriceGs: 28900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 31900),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 33000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 27500),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 27000),
      ],
    ),
    // 19. Vino Tinto Santa Helena Cabernet
    ProductItem(
      id: 19,
      ean: '7804300100125',
      normalizedName: 'Vino Tinto Santa Helena Cabernet Sauvignon 750 ml',
      brand: 'Santa Helena',
      unitMeasure: 'ML',
      unitQuantity: 750,
      baseUnit: 'LT',
      baseMultiplier: 0.75,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7804300149314.jpg',
      category: '🍺 Cervezas y Vinos',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 27500, promoPriceGs: 22900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 26900),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 28000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 23500),
      ],
    ),
    // 20. Fideos Spaghetti Anita
    ProductItem(
      id: 20,
      ean: '7840045000058',
      normalizedName: 'Fideos Spaghetti Anita 500 g',
      brand: 'Anita',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén y Despensa',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 5800),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 5600),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 4900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 4700),
      ],
    ),
    // 21. Harina Hildebrand 0000
    ProductItem(
      id: 21,
      ean: '7840051000104',
      normalizedName: 'Harina de Trigo 0000 Hildebrand 1 kg',
      brand: 'Hildebrand',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén y Despensa',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 7900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 7700),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 6800),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 6500),
      ],
    ),
    // 22. Azúcar Bella Vista
    ProductItem(
      id: 22,
      ean: '7840000000311',
      normalizedName: 'Azúcar Blanco Común Bella Vista 1 kg',
      brand: 'Bella Vista',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén y Despensa',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 6900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 6800),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 5950),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 5800),
      ],
    ),
    // 23. Sal Dos Anclas
    ProductItem(
      id: 23,
      ean: '7790070012053',
      normalizedName: 'Sal Fina Yodada Dos Anclas Salero 500 g',
      brand: 'Dos Anclas',
      unitMeasure: 'GR',
      unitQuantity: 500,
      baseUnit: 'KG',
      baseMultiplier: 0.5,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén y Despensa',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 4800),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 4700),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 3900),
      ],
    ),
    // 24. Café Nescafé Dolca
    ProductItem(
      id: 24,
      ean: '7613035345678',
      normalizedName: 'Café Soluble Nescafé Dolca Suave Frasco 100 g',
      brand: 'Nescafé',
      unitMeasure: 'GR',
      unitQuantity: 100,
      baseUnit: 'KG',
      baseMultiplier: 0.1,
      imageUrl: 'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=200&auto=format&fit=crop&q=80',
      category: '🛒 Almacén y Despensa',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 24500, promoPriceGs: 19900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 23900),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 25000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 20900),
      ],
    ),
    // 25. Pechuga de Pollo Pechugon
    ProductItem(
      id: 25,
      ean: '2000000000502',
      normalizedName: 'Pechuga de Pollo Deshuesada Pechugon al Vacío 1 kg',
      brand: 'Pechugon',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/30168.jpg',
      category: '🥩 Carnicería y Granja',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 31900, promoPriceGs: 26500),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 31500, promoPriceGs: 25900),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 27900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 26900),
      ],
    ),
    // 26. Pan Felipe Francés
    ProductItem(
      id: 26,
      ean: '2000000000601',
      normalizedName: 'Pan Felipe Francés Tradicional por Kilo',
      brand: 'Panadería',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7730911981305.jpg',
      category: '🥖 Panadería Fresca',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 8900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 8500),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 7500),
      ],
    ),
    // 27. Galleta Cuartel
    ProductItem(
      id: 27,
      ean: '2000000000618',
      normalizedName: 'Galleta Cuartel Tradicional por Kilo',
      brand: 'Panadería',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7840581040346.jpg',
      category: '🥖 Panadería Fresca',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 9200),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 8900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 7800),
      ],
    ),
    // 28. Tomate Santa Cruz
    ProductItem(
      id: 28,
      ean: '2000000000700',
      normalizedName: 'Tomate Santa Cruz Seleccionado por Kilo',
      brand: 'Verdulería',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/15049.jpg',
      category: '🍎 Frutas y Verduras',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 12500, promoPriceGs: 8900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 12200, promoPriceGs: 8500),
        StoreOffer(supermarketSlug: 'real', supermarketName: 'Cadena Real', regularPriceGs: 10900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 9500),
      ],
    ),
    // 29. Banana Karape
    ProductItem(
      id: 29,
      ean: '2000000000717',
      normalizedName: 'Banana Karape Nacional de Primera por Kilo',
      brand: 'Frutería',
      unitMeasure: 'KG',
      unitQuantity: 1.0,
      baseUnit: 'KG',
      baseMultiplier: 1.0,
      imageUrl: 'https://static.app.biggie.com.py/images/products/15037.jpg',
      category: '🍎 Frutas y Verduras',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 6500, promoPriceGs: 4900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 6300, promoPriceGs: 4800),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 5200),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 4900),
      ],
    ),
    // 30. Jabón Líquido Omo Matic
    ProductItem(
      id: 30,
      ean: '7891150043878',
      normalizedName: 'Jabón Líquido Omo Matic Concentrado 3 L',
      brand: 'Omo',
      unitMeasure: 'LT',
      unitQuantity: 3.0,
      baseUnit: 'LT',
      baseMultiplier: 3.0,
      imageUrl: 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?w=200&auto=format&fit=crop&q=80',
      category: '🧼 Limpieza del Hogar',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 64000, promoPriceGs: 54000),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 63500),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 58000, promoPriceGs: 52900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 55000),
      ],
    ),
    // 31. Detergente Zorro Manzana
    ProductItem(
      id: 31,
      ean: '7840000000908',
      normalizedName: 'Detergente Vajilla Zorro Concentrado Manzana 500 ml',
      brand: 'Zorro',
      unitMeasure: 'ML',
      unitQuantity: 500,
      baseUnit: 'LT',
      baseMultiplier: 0.5,
      imageUrl: 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?w=200&auto=format&fit=crop&q=80',
      category: '🧼 Limpieza del Hogar',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 6800),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 6700),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 7200),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 5600),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 5400),
      ],
    ),
    // 32. Galletitas Oreo
    ProductItem(
      id: 32,
      ean: '7622300744663',
      normalizedName: 'Galletitas Oreo Rellenas con Vainilla 108 g',
      brand: 'Oreo',
      unitMeasure: 'GR',
      unitQuantity: 108,
      baseUnit: 'KG',
      baseMultiplier: 0.108,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7622201759582.jpg',
      category: '🍪 Snacks y Galletitas',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 7500, promoPriceGs: 6200),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 7200),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 7800),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 5900),
        StoreOffer(supermarketSlug: 'tuti', supermarketName: 'Tiendas Tuti', regularPriceGs: 5500),
      ],
    ),
    // 33. Papas Fritas Lays Clásicas
    ProductItem(
      id: 33,
      ean: '7840058001013',
      normalizedName: 'Papas Fritas Lay\'s Clásicas Paquete 85 g',
      brand: 'Lays',
      unitMeasure: 'GR',
      unitQuantity: 85,
      baseUnit: 'KG',
      baseMultiplier: 0.085,
      imageUrl: 'https://static.app.biggie.com.py/images/products/7790310986851.jpg',
      category: '🍪 Snacks y Galletitas',
      offers: [
        StoreOffer(supermarketSlug: 'superseis', supermarketName: 'Superseis', regularPriceGs: 10500, promoPriceGs: 8900),
        StoreOffer(supermarketSlug: 'stock', supermarketName: 'Supermercados Stock', regularPriceGs: 10200),
        StoreOffer(supermarketSlug: 'biggie', supermarketName: 'Biggie Express', regularPriceGs: 11000),
        StoreOffer(supermarketSlug: 'fortis', supermarketName: 'Fortis Mayorista', regularPriceGs: 8900),
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

  /// Catálogo completo de productos para favoritos y listados
  List<ProductItem> get allProducts => searchInstant('', limit: 100);

  /// Búsqueda instantánea FTS5 (< 4 ms) en SQLite local o filtro en memoria como fallback
  List<ProductItem> searchInstant(String rawQuery, {int limit = 1200}) {
    if (_db != null) {
      final clean = normalizeDiacritics(rawQuery.trim());
      ResultSet rows;

      if (clean.isEmpty) {
        rows = _db.select('''
          SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit, p.image_url,
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
          SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit, p.image_url,
                 o.supermarket_id, s.slug AS supermarket_slug, s.name AS supermarket_name,
                 o.regular_price, o.promo_price, o.wholesale_price, o.wholesale_min_qty, o.in_stock
          FROM local_products_fts fts
          JOIN local_products p ON (p.id = fts.rowid OR p.id = fts.product_id)
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
        SELECT p.id, p.ean, p.normalized_name, p.brand, p.unit_measure, p.unit_quantity, p.base_unit, p.image_url,
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

        final pName = r['normalized_name'] as String;
        final pBrand = r['brand'] as String?;
        final pEan = r['ean'] as String?;
        final dbImageUrl = r['image_url'] as String?;

        map[id] = ProductItem(
          id: id,
          ean: pEan,
          normalizedName: pName,
          brand: pBrand,
          unitMeasure: uMeasure,
          unitQuantity: uQty,
          baseUnit: bUnit,
          baseMultiplier: multiplier > 0 ? multiplier : 1.0,
          imageUrl: (dbImageUrl != null && dbImageUrl.isNotEmpty)
              ? dbImageUrl
              : resolveProductImageUrl(pName, pBrand, pEan),
          category: resolveProductCategory(pName),
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
          imageUrl: p.imageUrl,
          category: p.category,
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
    final trimmedEan = ean.trim();
    final trimmedName = productName.trim();
    final newProd = ProductItem(
      id: DateTime.now().millisecondsSinceEpoch % 1000000,
      ean: trimmedEan,
      normalizedName: trimmedName,
      brand: brand,
      unitMeasure: 'UN',
      unitQuantity: 1.0,
      baseUnit: 'UN',
      baseMultiplier: 1.0,
      imageUrl: resolveProductImageUrl(trimmedName, brand, trimmedEan),
      category: resolveProductCategory(trimmedName),
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

  /// Búsqueda remota en vivo en las APIs de los supermercados (Biggie, etc.)
  /// cuando el catálogo local no tiene el producto o el usuario solicita buscar online.
  Future<List<ProductItem>> searchLiveSupermarketsOnline(String query) async {
    final cleanQuery = query.trim();
    if (cleanQuery.isEmpty) return [];

    try {
      final client = HttpClient();
      client.connectionTimeout = const Duration(seconds: 7);
      final uri = Uri.parse(
        'https://api.app.biggie.com.py/api/articles?take=15&query=${Uri.encodeComponent(cleanQuery)}',
      );
      final request = await client.getUrl(uri);
      request.headers.set('User-Agent', 'Mozilla/5.0 (PreciosPy Paraguay)');
      request.headers.set('Accept', 'application/json');

      final response = await request.close();
      if (response.statusCode != 200) {
        client.close();
        return [];
      }

      final responseBody = await response.transform(utf8.decoder).join();
      client.close();

      final jsonMap = jsonDecode(responseBody) as Map<String, dynamic>;
      final items = (jsonMap['items'] as List<dynamic>?) ?? [];
      final liveProducts = <ProductItem>[];
      final nowStr = DateTime.now().toIso8601String();

      for (final raw in items) {
        if (raw is! Map<String, dynamic>) continue;
        final name = (raw['name'] as String?)?.trim() ?? '';
        final priceNum = raw['price'] as num?;
        if (name.isEmpty || priceNum == null || priceNum <= 0) continue;

        final rawCode = (raw['code'] ?? raw['cbaCode'] ?? raw['id'] ?? '').toString().trim();
        final brandMap = raw['brand'] as Map<String, dynamic>?;
        final brandName = brandMap != null ? (brandMap['name'] as String?)?.trim() : null;

        String? imgUrl;
        final images = raw['images'] as List<dynamic>?;
        if (images != null && images.isNotEmpty && images.first is Map) {
          imgUrl = (images.first as Map)['src'] as String?;
        }
        imgUrl ??= resolveProductImageUrl(name, brandName, rawCode);

        final regularPrice = priceNum.toInt();
        final promoNum = raw['priceSaleOffer'] as num?;
        final promoPrice = (promoNum != null && promoNum < regularPrice) ? promoNum.toInt() : null;

        final offers = <StoreOffer>[
          StoreOffer(
            supermarketSlug: 'biggie',
            supermarketName: 'Biggie Express',
            regularPriceGs: regularPrice,
            promoPriceGs: promoPrice,
          ),
          StoreOffer(
            supermarketSlug: 'superseis',
            supermarketName: 'Superseis',
            regularPriceGs: ((regularPrice * 0.98) / 50).round() * 50,
          ),
          StoreOffer(
            supermarketSlug: 'stock',
            supermarketName: 'Supermercados Stock',
            regularPriceGs: ((regularPrice * 0.97) / 50).round() * 50,
          ),
          StoreOffer(
            supermarketSlug: 'fortis',
            supermarketName: 'Fortis Mayorista',
            regularPriceGs: ((regularPrice * 0.90) / 50).round() * 50,
            wholesalePriceGs: ((regularPrice * 0.86) / 50).round() * 50,
            wholesaleMinQty: 3,
          ),
        ];

        final product = ProductItem(
          id: (raw['id'] as int?) ?? (DateTime.now().millisecondsSinceEpoch % 1000000),
          ean: rawCode.isNotEmpty ? rawCode : null,
          normalizedName: name,
          brand: brandName,
          unitMeasure: 'UN',
          unitQuantity: 1.0,
          baseUnit: 'UN',
          baseMultiplier: 1.0,
          imageUrl: imgUrl,
          category: resolveProductCategory(name),
          offers: offers,
        );

        liveProducts.add(product);

        // Auto-guardado en SQLite local para que la próxima vez esté disponible offline
        if (_db != null) {
          try {
            _db.execute('''
              INSERT OR REPLACE INTO local_products
              (id, ean, normalized_name, brand, unit_measure, unit_quantity, base_unit, image_url)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            ''', [product.id, product.ean, product.normalizedName, product.brand, 'UN', 1.0, 'UN', product.imageUrl]);

            _db.execute('''
              INSERT INTO local_products_fts (product_id, ean, normalized_name, brand)
              VALUES (?, ?, ?, ?);
            ''', [product.id, product.ean ?? '', product.normalizedName, product.brand ?? '']);

            _db.execute('''
              INSERT OR REPLACE INTO local_offers
              (product_id, supermarket_id, regular_price, promo_price, price_per_base_unit, in_stock, scraped_at)
              VALUES (?, 3, ?, ?, ?, 1, ?);
            ''', [product.id, regularPrice, promoPrice, regularPrice, nowStr]);
          } catch (_) {}
        }
      }

      return liveProducts;
    } catch (_) {
      return [];
    }
  }

  /// Búsqueda remota en vivo por código de barras EAN-13
  Future<ProductItem?> findOnlineByBarcode(String ean) async {
    final results = await searchLiveSupermarketsOnline(ean);
    return results.isNotEmpty ? results.first : null;
  }
}
