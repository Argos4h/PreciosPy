import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../data/local/local_catalog_repository.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../state/app_providers.dart';

class SmartCartScreen extends ConsumerWidget {
  const SmartCartScreen({super.key});

  void _showBestStoreReport({
    required BuildContext context,
    required WidgetRef ref,
    required List<SmartCartSummary> rankings,
    required SplitCartResult splitResult,
    required String cityName,
    required bool isCashOnly,
  }) {
    if (rankings.isEmpty) return;

    final winner = rankings.first;
    final worst = rankings.last;
    final maxSavingsVsWorst = worst.netFinalCostGs - winner.netFinalCostGs;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          constraints: BoxConstraints(
            maxHeight: MediaQuery.of(ctx).size.height * 0.88,
          ),
          decoration: BoxDecoration(
            color: isDark ? const Color(0xFF1E293B) : Colors.white,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
          ),
          padding: const EdgeInsets.fromLTRB(20, 14, 20, 24),
          child: Column(
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
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.auto_awesome_rounded, color: Color(0xFF10B981), size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Dónde te conviene comprar',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          isCashOnly
                              ? '📍 Sucursales en $cityName • 💵 Solo Efectivo (Precios de góndola)'
                              : '📍 Sucursales en $cityName • 💳 Descuentos bancarios de hoy',
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: isCashOnly
                                ? const Color(0xFF10B981)
                                : (isDark ? const Color(0xFF38BDF8) : const Color(0xFF0284C7)),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // SELECTOR SEGMENTADO: [ 💳 MIS TARJETAS ] vs [ 💵 SOLO EFECTIVO ]
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(
                    color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                  ),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: InkWell(
                        onTap: () {
                          if (isCashOnly) {
                            ref.read(cashOnlyModeProvider.notifier).state = false;
                          }
                        },
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          decoration: BoxDecoration(
                            color: !isCashOnly
                                ? const Color(0xFF10B981)
                                : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.credit_card_rounded,
                                size: 15,
                                color: !isCashOnly ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                              ),
                              const SizedBox(width: 6),
                              Text(
                                'Con Mis Tarjetas',
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w800,
                                  color: !isCashOnly ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Expanded(
                      child: InkWell(
                        onTap: () {
                          if (!isCashOnly) {
                            ref.read(cashOnlyModeProvider.notifier).state = true;
                          }
                        },
                        borderRadius: BorderRadius.circular(10),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          decoration: BoxDecoration(
                            color: isCashOnly
                                ? const Color(0xFF10B981)
                                : Colors.transparent,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.payments_rounded,
                                size: 15,
                                color: isCashOnly ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                              ),
                              const SizedBox(width: 6),
                              Text(
                                'Solo Efectivo',
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w800,
                                  color: isCashOnly ? Colors.white : (isDark ? Colors.white70 : Colors.black87),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),
              Expanded(
                child: ListView(
                  children: [
                    // 1. RECOMENDACIÓN PRINCIPAL: 1 SOLO SUPERMERCADO
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: isDark
                              ? [const Color(0xFF064E3B), const Color(0xFF0F172A)]
                              : [const Color(0xFFD1FAE5), const Color(0xFFF0FDF4)],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: const Color(0xFF10B981), width: 1.5),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Row(
                                children: [
                                  const Text('🥇', style: TextStyle(fontSize: 20)),
                                  const SizedBox(width: 6),
                                  Text(
                                    winner.supermarketName,
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w900,
                                      color: isDark ? Colors.white : const Color(0xFF065F46),
                                    ),
                                  ),
                                ],
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                decoration: BoxDecoration(
                                  color: const Color(0xFF10B981),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: const Text(
                                  'MEJOR OPCIÓN',
                                  style: TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.white),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: [
                              Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    'Total Neto a Pagar:',
                                    style: TextStyle(
                                      fontSize: 12,
                                      color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF047857),
                                    ),
                                  ),
                                  Text(
                                    GuaraniFormatter.format(winner.netFinalCostGs),
                                    style: TextStyle(
                                      fontSize: 24,
                                      fontWeight: FontWeight.w900,
                                      color: isDark ? const Color(0xFF34D399) : const Color(0xFF065F46),
                                    ),
                                  ),
                                ],
                              ),
                              if (maxSavingsVsWorst > 0)
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF10B981).withValues(alpha: 0.2),
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.end,
                                    children: [
                                      Text(
                                        'Ahorrás hasta',
                                        style: TextStyle(
                                          fontSize: 10,
                                          color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF065F46),
                                        ),
                                      ),
                                      Text(
                                        GuaraniFormatter.format(maxSavingsVsWorst),
                                        style: const TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.w900,
                                          color: Color(0xFF10B981),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 10),
                          Divider(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                          const SizedBox(height: 6),
                          Row(
                            children: [
                              Icon(
                                isCashOnly ? Icons.payments_rounded : Icons.credit_card_rounded,
                                size: 16,
                                color: const Color(0xFF10B981),
                              ),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  isCashOnly
                                      ? 'Pagas en caja ${GuaraniFormatter.format(winner.totalCashAtPosGs)} en Efectivo (Precios directos de góndola)'
                                      : (winner.appliedCardName != null
                                          ? 'Pagas en caja ${GuaraniFormatter.format(winner.totalCashAtPosGs)} con ${winner.appliedCardName} (Reintegro: ${GuaraniFormatter.format(winner.totalCashbackGs)})'
                                          : 'Pagas en caja ${GuaraniFormatter.format(winner.totalCashAtPosGs)} en Efectivo (Sin promo bancaria hoy)'),
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w600,
                                    color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF334155),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          if (winner.capReached) ...[
                            const SizedBox(height: 6),
                            const Text(
                              '⚠️ Alcanzaste el tope de compra con esta tarjeta; el excedente se calculó a precio góndola.',
                              style: TextStyle(fontSize: 10, color: Color(0xFFF59E0B)),
                            ),
                          ],
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // 2. OPCIÓN ALTERNATIVA: COMPRA DIVIDIDA (SPLIT-CART)
                    if (splitResult.isSplitRecommended) ...[
                      Container(
                        padding: const EdgeInsets.all(14),
                        decoration: BoxDecoration(
                          color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF0FDF4),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(color: const Color(0xFF34D399).withValues(alpha: 0.5)),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Row(
                                  children: [
                                    const Icon(Icons.alt_route_rounded, color: Color(0xFF10B981), size: 20),
                                    const SizedBox(width: 8),
                                    Text(
                                      'Opción Dividida (2 Supermercados)',
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w800,
                                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                                      ),
                                    ),
                                  ],
                                ),
                                Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF10B981).withValues(alpha: 0.2),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text(
                                    '+${GuaraniFormatter.format(splitResult.additionalSavingsGs)} extra',
                                    style: const TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.w800,
                                      color: Color(0xFF10B981),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Si tienes tiempo para hacer 2 paradas, gastarías ${GuaraniFormatter.format(splitResult.combinedNetCostGs)} en total.',
                              style: TextStyle(
                                fontSize: 12,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF475569),
                              ),
                            ),
                            const SizedBox(height: 8),
                            ...splitResult.splitGroups.map((group) {
                              return Padding(
                                padding: const EdgeInsets.symmetric(vertical: 2),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(
                                      '• ${group.supermarketName} (${group.items.length} ítems)',
                                      style: TextStyle(
                                        fontSize: 12,
                                        fontWeight: FontWeight.w600,
                                        color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF334155),
                                      ),
                                    ),
                                    Text(
                                      GuaraniFormatter.format(group.netCostGs),
                                      style: const TextStyle(
                                        fontSize: 12,
                                        fontWeight: FontWeight.w700,
                                        color: Color(0xFF10B981),
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            }),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),
                    ],

                    // 3. COMPARATIVA COMPLETA DE TODAS LAS CADENAS
                    Text(
                      'Comparativa de Todas las Cadenas',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w800,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 8),
                    ...rankings.asMap().entries.map((entry) {
                      final idx = entry.key;
                      final summary = entry.value;
                      final isFirst = idx == 0;
                      final diff = summary.netFinalCostGs - winner.netFinalCostGs;

                      return Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                        decoration: BoxDecoration(
                          color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC),
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(
                            color: isFirst
                                ? const Color(0xFF10B981)
                                : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                          ),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(
                                      '#${idx + 1} ${summary.supermarketName}',
                                      style: TextStyle(
                                        fontSize: 13,
                                        fontWeight: FontWeight.w700,
                                        color: isFirst
                                            ? const Color(0xFF10B981)
                                            : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                      ),
                                    ),
                                    if (summary.missingProductsCount > 0) ...[
                                      const SizedBox(width: 6),
                                      Text(
                                        '(${summary.missingProductsCount} sin stock)',
                                        style: const TextStyle(fontSize: 10, color: Color(0xFFF59E0B)),
                                      ),
                                    ],
                                  ],
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  isFirst
                                      ? 'La opción más económica hoy'
                                      : '+${GuaraniFormatter.format(diff)} más caro',
                                  style: TextStyle(
                                    fontSize: 11,
                                    color: isFirst
                                        ? const Color(0xFF10B981)
                                        : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                  ),
                                ),
                              ],
                            ),
                            Text(
                              GuaraniFormatter.format(summary.netFinalCostGs),
                              style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w800,
                                color: isFirst
                                    ? const Color(0xFF10B981)
                                    : (isDark ? Colors.white : const Color(0xFF0F172A)),
                              ),
                            ),
                          ],
                        ),
                      );
                    }),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildProductThumbnail(BuildContext context, ProductItem product) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cat = product.category ?? '🛒 Almacén';
    String emoji = '🛒';
    if (cat.contains('Yerba')) emoji = '🌿';
    if (cat.contains('Lácteos')) emoji = '🥛';
    if (cat.contains('Cerveza')) emoji = '🍺';
    if (cat.contains('Bebidas')) emoji = '🥤';
    if (cat.contains('Carne')) emoji = '🥩';
    if (cat.contains('Pan')) emoji = '🥖';

    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF334155) : const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(12),
      ),
      child: (product.imageUrl != null && product.imageUrl!.isNotEmpty)
          ? ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.network(
                product.imageUrl!,
                fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => Center(child: Text(emoji, style: const TextStyle(fontSize: 22))),
              ),
            )
          : Center(child: Text(emoji, style: const TextStyle(fontSize: 22))),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cart = ref.watch(smartCartProvider);
    final rankings = ref.watch(smartCartRankingsProvider);
    final splitResult = ref.watch(splitCartResultProvider);
    final selectedCity = ref.watch(selectedCityProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final cartItems = cart.entries.toList();

    return SafeArea(
      child: Column(
        children: [
          // Header de Mi Lista
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Mi Lista de Compras PY',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w900,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                    ),
                    Text(
                      cart.isEmpty
                          ? '📍 $selectedCity • ${isCashOnly ? "💵 Solo Efectivo" : "💳 Con Tarjetas"}'
                          : '${cart.length} productos cargados • 📍 $selectedCity • ${isCashOnly ? "💵 Solo Efectivo" : "💳 Con Tarjetas"}',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: isCashOnly ? const Color(0xFF10B981) : (isDark ? const Color(0xFF38BDF8) : const Color(0xFF0284C7)),
                      ),
                    ),
                  ],
                ),
                if (cart.isNotEmpty)
                  Row(
                    children: [
                      IconButton(
                        onPressed: () {
                          final buffer = StringBuffer();
                          buffer.writeln('🛒 Mi Lista de Compras PreciosPy');
                          buffer.writeln('📍 Ciudad: $selectedCity (${isCashOnly ? "Solo Efectivo" : "Con Tarjetas"})');
                          buffer.writeln();
                          for (final entry in cartItems) {
                            buffer.writeln('• ${entry.value}x ${entry.key.normalizedName}');
                          }
                          if (rankings.isNotEmpty) {
                            final winner = rankings.first;
                            buffer.writeln();
                            buffer.writeln('💡 Mejor opción calculada: ${winner.supermarketName} (${GuaraniFormatter.format(winner.netFinalCostGs)})');
                          }
                          Clipboard.setData(ClipboardData(text: buffer.toString()));
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              backgroundColor: const Color(0xFF10B981),
                              behavior: SnackBarBehavior.floating,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                              content: const Row(
                                children: [
                                  Icon(Icons.check_circle_rounded, color: Colors.white, size: 18),
                                  SizedBox(width: 8),
                                  Text(
                                    'Lista copiada para compartir por WhatsApp',
                                    style: TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                                  ),
                                ],
                              ),
                              duration: const Duration(milliseconds: 1400),
                            ),
                          );
                        },
                        icon: const Icon(Icons.share_rounded, size: 20, color: Color(0xFF0284C7)),
                        tooltip: 'Compartir Lista',
                      ),
                      TextButton.icon(
                        onPressed: () => ref.read(smartCartProvider.notifier).clearCart(),
                        icon: const Icon(Icons.delete_sweep_rounded, size: 18, color: Color(0xFFEF4444)),
                        label: const Text(
                          'Vaciar',
                          style: TextStyle(fontSize: 12, color: Color(0xFFEF4444), fontWeight: FontWeight.w700),
                        ),
                      ),
                    ],
                  ),
              ],
            ),
          ),

          // Agregado rápido horizontal
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: LocalCatalogRepository.initialCatalog.map((prod) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ActionChip(
                      avatar: Text(
                        prod.category?.contains('Yerba') == true
                            ? '🌿'
                            : prod.category?.contains('Lácteos') == true
                                ? '🥛'
                                : prod.category?.contains('Cerveza') == true
                                    ? '🍺'
                                    : '🥤',
                        style: const TextStyle(fontSize: 14),
                      ),
                      label: Text('+ ${prod.brand ?? prod.normalizedName.split(' ').first}'),
                      onPressed: () {
                        ref.read(smartCartProvider.notifier).addOrIncrement(prod);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
          const SizedBox(height: 6),

          // Lista de productos con ListView.builder (Ultra rápido & 60 FPS)
          Expanded(
            child: cart.isEmpty
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(32),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.shopping_cart_outlined,
                            size: 64,
                            color: isDark ? const Color(0xFF475569) : const Color(0xFF94A3B8),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            'Tu lista de compras está vacía',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                              color: isDark ? Colors.white : const Color(0xFF0F172A),
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            'Toca los botones rápidos arriba o busca cualquier producto en el comparador para sumarlo aquí.',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 13,
                              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                            ),
                          ),
                        ],
                      ),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    itemCount: cartItems.length,
                    itemBuilder: (context, index) {
                      final item = cartItems[index];
                      final product = item.key;
                      final qty = item.value;

                      return Card(
                        margin: const EdgeInsets.only(bottom: 10),
                        child: Padding(
                          padding: const EdgeInsets.all(12),
                          child: Row(
                            children: [
                              _buildProductThumbnail(context, product),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      product.normalizedName,
                                      maxLines: 2,
                                      overflow: TextOverflow.ellipsis,
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w700,
                                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                                      ),
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      product.category ?? '🛒 Almacén',
                                      style: TextStyle(
                                        fontSize: 11,
                                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  IconButton(
                                    visualDensity: VisualDensity.compact,
                                    onPressed: () =>
                                        ref.read(smartCartProvider.notifier).decrementOrRemove(product),
                                    icon: const Icon(Icons.remove_circle_outline_rounded, size: 22),
                                  ),
                                  Padding(
                                    padding: const EdgeInsets.symmetric(horizontal: 8),
                                    child: Text(
                                      '$qty',
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.w800,
                                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                                      ),
                                    ),
                                  ),
                                  IconButton(
                                    visualDensity: VisualDensity.compact,
                                    onPressed: () =>
                                        ref.read(smartCartProvider.notifier).addOrIncrement(product),
                                    icon: const Icon(Icons.add_circle_outline_rounded, size: 22, color: Color(0xFF10B981)),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),

          // EL BOTÓN DE ACCIÓN: "¿DÓNDE ME CONVIENE COMPRAR?"
          if (cart.isNotEmpty)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
              child: SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFF10B981),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    elevation: 3,
                  ),
                  icon: const Icon(Icons.auto_awesome_rounded, size: 22),
                  label: Text(
                    '¿DÓNDE ME CONVIENE COMPRAR? (${cart.length} ÍTEMS)',
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w900,
                      letterSpacing: 0.5,
                    ),
                  ),
                  onPressed: () {
                    _showBestStoreReport(
                      context: context,
                      ref: ref,
                      rankings: rankings,
                      splitResult: splitResult,
                      cityName: selectedCity,
                      isCashOnly: isCashOnly,
                    );
                  },
                ),
              ),
            ),
        ],
      ),
    );
  }
}
