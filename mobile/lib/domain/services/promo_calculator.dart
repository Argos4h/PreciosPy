import '../models/catalog_models.dart';

/// Motor determinista en Dart para calcular el Precio Final Real y optimizar el Carrito Inteligente
/// cruzando precios regulares, ofertas de góndola y promociones bancarias paraguayas.
class PromoCalculator {
  const PromoCalculator._();

  static EvaluatedOffer evaluateOfferForWallet({
    required ProductItem product,
    required StoreOffer offer,
    required List<BankPromotion> allPromotions,
    required Set<String> userCardSlugs,
    required int isoWeekday,
  }) {
    final gondolaBest = offer.gondolaBestPriceGs;
    var bestFinalPrice = gondolaBest;
    var bestCashOutflow = gondolaBest;
    var bestCashback = 0;
    BankPromotion? bestPromo;

    var pricingNote = (offer.promoPriceGs != null && offer.promoPriceGs! < offer.regularPriceGs)
        ? 'Oferta directa de góndola'
        : 'Precio regular de góndola';

    final eligiblePromos = allPromotions.where(
      (p) =>
          p.supermarketSlug == offer.supermarketSlug &&
          userCardSlugs.contains(p.cardSlug) &&
          p.isValidOnWeekday(isoWeekday),
    );

    for (final promo in eligiblePromos) {
      final eligibleBase = promo.appliesToPromoPrice ? gondolaBest : offer.regularPriceGs;
      var rawDiscount = (eligibleBase * (promo.discountPct / 100.0)).round();

      if (promo.maxRefundGs != null && rawDiscount > promo.maxRefundGs!) {
        rawDiscount = promo.maxRefundGs!;
      }

      final candidateFinalPrice = eligibleBase - rawDiscount;

      if (candidateFinalPrice < bestFinalPrice) {
        bestFinalPrice = candidateFinalPrice;
        bestPromo = promo;
        if (promo.mechanism == DiscountMechanism.instantPos) {
          bestCashOutflow = candidateFinalPrice;
          bestCashback = 0;
          pricingNote = '${promo.discountPct.toStringAsFixed(0)}% dto. en caja con ${promo.cardName}';
        } else {
          bestCashOutflow = eligibleBase;
          bestCashback = rawDiscount;
          pricingNote = '${promo.discountPct.toStringAsFixed(0)}% reintegro con ${promo.cardName}';
        }
      } else if (offer.promoPriceGs != null &&
          !promo.appliesToPromoPrice &&
          candidateFinalPrice >= gondolaBest &&
          bestPromo == null) {
        pricingNote = 'Conviene oferta de góndola (No acumulable con ${promo.cardName})';
      }
    }

    final multiplier = product.baseMultiplier > 0 ? product.baseMultiplier : 1.0;
    final pricePerBaseUnit = (bestFinalPrice / multiplier).round();

    return EvaluatedOffer(
      offer: offer,
      effectiveFinalPriceGs: bestFinalPrice,
      cashOutflowAtPosGs: bestCashOutflow,
      cashbackAmountGs: bestCashback,
      pricePerBaseUnitGs: pricePerBaseUnit,
      baseUnit: product.baseUnit,
      appliedPromotion: bestPromo,
      pricingNote: pricingNote,
    );
  }

  /// Ordena todas las ofertas de un producto desde la más barata hoy (con las tarjetas del usuario)
  /// hasta la más cara, filtrando opcionalmente por supermercados disponibles en la ciudad del usuario.
  static List<EvaluatedOffer> rankProductOffers({
    required ProductItem product,
    required List<BankPromotion> allPromotions,
    required Set<String> userCardSlugs,
    required int isoWeekday,
    Set<String>? availableSupermarketSlugs,
  }) {
    final candidateOffers = (availableSupermarketSlugs != null && availableSupermarketSlugs.isNotEmpty)
        ? product.offers.where((o) => availableSupermarketSlugs.contains(o.supermarketSlug))
        : product.offers;

    final evaluated = candidateOffers
        .map(
          (offer) => evaluateOfferForWallet(
            product: product,
            offer: offer,
            allPromotions: allPromotions,
            userCardSlugs: userCardSlugs,
            isoWeekday: isoWeekday,
          ),
        )
        .toList();

    evaluated.sort((a, b) => a.effectiveFinalPriceGs.compareTo(b.effectiveFinalPriceGs));
    return evaluated;
  }

