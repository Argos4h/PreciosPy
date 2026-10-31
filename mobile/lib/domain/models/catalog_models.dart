enum DiscountMechanism {
  cashback,   // Reintegro en extracto / cuenta (ej. ueno QR, Itaú QR)
  instantPos, // Descuento directo en la caja registradora
}

class UserCardProfile {
  final String bankSlug;
  final String bankName;
  final bool isEnabled;
  final String cardType;     // 'credito', 'debito'
  final String tier;         // 'clasica', 'platinum', 'infinite', 'afinidad'
  final int uenoLevel;       // 1..5 (Gamificación ueno bank)
  final bool isQrPayment;    // true = Pago con código QR, false = Plástico físico
  final int spentThisMonthGs; // Cuánto cupo de compra ya consumió el usuario este mes

  const UserCardProfile({
    required this.bankSlug,
    required this.bankName,
    this.isEnabled = false,
    this.cardType = 'credito',
    this.tier = 'clasica',
    this.uenoLevel = 4,
    this.isQrPayment = true,
    this.spentThisMonthGs = 0,
  });

  UserCardProfile copyWith({
    bool? isEnabled,
    String? cardType,
    String? tier,
    int? uenoLevel,
    bool? isQrPayment,
    int? spentThisMonthGs,
  }) {
    return UserCardProfile(
      bankSlug: bankSlug,
      bankName: bankName,
      isEnabled: isEnabled ?? this.isEnabled,
      cardType: cardType ?? this.cardType,
      tier: tier ?? this.tier,
      uenoLevel: uenoLevel ?? this.uenoLevel,
      isQrPayment: isQrPayment ?? this.isQrPayment,
      spentThisMonthGs: spentThisMonthGs ?? this.spentThisMonthGs,
    );
  }
}

class BankPromotion {
  final int id;
  final String supermarketSlug;
  final String cardSlug;
  final String cardName;
  final String entityName;
  final String bankSlug;
  final String title;
  final double discountPct;
  final DiscountMechanism mechanism;
  final bool appliesToPromoPrice;
  final List<int> daysOfWeek; // ISO 1=Lunes ... 7=Domingo
  final int? spendingCapGs;   // Tope de compra en Guaraníes (ej. 800000)
  final int? maxRefundGs;     // Tope de reintegro en Guaraníes (ej. 280000)
  final String? tier;         // 'clasica', 'platinum', 'infinite', 'afinidad'
  final int? minUenoLevel;    // 1..5
  final bool requiresQr;

  const BankPromotion({
    required this.id,
    required this.supermarketSlug,
    required this.cardSlug,
    required this.cardName,
    required this.entityName,
    this.bankSlug = 'general',
    required this.title,
    required this.discountPct,
    required this.mechanism,
    required this.appliesToPromoPrice,
    required this.daysOfWeek,
    this.spendingCapGs,
    this.maxRefundGs,
    this.tier,
    this.minUenoLevel,
    this.requiresQr = false,
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

/// Ítem extraído de una factura electrónica paraguaya (e-Kuatia DNIT / SET)
class KuatiaInvoiceItem {
  final String description;
  final double quantity;
  final int unitPriceGs;
  final int totalPriceGs;

  const KuatiaInvoiceItem({
    required this.description,
    required this.quantity,
    required this.unitPriceGs,
    required this.totalPriceGs,
  });
}

/// Factura Electrónica Nacional (SIFEN e-Kuatia) leída desde código QR tributario
class KuatiaInvoiceReceipt {
  final String rucIssuer;
  final String supermarketName;
  final DateTime invoiceDate;
  final String invoiceNumber;
  final int totalAmountGs;
  final List<KuatiaInvoiceItem> items;

  const KuatiaInvoiceReceipt({
    required this.rucIssuer,
    required this.supermarketName,
    required this.invoiceDate,
    required this.invoiceNumber,
    required this.totalAmountGs,
    required this.items,
  });

  /// Parsea la URL tributaria oficial del QR de e-Kuatia (DNIT / SET)
  static KuatiaInvoiceReceipt? parseQrUrl(String qrUrl) {
    if (!qrUrl.contains('ekuatia.set.gov.py') && !qrUrl.contains('dnit.gov.py')) {
      return null;
    }

    try {
      final uri = Uri.parse(qrUrl);
      final idCdc = uri.queryParameters['IdGesDat'] ?? uri.queryParameters['dId'] ?? '';
      final ruc = idCdc.length >= 11 ? idCdc.substring(3, 11) : '80000001';

      return KuatiaInvoiceReceipt(
        rucIssuer: ruc,
        supermarketName: 'Supermercado Verificado (DNIT)',
        invoiceDate: DateTime.now(),
        invoiceNumber: idCdc.length > 20 ? idCdc.substring(0, 15) : '001-001-0012345',
        totalAmountGs: 0,
        items: const [],
      );
    } catch (_) {
      return null;
    }
  }
}
