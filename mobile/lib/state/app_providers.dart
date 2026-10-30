import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/local/local_catalog_repository.dart';
import '../domain/models/catalog_models.dart';
import '../domain/services/promo_calculator.dart';

/// Repositorio local Offline-First
final catalogRepositoryProvider = Provider<LocalCatalogRepository>((ref) {
  return LocalCatalogRepository();
});

/// Promociones bancarias activas
final bankPromotionsProvider = Provider<List<BankPromotion>>((ref) {
  return ref.watch(catalogRepositoryProvider).promotions;
});

/// Supermercados soportados
final supermarketsProvider = Provider<Map<String, String>>((ref) {
  return ref.watch(catalogRepositoryProvider).supermarkets;
});

/// Consulta de búsqueda instantánea en la barra superior
final searchQueryProvider = StateProvider<String>((ref) => '');

/// Día de la semana simulado (ISO 1=Lunes ... 7=Domingo). Por defecto: Martes (2) o el día actual.
final selectedWeekdayProvider = StateProvider<int>((ref) => DateTime.now().weekday);

/// Tarjetas activas en la billetera del usuario paraguayo
final userWalletCardsProvider = StateProvider<Set<String>>((ref) {
  return {'ueno_credito_n4', 'itau_credito_clasica'};
});

/// Supermercado donde el usuario está parado físicamente cuando usa el Escáner de Pasillo
final activeStoreInAisleProvider = StateProvider<String>((ref) => 'superseis');

/// Estado del Carrito Inteligente: Mapa de (ProductItem -> Cantidad)
class SmartCartNotifier extends StateNotifier<Map<ProductItem, int>> {
  SmartCartNotifier()
      : super({
          LocalCatalogRepository.initialCatalog[0]: 2, // 2x Yerba Kurupí
          LocalCatalogRepository.initialCatalog[1]: 6, // 6x Leche Trébol 1L
          LocalCatalogRepository.initialCatalog[3]: 1, // 1x Pack Pilsen
        });

  void addOrIncrement(ProductItem product) {
    state = {
      ...state,
      product: (state[product] ?? 0) + 1,
    };
  }

  void decrementOrRemove(ProductItem product) {
    final current = state[product] ?? 0;
    if (current <= 1) {
      final copy = Map<ProductItem, int>.from(state);
      copy.remove(product);
      state = copy;
    } else {
      state = {
        ...state,
        product: current - 1,
      };
    }
  }
}

final smartCartProvider = StateNotifierProvider<SmartCartNotifier, Map<ProductItem, int>>((ref) {
  return SmartCartNotifier();
});

/// Productos filtrados en tiempo real (< 4 ms) según la búsqueda del usuario
final filteredProductsProvider = Provider<List<ProductItem>>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final query = ref.watch(searchQueryProvider);
  return repo.searchInstant(query);
});

/// Ranking en tiempo real de qué supermercado conviene más para comprar el Carrito Inteligente hoy
final smartCartRankingsProvider = Provider<List<SmartCartSummary>>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final cart = ref.watch(smartCartProvider);
  final wallet = ref.watch(userWalletCardsProvider);
  final weekday = ref.watch(selectedWeekdayProvider);

  return PromoCalculator.simulateCartAcrossSupermarkets(
    cartQuantities: cart,
    supermarketsBySlug: repo.supermarkets,
    allPromotions: repo.promotions,
    userCardSlugs: wallet,
    isoWeekday: weekday,
  );
});

/// Resultado del Optimizador de Compra Dividida (Split Cart)
final splitCartResultProvider = Provider<SplitCartResult>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final cart = ref.watch(smartCartProvider);
  final wallet = ref.watch(userWalletCardsProvider);
  final weekday = ref.watch(selectedWeekdayProvider);

  return PromoCalculator.optimizeSplitCart(
    cartQuantities: cart,
    supermarketsBySlug: repo.supermarkets,
    allPromotions: repo.promotions,
    userCardSlugs: wallet,
    isoWeekday: weekday,
  );
});
