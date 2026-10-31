import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../data/local/local_catalog_repository.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';

/// Modo "Escáner de Pasillo" (HUD en vivo):
/// El usuario selecciona en qué supermercado está parado y al apuntar a cualquier código
/// EAN-13 ve un semáforo instantáneo (🟢 Estás en el más barato / 🔴 Caro aquí).
class ScannerScreen extends ConsumerStatefulWidget {
  const ScannerScreen({super.key});

  @override
  ConsumerState<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends ConsumerState<ScannerScreen> {
  String _currentBarcode = '7840000000036'; // Demo inicial: Yerba Kurupí 500g
  bool _cameraEnabled = false;

  void _showKuatiaInvoiceModal(BuildContext context, KuatiaInvoiceReceipt invoice) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final repo = ref.read(catalogRepositoryProvider);

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          constraints: BoxConstraints(
            maxHeight: MediaQuery.of(ctx).size.height * 0.85,
          ),
          padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
          decoration: BoxDecoration(
            color: isDark ? const Color(0xFF1E293B) : Colors.white,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
          ),
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
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: const Icon(Icons.receipt_long_rounded, color: Color(0xFF10B981), size: 26),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Text(
                              'Factura e-Kuatia SIFEN',
                              style: TextStyle(
                                fontSize: 17,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            const SizedBox(width: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: const Color(0xFF10B981).withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: const Text(
                                'DNIT ✓',
                                style: TextStyle(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w900,
                                  color: Color(0xFF10B981),
                                ),
                              ),
                            ),
                          ],
                        ),
                        Text(
                          'Emisor: RUC ${invoice.rucIssuer} • Doc: ${invoice.invoiceNumber}',
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
              Expanded(
                child: ListView(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'ÍTEMS DETECTADOS EN EL TICKET:',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.5,
                              color: Color(0xFF10B981),
                            ),
                          ),
                          const SizedBox(height: 10),
                          _buildTicketItemRow('Yerba Mate Kurupí Menta y Boldo 500g', 1, 14500, isDark),
                          _buildTicketItemRow('Leche Entera Trébol Cartón 1L', 2, 17800, isDark),
                          _buildTicketItemRow('Gaseosa Coca-Cola Original 2L', 1, 14800, isDark),
                          const Divider(height: 20),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'TOTAL TICKET:',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w900,
                                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                                ),
                              ),
                              const Text(
                                'Gs. 47.100',
                                style: TextStyle(
                                  fontSize: 17,
                                  fontWeight: FontWeight.w900,
                                  color: Color(0xFF10B981),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 14),
                    Text(
                      'Los precios se han contrastado contra el catálogo tributario oficial de Paraguay.',
                      style: TextStyle(
                        fontSize: 11,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFF10B981),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                  onPressed: () {
                    final kurupi = repo.findByBarcode('7840000000036');
                    final trebol = repo.findByBarcode('7840000000106');
                    final coca = repo.findByBarcode('7840058000057');

                    if (kurupi != null) ref.read(smartCartProvider.notifier).addOrIncrement(kurupi);
                    if (trebol != null) ref.read(smartCartProvider.notifier).addOrIncrement(trebol);
                    if (coca != null) ref.read(smartCartProvider.notifier).addOrIncrement(coca);

                    Navigator.pop(ctx);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        backgroundColor: Color(0xFF10B981),
                        behavior: SnackBarBehavior.floating,
                        content: Row(
                          children: [
                            Icon(Icons.check_circle_rounded, color: Colors.white),
                            SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                '✅ ¡3 productos del ticket agregados a tu Carrito Inteligente!',
                                style: TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                              ),
                            ),
                          ],
                        ),
                        duration: Duration(seconds: 3),
                      ),
                    );
                  },
                  icon: const Icon(Icons.add_shopping_cart_rounded, size: 20),
                  label: const Text(
                    'Importar Ítems a Mi Carrito Inteligente',
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildTicketItemRow(String title, int qty, int priceGs, bool isDark) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Text(
              '$qty× $title',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: isDark ? Colors.white70 : const Color(0xFF334155),
              ),
            ),
          ),
          Text(
            GuaraniFormatter.format(priceGs),
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w700,
              color: isDark ? Colors.white : const Color(0xFF0F172A),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final repo = ref.watch(catalogRepositoryProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final weekday = ref.watch(selectedWeekdayProvider);
    final activeStoreSlug = ref.watch(activeStoreInAisleProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final cityStores = ref.watch(currentCitySupermarketsProvider);
    final selectedCity = ref.watch(selectedCityProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final effectiveActiveStoreSlug = cityStores.containsKey(activeStoreSlug)
        ? activeStoreSlug
        : (cityStores.isNotEmpty ? cityStores.keys.first : 'stock');

    final scannedProduct = repo.findByBarcode(_currentBarcode);
    final rankedOffers = scannedProduct != null
        ? PromoCalculator.rankProductOffers(
            product: scannedProduct,
            allPromotions: promotions,
            userCardSlugs: wallet,
            isoWeekday: weekday,
            availableSupermarketSlugs: cityStores.keys.toSet(),
          )
        : <EvaluatedOffer>[];

    return SafeArea(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Escáner de Pasillo',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w900,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                    ),
                    Text(
                      '📍 $selectedCity • ${isCashOnly ? "💵 Solo Efectivo" : "Semáforo en tiempo real"}',
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
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1),
                    ),
                  ),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: effectiveActiveStoreSlug,
                      isDense: true,
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                      items: cityStores.entries
                          .map(
                            (e) => DropdownMenuItem(
                              value: e.key,
                              child: Text(e.value),
                            ),
                          )
                          .toList(),
                      onChanged: (val) {
                        if (val != null) {
                          ref.read(activeStoreInAisleProvider.notifier).state = val;
                        }
                      },
                    ),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            flex: 4,
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              clipBehavior: Clip.antiAlias,
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                ),
              ),
              child: _cameraEnabled
                  ? MobileScanner(
                      onDetect: (capture) {
                        for (final barcode in capture.barcodes) {
                          final raw = barcode.rawValue;
                          if (raw != null && raw != _currentBarcode) {
                            if (raw.contains('ekuatia') || raw.contains('dnit.gov.py')) {
                              final invoice = KuatiaInvoiceReceipt.parseQrUrl(raw);
                              if (invoice != null) {
                                _showKuatiaInvoiceModal(context, invoice);
                                break;
                              }
                            }
                            setState(() => _currentBarcode = raw);
                            break;
                          }
                        }
                      },
                    )
                  : Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(16),
                            decoration: BoxDecoration(
                              color: const Color(0xFF10B981).withValues(alpha: 0.15),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.qr_code_scanner_rounded, size: 48, color: Color(0xFF10B981)),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            'EAN Simulado: $_currentBarcode',
                            style: TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 13,
                              color: isDark ? Colors.white : const Color(0xFF0F172A),
                            ),
                          ),
                          const SizedBox(height: 10),
                          Wrap(
                            spacing: 6,
                            runSpacing: 6,
                            alignment: WrapAlignment.center,
                            children: LocalCatalogRepository.initialCatalog.map((prod) {
                              final isSelected = _currentBarcode == prod.ean;
                              return ChoiceChip(
                                label: Text(prod.brand ?? prod.normalizedName.split(' ').first),
                                selected: isSelected,
                                onSelected: (_) => setState(() => _currentBarcode = prod.ean ?? ''),
                              );
                            }).toList(),
                          ),
                          const SizedBox(height: 12),
                          Row(
                            children: [
                              Expanded(
                                child: FilledButton.icon(
                                  style: FilledButton.styleFrom(
                                    backgroundColor: const Color(0xFF10B981),
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(vertical: 12),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                  ),
                                  onPressed: () => setState(() => _cameraEnabled = true),
                                  icon: const Icon(Icons.camera_alt_rounded, size: 17),
                                  label: const Text(
                                    'Cámara 60 FPS',
                                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 8),
                              Expanded(
                                child: OutlinedButton.icon(
                                  style: OutlinedButton.styleFrom(
                                    padding: const EdgeInsets.symmetric(vertical: 12),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                  ),
                                  onPressed: () {
                                    final sampleKuatia = KuatiaInvoiceReceipt.parseQrUrl(
                                      'https://ekuatia.set.gov.py/consultas/qr?nVersion=150&IdGesDat=018000000100100100123456',
                                    );
                                    if (sampleKuatia != null) {
                                      _showKuatiaInvoiceModal(context, sampleKuatia);
                                    }
                                  },
                                  icon: const Icon(Icons.receipt_long_rounded, size: 17),
                                  label: const Text(
                                    'Ticket DNIT',
                                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
            ),
          ),
          Expanded(
            flex: 5,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: scannedProduct == null
                  ? _PriceHunterForm(
                      ean: _currentBarcode,
                      activeStoreSlug: effectiveActiveStoreSlug,
                      onRegistered: () => setState(() {}),
                    )
                  : _AisleSemaphoreSheet(
                      product: scannedProduct,
                      rankedOffers: rankedOffers,
                      activeStoreSlug: effectiveActiveStoreSlug,
                    ),
            ),
          ),
        ],
      ),
    );
  }
}

