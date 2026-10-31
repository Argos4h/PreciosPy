// ignore_for_file: avoid_print
import 'package:flutter_test/flutter_test.dart';
import 'package:precios_py_mobile/core/formatters/guarani_formatter.dart';
import 'package:precios_py_mobile/data/local/local_catalog_repository.dart';
import 'package:precios_py_mobile/domain/services/promo_calculator.dart';
import 'package:precios_py_mobile/state/app_providers.dart';

void main() {
  group('PreciosPy Mobile Engine Tests', () {
    test('Formateador de Guaraníes con puntos de miles', () {
      expect(GuaraniFormatter.format(18500), 'Gs. 18.500');
      expect(GuaraniFormatter.format(1250000), 'Gs. 1.250.000');
      expect(GuaraniFormatter.formatPerBaseUnit(22750, 'KG'), 'Gs. 22.750 / KG');
    });

    test('Ranking de ofertas de Yerba Kurupí un Martes con ueno Nivel 4 + Itaú', () {
      final yerba = LocalCatalogRepository.initialCatalog.first;
      final ranked = PromoCalculator.rankProductOffers(
        product: yerba,
        allPromotions: LocalCatalogRepository.paraguayPromotions,
        userCardSlugs: {'ueno_credito_n4', 'itau_credito_clasica'},
        isoWeekday: 2, // Martes
      );

      // 1° Biggie con ueno Nivel 4 (35% sobre 17.500 = Gs. 11.375)
      expect(ranked.first.offer.supermarketSlug, 'biggie');
      expect(ranked.first.effectiveFinalPriceGs, 11375);

      // 2° Superseis con Martes Itaú (20% sobre regular 17.200 = Gs. 13.760 < oferta 14.500)
      expect(ranked[1].offer.supermarketSlug, 'superseis');
      expect(ranked[1].effectiveFinalPriceGs, 13760);
    });

    test('Optimizador de Compra Dividida (Split Cart)', () {
      final yerba = LocalCatalogRepository.initialCatalog[0];
      final leche = LocalCatalogRepository.initialCatalog[1];
      final cerveza = LocalCatalogRepository.initialCatalog[3];

      final cart = {
        yerba: 2,
        leche: 6,
        cerveza: 2,
      };

      final splitResult = PromoCalculator.optimizeSplitCart(
        cartQuantities: cart,
        supermarketsBySlug: LocalCatalogRepository.defaultSupermarkets,
        allPromotions: LocalCatalogRepository.paraguayPromotions,
        userCardSlugs: {'ueno_credito_n4', 'itau_credito_clasica'},
        isoWeekday: 2, // Martes
      );

      expect(splitResult.bestSingleStore.supermarketSlug, isNotEmpty);
      expect(splitResult.splitGroups, isNotEmpty);
      expect(splitResult.combinedNetCostGs, lessThanOrEqualTo(splitResult.bestSingleStore.netFinalCostGs));
      print('Mejor Single Store: ${splitResult.bestSingleStore.supermarketName} -> Gs. ${splitResult.bestSingleStore.netFinalCostGs}');
      print('Costo Dividido: Gs. ${splitResult.combinedNetCostGs} (Ahorro Extra: Gs. ${splitResult.additionalSavingsGs})');
      print('¿Se recomienda dividir?: ${splitResult.isSplitRecommended}');
    });

    test('Filtro por ciudad: Caacupé solo evalúa supermercados con sucursales en Caacupé', () {
      final repo = LocalCatalogRepository();
      final caacupeSlugs = repo.getSupermarketsInCity('Caacupé');

      // Caacupé solo cuenta con Stock, Superseis, Biggie y Tuti
      expect(caacupeSlugs, containsAll(['stock', 'superseis', 'biggie', 'tuti']));
      expect(caacupeSlugs, isNot(contains('casarica')));
      expect(caacupeSlugs, isNot(contains('arete')));
      expect(caacupeSlugs, isNot(contains('fortis')));
      expect(caacupeSlugs, isNot(contains('delimarket')));

      // Ranking de ofertas de Yerba solo debe mostrar súper de Caacupé
      final yerba = LocalCatalogRepository.initialCatalog.first;
      final rankedCaacupe = PromoCalculator.rankProductOffers(
        product: yerba,
        allPromotions: LocalCatalogRepository.paraguayPromotions,
        userCardSlugs: {'ueno_credito_n4', 'itau_credito_clasica'},
        isoWeekday: 2, // Martes
        availableSupermarketSlugs: caacupeSlugs.toSet(),
      );

      for (final offer in rankedCaacupe) {
        expect(caacupeSlugs, contains(offer.offer.supermarketSlug));
      }

      // Simulación de carrito en Caacupé
      final cart = {yerba: 2};
      final caacupeStores = Map.fromEntries(
        repo.supermarkets.entries.where((e) => caacupeSlugs.contains(e.key)),
      );

      final summaries = PromoCalculator.simulateCartAcrossSupermarkets(
        cartQuantities: cart,
        supermarketsBySlug: caacupeStores,
        allPromotions: LocalCatalogRepository.paraguayPromotions,
        userCardSlugs: {'ueno_credito_n4', 'itau_credito_clasica'},
        isoWeekday: 2,
      );

      expect(summaries.length, caacupeStores.length);
      for (final s in summaries) {
        expect(caacupeSlugs, contains(s.supermarketSlug));
      }
    });

    test('Modo Solo Efectivo: compara exclusivamente precios góndola ignorando tarjetas bancarias', () {
      final yerba = LocalCatalogRepository.initialCatalog.first;

      // Ranking con Solo Efectivo (userCardSlugs = {})
      final rankedCash = PromoCalculator.rankProductOffers(
        product: yerba,
        allPromotions: LocalCatalogRepository.paraguayPromotions,
        userCardSlugs: <String>{}, // Sin tarjetas
        isoWeekday: 2,
        availableSupermarketSlugs: {'superseis', 'stock', 'biggie', 'tuti'},
      );

      // Superseis tiene oferta de góndola a Gs. 14.500 para todo público
      expect(rankedCash.first.offer.supermarketSlug, 'superseis');
      expect(rankedCash.first.effectiveFinalPriceGs, 14500);
      expect(rankedCash.first.appliedPromotion, isNull);
      expect(rankedCash.first.pricingNote, contains('Oferta directa de góndola'));

      // Biggie tiene regular 17.500 y no aplica el 35% de ueno porque es en efectivo
      final biggieOffer = rankedCash.firstWhere((o) => o.offer.supermarketSlug == 'biggie');
      expect(biggieOffer.effectiveFinalPriceGs, 17500);
      expect(biggieOffer.appliedPromotion, isNull);

      // Tuti tiene regular 16.500
      final tutiOffer = rankedCash.firstWhere((o) => o.offer.supermarketSlug == 'tuti');
      expect(tutiOffer.effectiveFinalPriceGs, 16500);
    });

    test('Favoritos y Alertas (estilo Rebuscate): agrega y quita productos', () {
      final notifier = FavoritesNotifier();
      expect(notifier.state.contains(1), isTrue); // Yerba Kurupí por defecto
      notifier.toggleFavorite(1);
      expect(notifier.state.contains(1), isFalse);
      notifier.toggleFavorite(1);
      expect(notifier.state.contains(1), isTrue);
    });

    test('Promociones semanales: filtra por día y banco', () {
      const promos = LocalCatalogRepository.paraguayPromotions;
      // Martes (2): Itaú en Superseis
      final tuesdayPromos = promos.where((p) => p.isValidOnWeekday(2)).toList();
      expect(tuesdayPromos.any((p) => p.entityName == 'Banco Itaú'), isTrue);
      // Viernes (5): Familiar en Stock y ueno en Superseis
      final fridayPromos = promos.where((p) => p.isValidOnWeekday(5)).toList();
      expect(fridayPromos.any((p) => p.entityName == 'Banco Familiar'), isTrue);
      expect(fridayPromos.any((p) => p.supermarketSlug == 'superseis' && p.bankSlug == 'ueno'), isTrue);
    });
  });
}
