import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../state/app_providers.dart';

/// Pantalla "Mis Tarjetas PY":
/// Permite configurar con granularidad exacta:
/// - ueno bank: Niveles 1 al 5 (10% a 40%), tipo de tarjeta (Crédito QR / Débito) y consumo de tope mensual.
/// - Banco Itaú, Continental, Familiar, Atlas, Sudameris, GNB, Zeta y Basa:
///   Selección de Tier/Categoría (Clásica/Oro, Platinum, Black/Infinite, Afinidad),
///   método de pago (QR vs Plástico físico) y tope mensual restante.
class WalletScreen extends ConsumerWidget {
  const WalletScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final profiles = ref.watch(userWalletProfilesProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final activeCardsCount = profiles.values.where((p) => p.isEnabled).length;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final uenoProfile = profiles['ueno'];

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
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
                        isCashOnly
                            ? '💵 Modo Solo Efectivo activado'
                            : '$activeCardsCount bancos activos para comparar',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: isCashOnly ? FontWeight.w700 : FontWeight.w500,
                          color: isCashOnly
                              ? const Color(0xFF10B981)
                              : (isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: isCashOnly
                      ? const Color(0xFF10B981).withValues(alpha: 0.2)
                      : const Color(0xFF10B981).withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                ),
                child: Text(
                  isCashOnly ? '💵 Solo Efectivo' : 'Topes Activos',
                  style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: Color(0xFF10B981)),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'Configurá tus tarjetas, niveles y formas de pago. PreciosPy calcula automáticamente el Precio Final Real cruzando los días de descuento y los topes de reintegro.',
            style: TextStyle(
              fontSize: 12,
              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
              height: 1.4,
            ),
          ),
          const SizedBox(height: 16),

          // OPCIÓN MODO SOLO EFECTIVO
          Card(
            margin: const EdgeInsets.only(bottom: 16),
            color: isCashOnly
                ? (isDark ? const Color(0x2610B981) : const Color(0xFFD1FAE5))
                : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC)),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
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
                              ? 'Comparando precios directos de góndola (sin tarjetas bancarias).'
                              : 'Ignora las tarjetas y compara precios pagando únicamente en efectivo.',
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

          // 1. TARJETA DESTACADA: UENO BANK (NIVELES 1..5)
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

          const SizedBox(height: 12),

          // 2. DEMÁS BANCOS PARAGUAYOS
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
        ],
      ),
    );
  }
}

/// Tarjeta de Configuración Especial de ueno bank (Gamificación de Niveles)
class UenoConfigCard extends StatelessWidget {
  final UserCardProfile profile;
  final VoidCallback onToggle;
  final ValueChanged<int> onLevelChanged;
  final ValueChanged<bool> onPaymentMethodChanged;
  final ValueChanged<int> onSpentChanged;

  const UenoConfigCard({
    super.key,
    required this.profile,
    required this.onToggle,
    required this.onLevelChanged,
    required this.onPaymentMethodChanged,
    required this.onSpentChanged,
  });

  int _getCashbackPct(int level) {
    switch (level) {
      case 5:
        return 40;
      case 4:
        return 35;
      case 3:
        return 25;
      case 2:
        return 15;
      case 1:
      default:
        return 10;
    }
  }

