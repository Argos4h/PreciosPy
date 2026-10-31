import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../state/app_providers.dart';

/// Pantalla "Promos" (Calendario semanal de promociones bancarias):
/// Réplica fiel de la sección de Promos de Rebuscate Paraguay, con selector
/// de días de la semana (Lunes a Domingo), filtro entre "Mis Tarjetas" y "Todas las Promos",
/// desglose por banco y supermercado, y cálculo de topes de reintegro.
class PromosScreen extends ConsumerWidget {
  const PromosScreen({super.key});

  static const Map<int, String> _weekdayFullNames = {
    1: 'Lunes',
    2: 'Martes',
    3: 'Miércoles',
    4: 'Jueves',
    5: 'Viernes',
    6: 'Sábado',
    7: 'Domingo',
  };

  static const Map<int, String> _weekdayShortNames = {
    1: 'Lun',
    2: 'Mar',
    3: 'Mié',
    4: 'Jue',
    5: 'Vie',
    6: 'Sáb',
    7: 'Dom',
  };

  Color _getBankColor(String bankSlug) {
    switch (bankSlug) {
      case 'ueno':
        return const Color(0xFF00C9A7); // Cyan / Esmeralda ueno
      case 'itau':
        return const Color(0xFFEA580C); // Naranja Itaú
      case 'continental':
        return const Color(0xFF0284C7); // Azul Continental
      case 'familiar':
        return const Color(0xFFDC2626); // Rojo Familiar
      case 'atlas':
        return const Color(0xFF334155); // Azul Noche Atlas
      case 'sudameris':
        return const Color(0xFF7C3AED); // Violeta Sudameris Club
      case 'gnb':
        return const Color(0xFF2563EB); // Azul GNB
      case 'zeta':
        return const Color(0xFF9333EA); // Púrpura Zeta
      case 'basa':
        return const Color(0xFFD97706); // Ámbar Basa
      default:
        return const Color(0xFF10B981);
    }
  }