  /// Simula el costo de comprar todo el carrito en cada supermercado respetando el tope
  /// de compra mensual/diario (`spendingCapGs`) de cada banco.
  static List<SmartCartSummary> simulateCartAcrossSupermarkets({
    required Map<ProductItem, int> cartQuantities,
    required Map<String, String> supermarketsBySlug,
    required List<BankPromotion> allPromotions,
    required Set<String> userCardSlugs,
    required int isoWeekday,
  }) {
    final summaries = <SmartCartSummary>[];

    for (final entry in supermarketsBySlug.entries) {
      final supSlug = entry.key;
      final supName = entry.value;

      var totalRegular = 0;
      var totalGondola = 0;
      var missingCount = 0;
      final availableItems = <MapEntry<StoreOffer, int>>[];

      for (final cartEntry in cartQuantities.entries) {
        final product = cartEntry.key;
        final qty = cartEntry.value;
        final matchingOffers = product.offers.where((o) => o.supermarketSlug == supSlug);
        if (matchingOffers.isEmpty) {
          missingCount++;
          continue;
        }
        final offer = matchingOffers.first;
        availableItems.add(MapEntry(offer, qty));
        totalRegular += offer.regularPriceGs * qty;

        // Si el usuario compra por fardo/pack (>= wholesaleMinQty en mayoristas), aplica precio mayorista
        final effectiveUnit = (offer.wholesalePriceGs != null &&
                offer.wholesaleMinQty != null &&
                qty >= offer.wholesaleMinQty!)
            ? offer.wholesalePriceGs!
            : offer.gondolaBestPriceGs;

        totalGondola += effectiveUnit * qty;
      }

      if (availableItems.isEmpty) {
        continue;
      }

      var bestSummary = SmartCartSummary(
        supermarketSlug: supSlug,
        supermarketName: supName,
        totalRegularGs: totalRegular,
        totalGondolaGs: totalGondola,
        totalCashAtPosGs: totalGondola,
        totalCashbackGs: 0,
        netFinalCostGs: totalGondola,
        appliedCardName: null,
        capReached: false,
        missingProductsCount: missingCount,
      );

      final eligiblePromos = allPromotions.where(
        (p) =>
            p.supermarketSlug == supSlug &&
            userCardSlugs.contains(p.cardSlug) &&
            p.isValidOnWeekday(isoWeekday),
      );

      for (final promo in eligiblePromos) {
        var eligibleSpend = 0;
        var nonEligibleSpend = 0;

        for (final itemEntry in availableItems) {
          final offer = itemEntry.key;
          final qty = itemEntry.value;
          final gondolaUnit = offer.gondolaBestPriceGs;

          if (promo.appliesToPromoPrice) {
            eligibleSpend += gondolaUnit * qty;
          } else {
            final cardUnit = (offer.regularPriceGs * (1.0 - promo.discountPct / 100.0)).round();
            if (gondolaUnit <= cardUnit) {
              nonEligibleSpend += gondolaUnit * qty;
            } else {
              eligibleSpend += offer.regularPriceGs * qty;
            }
          }
        }

        var capReached = false;
        var cappedSpend = eligibleSpend;
        if (promo.spendingCapGs != null && eligibleSpend > promo.spendingCapGs!) {
          cappedSpend = promo.spendingCapGs!;
          capReached = true;
        }

        var discountGs = (cappedSpend * (promo.discountPct / 100.0)).round();
        if (promo.maxRefundGs != null && discountGs > promo.maxRefundGs!) {
          discountGs = promo.maxRefundGs!;
          capReached = true;
        }

        final grossTicket = eligibleSpend + nonEligibleSpend;
        final netCost = grossTicket - discountGs;
        final cashAtPos =
            promo.mechanism == DiscountMechanism.instantPos ? netCost : grossTicket;
        final cashback = promo.mechanism == DiscountMechanism.instantPos ? 0 : discountGs;

        if (netCost < bestSummary.netFinalCostGs) {
          bestSummary = SmartCartSummary(
            supermarketSlug: supSlug,
            supermarketName: supName,
            totalRegularGs: totalRegular,
            totalGondolaGs: totalGondola,
            totalCashAtPosGs: cashAtPos,
            totalCashbackGs: cashback,
            netFinalCostGs: netCost,
            appliedCardName: promo.cardName,
            capReached: capReached,
            missingProductsCount: missingCount,
          );
        }
      }

      summaries.add(bestSummary);
    }

    summaries.sort((a, b) {
      if (a.missingProductsCount != b.missingProductsCount) {
        return a.missingProductsCount.compareTo(b.missingProductsCount);
      }
      return a.netFinalCostGs.compareTo(b.netFinalCostGs);
    });

    return summaries;
  }

