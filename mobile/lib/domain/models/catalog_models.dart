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

  Map<String, dynamic> toJson() => {
    'bankSlug': bankSlug,
    'bankName': bankName,
    'isEnabled': isEnabled,
    'cardType': cardType,
    'tier': tier,
    'uenoLevel': uenoLevel,
    'isQrPayment': isQrPayment,
    'spentThisMonthGs': spentThisMonthGs,
  };

  factory UserCardProfile.fromJson(Map<String, dynamic> json) => UserCardProfile(
    bankSlug: json['bankSlug'] as String? ?? '',
    bankName: json['bankName'] as String? ?? '',
    isEnabled: json['isEnabled'] as bool? ?? false,
    cardType: json['cardType'] as String? ?? 'credito',
    tier: json['tier'] as String? ?? 'clasica',
    uenoLevel: json['uenoLevel'] as int? ?? 4,
    isQrPayment: json['isQrPayment'] as bool? ?? true,
    spentThisMonthGs: json['spentThisMonthGs'] as int? ?? 0,
  );
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

/// Sucursal física de un supermercado en una ciudad de Paraguay
class SupermarketBranch {
  final int id;
  final String supermarketSlug;
  final String supermarketName;
  final String branchName;
  final String city;
  final String department;
  final double latitude;
  final double longitude;
  final String address;

  const SupermarketBranch({
    required this.id,
    required this.supermarketSlug,
    required this.supermarketName,
    required this.branchName,
    required this.city,
    required this.department,
    required this.latitude,
    required this.longitude,
    required this.address,
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

  /// Parsea la URL tributaria oficial del QR de e-Kuatia (DNIT / SET) o el CDC directo de 44 dígitos
  static KuatiaInvoiceReceipt? parseQrUrl(String input) {
    final raw = input.trim();
    final lower = raw.toLowerCase();

    // Detección de URL oficial SIFEN (ekuatia.set.gov.py o dnit.gov.py) o formato de parámetros QR
    final isUrl = lower.contains('ekuatia') ||
        lower.contains('dnit.gov.py') ||
        lower.contains('set.gov.py') ||
        lower.contains('sifen') ||
        lower.contains('chashqr') ||
        lower.contains('idgesdat=') ||
        (lower.contains('id=') && lower.contains('nversion='));

    // O detección directa de un CDC numérico de 44 dígitos
    final isDirectCdc = RegExp(r'^\d{44}$').hasMatch(raw);

    if (!isUrl && !isDirectCdc) {
      return null;
    }

    try {
      String cdc = '';
      int totalGs = 0;

      if (isDirectCdc) {
        cdc = raw;
      } else {
        // Intentar parsear como URI
        Uri? uri;
        try {
          uri = Uri.parse(raw);
        } catch (_) {}

        final params = uri != null && uri.queryParameters.isNotEmpty
            ? uri.queryParameters
            : _parseQueryParamsManually(raw);

        // En el estándar SIFEN DNIT, el parámetro puede ser 'Id', 'IdGesDat', o 'dId'
        cdc = params['Id'] ?? params['id'] ?? params['IdGesDat'] ?? params['dId'] ?? '';

        // Si no vino en query params, buscar con regex 44 dígitos consecutivos
        if (cdc.length != 44) {
          final cdcMatch = RegExp(r'(\d{44})').firstMatch(raw);
          if (cdcMatch != null) {
            cdc = cdcMatch.group(1)!;
          }
        }

        // Total general del comprobante: dTotGralOpe
        final totalStr = params['dTotGralOpe'] ?? params['tot'] ?? params['total'] ?? '';
        if (totalStr.isNotEmpty) {
          totalGs = (double.tryParse(totalStr) ?? int.tryParse(totalStr) ?? 0).round();
        }
      }

      // Estructura oficial del CDC de 44 dígitos:
      // Pos 1-2: Tipo doc (01=Factura Electrónica)
      // Pos 3-10: RUC emisor (8 dígitos rellenos con 0)
      // Pos 11: DV emisor (1 dígito)
      // Pos 12-14: Establecimiento (3 dígitos)
      // Pos 15-17: Punto expedición (3 dígitos)
      // Pos 18-24: Número de documento (7 dígitos)
      // Pos 25: Tipo contribuyente (1 o 2)
      // Pos 26-33: Fecha AAAAMMDD (8 dígitos)
      String rucClean = '80000001-1';
      String docNum = '001-001-0001234';
      DateTime date = DateTime.now();
      String superName = 'Supermercado Verificado (DNIT)';

      if (cdc.length == 44) {
        final rucRaw = cdc.substring(2, 10).replaceFirst(RegExp(r'^0+'), '');
        final dvRaw = cdc.substring(10, 11);
        rucClean = '$rucRaw-$dvRaw';

        final est = cdc.substring(11, 14);
        final pexp = cdc.substring(14, 17);
        final num = cdc.substring(17, 24);
        docNum = '$est-$pexp-$num';

        final dateStr = cdc.substring(25, 33); // AAAAMMDD
        if (dateStr.length == 8) {
          final y = int.tryParse(dateStr.substring(0, 4));
          final m = int.tryParse(dateStr.substring(4, 6));
          final d = int.tryParse(dateStr.substring(6, 8));
          if (y != null && m != null && d != null) {
            date = DateTime(y, m, d);
          }
        }

        // Mapeo inteligente de RUC de cadenas paraguayas
        if (rucClean.startsWith('80017124') || rucClean.startsWith('80002166')) {
          superName = 'Supermercados Stock / Superseis';
        } else if (rucClean.startsWith('80097787') || rucClean.startsWith('80076755')) {
          superName = 'Biggie Express';
        } else if (rucClean.startsWith('80016027')) {
          superName = 'Fortis Mayorista';
        } else if (rucClean.startsWith('80003006')) {
          superName = 'Casa Grütter';
        } else if (rucClean.startsWith('80000014')) {
          superName = 'Supermercado Los Jardines';
        }
      }

      return KuatiaInvoiceReceipt(
        rucIssuer: rucClean,
        supermarketName: superName,
        invoiceDate: date,
        invoiceNumber: docNum,
        totalAmountGs: totalGs,
        items: const [],
      );
    } catch (_) {
      return null;
    }
  }

  static Map<String, String> _parseQueryParamsManually(String raw) {
    final result = <String, String>{};
    final qIndex = raw.indexOf('?');
    if (qIndex == -1 || qIndex == raw.length - 1) return result;
    final query = raw.substring(qIndex + 1);
    final pairs = query.split('&');
    for (final pair in pairs) {
      final parts = pair.split('=');
      if (parts.length == 2) {
        result[parts[0]] = Uri.decodeQueryComponent(parts[1]);
      }
    }
    return result;
  }
}
