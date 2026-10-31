import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';
import 'product_detail_sheet.dart';

class SearchScreen extends ConsumerWidget {
  const SearchScreen({super.key});

  static const Map<int, String> _weekdayLabels = {
    1: 'Lun',
    2: 'Mar',
    3: 'Mié',
    4: 'Jue',
    5: 'Vie',
    6: 'Sáb',
    7: 'Dom',
  };

  static const List<MapEntry<String, String>> _quickCategories = [
    MapEntry('', 'Todos'),
    MapEntry('yerba', '🌿 Yerba'),
    MapEntry('leche', '🥛 Lácteos'),
    MapEntry('cerveza', '🍺 Cerveza'),
    MapEntry('coca', '🥤 Gaseosas'),
    MapEntry('carne', '🥩 Carne'),
    MapEntry('pan', '🥖 Panadería'),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final products = ref.watch(filteredProductsProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final selectedWeekday = ref.watch(selectedWeekdayProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final themeMode = ref.watch(themeModeProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return SafeArea(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: const Color(0xFF10B981).withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Icon(Icons.shopping_bag_rounded, color: Color(0xFF10B981), size: 22),
                        ),
                        const SizedBox(width: 10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'PreciosPy',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            Text(
                              'Comparador en Paraguay',
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w500,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: const Color(0xFF10B981).withValues(alpha: 0.12),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(Icons.credit_card_rounded, size: 14, color: Color(0xFF10B981)),
                              const SizedBox(width: 4),
                              Text(
                                '${wallet.length} tarjetas',
                                style: const TextStyle(
                                  fontSize: 11,
                                  color: Color(0xFF10B981),
                                  fontWeight: FontWeight.w700,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 6),
                        IconButton(
                          tooltip: isDark ? 'Cambiar a Modo Claro' : 'Cambiar a Modo Oscuro',
                          icon: Icon(
                            isDark ? Icons.light_mode_rounded : Icons.dark_mode_rounded,
                            color: isDark ? Colors.amber : const Color(0xFF475569),
                          ),
                          onPressed: () {
                            ref.read(themeModeProvider.notifier).state =
                                themeMode == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
                          },
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                TextField(
                  onChanged: (value) => ref.read(searchQueryProvider.notifier).state = value,
                  decoration: InputDecoration(
                    hintText: 'Buscar yerba, leche trébol, cerveza o EAN...',
                    prefixIcon: const Icon(Icons.search_rounded, color: Color(0xFF10B981)),
                    suffixIcon: ref.watch(searchQueryProvider).isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear_rounded, size: 18),
                            onPressed: () => ref.read(searchQueryProvider.notifier).state = '',
                          )
                        : null,
                  ),
                ),
                const SizedBox(height: 10),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _weekdayLabels.entries.map((entry) {
                      final isSelected = entry.key == selectedWeekday;
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: ChoiceChip(
                          label: Text(entry.value),
                          selected: isSelected,
                          onSelected: (_) =>
                              ref.read(selectedWeekdayProvider.notifier).state = entry.key,
                        ),
                      );
                    }).toList(),
                  ),
                ),
                const SizedBox(height: 8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _quickCategories.map((cat) {
                      final currentQuery = ref.watch(searchQueryProvider);
                      final isSelected = currentQuery == cat.key;
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: FilterChip(
                          label: Text(cat.value),
                          selected: isSelected,
                          onSelected: (_) {
                            ref.read(searchQueryProvider.notifier).state = cat.key;
                          },
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: products.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.search_off_rounded,
                          size: 48,
                          color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'No encontramos productos con esa búsqueda',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    itemCount: products.length,
                    itemBuilder: (context, index) {
                      final product = products[index];
                      final rankedOffers = PromoCalculator.rankProductOffers(
                        product: product,
                        allPromotions: promotions,
                        userCardSlugs: wallet,
                        isoWeekday: selectedWeekday,
                      );
                      return _ProductComparisonCard(
                        product: product,
                        rankedOffers: rankedOffers,
                        onAddToCart: () {
                          ref.read(smartCartProvider.notifier).addOrIncrement(product);
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
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class _ProductComparisonCard extends StatelessWidget {
  final ProductItem product;
  final List<EvaluatedOffer> rankedOffers;
  final VoidCallback onAddToCart;

  const _ProductComparisonCard({
    required this.product,
    required this.rankedOffers,
    required this.onAddToCart,
  });

  Widget _buildCategoryThumbnail(BuildContext context, String? category) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cat = category ?? '🛒 Almacén';
    String emoji = '🛒';
    if (cat.contains('Yerba')) emoji = '🌿';
    if (cat.contains('Lácteos')) emoji = '🥛';
    if (cat.contains('Cerveza')) emoji = '🍺';
    if (cat.contains('Bebidas')) emoji = '🥤';
    if (cat.contains('Carne')) emoji = '🥩';
    if (cat.contains('Pan')) emoji = '🥖';

    return Container(
      width: 54,
      height: 54,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF334155) : const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Center(
        child: Text(emoji, style: const TextStyle(fontSize: 26)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (rankedOffers.isEmpty) return const SizedBox.shrink();
    final best = rankedOffers.first;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () {
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (_) => ProductDetailSheet(
              product: product,
              rankedOffers: rankedOffers,
            ),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Imagen / Thumbnail del Producto
                  ClipRRect(
                    borderRadius: BorderRadius.circular(14),
                    child: (product.imageUrl != null && product.imageUrl!.isNotEmpty)
                        ? Image.network(
                            product.imageUrl!,
                            width: 54,
                            height: 54,
                            fit: BoxFit.cover,
                            errorBuilder: (ctx, _, __) => _buildCategoryThumbnail(context, product.category),
                          )
                        : _buildCategoryThumbnail(context, product.category),
                  ),
                  const SizedBox(width: 12),
                  // Nombre y Detalles
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          product.normalizedName,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w700,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            if (product.category != null) ...[
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(
                                  product.category!,
                                  style: TextStyle(
                                    fontSize: 10,
                                    fontWeight: FontWeight.w600,
                                    color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 6),
                            ],
                            Expanded(
                              child: Text(
                                GuaraniFormatter.formatPerBaseUnit(best.pricePerBaseUnitGs, best.baseUnit),
                                style: TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w500,
                                  color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 6),
                  IconButton.filledTonal(
                    onPressed: onAddToCart,
                    style: IconButton.styleFrom(
                      backgroundColor: const Color(0xFF10B981).withValues(alpha: 0.15),
                      foregroundColor: const Color(0xFF10B981),
                    ),
                    icon: const Icon(Icons.add_shopping_cart_rounded, size: 20),
                    tooltip: 'Agregar a Mi Lista',
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Divider(
                height: 1,
                color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
              ),
              const SizedBox(height: 10),

              // Lista de ofertas por supermercado
              ...rankedOffers.asMap().entries.map((entry) {
                final idx = entry.key;
                final eval = entry.value;
                final isBest = idx == 0;

                final tileBg = isBest
                    ? (isDark ? const Color(0x2610B981) : const Color(0xFFECFDF5))
                    : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC));

                final tileBorder = isBest
                    ? const Color(0xFF10B981)
                    : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0));

                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
                  decoration: BoxDecoration(
                    color: tileBg,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: tileBorder),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Text(
                                  eval.offer.supermarketName,
                                  style: TextStyle(
                                    fontWeight: FontWeight.w700,
                                    fontSize: 13,
                                    color: isBest
                                        ? const Color(0xFF10B981)
                                        : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                  ),
                                ),
                                if (isBest) ...[
                                  const SizedBox(width: 6),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                    decoration: BoxDecoration(
                                      color: const Color(0xFF10B981),
                                      borderRadius: BorderRadius.circular(6),
                                    ),
                                    child: const Text(
                                      'MÁS BARATO',
                                      style: TextStyle(
                                        fontSize: 9,
                                        fontWeight: FontWeight.w900,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ),
                                ],
                              ],
                            ),
                            const SizedBox(height: 2),
                            Text(
                              eval.pricingNote,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 11,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                              ),
                            ),
                            if (eval.offer.wholesalePriceGs != null && eval.offer.wholesaleMinQty != null) ...[
                              const SizedBox(height: 3),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: const Color(0xFFF59E0B).withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(6),
                                  border: Border.all(color: const Color(0xFFF59E0B).withValues(alpha: 0.3)),
                                ),
                                child: Text(
                                  '📦 ${GuaraniFormatter.format(eval.offer.wholesalePriceGs!)} llevando ${eval.offer.wholesaleMinQty}+ un.',
                                  style: const TextStyle(
                                    fontSize: 9,
                                    fontWeight: FontWeight.w800,
                                    color: Color(0xFFF59E0B),
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            GuaraniFormatter.format(eval.effectiveFinalPriceGs),
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w800,
                              color: isBest
                                  ? const Color(0xFF10B981)
                                  : (isDark ? Colors.white : const Color(0xFF0F172A)),
                            ),
                          ),
                          if (eval.effectiveFinalPriceGs < eval.offer.regularPriceGs)
                            Text(
                              'Góndola: ${GuaraniFormatter.format(eval.offer.regularPriceGs)}',
                              style: TextStyle(
                                fontSize: 10,
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
        ),
      ),
    );
  }
}
