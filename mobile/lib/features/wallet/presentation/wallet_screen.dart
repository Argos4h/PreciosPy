import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../state/app_providers.dart';

/// Pantalla "Mis Tarjetas PY":
/// Permite activar o desactivar las tarjetas y niveles de banco del usuario (ueno, Itaú,
/// Continental, Familiar, etc.) recalculando todos los precios de la app en tiempo real.
class WalletScreen extends ConsumerWidget {
  const WalletScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activeCards = ref.watch(userWalletCardsProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: const Color(0xFF10B981).withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.credit_card_rounded, color: Color(0xFF10B981), size: 22),
              ),
              const SizedBox(width: 10),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Mi Billetera PY',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                  Text(
                    'Activa tus tarjetas bancarias',
                    style: TextStyle(
                      fontSize: 12,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'Seleccioná tus tarjetas y niveles para que PreciosPy calcule tu Precio Final Real en cada góndola de Asunción y Gran Asunción.',
            style: TextStyle(
              fontSize: 13,
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
            ),
          ),
          const SizedBox(height: 16),
          ...promotions.map((promo) {
            final isSelected = activeCards.contains(promo.cardSlug);
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              child: SwitchListTile(
                value: isSelected,
                activeTrackColor: const Color(0xFF10B981),
                activeThumbColor: Colors.white,
                title: Text(
                  promo.cardName,
                  style: TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 15,
                    color: isDark ? Colors.white : const Color(0xFF0F172A),
                  ),
                ),
                subtitle: Padding(
                  padding: const EdgeInsets.only(top: 4),
                  child: Text(
                    '${promo.title}\nTope compra: ${promo.spendingCapGs != null ? GuaraniFormatter.format(promo.spendingCapGs!) : "Sin tope"} • ${promo.appliesToPromoPrice ? "Acumulable con ofertas" : "No acumulable"}',
                    style: TextStyle(
                      fontSize: 12,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                  ),
                ),
                isThreeLine: true,
                onChanged: (checked) {
                  final next = Set<String>.from(activeCards);
                  if (checked) {
                    next.add(promo.cardSlug);
                  } else {
                    next.remove(promo.cardSlug);
                  }
                  ref.read(userWalletCardsProvider.notifier).state = next;
                },
              ),
            );
          }),
        ],
      ),
    );
  }
}
