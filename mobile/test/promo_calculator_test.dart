// ignore_for_file: avoid_print
import 'package:flutter_test/flutter_test.dart';
import 'package:precios_py_mobile/core/formatters/guarani_formatter.dart';
import 'package:precios_py_mobile/data/local/local_catalog_repository.dart';
import 'package:precios_py_mobile/domain/services/promo_calculator.dart';

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
  });
}
