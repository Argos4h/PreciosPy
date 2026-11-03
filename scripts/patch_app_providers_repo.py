with open('mobile/lib/state/app_providers.dart', 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

old_p = """/// Repositorio local Offline-First
final catalogRepositoryProvider = Provider<LocalCatalogRepository>((ref) {
  return LocalCatalogRepository();
});"""

new_p = """/// Repositorio local Offline-First reactivo
final catalogRepositoryProvider = StateProvider<LocalCatalogRepository>((ref) {
  return LocalCatalogRepository();
});"""

if old_p in c:
    c = c.replace(old_p, new_p, 1)
    print("Replaced catalogRepositoryProvider successfully!")

with open('mobile/lib/state/app_providers.dart', 'w', encoding='utf-8') as f:
    f.write(c)

