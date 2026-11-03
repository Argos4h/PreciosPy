import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/local/local_catalog_repository.dart';
import '../domain/models/catalog_models.dart';
import '../domain/services/promo_calculator.dart';

/// Modo Claro / Oscuro amigable
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.dark);

/// Repositorio local Offline-First reactivo
final catalogRepositoryProvider = StateProvider<LocalCatalogRepository>((ref) {
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

/// Ciudad seleccionada o detectada por GPS (por defecto 'Caacupé')
final selectedCityProvider = StateProvider<String>((ref) => 'Caacupé');

/// Supermercados con sucursales físicas activas en la ciudad seleccionada
final currentCitySupermarketsProvider = Provider<Map<String, String>>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final city = ref.watch(selectedCityProvider);
  final activeSlugs = repo.getSupermarketsInCity(city);
  return Map.fromEntries(
    repo.supermarkets.entries.where((e) => activeSlugs.contains(e.key)),
  );
});

/// Consulta de búsqueda instantánea en la barra superior
final searchQueryProvider = StateProvider<String>((ref) => '');

/// Día de la semana simulado (ISO 1=Lunes ... 7=Domingo). Por defecto: Martes (2) o el día actual.
final selectedWeekdayProvider = StateProvider<int>((ref) => DateTime.now().weekday);

