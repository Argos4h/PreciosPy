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

    final isDark = Theme.of(context).brightness == Brightness.dark;
    final best = rankedOffers.first;
    final trustAnalysis = PromoCalculator.analyzePriceTrust(offer: best.offer);

    Color badgeColor;
    Color badgeBg;
    IconData badgeIcon;

    switch (trustAnalysis.level) {
      case PriceTrustLevel.allTimeLow:
        badgeColor = const Color(0xFF10B981);
        badgeBg = isDark ? const Color(0x2610B981) : const Color(0xFFD1FAE5);
        badgeIcon = Icons.stars_rounded;
      case PriceTrustLevel.suspiciousInflation:
        badgeColor = const Color(0xFFF59E0B);
        badgeBg = isDark ? const Color(0x26F59E0B) : const Color(0xFFFEF3C7);
        badgeIcon = Icons.warning_rounded;
      case PriceTrustLevel.fairDiscount:
        badgeColor = const Color(0xFF0284C7);
        badgeBg = isDark ? const Color(0x260284C7) : const Color(0xFFE0F2FE);
        badgeIcon = Icons.verified_rounded;
      case PriceTrustLevel.stable:
        badgeColor = isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B);
        badgeBg = isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9);
        badgeIcon = Icons.info_outline_rounded;
    }

    final sheetBg = isDark ? const Color(0xFF1E293B) : Colors.white;
    final cardBg = isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC);
    final cardBorder = isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0);

    return Container(
      padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
      decoration: BoxDecoration(
        color: sheetBg,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
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
                color: isDark ? const Color(0xFF475569) : const Color(0xFFCBD5E1),
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
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w800,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Código EAN: ${product.ean ?? "Sin código"} • Marca: ${product.brand ?? "Genérica"}',
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
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
                      backgroundColor: const Color(0xFF10B981),
                      behavior: SnackBarBehavior.floating,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      content: Text(
                        '${product.normalizedName} agregado a tu lista',
                        style: const TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                      ),
                      duration: const Duration(milliseconds: 900),
                    ),
                  );
                },
                style: IconButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981).withValues(alpha: 0.15),
                  foregroundColor: const Color(0xFF10B981),
                ),
                icon: const Icon(Icons.add_shopping_cart_rounded),
                tooltip: 'Agregar a Mi Lista',
              ),
            ],
          ),
          const SizedBox(height: 16),

          // 1. BANNER: Detector de Ofertas Falsas & Mínimo Histórico
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: badgeBg,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: badgeColor.withValues(alpha: 0.5)),
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
                        style: TextStyle(
                          fontSize: 12,
                          color: isDark ? const Color(0xFFE2E8F0) : const Color(0xFF334155),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // 2. Historial y Gráfico de Precios (Visual 30 días)
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Evolución del Precio (Últimos 30 días)',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                ),
              ),
              if (trustAnalysis.history.length >= 2) ...[
                Builder(
                  builder: (_) {
                    final firstPrice = trustAnalysis.history.first.effectivePriceGs;
                    final currentPrice = trustAnalysis.history.last.effectivePriceGs;
                    final diffPct = ((currentPrice - firstPrice) / firstPrice * 100).round();
                    final isCheaper = diffPct < 0;
                    final isMoreExpensive = diffPct > 0;

                    return Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: isCheaper
                            ? const Color(0xFF10B981).withValues(alpha: 0.15)
                            : (isMoreExpensive
                                ? const Color(0xFFEF4444).withValues(alpha: 0.15)
                                : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0))),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        isCheaper
                            ? '📉 $diffPct% vs hace 15d'
                            : (isMoreExpensive ? '📈 +$diffPct%' : '📊 Estable'),
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w800,
                          color: isCheaper
                              ? const Color(0xFF10B981)
                              : (isMoreExpensive
                                  ? const Color(0xFFEF4444)
                                  : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF475569))),
                        ),
                      ),
                    );
                  },
                ),
              ],
            ],
          ),
          const SizedBox(height: 10),
          // Gráfico de Área/Líneas estilizado
          Container(
            height: 110,
            padding: const EdgeInsets.fromLTRB(12, 16, 12, 10),
            decoration: BoxDecoration(
              color: cardBg,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: cardBorder),
            ),
            child: CustomPaint(
              size: const Size(double.infinity, 80),
              painter: _PriceTrendChartPainter(
                points: trustAnalysis.history.map((p) => p.effectivePriceGs.toDouble()).toList(),
                labels: trustAnalysis.history.map((p) {
                  final days = DateTime.now().difference(p.date).inDays;
                  return days == 0 ? 'Hoy' : '-${days}d';
                }).toList(),
                isDark: isDark,
              ),
            ),
          ),
          const SizedBox(height: 10),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: trustAnalysis.history.map((point) {
                final daysAgo = DateTime.now().difference(point.date).inDays;
                final label = daysAgo == 0 ? 'Hoy' : 'Hace ${daysAgo}d';
                return Container(
                  margin: const EdgeInsets.only(right: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: cardBg,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: cardBorder),
                  ),
                  child: Column(
                    children: [
                      Text(
                        label,
                        style: TextStyle(
                          fontSize: 11,
                          color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        GuaraniFormatter.format(point.effectivePriceGs),
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w800,
                          color: isDark ? Colors.white : const Color(0xFF0F172A),
                        ),
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ),
          const SizedBox(height: 16),

          // 3. Comparativa en Vivo en Góndolas
          Text(
            'Precios Actuales por Supermercado',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w700,
              color: isDark ? Colors.white : const Color(0xFF0F172A),
            ),
          ),
          const SizedBox(height: 8),
          ...rankedOffers.map((eval) {
            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
              decoration: BoxDecoration(
                color: cardBg,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: cardBorder),
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
                          style: TextStyle(
                            fontWeight: FontWeight.w700,
                            fontSize: 13,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          eval.pricingNote,
                          style: TextStyle(
                            fontSize: 11,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
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
                          color: Color(0xFF10B981),
                        ),
                      ),
                      if (eval.effectiveFinalPriceGs < eval.offer.regularPriceGs)
                        Text(
                          GuaraniFormatter.format(eval.offer.regularPriceGs),
                          style: TextStyle(
                            fontSize: 11,
                            color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8),
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

class _PriceTrendChartPainter extends CustomPainter {
  final List<double> points;
  final List<String> labels;
  final bool isDark;

  _PriceTrendChartPainter({
    required this.points,
    required this.labels,
    required this.isDark,
  });

  @override
  void paint(Canvas canvas, Size size) {
    if (points.isEmpty) return;

    final minPrice = points.reduce((a, b) => a < b ? a : b);
    final maxPrice = points.reduce((a, b) => a > b ? a : b);
    final range = (maxPrice - minPrice) == 0 ? 1.0 : (maxPrice - minPrice);

    final linePaint = Paint()
      ..color = const Color(0xFF10B981)
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;

    final dotPaint = Paint()
      ..color = const Color(0xFF10B981)
      ..style = PaintingStyle.fill;

    final dotInnerPaint = Paint()
      ..color = isDark ? const Color(0xFF0F172A) : Colors.white
      ..style = PaintingStyle.fill;

    final fillPaint = Paint()
      ..shader = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          const Color(0xFF10B981).withValues(alpha: 0.35),
          const Color(0xFF10B981).withValues(alpha: 0.0),
        ],
      ).createShader(Rect.fromLTWH(0, 0, size.width, size.height))
      ..style = PaintingStyle.fill;

    final stepX = points.length > 1 ? size.width / (points.length - 1) : size.width;
    final path = Path();
    final fillPath = Path();

    final List<Offset> offsets = [];
    for (int i = 0; i < points.length; i++) {
      final x = points.length > 1 ? i * stepX : size.width / 2;
      final norm = (points[i] - minPrice) / range;
      final y = size.height - 14 - (norm * (size.height - 28));
      offsets.add(Offset(x, y));

      if (i == 0) {
        path.moveTo(x, y);
        fillPath.moveTo(x, size.height);
        fillPath.lineTo(x, y);
      } else {
        path.lineTo(x, y);
        fillPath.lineTo(x, y);
      }
    }

    if (offsets.isNotEmpty) {
      fillPath.lineTo(offsets.last.dx, size.height);
      fillPath.close();
      canvas.drawPath(fillPath, fillPaint);
      canvas.drawPath(path, linePaint);

      for (final off in offsets) {
        canvas.drawCircle(off, 4.5, dotPaint);
        canvas.drawCircle(off, 2.5, dotInnerPaint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant _PriceTrendChartPainter oldDelegate) {
    return oldDelegate.points != points || oldDelegate.isDark != isDark;
  }
}