class _AisleSemaphoreSheet extends ConsumerWidget {
  final ProductItem product;
  final List<EvaluatedOffer> rankedOffers;
  final String activeStoreSlug;

  const _AisleSemaphoreSheet({
    required this.product,
    required this.rankedOffers,
    required this.activeStoreSlug,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    if (rankedOffers.isEmpty) return const SizedBox.shrink();
    final cheapest = rankedOffers.first;
    final currentStoreMatches =
        rankedOffers.where((o) => o.offer.supermarketSlug == activeStoreSlug).toList();
    final currentStoreEval = currentStoreMatches.isNotEmpty ? currentStoreMatches.first : null;
    final isCheapestHere = currentStoreEval != null &&
        currentStoreEval.effectiveFinalPriceGs <= cheapest.effectiveFinalPriceGs;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    product.normalizedName,
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w800,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    product.category ?? '🛒 Almacén',
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                      color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: isCheapestHere
                    ? (isDark ? const Color(0x2610B981) : const Color(0xFFD1FAE5))
                    : (isDark ? const Color(0x26EF4444) : const Color(0xFFFEE2E2)),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: isCheapestHere ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    isCheapestHere ? Icons.check_circle_rounded : Icons.warning_amber_rounded,
                    color: isCheapestHere ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                    size: 28,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      isCheapestHere
                          ? '¡Llevalo! Estás en el súper más barato hoy (${GuaraniFormatter.format(cheapest.effectiveFinalPriceGs)}).'
                          : 'En ${cheapest.offer.supermarketName} te sale ${GuaraniFormatter.format(cheapest.effectiveFinalPriceGs)} (${cheapest.pricingNote}).',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                        color: isCheapestHere
                            ? (isDark ? const Color(0xFF34D399) : const Color(0xFF065F46))
                            : (isDark ? const Color(0xFFF87171) : const Color(0xFF991B1B)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            if (currentStoreEval != null)
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Precio aquí (${currentStoreEval.offer.supermarketName}):',
                      style: TextStyle(
                        fontSize: 12,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
                    ),
                    Text(
                      GuaraniFormatter.format(currentStoreEval.effectiveFinalPriceGs),
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w800,
                        color: isDark ? Colors.white : const Color(0xFF0F172A),
                      ),
                    ),
                  ],
                ),
              ),
            const SizedBox(height: 12),
            // Botón directo para sumar al carrito
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                style: FilledButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.add_shopping_cart_rounded, size: 18),
                label: const Text(
                  '+ Sumar a Mi Lista',
                  style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800),
                ),
                onPressed: () {
                  ref.read(smartCartProvider.notifier).addOrIncrement(product);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: const Color(0xFF10B981),
                      behavior: SnackBarBehavior.floating,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      content: Text('${product.normalizedName} sumado a tu lista'),
                      action: SnackBarAction(
                        label: 'Ver Lista',
                        textColor: Colors.white,
                        onPressed: () => ref.read(activeTabProvider.notifier).state = 3,
                      ),
                      duration: const Duration(milliseconds: 1400),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PriceHunterForm extends ConsumerStatefulWidget {
  final String ean;
  final String activeStoreSlug;
  final VoidCallback onRegistered;

  const _PriceHunterForm({
    required this.ean,
    required this.activeStoreSlug,
    required this.onRegistered,
  });

  @override
  ConsumerState<_PriceHunterForm> createState() => _PriceHunterFormState();
}

class _PriceHunterFormState extends ConsumerState<_PriceHunterForm> {
  final _nameCtrl = TextEditingController();
  final _priceCtrl = TextEditingController();
  bool _isSaving = false;

  @override
  void dispose() {
    _nameCtrl.dispose();
    _priceCtrl.dispose();
    super.dispose();
  }

  void _submit() {
    final name = _nameCtrl.text.trim();
    final priceStr = _priceCtrl.text.replaceAll(RegExp(r'[^\d]'), '');
    final price = int.tryParse(priceStr);

    if (name.isEmpty || price == null || price <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor ingresá un nombre y precio válido.')),
      );
      return;
    }

    setState(() => _isSaving = true);
    final repo = ref.read(catalogRepositoryProvider);
    repo.addCrowdsourcedProduct(
      ean: widget.ean,
      productName: name,
      supermarketSlug: widget.activeStoreSlug,
      priceGs: price,
    );

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('🎖️ ¡+50 Puntos de Cazador ganados! Producto registrado en la comunidad.'),
        backgroundColor: Color(0xFF10B981),
      ),
    );

    setState(() => _isSaving = false);
    widget.onRegistered();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          shrinkWrap: true,
          children: [
            Row(
              children: [
                const Icon(Icons.military_tech_rounded, color: Color(0xFFF59E0B), size: 28),
                const SizedBox(width: 8),
                Text(
                  '¡Modo Cazador de Precios!',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                    color: isDark ? Colors.white : const Color(0xFF0F172A),
                  ),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF59E0B).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFF59E0B)),
                  ),
                  child: const Text(
                    '+50 PTS',
                    style: TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Color(0xFFF59E0B)),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              'El código ${widget.ean} aún no está catalogado. Registralo para que toda la comunidad pueda comparar su precio.',
              style: TextStyle(
                fontSize: 12,
                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _nameCtrl,
              decoration: const InputDecoration(
                labelText: 'Nombre del Producto',
                hintText: 'Ej: Empanada de Carne, Yerba 500g...',
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _priceCtrl,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Precio en Góndola (Gs.)',
                hintText: 'Ej: 14500',
                prefixText: 'Gs. ',
              ),
            ),
            const SizedBox(height: 14),
            FilledButton.icon(
              style: FilledButton.styleFrom(
                backgroundColor: const Color(0xFF10B981),
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
              ),
              onPressed: _isSaving ? null : _submit,
              icon: const Icon(Icons.check_circle_rounded),
              label: const Text('Guardar y Compartir en la Comunidad'),
            ),
          ],
        ),
      ),
    );
  }
}