/// Estado detallado de la billetera del usuario por banco y nivel/tier
class UserWalletProfilesNotifier extends StateNotifier<Map<String, UserCardProfile>> {
  UserWalletProfilesNotifier()
      : super({
          'ueno': const UserCardProfile(
            bankSlug: 'ueno',
            bankName: 'ueno bank',
            isEnabled: true,
            cardType: 'credito',
            tier: 'n4',
            uenoLevel: 4,
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'itau': const UserCardProfile(
            bankSlug: 'itau',
            bankName: 'Banco Itaú',
            isEnabled: true,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'continental': const UserCardProfile(
            bankSlug: 'continental',
            bankName: 'Banco Continental',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'familiar': const UserCardProfile(
            bankSlug: 'familiar',
            bankName: 'Banco Familiar',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'atlas': const UserCardProfile(
            bankSlug: 'atlas',
            bankName: 'Banco Atlas',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'sudameris': const UserCardProfile(
            bankSlug: 'sudameris',
            bankName: 'Banco Sudameris',
            isEnabled: false,
            cardType: 'credito',
            tier: 'infinite',
            isQrPayment: false,
            spentThisMonthGs: 0,
          ),
          'gnb': const UserCardProfile(
            bankSlug: 'gnb',
            bankName: 'Banco GNB',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'zeta': const UserCardProfile(
            bankSlug: 'zeta',
            bankName: 'Zeta Banco',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: true,
            spentThisMonthGs: 0,
          ),
          'basa': const UserCardProfile(
            bankSlug: 'basa',
            bankName: 'Banco Basa',
            isEnabled: false,
            cardType: 'credito',
            tier: 'clasica',
            isQrPayment: false,
            spentThisMonthGs: 0,
          ),
        });

  void toggleBank(String bankSlug) {
    final current = state[bankSlug];
    if (current == null) return;
    state = {
      ...state,
      bankSlug: current.copyWith(isEnabled: !current.isEnabled),
    };
  }

  void setTier(String bankSlug, String tier) {
    final current = state[bankSlug];
    if (current == null) return;
    state = {
      ...state,
      bankSlug: current.copyWith(tier: tier),
    };
  }

  void setUenoLevel(int level) {
    final current = state['ueno'];
    if (current == null) return;
    state = {
      ...state,
      'ueno': current.copyWith(uenoLevel: level, tier: 'n$level'),
    };
  }

  void setCardType(String bankSlug, String cardType) {
    final current = state[bankSlug];
    if (current == null) return;
    state = {
      ...state,
      bankSlug: current.copyWith(cardType: cardType),
    };
  }

  void setPaymentMethod(String bankSlug, bool isQr) {
    final current = state[bankSlug];
    if (current == null) return;
    state = {
      ...state,
      bankSlug: current.copyWith(isQrPayment: isQr),
    };
  }

  void setSpentThisMonth(String bankSlug, int spentGs) {
    final current = state[bankSlug];
    if (current == null) return;
    state = {
      ...state,
      bankSlug: current.copyWith(spentThisMonthGs: spentGs),
    };
  }

  static Set<String> deriveCardSlugs(Map<String, UserCardProfile> profiles) {
    final slugs = <String>{};
    for (final entry in profiles.entries) {
      final p = entry.value;
      if (!p.isEnabled) continue;

      if (p.bankSlug == 'ueno') {
        slugs.add('ueno_credito_n${p.uenoLevel}');
        slugs.add('ueno_superseis');
      } else if (p.bankSlug == 'itau') {
        if (p.tier == 'infinite') {
          slugs.add('itau_credito_infinite');
          slugs.add('itau_credito_platinum');
          slugs.add('itau_credito_clasica');
        } else if (p.tier == 'platinum') {
          slugs.add('itau_credito_platinum');
          slugs.add('itau_credito_clasica');
        } else if (p.tier == 'afinidad') {
          slugs.add('itau_afinidad');
          slugs.add('itau_credito_clasica');
        } else {
          slugs.add('itau_credito_clasica');
        }
      } else if (p.bankSlug == 'continental') {
        if (p.tier == 'infinite') {
          slugs.add('continental_black');
          slugs.add('continental_credito');
        } else {
          slugs.add('continental_credito');
        }
      } else if (p.bankSlug == 'familiar') {
        if (p.tier == 'platinum' || p.tier == 'infinite') {
          slugs.add('familiar_platinum');
          slugs.add('familiar_credito');
        } else {
          slugs.add('familiar_credito');
        }
      } else if (p.bankSlug == 'atlas') {
        if (p.tier == 'infinite') {
          slugs.add('atlas_black');
          slugs.add('atlas_credito');
        } else {
          slugs.add('atlas_credito');
        }
      } else if (p.bankSlug == 'sudameris') {
        slugs.add('sudameris_infinite');
      } else if (p.bankSlug == 'gnb') {
        slugs.add('gnb_credito');
      } else if (p.bankSlug == 'zeta') {
        slugs.add('zeta_qr');
      } else if (p.bankSlug == 'basa') {
        slugs.add('basa_credito');
      }
    }
    return slugs;
  }
}

/// Provider de perfiles bancarios configurables por el usuario
final userWalletProfilesProvider =
    StateNotifierProvider<UserWalletProfilesNotifier, Map<String, UserCardProfile>>((ref) {
  return UserWalletProfilesNotifier();
});

/// Modo Solo Efectivo (true = ignorar tarjetas bancarias y comparar solo precios directos de góndola)
final cashOnlyModeProvider = StateProvider<bool>((ref) => false);

/// Tarjetas activas derivadas en la billetera del usuario paraguayo (vacío si está en Modo Solo Efectivo)
final userWalletCardsProvider = Provider<Set<String>>((ref) {
  final isCashOnly = ref.watch(cashOnlyModeProvider);
  if (isCashOnly) return <String>{};
  final profiles = ref.watch(userWalletProfilesProvider);
  return UserWalletProfilesNotifier.deriveCardSlugs(profiles);
});

/// Supermercado donde el usuario está parado físicamente cuando usa el Escáner de Pasillo
final activeStoreInAisleProvider = StateProvider<String>((ref) => 'superseis');

/// Estado del Carrito Inteligente: Mapa de (ProductItem -> Cantidad)
class SmartCartNotifier extends StateNotifier<Map<ProductItem, int>> {
  SmartCartNotifier() : super({});

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

  void clearCart() {
    state = {};
  }
}

final smartCartProvider = StateNotifierProvider<SmartCartNotifier, Map<ProductItem, int>>((ref) {
  return SmartCartNotifier();
});

/// Categoría de producto seleccionada para filtrado (vacío = todas las categorías)
final selectedCategoryProvider = StateProvider<String>((ref) => '');

/// Supermercado específico seleccionado para filtrado (vacío = todos los supermercados)
final selectedSupermarketFilterProvider = StateProvider<String>((ref) => '');

/// Productos filtrados en tiempo real (< 4 ms) según búsqueda, categoría y supermercado

/// Estado de búsqueda remota en vivo en supermercados (Biggie API)
final isSearchingOnlineProvider = StateProvider<bool>((ref) => false);
final onlineSearchResultsProvider = StateProvider<List<ProductItem>>((ref) => []);

final onlineSearchActionProvider = Provider((ref) {
  return (String query) async {
    final clean = query.trim();
    if (clean.isEmpty) return;
    ref.read(isSearchingOnlineProvider.notifier).state = true;
    try {
      final repo = ref.read(catalogRepositoryProvider);
      final liveResults = await repo.searchLiveSupermarketsOnline(clean);
      ref.read(onlineSearchResultsProvider.notifier).state = liveResults;
    } finally {
      ref.read(isSearchingOnlineProvider.notifier).state = false;
    }
  };
});

final filteredProductsProvider = Provider<List<ProductItem>>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final query = ref.watch(searchQueryProvider);
  final category = ref.watch(selectedCategoryProvider);
  final selectedStore = ref.watch(selectedSupermarketFilterProvider);
  var items = repo.searchInstant(query, limit: 1200);

  // Si no hay resultados locales pero hubo búsqueda online en vivo, usar los resultados encontrados
  if (items.isEmpty && query.trim().isNotEmpty) {
    final onlineItems = ref.watch(onlineSearchResultsProvider);
    if (onlineItems.isNotEmpty) {
      items = onlineItems;
    }
  }

    // Filtrar por supermercado si el usuario eligio uno especifico (ej. Biggie, Stock, Fortis)
  if (selectedStore.isNotEmpty) {
    items = items.where((p) => p.offers.any((o) => o.supermarketSlug == selectedStore)).toList();
  }

  // Filtrar por marca si el usuario selecciono una en el modal emergente
  final selectedBrand = ref.watch(selectedBrandProvider);
  if (selectedBrand != null && selectedBrand.trim().isNotEmpty) {
    items = items.where((p) => (p.brand ?? '').toLowerCase() == selectedBrand.toLowerCase().trim()).toList();
  }

  if (category.isEmpty) return items;

  return items.where((p) {
    final cat = (p.category ?? '').toLowerCase();
    final name = p.normalizedName.toLowerCase();
    switch (category) {
      case 'yerba':
        return cat.contains('yerba') || name.contains('yerba');
      case 'lacteos':
        return cat.contains('lácteo') ||
            cat.contains('lacteo') ||
            name.contains('leche') ||
            name.contains('queso') ||
            name.contains('yogur') ||
            name.contains('manteca');
      case 'carniceria':
        return cat.contains('carne') ||
            cat.contains('carnicería') ||
            name.contains('carne') ||
            name.contains('costilla') ||
            name.contains('asado') ||
            name.contains('pollo') ||
            name.contains('pechug');
      case 'bebidas':
        return (cat.contains('bebida') && !cat.contains('vino') && !cat.contains('cerveza')) ||
            name.contains('coca') ||
            name.contains('gaseosa') ||
            name.contains('pulp') ||
            name.contains('sprite') ||
            name.contains('jugo') ||
            name.contains('puro sol');
      case 'cerveza':
        return cat.contains('cerveza') ||
            cat.contains('vino') ||
            name.contains('pilsen') ||
            name.contains('brahma') ||
            name.contains('vino') ||
            name.contains('helena');
      case 'almacen':
        return cat.contains('almacén') ||
            cat.contains('almacen') ||
            name.contains('arroz') ||
            name.contains('fideo') ||
            name.contains('aceite') ||
            name.contains('harina') ||
            name.contains('azúcar') ||
            name.contains('azucar') ||
            name.contains('sal') ||
            name.contains('café') ||
            name.contains('cafe');
      case 'panaderia':
        return cat.contains('pan') ||
            name.contains('pan') ||
            name.contains('felipe') ||
            name.contains('cuartel') ||
            name.contains('chipa');
      case 'limpieza':
        return cat.contains('limpieza') ||
            name.contains('jabón') ||
            name.contains('jabon') ||
            name.contains('omo') ||
            name.contains('detergente') ||
            name.contains('zorro') ||
            name.contains('lavandina');
      case 'galletitas':
        return cat.contains('snack') ||
            cat.contains('galletita') ||
            name.contains('oreo') ||
            name.contains('lay') ||
            name.contains('papa');
      case 'frutas':
        return cat.contains('fruta') ||
            cat.contains('verdura') ||
            name.contains('tomate') ||
            name.contains('banana') ||
            name.contains('cebolla');
      default:
        return cat.contains(category) || name.contains(category);
    }
  }).toList();
});

/// Ranking en tiempo real de qué supermercado conviene más para comprar el Carrito Inteligente hoy
final smartCartRankingsProvider = Provider<List<SmartCartSummary>>((ref) {
  final repo = ref.watch(catalogRepositoryProvider);
  final cart = ref.watch(smartCartProvider);
  final wallet = ref.watch(userWalletCardsProvider);
  final weekday = ref.watch(selectedWeekdayProvider);
  final cityStores = ref.watch(currentCitySupermarketsProvider);

  return PromoCalculator.simulateCartAcrossSupermarkets(
    cartQuantities: cart,
    supermarketsBySlug: cityStores,
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
  final cityStores = ref.watch(currentCitySupermarketsProvider);

  return PromoCalculator.optimizeSplitCart(
    cartQuantities: cart,
    supermarketsBySlug: cityStores,
    allPromotions: repo.promotions,
    userCardSlugs: wallet,
    isoWeekday: weekday,
  );
});

/// Gestión de productos favoritos y alertas de precio (al estilo Rebuscate)
class FavoritesNotifier extends StateNotifier<Set<int>> {
  FavoritesNotifier() : super({}); // Yerba Kurupí (id: 1) y Leche Trébol (id: 2) por defecto

  void toggleFavorite(int productId) {
    if (state.contains(productId)) {
      state = Set.from(state)..remove(productId);
    } else {
      state = Set.from(state)..add(productId);
    }
  }

  bool isFavorite(int productId) => state.contains(productId);
}

final favoritesProvider = StateNotifierProvider<FavoritesNotifier, Set<int>>((ref) {
  return FavoritesNotifier();
});

/// Filtro de la pestaña Promos: ¿mostrar sólo promociones de mis tarjetas o todas las de Paraguay?
final promosFilterOnlyUserCardsProvider = StateProvider<bool>((ref) => false);

/// Pestaña activa en la barra de navegación (0=Precios, 1=Promos, 2=Escáner, 3=Listas, 4=Perfil)
final activeTabProvider = StateProvider<int>((ref) => 0);




/// Filtro opcional por marca seleccionada en el diAlogo emergente
final selectedBrandProvider = StateProvider<String?>((ref) => null);
