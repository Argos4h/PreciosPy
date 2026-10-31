import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../data/local/local_catalog_repository.dart';
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

  void _showCityPicker(BuildContext context, WidgetRef ref) {
    final currentCity = ref.read(selectedCityProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          decoration: BoxDecoration(
            color: isDark ? const Color(0xFF1E293B) : Colors.white,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
          ),
          padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
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
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0284C7).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.location_on_rounded, color: Color(0xFF0284C7), size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Seleccionar tu Ciudad',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          'Solo verás supermercados con sucursal física cercana',
                          style: TextStyle(
                            fontSize: 12,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              ...LocalCatalogRepository.paraguayCities.map((item) {
                final cityName = item['city']!;
                final dept = item['dept']!;
                final badge = item['badge']!;
                final isSelected = cityName.toLowerCase() == currentCity.toLowerCase();

                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () {
                      ref.read(selectedCityProvider.notifier).state = cityName;
                      Navigator.of(ctx).pop();
                    },
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? (isDark ? const Color(0x260284C7) : const Color(0xFFE0F2FE))
                            : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: isSelected
                              ? const Color(0xFF0284C7)
                              : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                          width: isSelected ? 1.5 : 1.0,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            cityName == 'Todas' ? Icons.public_rounded : Icons.location_city_rounded,
                            color: isSelected ? const Color(0xFF0284C7) : const Color(0xFF64748B),
                            size: 20,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(
                                      cityName,
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.w800,
                                        color: isSelected
                                            ? const Color(0xFF0284C7)
                                            : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                      ),
                                    ),
                                    const SizedBox(width: 6),
                                    Text(
                                      '($dept)',
                                      style: TextStyle(
                                        fontSize: 11,
                                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  badge,
                                  style: TextStyle(
                                    fontSize: 11,
                                    color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569),
                                  ),
                                ),
                              ],
                            ),
                          ),
                          if (isSelected)
                            const Icon(Icons.check_circle_rounded, color: Color(0xFF0284C7), size: 22),
                        ],
                      ),
                    ),
                  ),
                );
              }),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final products = ref.watch(filteredProductsProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final selectedWeekday = ref.watch(selectedWeekdayProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final selectedCity = ref.watch(selectedCityProvider);
    final cityStores = ref.watch(currentCitySupermarketsProvider);
    final themeMode = ref.watch(themeModeProvider);
    final favorites = ref.watch(favoritesProvider);
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
                            InkWell(
                              onTap: () => _showCityPicker(context, ref),
                              borderRadius: BorderRadius.circular(6),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(Icons.location_on_rounded, size: 12, color: Color(0xFF0284C7)),
                                  const SizedBox(width: 2),
                                  Text(
                                    selectedCity == 'Todas' ? 'Todo Paraguay' : selectedCity,
                                    style: const TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.w700,
                                      color: Color(0xFF0284C7),
                                    ),
                                  ),
                                  const Icon(Icons.arrow_drop_down_rounded, size: 16, color: Color(0xFF0284C7)),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        InkWell(
                          onTap: () {
                            final next = !ref.read(cashOnlyModeProvider);
                            ref.read(cashOnlyModeProvider.notifier).state = next;
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                backgroundColor: next ? const Color(0xFF10B981) : const Color(0xFF0284C7),
                                behavior: SnackBarBehavior.floating,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                content: Text(
                                  next
                                      ? '💵 Modo Solo Efectivo: precios de góndola sin tarjetas'
                                      : '💳 Modo Tarjetas: aplicando tus promociones bancarias',
                                  style: const TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                                ),
                                duration: const Duration(milliseconds: 1400),
                              ),
                            );
                          },
                          borderRadius: BorderRadius.circular(16),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                            decoration: BoxDecoration(
                              color: isCashOnly
                                  ? const Color(0xFF10B981).withValues(alpha: 0.22)
                                  : const Color(0xFF10B981).withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                color: isCashOnly
                                    ? const Color(0xFF10B981)
                                    : const Color(0xFF10B981).withValues(alpha: 0.3),
                                width: isCashOnly ? 1.5 : 1.0,
                              ),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  isCashOnly ? Icons.payments_rounded : Icons.credit_card_rounded,
                                  size: 14,
                                  color: const Color(0xFF10B981),
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  isCashOnly ? '💵 Efectivo' : '${wallet.length} tarjetas',
                                  style: const TextStyle(
                                    fontSize: 11,
                                    color: Color(0xFF10B981),
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                              ],
                            ),
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
                if (isCashOnly)
                  Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.payments_rounded, size: 14, color: Color(0xFF10B981)),
                        const SizedBox(width: 6),
                        const Expanded(
                          child: Text(
                            'Modo Solo Efectivo: precios directos de góndola',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                              color: Color(0xFF10B981),
                            ),
                          ),
                        ),
                        InkWell(
                          onTap: () => ref.read(cashOnlyModeProvider.notifier).state = false,
                          child: const Text(
                            'Usar Tarjetas',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              color: Color(0xFF10B981),
                              decoration: TextDecoration.underline,
                            ),
                          ),
                        ),
                      ],
                    ),
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
                // Categorías rápidas
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
                const SizedBox(height: 8),
                // Selector de día para aplicar descuentos vigentes
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today_rounded,
                      size: 13,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      'Promos de:',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: _weekdayLabels.entries.map((entry) {
                            final isSelected = entry.key == selectedWeekday;
                            return Padding(
                              padding: const EdgeInsets.only(right: 4),
                              child: ChoiceChip(
                                visualDensity: VisualDensity.compact,
                                label: Text(
                                  entry.value,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                                  ),
                                ),
                                selected: isSelected,
                                onSelected: (_) =>
                                    ref.read(selectedWeekdayProvider.notifier).state = entry.key,
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                  ],
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
                        availableSupermarketSlugs: cityStores.keys.toSet(),
                      );
                      return _ProductComparisonCard(
                        product: product,
                        rankedOffers: rankedOffers,
                        isFavorite: favorites.contains(product.id),
                        onToggleFavorite: () {
                          ref.read(favoritesProvider.notifier).toggleFavorite(product.id);
                        },
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
  final bool isFavorite;
  final VoidCallback onToggleFavorite;

  const _ProductComparisonCard({
    required this.product,
    required this.rankedOffers,
    required this.onAddToCart,
    required this.isFavorite,
    required this.onToggleFavorite,
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
                  // Imagen / Thumbnail con botón corazón de favoritos integrado en la esquina
                  Stack(
                    children: [
                      ClipRRect(
                        borderRadius: BorderRadius.circular(14),
                        child: (product.imageUrl != null && product.imageUrl!.isNotEmpty)
                            ? Image.network(
                                product.imageUrl!,
                                width: 58,
                                height: 58,
                                fit: BoxFit.cover,
                                errorBuilder: (ctx, _, __) => _buildCategoryThumbnail(context, product.category),
                              )
                            : _buildCategoryThumbnail(context, product.category),
                      ),
                      Positioned(
                        top: 2,
                        right: 2,
                        child: InkWell(
                          onTap: onToggleFavorite,
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            padding: const EdgeInsets.all(3.5),
                            decoration: BoxDecoration(
                              color: isFavorite
                                  ? const Color(0xFFEF4444).withValues(alpha: 0.2)
                                  : (isDark ? const Color(0x99000000) : const Color(0xB3FFFFFF)),
                              shape: BoxShape.circle,
                            ),
                            child: Icon(
                              isFavorite ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                              color: isFavorite
                                  ? const Color(0xFFEF4444)
                                  : (isDark ? Colors.white70 : const Color(0xFF64748B)),
                              size: 15,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(width: 12),
                  // Nombre, categoría y precio unitario
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          product.normalizedName,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontSize: 14.5,
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
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                              decoration: BoxDecoration(
                                color: const Color(0xFF10B981).withValues(alpha: 0.15),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: const Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Text('🟢', style: TextStyle(fontSize: 7)),
                                  SizedBox(width: 3),
                                  Text(
                                    'Hoy',
                                    style: TextStyle(fontSize: 9, fontWeight: FontWeight.w700, color: Color(0xFF10B981)),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  // Botón "+ Lista" limpio y fácil de presionar
                  FilledButton.tonalIcon(
                    onPressed: onAddToCart,
                    style: FilledButton.styleFrom(
                      backgroundColor: const Color(0xFF10B981).withValues(alpha: 0.15),
                      foregroundColor: const Color(0xFF10B981),
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      minimumSize: const Size(0, 32),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    icon: const Icon(Icons.add_shopping_cart_rounded, size: 15),
                    label: const Text(
                      '+ Lista',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.w800),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Divider(
                height: 1,
                color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
              ),
              const SizedBox(height: 10),

              // Lista de ofertas por supermercado (con diferencias claras vs el más barato)
              ...rankedOffers.asMap().entries.map((entry) {
                final idx = entry.key;
                final eval = entry.value;
                final isBest = idx == 0;
                final diffGs = eval.effectiveFinalPriceGs - best.effectiveFinalPriceGs;

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
                            )
                          else if (!isBest && diffGs > 0)
                            Text(
                              '+${GuaraniFormatter.format(diffGs)}',
                              style: const TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.w600,
                                color: Color(0xFFEF4444),
                              ),
                            ),
                        ],
                      ),
                    ],
                  ),
                );
              }),

              // Hint sutil al pie de la tarjeta para invitar al detalle de transparencia
              const SizedBox(height: 4),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'Ver historial de precios DNIT y ofertas falsas',
                    style: TextStyle(
                      fontSize: 10.5,
                      fontWeight: FontWeight.w600,
                      color: isDark ? const Color(0xFF38BDF8) : const Color(0xFF0284C7),
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.chevron_right_rounded,
                    size: 14,
                    color: isDark ? const Color(0xFF38BDF8) : const Color(0xFF0284C7),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

