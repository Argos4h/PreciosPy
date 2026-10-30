// ignore_for_file: avoid_print
import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:precios_py_mobile/data/local/local_catalog_repository.dart';
import 'package:sqlite3/sqlite3.dart';

void main() {
  group('SQLite FTS5 Local Catalog Tests', () {
    test('Cargar catálogo SQLite real generado por el scraper nocturno', () {
      final dbFile = File('assets/db/catalog_latest.db');
      expect(dbFile.existsSync(), isTrue, reason: 'El archivo catalog_latest.db debe existir');

      final db = sqlite3.open(dbFile.path);
      final repo = LocalCatalogRepository(sqliteDb: db);

      // 1. Probar búsqueda FTS5 sin tildes sobre productos reales en vivo
      final yerbaHits = repo.searchInstant('yerba');
      expect(yerbaHits, isNotEmpty, reason: 'Debe encontrar yerbas en el catálogo');
      print('Yerba hits encontrados: ${yerbaHits.length}');
      for (final p in yerbaHits.take(3)) {
        print(' - [${p.ean ?? "S/D"}] ${p.normalizedName} (${p.offers.length} ofertas)');
      }

      // 2. Probar búsqueda de cerveza o coca cola
      final drinkHits = repo.searchInstant('coca cola');
      expect(drinkHits, isNotEmpty);
      print('Coca-Cola hits encontrados: ${drinkHits.length}');

      // 3. Probar búsqueda exacta por EAN-13
      final firstWithEan = yerbaHits.firstWhere((p) => p.ean != null, orElse: () => drinkHits.first);
      if (firstWithEan.ean != null) {
        final found = repo.findByBarcode(firstWithEan.ean!);
        expect(found, isNotNull);
        expect(found!.id, equals(firstWithEan.id));
      }

      // 4. Probar promociones bancarias cargadas de la base de datos
      final promos = repo.promotions;
      expect(promos, isNotEmpty);
      print('Promociones bancarias cargadas: ${promos.length}');

      db.dispose();
    });
  });
}

