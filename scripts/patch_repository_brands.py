import sys

with open('mobile/lib/data/local/local_catalog_repository.dart', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'List<ProductItem> searchInstant(String rawQuery, {int limit = 30}) {',
    'List<ProductItem> searchInstant(String rawQuery, {int limit = 1200}) {'
)

brand_method = """
  /// Devuelve todas las marcas registradas en el catalogo con su conteo
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
"""

if 'getUniqueBrands()' not in code:
    idx_insert = code.find('Map<String, String> get supermarkets')
    code = code[:idx_insert] + brand_method + '\n  ' + code[idx_insert:]

with open('mobile/lib/data/local/local_catalog_repository.dart', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated LocalCatalogRepository with getUniqueBrands!')