  /// Optimizador de "Compra Dividida" (Split-Cart Killer Feature):
  /// Calcula si dividir la compra entre 2 supermercados ahorra dinero significativo
  /// comparado con comprar todo en un solo lugar.
  static SplitCartResult optimizeSplitCart({
    required Map<ProductItem, int> cartQuantities,
    required Map<String, String> supermarketsBySlug,
    required List<BankPromotion> allPromotions,
    required Set<String> userCardSlugs,
    required int isoWeekday,
  }) {
    final singleStoreRankings = simulateCartAcrossSupermarkets(
      cartQuantities: cartQuantities,
      supermarketsBySlug: supermarketsBySlug,
      allPromotions: allPromotions,
      userCardSlugs: userCardSlugs,
      isoWeekday: isoWeekday,
    );

    if (singleStoreRankings.isEmpty) {
      return const SplitCartResult(
        bestSingleStore: SmartCartSummary(
          supermarketSlug: '',
          supermarketName: 'Sin datos',
          totalRegularGs: 0,
          totalGondolaGs: 0,
          totalCashAtPosGs: 0,
          totalCashbackGs: 0,
          netFinalCostGs: 0,
          capReached: false,
          missingProductsCount: 0,
        ),
        splitGroups: [],
        combinedNetCostGs: 0,
        additionalSavingsGs: 0,
        isSplitRecommended: false,
      );
    }

    final bestSingle = singleStoreRankings.first;

    // 1. Asignar cada producto al supermercado que ofrece el menor precio final real individual hoy
    final itemsByStore = <String, List<MapEntry<ProductItem, int>>>{};

    for (final entry in cartQuantities.entries) {
      final product = entry.key;
      final qty = entry.value;

      if (product.offers.isEmpty) continue;

      final ranked = rankProductOffers(
        product: product,
        allPromotions: allPromotions,
        userCardSlugs: userCardSlugs,
        isoWeekday: isoWeekday,
      );

      final winnerOffer = ranked.first;
      final chosenStoreSlug = winnerOffer.offer.supermarketSlug;

      itemsByStore.putIfAbsent(chosenStoreSlug, () => []).add(MapEntry(product, qty));
    }

    // 2. Calcular los subtotales para cada grupo de tienda respetando promociones y topes
    final splitGroups = <SplitCartStoreGroup>[];
    var combinedNet = 0;

    for (final storeEntry in itemsByStore.entries) {
      final slug = storeEntry.key;
      final items = storeEntry.value;
      final supName = supermarketsBySlug[slug] ?? slug;

      var subTotalGondola = 0;
      final availableItems = <MapEntry<StoreOffer, int>>[];

      for (final item in items) {
        final product = item.key;
        final qty = item.value;
        final offer = product.offers.firstWhere((o) => o.supermarketSlug == slug);
        availableItems.add(MapEntry(offer, qty));
        subTotalGondola += offer.gondolaBestPriceGs * qty;
      }

      var bestCashAtPos = subTotalGondola;
      var bestCashback = 0;
      var bestNetCost = subTotalGondola;
      String? bestCard;

      final eligiblePromos = allPromotions.where(
        (p) =>
            p.supermarketSlug == slug &&
            userCardSlugs.contains(p.cardSlug) &&
            p.isValidOnWeekday(isoWeekday),
      );

      for (final promo in eligiblePromos) {
        var eligibleSpend = 0;
        var nonEligibleSpend = 0;

        for (final item in availableItems) {
          final offer = item.key;
          final qty = item.value;
          final gondolaUnit = offer.gondolaBestPriceGs;

          if (promo.appliesToPromoPrice) {
            eligibleSpend += gondolaUnit * qty;
          } else {
            final cardUnit = (offer.regularPriceGs * (1.0 - promo.discountPct / 100.0)).round();
            if (gondolaUnit <= cardUnit) {
              nonEligibleSpend += gondolaUnit * qty;
            } else {
              eligibleSpend += offer.regularPriceGs * qty;
            }
          }
        }

        var cappedSpend = eligibleSpend;
        if (promo.spendingCapGs != null && eligibleSpend > promo.spendingCapGs!) {
          cappedSpend = promo.spendingCapGs!;
        }

        var discountGs = (cappedSpend * (promo.discountPct / 100.0)).round();
        if (promo.maxRefundGs != null && discountGs > promo.maxRefundGs!) {
          discountGs = promo.maxRefundGs!;
        }

        final grossTicket = eligibleSpend + nonEligibleSpend;
        final netCost = grossTicket - discountGs;

        if (netCost < bestNetCost) {
          bestNetCost = netCost;
          bestCashAtPos = promo.mechanism == DiscountMechanism.instantPos ? netCost : grossTicket;
          bestCashback = promo.mechanism == DiscountMechanism.instantPos ? 0 : discountGs;
          bestCard = promo.cardName;
        }
      }

      splitGroups.add(
        SplitCartStoreGroup(
          supermarketSlug: slug,
          supermarketName: supName,
          items: items,
          totalCashAtPosGs: bestCashAtPos,
          totalCashbackGs: bestCashback,
          netCostGs: bestNetCost,
          appliedCardName: bestCard,
        ),
      );

      combinedNet += bestNetCost;
    }

    final additionalSavings = bestSingle.netFinalCostGs - combinedNet;
    // Solo recomendamos compra dividida si hay más de 1 supermercado y el ahorro adicional es relevante (>= Gs. 10.000)
    final isRecommended = splitGroups.length > 1 && additionalSavings >= 10000;

    return SplitCartResult(
      bestSingleStore: bestSingle,
      splitGroups: splitGroups,
      combinedNetCostGs: combinedNet,
      additionalSavingsGs: additionalSavings > 0 ? additionalSavings : 0,
      isSplitRecommended: isRecommended,
    );
  }

