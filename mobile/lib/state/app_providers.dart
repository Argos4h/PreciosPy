import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/local/local_catalog_repository.dart';
import '../domain/models/catalog_models.dart';
import '../domain/services/promo_calculator.dart';

/// Modo Claro / Oscuro amigable
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.light);

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

/// Tarjetas activas derivadas en la billetera del usuario paraguayo
final userWalletCardsProvider = Provider<Set<String>>((ref) {
  final profiles = ref.watch(userWalletProfilesProvider);
  return UserWalletProfilesNotifier.deriveCardSlugs(profiles);
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

  void clearCart() {
    state = {};
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
