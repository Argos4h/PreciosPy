with open('mobile/lib/data/local/local_catalog_repository.dart', 'r', encoding='utf-8') as f:
    content = f.read().replace('\r\n', '\n')

old_code = """  /// Abre o inicializa el repositorio leyendo el archivo SQLite desde los assets de Flutter
  static Future<LocalCatalogRepository> createFromAsset({
    String assetPath = 'assets/db/catalog_latest.db',
  }) async {
    try {
      final docDir = await getApplicationDocumentsDirectory();
      final targetFile = File(p.join(docDir.path, 'catalog_latest.db'));

      final byteData = await rootBundle.load(assetPath);
      final bytes = byteData.buffer.asUint8List(
        byteData.offsetInBytes,
        byteData.lengthInBytes,
      );

      // Si no existe localmente o el archivo en assets es más reciente/distinto tamaño, actualizamos
      if (!await targetFile.exists() || (await targetFile.length()) != bytes.length) {
        await targetFile.writeAsBytes(bytes, flush: true);
      }

      final db = sqlite3.open(targetFile.path);
      return LocalCatalogRepository(sqliteDb: db);
    } catch (e) {
      // Fallback elegante a catálogo en memoria si ocurre un error de permisos o I/O
      return LocalCatalogRepository();
    }
  }"""

new_code = """  /// URL en la nube (GitHub Raw) donde se aloja el catálogo SQLite oficial actualizado automáticamente
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
  }"""

# Buscar con regex o coincidencia flexible
idx = content.find("static Future<LocalCatalogRepository> createFromAsset")
if idx != -1:
    start = content.rfind("///", 0, idx)
    end = content.find("Map<String, int> getUniqueBrands()", idx)
    content = content[:start] + new_code + "\n\n  " + content[end:]
    print("Replaced createFromAsset with syncCloudCatalogSilently successfully!")

with open('mobile/lib/data/local/local_catalog_repository.dart', 'w', encoding='utf-8') as f:
    f.write(content)