  /// Detector de Ofertas Falsas e Historial de Precios:
  /// Identifica si el precio actual es mínimo histórico o si el supermercado
  /// infló el precio regular antes de aplicar el descuento.
  static PriceTrustAnalysis analyzePriceTrust({
    required StoreOffer offer,
    List<PriceHistoryPoint>? customHistory,
  }) {
    final now = DateTime.now();
    final effectiveCurrent = offer.gondolaBestPriceGs;

    final history = customHistory ?? [
      PriceHistoryPoint(
        date: now.subtract(const Duration(days: 30)),
        regularPriceGs: offer.regularPriceGs,
      ),
      PriceHistoryPoint(
        date: now.subtract(const Duration(days: 14)),
        regularPriceGs: offer.regularPriceGs,
      ),
      PriceHistoryPoint(
        date: now.subtract(const Duration(days: 3)),
        regularPriceGs: offer.regularPriceGs,
      ),
      PriceHistoryPoint(
        date: now,
        regularPriceGs: offer.regularPriceGs,
        promoPriceGs: offer.promoPriceGs,
      ),
    ];

    var minPrice = effectiveCurrent;
    var maxPrice = offer.regularPriceGs;
    var sum = 0;

    for (final p in history) {
      final eff = p.effectivePriceGs;
      if (eff < minPrice) minPrice = eff;
      if (p.regularPriceGs > maxPrice) maxPrice = p.regularPriceGs;
      sum += eff;
    }
    final avg30Days = (sum / history.length).round();

    PriceTrustLevel level;
    String badgeLabel;
    String explanation;

    final oldest = history.first;
    final isInflated = offer.promoPriceGs != null &&
        offer.regularPriceGs > (oldest.regularPriceGs * 1.12);

    if (isInflated) {
      level = PriceTrustLevel.suspiciousInflation;
      final inflPct = (((offer.regularPriceGs - oldest.regularPriceGs) / oldest.regularPriceGs) * 100).round();
      badgeLabel = 'OFERTA DUDOSA ⚠️';
      explanation = 'El supermercado infló el precio regular un $inflPct% antes de publicar la oferta.';
    } else if (offer.promoPriceGs != null && effectiveCurrent <= minPrice) {
      level = PriceTrustLevel.allTimeLow;
      badgeLabel = 'MÍNIMO HISTÓRICO 🟢';
      explanation = 'Este es el precio más bajo registrado en los últimos 30 días.';
    } else if (offer.promoPriceGs != null && offer.promoPriceGs! < offer.regularPriceGs) {
      level = PriceTrustLevel.fairDiscount;
      badgeLabel = 'OFERTA REAL 🔵';
      explanation = 'Descuento genuino sobre el precio promedio habitual.';
    } else {
      level = PriceTrustLevel.stable;
      badgeLabel = 'PRECIO ESTABLE ⚪';
      explanation = 'Precio habitual sin variaciones atípicas.';
    }

    return PriceTrustAnalysis(
      level: level,
      badgeLabel: badgeLabel,
      explanation: explanation,
      historicMinGs: minPrice,
      historicMaxGs: maxPrice,
      average30DaysGs: avg30Days,
      history: history,
    );
  }
}
