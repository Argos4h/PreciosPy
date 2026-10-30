import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../state/app_providers.dart';

enum CartViewMode {
  singleStore,
  splitCart,
}

final cartViewModeProvider = StateProvider<CartViewMode>((ref) => CartViewMode.singleStore);

class SmartCartScreen extends ConsumerWidget {
  const SmartCartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cart = ref.watch(smartCartProvider);
    final rankings = ref.watch(smartCartRankingsProvider);
    final splitResult = ref.watch(splitCartResultProvider);
    final viewMode = ref.watch(cartViewModeProvider);

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Carrito Inteligente PY',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
                  ),
                  SizedBox(height: 2),
                  Text(
                    'Optimizado con topes de compra bancarios.',
                    style: TextStyle(fontSize: 12, color: Colors.white60),
                  ),
                ],
              ),
              if (splitResult.isSplitRecommended)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: const Color(0x3300875A),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: const Color(0xFF3FB950)),
                  ),
                  child: Text(
                    '-${GuaraniFormatter.format(splitResult.additionalSavingsGs)} dividiendo',
                    style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF3FB950),
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 14),

          // Selector de Modo: 1 Súper vs Compra Dividida
          SegmentedButton<CartViewMode>(
            segments: [
              const ButtonSegment(
                value: CartViewMode.singleStore,
                icon: Icon(Icons.store_rounded),
                label: Text('1 Solo Súper'),
              ),
              ButtonSegment(
                value: CartViewMode.splitCart,
                icon: const Icon(Icons.alt_route_rounded),
                label: Text(
                  splitResult.isSplitRecommended
                      ? 'Compra Dividida ✨'
                      : 'Compra Dividida',
                ),
              ),
            ],
            selected: {viewMode},
            onSelectionChanged: (val) {
              ref.read(cartViewModeProvider.notifier).state = val.first;
            },
          ),
          const SizedBox(height: 16),

          if (viewMode == CartViewMode.singleStore) ...[
            const Text(
              'Ranking de Supermercados para tu Lista Hoy',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 8),
            ...rankings.asMap().entries.map((entry) {
              final idx = entry.key;
              final summary = entry.value;
              final isWinner = idx == 0;

              return Card(
                margin: const EdgeInsets.only(bottom: 10),
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              Text(
                                '#${idx + 1} ${summary.supermarketName}',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w800,
                                  color: isWinner ? const Color(0xFF3FB950) : Colors.white,
                                ),
                              ),
                              if (summary.missingProductsCount > 0) ...[
                                const SizedBox(width: 8),
                                Text(
                                  '(${summary.missingProductsCount} sin stock)',
                                  style: const TextStyle(fontSize: 12, color: Colors.orangeAccent),
                                ),
                              ],
                            ],
                          ),
                          Text(
                            GuaraniFormatter.format(summary.netFinalCostGs),
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                              color: isWinner ? const Color(0xFF3FB950) : Colors.white,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(
                        summary.appliedCardName != null
                            ? 'Pagando en caja ${GuaraniFormatter.format(summary.totalCashAtPosGs)} con ${summary.appliedCardName} (Reintegro: ${GuaraniFormatter.format(summary.totalCashbackGs)})'
                            : 'Sin promo bancaria aplicable hoy (Total en caja: ${GuaraniFormatter.format(summary.totalCashAtPosGs)})',
                        style: const TextStyle(fontSize: 12, color: Colors.white70),
                      ),
                      if (summary.capReached) ...[
                        const SizedBox(height: 6),
                        const Text(
                          '⚠️ Alcanzaste el tope de compra de la tarjeta; el excedente se calculó a precio normal.',
                          style: TextStyle(fontSize: 11, color: Colors.amberAccent),
                        ),
                      ],
                    ],
                  ),
                ),
              );
            }),
          ] else ...[
            // VISTA: Compra Dividida Inteligente
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: splitResult.isSplitRecommended
                    ? const Color(0x2600875A)
                    : const Color(0xFF161B22),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: splitResult.isSplitRecommended
                      ? const Color(0xFF3FB950)
                      : const Color(0xFF30363D),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    splitResult.isSplitRecommended
                        ? Icons.savings_rounded
                        : Icons.info_outline_rounded,
                    color: splitResult.isSplitRecommended
                        ? const Color(0xFF3FB950)
                        : Colors.white70,
                    size: 32,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          splitResult.isSplitRecommended
                              ? '¡Ahorrás ${GuaraniFormatter.format(splitResult.additionalSavingsGs)} dividiendo tu compra!'
                              : 'No conviene dividir la compra hoy',
                          style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          splitResult.isSplitRecommended
                              ? 'Costo Total Dividido: ${GuaraniFormatter.format(splitResult.combinedNetCostGs)} (vs. ${GuaraniFormatter.format(splitResult.bestSingleStore.netFinalCostGs)} en ${splitResult.bestSingleStore.supermarketName})'
                              : 'Comprar todo en ${splitResult.bestSingleStore.supermarketName} te da prácticamente el mismo ahorro sin hacer dos viajes.',
                          style: const TextStyle(fontSize: 12, color: Colors.white70),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 14),
            ...splitResult.splitGroups.map((group) {
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Parada: ${group.supermarketName}',
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
                          ),
                          Text(
                            GuaraniFormatter.format(group.netCostGs),
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w900,
                              color: Color(0xFF3FB950),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        group.appliedCardName != null
                            ? 'Usar: ${group.appliedCardName} (En caja: ${GuaraniFormatter.format(group.totalCashAtPosGs)} • Reintegro: ${GuaraniFormatter.format(group.totalCashbackGs)})'
                            : 'Sin promo bancaria (Total en caja: ${GuaraniFormatter.format(group.totalCashAtPosGs)})',
                        style: const TextStyle(fontSize: 11, color: Colors.white70),
                      ),
                      const Divider(height: 18, color: Color(0xFF30363D)),
                      ...group.items.map((it) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 3),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Expanded(
                                child: Text(
                                  '• ${it.value}x ${it.key.normalizedName}',
                                  style: const TextStyle(fontSize: 13),
                                ),
                              ),
                            ],
                          ),
                        );
                      }),
                    ],
                  ),
                ),
              );
            }),
          ],

          const SizedBox(height: 16),
          const Text(
            'Productos en tu Lista',
            style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 8),
          ...cart.entries.map((entry) {
            final product = entry.key;
            final qty = entry.value;
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                title: Text(
                  product.normalizedName,
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                ),
                subtitle: Text('EAN: ${product.ean ?? "S/D"}'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    IconButton(
                      onPressed: () =>
                          ref.read(smartCartProvider.notifier).decrementOrRemove(product),
                      icon: const Icon(Icons.remove_circle_outline),
                    ),
                    Text('$qty', style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
                    IconButton(
                      onPressed: () => ref.read(smartCartProvider.notifier).addOrIncrement(product),
                      icon: const Icon(Icons.add_circle_outline),
                    ),
                  ],
                ),
              ),
            );
          }),
        ],
      ),
    );
  }
}
