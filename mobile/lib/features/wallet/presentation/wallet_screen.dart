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

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Mi Billetera PY',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 4),
          const Text(
            'Seleccioná tus tarjetas y niveles para que PreciosPy calcule tu Precio Final Real en cada góndola.',
            style: TextStyle(fontSize: 13, color: Colors.white60),
          ),
          const SizedBox(height: 16),
          ...promotions.map((promo) {
            final isSelected = activeCards.contains(promo.cardSlug);
            return Card(
              margin: const EdgeInsets.only(bottom: 10),
              child: SwitchListTile(
                value: isSelected,
                activeThumbColor: const Color(0xFF3FB950),
                title: Text(
                  promo.cardName,
                  style: const TextStyle(fontWeight: FontWeight.w700),
                ),
                subtitle: Text(
                  '${promo.title}\nTope compra: ${promo.spendingCapGs != null ? GuaraniFormatter.format(promo.spendingCapGs!) : "Sin tope"} • ${promo.appliesToPromoPrice ? "Acumulable con ofertas" : "No acumulable con ofertas"}',
                  style: const TextStyle(fontSize: 12, color: Colors.white70),
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

