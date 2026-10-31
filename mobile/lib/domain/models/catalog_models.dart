enum DiscountMechanism {
  cashback,   // Reintegro en extracto / cuenta (ej. ueno QR, Itaú QR)
  instantPos, // Descuento directo en la caja registradora
}

class BankPromotion {
  final int id;
  final String supermarketSlug;
  final String cardSlug;
  final String cardName;
  final String entityName;
  final String title;
  final double discountPct;
  final DiscountMechanism mechanism;
  final bool appliesToPromoPrice;
  final List<int> daysOfWeek; // ISO 1=Lunes ... 7=Domingo
  final int? spendingCapGs;   // Tope de compra en Guaraníes (ej. 800000)
  final int? maxRefundGs;     // Tope de reintegro en Guaraníes (ej. 280000)

  const BankPromotion({
    required this.id,
    required this.supermarketSlug,
    required this.cardSlug,
    required this.cardName,
    required this.entityName,
    required this.title,
    required this.discountPct,
    required this.mechanism,
    required this.appliesToPromoPrice,
    required this.daysOfWeek,
    this.spendingCapGs,
    this.maxRefundGs,
  });

  bool isValidOnWeekday(int isoWeekday) => daysOfWeek.contains(isoWeekday);
}

class StoreOffer {
  final String supermarketSlug;
  final String supermarketName;
  final int regularPriceGs;
  final int? promoPriceGs;
  final int? wholesalePriceGs;
  final int? wholesaleMinQty;
  final bool inStock;

  const StoreOffer({
    required this.supermarketSlug,
    required this.supermarketName,
    required this.regularPriceGs,
    this.promoPriceGs,
    this.wholesalePriceGs,
    this.wholesaleMinQty,
    this.inStock = true,
  });

  int get gondolaBestPriceGs =>
      (promoPriceGs != null && promoPriceGs! > 0 && promoPriceGs! < regularPriceGs)
          ? promoPriceGs!
          : regularPriceGs;
}

class ProductItem {
  final int id;
  final String? ean;
  final String normalizedName;
  final String? brand;
  final String unitMeasure; // 'GR', 'KG', 'ML', 'LT', 'UN'
  final double unitQuantity;
  final String baseUnit;    // 'KG', 'LT', 'UN'
  final double baseMultiplier;
  final String? imageUrl;
  final String? category;
  final List<StoreOffer> offers;

  const ProductItem({
    required this.id,
    this.ean,
    required this.normalizedName,
    this.brand,
    required this.unitMeasure,
    required this.unitQuantity,
    required this.baseUnit,
    required this.baseMultiplier,
    this.imageUrl,
    this.category,
    required this.offers,
  });
}

class EvaluatedOffer {
  final StoreOffer offer;
  final int effectiveFinalPriceGs;
  final int cashOutflowAtPosGs;
  final int cashbackAmountGs;
  final int pricePerBaseUnitGs;
  final String baseUnit;
  final BankPromotion? appliedPromotion;
  final String pricingNote;

  const EvaluatedOffer({
    required this.offer,
    required this.effectiveFinalPriceGs,
    required this.cashOutflowAtPosGs,
    required this.cashbackAmountGs,
    required this.pricePerBaseUnitGs,
    required this.baseUnit,
    this.appliedPromotion,
    required this.pricingNote,
  });

  int get totalSavingsGs => offer.regularPriceGs - effectiveFinalPriceGs;

  int get savingsPercentage => offer.regularPriceGs > 0
      ? ((totalSavingsGs / offer.regularPriceGs) * 100).round()
      : 0;
}

class SmartCartSummary {
  final String supermarketSlug;
  final String supermarketName;
  final int totalRegularGs;
  final int totalGondolaGs;
  final int totalCashAtPosGs;
  final int totalCashbackGs;
  final int netFinalCostGs;
  final String? appliedCardName;
  final bool capReached;
  final int missingProductsCount;

  const SmartCartSummary({
    required this.supermarketSlug,
    required this.supermarketName,
    required this.totalRegularGs,
    required this.totalGondolaGs,
    required this.totalCashAtPosGs,
    required this.totalCashbackGs,
    required this.netFinalCostGs,
    this.appliedCardName,
    required this.capReached,
    required this.missingProductsCount,
  });
}

class SplitCartStoreGroup {
  final String supermarketSlug;
  final String supermarketName;
  final List<MapEntry<ProductItem, int>> items;
  final int totalCashAtPosGs;
  final int totalCashbackGs;
  final int netCostGs;
  final String? appliedCardName;

  const SplitCartStoreGroup({
    required this.supermarketSlug,
    required this.supermarketName,
    required this.items,
    required this.totalCashAtPosGs,
    required this.totalCashbackGs,
    required this.netCostGs,
    this.appliedCardName,
  });
}

class SplitCartResult {
  final SmartCartSummary bestSingleStore;
  final List<SplitCartStoreGroup> splitGroups;
  final int combinedNetCostGs;
  final int additionalSavingsGs;
  final bool isSplitRecommended;

  const SplitCartResult({
    required this.bestSingleStore,
    required this.splitGroups,
    required this.combinedNetCostGs,
    required this.additionalSavingsGs,
    required this.isSplitRecommended,
  });
}

class PriceHistoryPoint {
  final DateTime date;
  final int regularPriceGs;
  final int? promoPriceGs;

  const PriceHistoryPoint({
    required this.date,
    required this.regularPriceGs,
    this.promoPriceGs,
  });

  int get effectivePriceGs =>
      (promoPriceGs != null && promoPriceGs! > 0 && promoPriceGs! < regularPriceGs)
          ? promoPriceGs!
          : regularPriceGs;
}

enum PriceTrustLevel {
  allTimeLow,          // 🟢 Mínimo histórico (precio más bajo en 60 días)
  suspiciousInflation, // ⚠️ Oferta dudosa (subieron el regular antes de ofertar)
  fairDiscount,        // 🔵 Oferta real / descuento genuino
  stable,              // ⚪ Precio habitual estable
}

class PriceTrustAnalysis {
  final PriceTrustLevel level;
  final String badgeLabel;
  final String explanation;
  final int historicMinGs;
  final int historicMaxGs;
  final int average30DaysGs;
  final List<PriceHistoryPoint> history;

  const PriceTrustAnalysis({
    required this.level,
    required this.badgeLabel,
    required this.explanation,
    required this.historicMinGs,
    required this.historicMaxGs,
    required this.average30DaysGs,
    required this.history,
  });
}
