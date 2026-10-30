import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';

class ProductDetailSheet extends ConsumerWidget {
  final ProductItem product;
  final List<EvaluatedOffer> rankedOffers;

  const ProductDetailSheet({
    super.key,
    required this.product,
    required this.rankedOffers,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    if (rankedOffers.isEmpty) {
      return const SizedBox(height: 200, child: Center(child: Text('Sin ofertas disponibles.')));
    }

    final best = rankedOffers.first;
    final trustAnalysis = PromoCalculator.analyzePriceTrust(offer: best.offer);

    Color badgeColor;
    Color badgeBg;
    IconData badgeIcon;

    switch (trustAnalysis.level) {
      case PriceTrustLevel.allTimeLow:
        badgeColor = const Color(0xFF3FB950);
        badgeBg = const Color(0x3300875A);
        badgeIcon = Icons.stars_rounded;
      case PriceTrustLevel.suspiciousInflation:
        badgeColor = Colors.amberAccent;
        badgeBg = const Color(0x33FFC107);
        badgeIcon = Icons.warning_rounded;
      case PriceTrustLevel.fairDiscount:
        badgeColor = Colors.lightBlueAccent;
        badgeBg = const Color(0x330288D1);
        badgeIcon = Icons.verified_rounded;
      case PriceTrustLevel.stable:
        badgeColor = Colors.white70;
        badgeBg = const Color(0xFF21262D);
        badgeIcon = Icons.info_outline_rounded;
    }

    return Container(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
      decoration: const BoxDecoration(
        color: Color(0xFF161B22),
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: ListView(
        shrinkWrap: true,
        children: [
          Center(
            child: Container(
              width: 44,
              height: 4,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: const Color(0xFF30363D),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      product.normalizedName,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Código EAN: ${product.ean ?? "Sin código"} • Marca: ${product.brand ?? "Genérica"}',
                      style: const TextStyle(fontSize: 12, color: Colors.white60),
                    ),
                  ],
                ),
              ),
              IconButton.filledTonal(
                onPressed: () {
                  ref.read(smartCartProvider.notifier).addOrIncrement(product);
                  Navigator.pop(context);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('${product.normalizedName} agregado al Carrito PY'),
                      duration: const Duration(milliseconds: 900),
                    ),
                  );
                },
                icon: const Icon(Icons.add_shopping_cart_rounded),
                tooltip: 'Agregar al Carrito',
              ),
            ],
          ),
          const SizedBox(height: 16),

          // 1. BANNER: Detector de Ofertas Falsas & Mínimo Histórico
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: badgeBg,
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: badgeColor),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(badgeIcon, color: badgeColor, size: 26),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        trustAnalysis.badgeLabel,
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w900,
                          color: badgeColor,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        trustAnalysis.explanation,
                        style: const TextStyle(fontSize: 12, color: Colors.white),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // 2. Historial de Precios (Visual Timeline)
          const Text(
            'Evolución del Precio (Últimos 30 días)',
            style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 8),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: trustAnalysis.history.map((point) {
                final daysAgo = DateTime.now().difference(point.date).inDays;
                final label = daysAgo == 0 ? 'Hoy' : 'Hace ${daysAgo}d';
                return Container(
                  margin: const EdgeInsets.only(right: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFF0D1117),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF30363D)),
                  ),
                  child: Column(
                    children: [
                      Text(label, style: const TextStyle(fontSize: 11, color: Colors.white60)),
                      const SizedBox(height: 4),
                      Text(
                        GuaraniFormatter.format(point.effectivePriceGs),
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w800),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),

          // 3. Comparativa en Vivo en Góndolas
          const Text(
            'Precios Actuales por Supermercado',
            style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 8),
          ...rankedOffers.map((eval) {
            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              decoration: BoxDecoration(
                color: const Color(0xFF0D1117),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFF30363D)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          eval.offer.supermarketName,
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                        Text(
                          eval.pricingNote,
                          style: const TextStyle(fontSize: 11, color: Colors.white70),
                        ),
                      ],
                    ),
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        GuaraniFormatter.format(eval.effectiveFinalPriceGs),
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w800,
                          color: Color(0xFF3FB950),
                        ),
                      ),
                      if (eval.effectiveFinalPriceGs < eval.offer.regularPriceGs)
                        Text(
                          GuaraniFormatter.format(eval.offer.regularPriceGs),
                          style: const TextStyle(
                            fontSize: 11,
                            color: Colors.white54,
                            decoration: TextDecoration.lineThrough,
                          ),
                        ),
                    ],
                  ),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }
}
