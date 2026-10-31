import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../data/local/local_catalog_repository.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';
import '../../wallet/presentation/wallet_screen.dart';

/// Pantalla "Perfil":
/// Réplica fiel de la sección Perfil de Rebuscate Paraguay, agrupando:
/// 1. Resumen de Perfil de Compras y Ciudad Activa.
/// 2. Interruptor de "Modo Solo Efectivo" (góndola vs tarjetas).
/// 3. "Alertas de Precio y Favoritos" seguidos en tiempo real.
/// 4. "Mis Tarjetas Bancarias" con configuración de niveles ueno y tiers de Itaú/otros.
/// 5. Preferencias de Visualización (Modo Oscuro / Claro) y SIFEN e-Kuatia DNIT.
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

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
                          'Filtra los supermercados con sucursales cercanas',
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
                final isSelected = cityName == currentCity;

                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    onTap: () {
                      ref.read(selectedCityProvider.notifier).state = cityName;
                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          backgroundColor: const Color(0xFF0284C7),
                          behavior: SnackBarBehavior.floating,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          content: Text(
                            '📍 Ciudad cambiada a $cityName',
                            style: const TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                          ),
                          duration: const Duration(milliseconds: 900),
                        ),
                      );
                    },
                    borderRadius: BorderRadius.circular(16),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? const Color(0xFF0284C7).withValues(alpha: 0.15)
                            : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isSelected
                              ? const Color(0xFF0284C7)
                              : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
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
                                      cityName,
                                      style: TextStyle(
                                        fontSize: 14,
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
    final profiles = ref.watch(userWalletProfilesProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final selectedCity = ref.watch(selectedCityProvider);
    final favorites = ref.watch(favoritesProvider);
    final allProducts = ref.watch(catalogRepositoryProvider).allProducts;
    final promotions = ref.watch(bankPromotionsProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final weekday = ref.watch(selectedWeekdayProvider);
    final cityStores = ref.watch(currentCitySupermarketsProvider);
    final themeMode = ref.watch(themeModeProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final activeCardsCount = profiles.values.where((p) => p.isEnabled).length;
    final uenoProfile = profiles['ueno'];

    // Filtrar los productos marcados como favoritos
    final favoriteProducts = allProducts.where((p) => favorites.contains(p.id)).toList();

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // 1. Tarjeta Principal de Perfil del Usuario
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 56,
                    height: 56,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [Color(0xFF10B981), Color(0xFF0284C7)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(18),
                      boxShadow: [
                        BoxShadow(
                          color: const Color(0xFF10B981).withValues(alpha: 0.3),
                          blurRadius: 8,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: const Center(
                      child: Text('🇵🇾', style: TextStyle(fontSize: 28)),
                    ),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Mi Perfil de Compras',
                          style: TextStyle(
                            fontSize: 17,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        const SizedBox(height: 3),
                        InkWell(
                          onTap: () => _showCityPicker(context, ref),
                          borderRadius: BorderRadius.circular(6),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(Icons.location_on_rounded, size: 13, color: Color(0xFF0284C7)),
                              const SizedBox(width: 3),
                              Text(
                                selectedCity == 'Todas' ? 'Todo Paraguay' : selectedCity,
                                style: const TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w700,
                                  color: Color(0xFF0284C7),
                                ),
                              ),
                              const Icon(Icons.arrow_drop_down_rounded, size: 16, color: Color(0xFF0284C7)),
                            ],
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          isCashOnly
                              ? '💵 Modo Solo Efectivo activo'
                              : '💳 $activeCardsCount bancos configurados',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: isCashOnly
                                ? const Color(0xFF10B981)
                                : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: () {
                      final next = themeMode == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
                      ref.read(themeModeProvider.notifier).state = next;
                    },
                    icon: Icon(
                      themeMode == ThemeMode.dark ? Icons.light_mode_rounded : Icons.dark_mode_rounded,
                      color: const Color(0xFFF59E0B),
                    ),
                    tooltip: 'Cambiar Tema',
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // 2. SWITCH MODO SOLO EFECTIVO
          Card(
            color: isCashOnly
                ? (isDark ? const Color(0x2610B981) : const Color(0xFFD1FAE5))
                : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC)),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(20),
              side: BorderSide(
                color: isCashOnly
                    ? const Color(0xFF10B981)
                    : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                width: isCashOnly ? 1.5 : 1.0,
              ),
            ),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: isCashOnly
                          ? const Color(0xFF10B981).withValues(alpha: 0.2)
                          : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Icon(
                      Icons.payments_rounded,
                      color: isCashOnly ? const Color(0xFF10B981) : (isDark ? Colors.white70 : Colors.black87),
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(
                              'Modo Solo Efectivo',
                              style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w800,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            if (isCashOnly) ...[
                              const SizedBox(width: 6),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(
                                  color: const Color(0xFF10B981),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: const Text(
                                  'ACTIVO',
                                  style: TextStyle(fontSize: 9, fontWeight: FontWeight.w900, color: Colors.white),
                                ),
                              ),
                            ],
                          ],
                        ),
                        const SizedBox(height: 2),
                        Text(
                          isCashOnly
                              ? 'Comparando precios directos de góndola sin tarjetas bancarias.'
                              : 'Ignora las promociones bancarias y calcula pagos en efectivo.',
                          style: TextStyle(
                            fontSize: 11,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Switch(
                    value: isCashOnly,
                    activeThumbColor: const Color(0xFF10B981),
                    onChanged: (val) {
                      ref.read(cashOnlyModeProvider.notifier).state = val;
                    },
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          // 3. MIS ALERTAS DE PRECIO Y FAVORITOS (Al estilo Rebuscate)
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  const Icon(Icons.favorite_rounded, color: Color(0xFFEF4444), size: 18),
                  const SizedBox(width: 6),
                  Text(
                    'Mis Alertas y Favoritos',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w900,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFFEF4444).withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${favoriteProducts.length} productos',
                  style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: Color(0xFFEF4444)),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),

          if (favoriteProducts.isEmpty)
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    const Icon(Icons.favorite_border_rounded, color: Color(0xFF94A3B8), size: 28),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Marcá el corazón en cualquier producto para activar alertas cuando baje de precio.',
                        style: TextStyle(
                          fontSize: 12,
                          color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            )
          else
            ...favoriteProducts.map((product) {
              final ranked = PromoCalculator.rankProductOffers(
                product: product,
                allPromotions: promotions,
                userCardSlugs: wallet,
                isoWeekday: weekday,
                availableSupermarketSlugs: cityStores.keys.toSet(),
              );
              final best = ranked.isNotEmpty ? ranked.first : null;

              return Card(
                margin: const EdgeInsets.only(bottom: 8),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Container(
                        width: 44,
                        height: 44,
                        decoration: BoxDecoration(
                          color: isDark ? const Color(0xFF334155) : const Color(0xFFF1F5F9),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Center(
                          child: Text(
                            product.category?.contains('Yerba') == true ? '🌿' : '🥛',
                            style: const TextStyle(fontSize: 22),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              product.normalizedName,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w700,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            const SizedBox(height: 2),
                            if (best != null)
                              Row(
                                children: [
                                  Text(
                                    best.offer.supermarketName,
                                    style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: Color(0xFF10B981)),
                                  ),
                                  const SizedBox(width: 6),
                                  Text(
                                    GuaraniFormatter.format(best.effectiveFinalPriceGs),
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w900,
                                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                                    ),
                                  ),
                                ],
                              ),
                          ],
                        ),
                      ),
                      IconButton(
                        onPressed: () {
                          ref.read(favoritesProvider.notifier).toggleFavorite(product.id);
                        },
                        icon: const Icon(Icons.favorite_rounded, color: Color(0xFFEF4444), size: 20),
                        tooltip: 'Quitar de favoritos',
                      ),
                    ],
                  ),
                ),
              );
            }),

          const SizedBox(height: 16),

          // 4. MIS TARJETAS BANCARIAS
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  const Icon(Icons.credit_card_rounded, color: Color(0xFF10B981), size: 18),
                  const SizedBox(width: 6),
                  Text(
                    'Mis Tarjetas Bancarias',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w900,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                ],
              ),
              Text(
                '$activeCardsCount activas',
                style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: Color(0xFF10B981)),
              ),
            ],
          ),
          const SizedBox(height: 8),

          // ueno bank
          if (uenoProfile != null)
            UenoConfigCard(
              profile: uenoProfile,
              onToggle: () => ref.read(userWalletProfilesProvider.notifier).toggleBank('ueno'),
              onLevelChanged: (lvl) => ref.read(userWalletProfilesProvider.notifier).setUenoLevel(lvl),
              onPaymentMethodChanged: (isQr) =>
                  ref.read(userWalletProfilesProvider.notifier).setPaymentMethod('ueno', isQr),
              onSpentChanged: (spent) =>
                  ref.read(userWalletProfilesProvider.notifier).setSpentThisMonth('ueno', spent),
            ),

          const SizedBox(height: 8),

          // Resto de los bancos paraguayos
          ...profiles.entries.where((e) => e.key != 'ueno').map((entry) {
            final bankSlug = entry.key;
            final profile = entry.value;

            return StandardBankConfigCard(
              profile: profile,
              onToggle: () => ref.read(userWalletProfilesProvider.notifier).toggleBank(bankSlug),
              onTierChanged: (tier) =>
                  ref.read(userWalletProfilesProvider.notifier).setTier(bankSlug, tier),
              onPaymentMethodChanged: (isQr) =>
                  ref.read(userWalletProfilesProvider.notifier).setPaymentMethod(bankSlug, isQr),
              onSpentChanged: (spent) =>
                  ref.read(userWalletProfilesProvider.notifier).setSpentThisMonth(bankSlug, spent),
            );
          }),

          const SizedBox(height: 16),

          // 5. TRANSPARENCIA Y SIFEN e-Kuatia (DNIT)
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.verified_user_rounded, color: Color(0xFF10B981), size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'SIFEN e-Kuatia DNIT',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w800,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'Catálogo SQLite Offline-First sincronizado con tickets tributarios oficiales de Paraguay.',
                          style: TextStyle(
                            fontSize: 11,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}
