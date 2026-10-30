import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';
import 'data/local/local_catalog_repository.dart';
import 'state/app_providers.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final repo = await LocalCatalogRepository.createFromAsset();

  runApp(
    ProviderScope(
      overrides: [
        catalogRepositoryProvider.overrideWithValue(repo),
      ],
      child: const PreciosPyApp(),
    ),
  );
}
