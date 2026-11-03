import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';
import 'data/local/local_catalog_repository.dart';
import 'state/app_providers.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 1. Inicia inmediatamente con el catálogo local SQLite para respuesta instantánea en < 4 ms
  final repo = await LocalCatalogRepository.createFromAsset();

  final container = ProviderContainer(
    overrides: [
      catalogRepositoryProvider.overrideWith((ref) => repo),
    ],
  );

  runApp(
    UncontrolledProviderScope(
      container: container,
      child: const PreciosPyApp(),
    ),
  );

  // 2. En segundo plano (sin bloquear al usuario), sincroniza silenciosamente el catálogo desde la nube
  Future.microtask(() async {
    final updated = await LocalCatalogRepository.syncCloudCatalogSilently();
    if (updated) {
      // Si la nube tenía precios más nuevos, recarga el repositorio en vivo sin necesidad de reiniciar
      final freshRepo = await LocalCatalogRepository.createFromAsset();
      container.read(catalogRepositoryProvider.notifier).state = freshRepo;
    }
  });
}
