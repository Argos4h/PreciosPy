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
    MapEntry('leche', '🥛 Leche'),
    MapEntry('cerveza', '🍺 Cerveza'),
    MapEntry('coca', '🥤 Gaseosas'),
    MapEntry('carne', '🥩 Carne'),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final products = ref.watch(filteredProductsProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final selectedWeekday = ref.watch(selectedWeekdayProvider);
    final promotions = ref.watch(bankPromotionsProvider);

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
                    const Text(
                      'PreciosPy',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0x3300875A),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: const Color(0xFF00875A)),
                      ),
                      child: Text(
                        'Offline-First • ${wallet.length} tarjetas activas',
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color(0xFF3FB950),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                TextField(
                  onChanged: (value) => ref.read(searchQueryProvider.notifier).state = value,
                  decoration: InputDecoration(
                    hintText: 'Buscar yerba, leche trébol, cerveza o EAN...',
                    prefixIcon: const Icon(Icons.bolt_rounded, color: Color(0xFF3FB950)),
                    filled: true,
                    fillColor: const Color(0xFF161B22),
                    contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(14),
                      borderSide: const BorderSide(color: Color(0xFF30363D)),
                    ),
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
            child: ListView.builder(
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
                        content: Text('${product.normalizedName} agregado al Carrito PY'),
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

  @override
  Widget build(BuildContext context) {
    if (rankedOffers.isEmpty) return const SizedBox.shrink();
    final best = rankedOffers.first;

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
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        product.normalizedName,
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'EAN: ${product.ean ?? "S/D"} • ${GuaraniFormatter.formatPerBaseUnit(best.pricePerBaseUnitGs, best.baseUnit)}',
                        style: const TextStyle(fontSize: 12, color: Colors.white60),
                      ),
                    ],
                  ),
                ),
                IconButton.filledTonal(
                  onPressed: onAddToCart,
                  icon: const Icon(Icons.add_shopping_cart_rounded, size: 20),
                  tooltip: 'Agregar al Carrito Inteligente',
                ),
              ],
            ),
            const Divider(height: 20, color: Color(0xFF30363D)),
            ...rankedOffers.asMap().entries.map((entry) {
              final idx = entry.key;
              final eval = entry.value;
              final isBest = idx == 0;

              return Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                decoration: BoxDecoration(
                  color: isBest
                      ? const Color(0x2400875A)
                      : const Color(0xFF0D1117),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isBest ? const Color(0xFF3FB950) : const Color(0xFF21262D),
                  ),
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
                                  color: isBest ? const Color(0xFF3FB950) : Colors.white,
                                ),
                              ),
                              if (isBest) ...[
                                const SizedBox(width: 6),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF3FB950),
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: const Text(
                                    'MÁS BARATO HOY',
                                    style: TextStyle(
                                      fontSize: 9,
                                      fontWeight: FontWeight.w900,
                                      color: Colors.black,
                                    ),
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: 2),
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
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w800,
                            color: isBest ? const Color(0xFF3FB950) : Colors.white,
                          ),
                        ),
                        if (eval.effectiveFinalPriceGs < eval.offer.regularPriceGs)
                          Text(
                            'Góndola: ${GuaraniFormatter.format(eval.offer.regularPriceGs)}',
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
      ),
    ),
  );
  }
}