  String _getBankIcon(String bankSlug) {
    switch (bankSlug) {
      case 'ueno':
        return '🟢';
      case 'itau':
        return '🟧';
      case 'continental':
        return '🔵';
      case 'familiar':
        return '🔴';
      case 'atlas':
        return '🏛️';
      case 'sudameris':
        return '🟣';
      case 'gnb':
        return '🏦';
      case 'zeta':
        return '⚡';
      case 'basa':
        return '🟡';
      default:
        return '💳';
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final promotions = ref.watch(bankPromotionsProvider);
    final userCards = ref.watch(userWalletCardsProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final selectedWeekday = ref.watch(selectedWeekdayProvider);
    final filterOnlyUserCards = ref.watch(promosFilterOnlyUserCardsProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    // Filtrar promociones por el día de la semana seleccionado
    final dayPromotions = promotions.where((p) => p.isValidOnWeekday(selectedWeekday)).toList();

    // Filtrar por tarjetas del usuario si el filtro está activado
    final filteredPromotions = filterOnlyUserCards
        ? dayPromotions.where((p) => userCards.contains(p.cardSlug)).toList()
        : dayPromotions;

    return SafeArea(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header: Título y estado
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
                          child: const Icon(Icons.local_offer_rounded, color: Color(0xFF10B981), size: 22),
                        ),
                        const SizedBox(width: 10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Promos de la Semana',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            Text(
                              '${_weekdayFullNames[selectedWeekday]} • ${filteredPromotions.length} promociones vigentes',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFF10B981).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                      ),
                      child: Text(
                        '${filteredPromotions.length} promos',
                        style: const TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFF10B981),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Aviso si está en Modo Solo Efectivo
                if (isCashOnly)
                  Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                    ),
                    child: Row(
                      children: [
                        const Text('💵', style: TextStyle(fontSize: 14)),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Modo Solo Efectivo activo: Las tarjetas están pausadas en tus compras, pero podés explorar el calendario aquí.',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: isDark ? const Color(0xFFD1FAE5) : const Color(0xFF065F46),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                // Barra selectora de Días de la Semana
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: List.generate(7, (index) {
                      final day = index + 1;
                      final isSelected = day == selectedWeekday;
                      final shortName = _weekdayShortNames[day]!;
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: ChoiceChip(
                          label: Text(
                            shortName,
                            style: TextStyle(
                              fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                              fontSize: 12,
                            ),
                          ),
                          selected: isSelected,
                          onSelected: (_) {
                            ref.read(selectedWeekdayProvider.notifier).state = day;
                          },
                        ),
                      );
                    }),
                  ),
                ),
                const SizedBox(height: 10),

                // Control Segmentado: [ 💳 Mis Tarjetas ] vs [ 🌐 Todas las Promos ]
                Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: InkWell(
                          onTap: () {
                            ref.read(promosFilterOnlyUserCardsProvider.notifier).state = false;
                          },
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            decoration: BoxDecoration(
                              color: !filterOnlyUserCards
                                  ? const Color(0xFF10B981)
                                  : Colors.transparent,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            alignment: Alignment.center,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.public_rounded,
                                  size: 14,
                                  color: !filterOnlyUserCards
                                      ? Colors.white
                                      : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  'Todas las Promos (${dayPromotions.length})',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w700,
                                    color: !filterOnlyUserCards
                                        ? Colors.white
                                        : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 4),
                      Expanded(
                        child: InkWell(
                          onTap: () {
                            ref.read(promosFilterOnlyUserCardsProvider.notifier).state = true;
                          },
                          borderRadius: BorderRadius.circular(12),
                          child: Container(
                            padding: const EdgeInsets.symmetric(vertical: 8),
                            decoration: BoxDecoration(
                              color: filterOnlyUserCards
                                  ? const Color(0xFF10B981)
                                  : Colors.transparent,
                              borderRadius: BorderRadius.circular(12),
                            ),
                            alignment: Alignment.center,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.credit_card_rounded,
                                  size: 14,
                                  color: filterOnlyUserCards
                                      ? Colors.white
                                      : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                ),
                                const SizedBox(width: 6),
                                Text(
                                  'Mis Tarjetas (${dayPromotions.where((p) => userCards.contains(p.cardSlug)).length})',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w700,
                                    color: filterOnlyUserCards
                                        ? Colors.white
                                        : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
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
              ],
            ),
          ),

          // Listado de Tarjetas de Promociones
          Expanded(
            child: filteredPromotions.isEmpty
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.savings_outlined,
                            size: 52,
                            color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            filterOnlyUserCards
                                ? 'No tenés tarjetas activas con promo este ${_weekdayFullNames[selectedWeekday]}'
                                : 'No hay promociones registradas para este día',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w700,
                              color: isDark ? Colors.white : const Color(0xFF0F172A),
                            ),
                          ),
                          const SizedBox(height: 6),
                          Text(
                            filterOnlyUserCards
                                ? 'Podés ver qué otros bancos ofrecen reintegros cambiando a "Todas las Promos", o activar más tarjetas en tu Perfil.'
                                : 'Seleccioná otro día de la semana para explorar los descuentos.',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 12,
                              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                            ),
                          ),
                          if (filterOnlyUserCards) ...[
                            const SizedBox(height: 14),
                            FilledButton.tonalIcon(
                              onPressed: () {
                                ref.read(promosFilterOnlyUserCardsProvider.notifier).state = false;
                              },
                              icon: const Icon(Icons.public_rounded, size: 16),
                              label: const Text('Ver todas las promos del día'),
                            ),
                          ],
                        ],
                      ),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    itemCount: filteredPromotions.length,
                    itemBuilder: (context, index) {
                      final promo = filteredPromotions[index];
                      final bankColor = _getBankColor(promo.bankSlug);
                      final bankIcon = _getBankIcon(promo.bankSlug);
                      final isUserCard = userCards.contains(promo.cardSlug);

                      // Nombre del supermercado legible
                      String storeName = promo.supermarketSlug.toUpperCase();
                      if (promo.supermarketSlug == 'superseis') storeName = 'Superseis';
                      if (promo.supermarketSlug == 'stock') storeName = 'Supermercados Stock';
                      if (promo.supermarketSlug == 'biggie') storeName = 'Biggie Express';
                      if (promo.supermarketSlug == 'casarica') storeName = 'Casa Rica Gourmet';
                      if (promo.supermarketSlug == 'arete') storeName = 'Supermercados Areté';

                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        clipBehavior: Clip.antiAlias,
                        child: Padding(
                          padding: const EdgeInsets.all(14),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  // Emblema del Banco
                                  Container(
                                    width: 44,
                                    height: 44,
                                    decoration: BoxDecoration(
                                      color: bankColor.withValues(alpha: 0.15),
                                      borderRadius: BorderRadius.circular(12),
                                      border: Border.all(color: bankColor.withValues(alpha: 0.3)),
                                    ),
                                    child: Center(
                                      child: Text(bankIcon, style: const TextStyle(fontSize: 22)),
                                    ),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                          children: [
                                            Text(
                                              promo.entityName,
                                              style: TextStyle(
                                                fontSize: 14,
                                                fontWeight: FontWeight.w800,
                                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                                              ),
                                            ),
                                            // Badge de descuento
                                            Container(
                                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                                              decoration: BoxDecoration(
                                                color: bankColor,
                                                borderRadius: BorderRadius.circular(8),
                                              ),
                                              child: Text(
                                                '${promo.discountPct.toInt()}% OFF',
                                                style: const TextStyle(
                                                  fontSize: 12,
                                                  fontWeight: FontWeight.w900,
                                                  color: Colors.white,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 2),
                                        Row(
                                          children: [
                                            const Icon(Icons.storefront_rounded, size: 13, color: Color(0xFF10B981)),
                                            const SizedBox(width: 4),
                                            Text(
                                              storeName,
                                              style: const TextStyle(
                                                fontSize: 12,
                                                fontWeight: FontWeight.w700,
                                                color: Color(0xFF10B981),
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 10),

                              // Título descriptivo de la promoción
                              Text(
                                promo.title,
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: isDark ? const Color(0xFFE2E8F0) : const Color(0xFF1E293B),
                                ),
                              ),
                              const SizedBox(height: 8),

                              // Requisitos y Chips informativos
                              Wrap(
                                spacing: 6,
                                runSpacing: 4,
                                children: [
                                  if (promo.requiresQr)
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                      decoration: BoxDecoration(
                                        color: const Color(0xFF0284C7).withValues(alpha: 0.15),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: const Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Icon(Icons.qr_code_rounded, size: 11, color: Color(0xFF0284C7)),
                                          SizedBox(width: 3),
                                          Text(
                                            'Pago con QR',
                                            style: TextStyle(
                                              fontSize: 10,
                                              fontWeight: FontWeight.w700,
                                              color: Color(0xFF0284C7),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  if (promo.spendingCapGs != null)
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                      decoration: BoxDecoration(
                                        color: isDark ? const Color(0xFF334155) : const Color(0xFFF1F5F9),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Text(
                                        'Tope mensual: ${GuaraniFormatter.format(promo.spendingCapGs!)}',
                                        style: TextStyle(
                                          fontSize: 10,
                                          fontWeight: FontWeight.w600,
                                          color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569),
                                        ),
                                      ),
                                    ),
                                  if (promo.minUenoLevel != null)
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                                      decoration: BoxDecoration(
                                        color: const Color(0xFF00C9A7).withValues(alpha: 0.15),
                                        borderRadius: BorderRadius.circular(6),
                                      ),
                                      child: Text(
                                        'Nivel ${promo.minUenoLevel}+ ueno',
                                        style: const TextStyle(
                                          fontSize: 10,
                                          fontWeight: FontWeight.w700,
                                          color: Color(0xFF0F766E),
                                        ),
                                      ),
                                    ),
                                ],
                              ),
                              const SizedBox(height: 8),

                              // Estado: ¿Aplica a mis tarjetas?
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                                decoration: BoxDecoration(
                                  color: isUserCard
                                      ? const Color(0xFF10B981).withValues(alpha: 0.15)
                                      : (isDark ? const Color(0xFF334155) : const Color(0xFFF1F5F9)),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Row(
                                      children: [
                                        Icon(
                                          isUserCard ? Icons.check_circle_rounded : Icons.info_outline_rounded,
                                          size: 14,
                                          color: isUserCard
                                              ? const Color(0xFF10B981)
                                              : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                        ),
                                        const SizedBox(width: 6),
                                        Text(
                                          isUserCard
                                              ? 'Aplica con tus tarjetas guardadas'
                                              : 'Requiere: ${promo.cardName}',
                                          style: TextStyle(
                                            fontSize: 11,
                                            fontWeight: isUserCard ? FontWeight.w700 : FontWeight.w500,
                                            color: isUserCard
                                                ? const Color(0xFF10B981)
                                                : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                                          ),
                                        ),
                                      ],
                                    ),
                                    Text(
                                      promo.mechanism == DiscountMechanism.cashback
                                          ? 'Reintegro en extracto'
                                          : 'Descuento en caja',
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