  int _getSpendingCap(int level) {
    switch (level) {
      case 5:
        return 1000000;
      case 4:
        return 800000;
      case 3:
        return 600000;
      case 2:
        return 400000;
      case 1:
      default:
        return 300000;
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final currentCashback = _getCashbackPct(profile.uenoLevel);
    final currentCap = _getSpendingCap(profile.uenoLevel);
    final remainingCap = (currentCap - profile.spentThisMonthGs).clamp(0, currentCap);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(
          color: profile.isEnabled ? const Color(0xFF10B981) : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
          width: profile.isEnabled ? 1.5 : 1.0,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: [
                    Container(
                      width: 36,
                      height: 36,
                      decoration: BoxDecoration(
                        color: const Color(0xFF00E5FF).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: const Center(
                        child: Text('🟢', style: TextStyle(fontSize: 18)),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'ueno bank',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          'Biggie Express • Superseis',
                          style: TextStyle(
                            fontSize: 11,
                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                Switch(
                  value: profile.isEnabled,
                  activeTrackColor: const Color(0xFF10B981),
                  activeThumbColor: Colors.white,
                  onChanged: (_) => onToggle(),
                ),
              ],
            ),
            if (profile.isEnabled) ...[
              const SizedBox(height: 14),
              Divider(height: 1, color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
              const SizedBox(height: 12),

              // Selector de Nivel ueno (1 al 5)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Tu Nivel en ueno:',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      '$currentCashback% reintegro',
                      style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w800, color: Color(0xFF10B981)),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [1, 2, 3, 4, 5].map((lvl) {
                    final isSelected = profile.uenoLevel == lvl;
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: Text(
                          lvl == 5
                              ? '👑 Nivel 5'
                              : lvl == 4
                                  ? '⭐ Nivel 4'
                                  : 'Nivel $lvl',
                        ),
                        selected: isSelected,
                        onSelected: (_) => onLevelChanged(lvl),
                      ),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 12),

              // Método de pago: QR vs Tarjeta Física
              Text(
                'Método de Pago:',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 6),
              Row(
                children: [
                  Expanded(
                    child: ChoiceChip(
                      label: const Center(child: Text('📱 Pago con QR ueno')),
                      selected: profile.isQrPayment,
                      onSelected: (val) {
                        if (val) onPaymentMethodChanged(true);
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: ChoiceChip(
                      label: const Center(child: Text('💳 Tarjeta Física')),
                      selected: !profile.isQrPayment,
                      onSelected: (val) {
                        if (val) onPaymentMethodChanged(false);
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Control de Cupo / Tope Mensual Consumido
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Tope Mensual de Reintegro:',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                  Text(
                    'Cupo libre: ${GuaraniFormatter.format(remainingCap)}',
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: remainingCap > 0 ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: LinearProgressIndicator(
                  value: currentCap > 0 ? (profile.spentThisMonthGs / currentCap).clamp(0.0, 1.0) : 0.0,
                  backgroundColor: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                  color: const Color(0xFF10B981),
                  minHeight: 6,
                ),
              ),
              const SizedBox(height: 6),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Consumido este mes:',
                    style: TextStyle(
                      fontSize: 11,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                  ),
                  Text(
                    GuaraniFormatter.format(profile.spentThisMonthGs),
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w800,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                ],
              ),
              Slider(
                value: profile.spentThisMonthGs.toDouble().clamp(0.0, currentCap.toDouble()),
                min: 0,
                max: currentCap.toDouble(),
                divisions: 10,
                activeColor: const Color(0xFF10B981),
                onChanged: (val) => onSpentChanged(val.round()),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

/// Tarjeta de Configuración para Bancos Estándar (Itaú, Continental, Familiar, Atlas, etc.)
class StandardBankConfigCard extends StatelessWidget {
  final UserCardProfile profile;
  final VoidCallback onToggle;
  final ValueChanged<String> onTierChanged;
  final ValueChanged<bool> onPaymentMethodChanged;
  final ValueChanged<int> onSpentChanged;

  const StandardBankConfigCard({
    super.key,
    required this.profile,
    required this.onToggle,
    required this.onTierChanged,
    required this.onPaymentMethodChanged,
    required this.onSpentChanged,
  });

  String _getBankSubtext(String slug) {
    switch (slug) {
      case 'itau':
        return 'Martes Superseis (20-25%) • Jueves Casa Rica (25%)';
      case 'continental':
        return 'Miércoles Supermercados Areté (20-25%)';
      case 'familiar':
        return 'Viernes Supermercados Stock (20-25%)';
      case 'atlas':
        return 'Lunes Stock y Box Mayorista (20-25%)';
      case 'sudameris':
        return 'Jueves Gourmet Casa Rica (25%)';
      case 'gnb':
        return 'Miércoles Superseis y Stock (20%)';
      case 'zeta':
        return 'Sábados QR en comercios adheridos (20%)';
      case 'basa':
        return 'Domingos Supermercados Stock (20%)';
      default:
        return 'Promociones bancarias paraguayas';
    }
  }

  String _getBankEmoji(String slug) {
    switch (slug) {
      case 'itau':
        return '🟧';
      case 'continental':
        return '🟩';
      case 'familiar':
        return '🟦';
      case 'atlas':
        return '🟥';
      case 'sudameris':
        return '🔴';
      case 'gnb':
        return '🔵';
      case 'zeta':
        return '🟣';
      case 'basa':
        return '🟡';
      default:
        return '💳';
    }
  }

  List<MapEntry<String, String>> _getTiersForBank(String slug) {
    if (slug == 'itau') {
      return const [
        MapEntry('clasica', 'Clásica / Oro (20%)'),
        MapEntry('platinum', 'Platinum (25%)'),
        MapEntry('infinite', 'Personal Bank (25-30%)'),
        MapEntry('afinidad', 'Afinidad Superseis'),
      ];
    } else if (slug == 'continental') {
      return const [
        MapEntry('clasica', 'Clásica / Oro (20%)'),
        MapEntry('infinite', 'Black / Signature (25%)'),
      ];
    } else if (slug == 'familiar') {
      return const [
        MapEntry('clasica', 'Clásica (20%)'),
        MapEntry('platinum', 'Mujer / Platinum (25%)'),
      ];
    } else if (slug == 'atlas') {
      return const [
        MapEntry('clasica', 'Clásica (20%)'),
        MapEntry('infinite', 'Platinum / Black (25%)'),
      ];
    } else if (slug == 'sudameris') {
      return const [
        MapEntry('infinite', 'Black / Infinite (25%)'),
        MapEntry('clasica', 'Clásica / Oro (20%)'),
      ];
    } else {
      return const [
        MapEntry('clasica', 'Estándar / Clásica (20%)'),
        MapEntry('infinite', 'Premium / Black (25%)'),
      ];
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final tiers = _getTiersForBank(profile.bankSlug);
    const standardCap = 1000000;
    final remainingCap = (standardCap - profile.spentThisMonthGs).clamp(0, standardCap);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(
          color: profile.isEnabled ? const Color(0xFF10B981) : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
          width: profile.isEnabled ? 1.5 : 1.0,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: const Color(0xFF10B981).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Center(
                    child: Text(_getBankEmoji(profile.bankSlug), style: const TextStyle(fontSize: 18)),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        profile.bankName,
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w800,
                          color: isDark ? Colors.white : const Color(0xFF0F172A),
                        ),
                      ),
                      Text(
                        _getBankSubtext(profile.bankSlug),
                        style: TextStyle(
                          fontSize: 11,
                          color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Switch(
                  value: profile.isEnabled,
                  activeTrackColor: const Color(0xFF10B981),
                  activeThumbColor: Colors.white,
                  onChanged: (_) => onToggle(),
                ),
              ],
            ),
            if (profile.isEnabled) ...[
              const SizedBox(height: 12),
              Divider(height: 1, color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
              const SizedBox(height: 10),

              // Selector de Categoría / Tier de Tarjeta
              Text(
                'Categoría de Tarjeta:',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: tiers.map((t) {
                    final isSelected = profile.tier == t.key;
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: Text(t.value),
                        selected: isSelected,
                        onSelected: (_) => onTierChanged(t.key),
                      ),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 10),

              // Método de pago: QR vs Físico
              Row(
                children: [
                  Expanded(
                    child: ChoiceChip(
                      label: const Center(child: Text('📱 Pago QR')),
                      selected: profile.isQrPayment,
                      onSelected: (val) {
                        if (val) onPaymentMethodChanged(true);
                      },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: ChoiceChip(
                      label: const Center(child: Text('💳 Tarjeta Física')),
                      selected: !profile.isQrPayment,
                      onSelected: (val) {
                        if (val) onPaymentMethodChanged(false);
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),

              // Tope Mensual Consumido
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Cupo disponible este mes:',
                    style: TextStyle(
                      fontSize: 11,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                  ),
                  Text(
                    GuaraniFormatter.format(remainingCap),
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w800,
                      color: remainingCap > 0 ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                    ),
                  ),
                ],
              ),
              Slider(
                value: profile.spentThisMonthGs.toDouble().clamp(0.0, standardCap.toDouble()),
                min: 0,
                max: standardCap.toDouble(),
                divisions: 10,
                activeColor: const Color(0xFF10B981),
                onChanged: (val) => onSpentChanged(val.round()),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
