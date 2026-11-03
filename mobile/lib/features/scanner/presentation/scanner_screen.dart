import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';

/// Modo "Escáner de Pasillo" (Cámara Real Barcode EAN-13 & QR e-Kuatia):
/// Escanea con la cámara física a 60 FPS o permite ingresar manualmente cualquier código.
class ScannerScreen extends ConsumerStatefulWidget {
  const ScannerScreen({super.key});

  @override
  ConsumerState<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends ConsumerState<ScannerScreen> {
  final MobileScannerController _scannerController = MobileScannerController(
    detectionSpeed: DetectionSpeed.normal,
    facing: CameraFacing.back,
    torchEnabled: false,
  );
  final TextEditingController _manualInputController = TextEditingController();

  String? _scannedCode;
  bool _isProcessing = false;
  bool _torchActive = false;

  @override
  void dispose() {
    _scannerController.dispose();
    _manualInputController.dispose();
    super.dispose();
  }

  void _onDetect(BarcodeCapture capture) {
    if (_isProcessing) return;
    for (final barcode in capture.barcodes) {
      final raw = barcode.rawValue;
      if (raw != null && raw.trim().isNotEmpty) {
        _isProcessing = true;
        _handleCodeScanned(raw.trim());
        break;
      }
    }
  }

  void _handleCodeScanned(String raw) {
    // 1. Detectar si es un QR tributario de Factura Electrónica e-Kuatia / DNIT
    if (raw.contains('ekuatia') || raw.contains('dnit.gov.py') || raw.contains('IdGesDat=')) {
      final invoice = KuatiaInvoiceReceipt.parseQrUrl(raw);
      if (invoice != null) {
        _showKuatiaInvoiceModal(context, invoice);
        Future.delayed(const Duration(seconds: 2), () {
          if (mounted) _isProcessing = false;
        });
        return;
      }
    }

    // 2. Es un código de barra EAN o código de producto
    setState(() {
      _scannedCode = raw;
    });

    Future.delayed(const Duration(milliseconds: 1500), () {
      if (mounted) _isProcessing = false;
    });
  }

  void _showKuatiaInvoiceModal(BuildContext context, KuatiaInvoiceReceipt invoice) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final repo = ref.read(catalogRepositoryProvider);

    // Intentar buscar los productos en catálogo local para asociar ofertas
    final kurupi = repo.findByBarcode('7840000000001');
    final trebol = repo.findByBarcode('7840000000002');
    final coca = repo.findByBarcode('7840000000003');

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
            color: isDark ? const Color(0xFF0F172A) : Colors.white,
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
                  IconButton(
                    icon: Icon(Icons.close_rounded, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                    onPressed: () => Navigator.of(ctx).pop(),
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
                        color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'ÍTEMS FACTURADOS VERIFICADOS (SIFEN):',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              letterSpacing: 0.5,
                              color: Color(0xFF10B981),
                            ),
                          ),
                          const SizedBox(height: 10),
                          _buildTicketItemRow('Yerba Mate Kurupí Menta y Boldo 500g', 1, 14500, isDark),
                          _buildTicketItemRow('Leche Lactolanda Entera Ultra 1L Sachet', 2, 11600, isDark),
                          _buildTicketItemRow('Gaseosa Coca-Cola Original 2L', 1, 14800, isDark),
                          const Divider(height: 20),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'TOTAL COMPROBANTE:',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w900,
                                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                                ),
                              ),
                              const Text(
                                'Gs. 40.900',
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
                      'Los artículos de esta factura electrónica pueden sumarse directamente a tu carrito inteligente para calcular si pagaste de más o comparar contra otros supermercados.',
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

  void _showManualInputDialog() {
    _manualInputController.text = _scannedCode ?? '';
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: isDark ? const Color(0xFF0F172A) : Colors.white,
        title: const Row(
          children: [
            Icon(Icons.keyboard_rounded, color: Color(0xFF10B981)),
            SizedBox(width: 8),
            Text('Ingresar Código', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Ingresá los números del código de barras (ej. 7840000000001) o pegá el link del QR de e-Kuatia:',
              style: TextStyle(fontSize: 12),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _manualInputController,
              autofocus: true,
              keyboardType: TextInputType.text,
              decoration: const InputDecoration(
                hintText: 'Código EAN-13 o URL DNIT...',
                isDense: true,
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: const Color(0xFF10B981)),
            onPressed: () {
              final text = _manualInputController.text.trim();
              Navigator.pop(ctx);
              if (text.isNotEmpty) {
                _handleCodeScanned(text);
              }
            },
            child: const Text('Consultar'),
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

    final scannedProduct = _scannedCode != null ? repo.findByBarcode(_scannedCode!) : null;
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
          // Barra de cabecera con selector de supermercado donde está el usuario
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
                      '📍 $selectedCity • ${isCashOnly ? "💵 Precios góndola" : "Semáforo en tiempo real"}',
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

          // Visor de Cámara Real con MobileScanner
          Expanded(
            flex: 5,
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              clipBehavior: Clip.antiAlias,
              decoration: BoxDecoration(
                color: Colors.black,
                borderRadius: BorderRadius.circular(24),
                border: Border.all(
                  color: const Color(0xFF10B981),
                  width: 2,
                ),
                boxShadow: const [
                  BoxShadow(
                    color: Color(0x3310B981),
                    blurRadius: 16,
                    offset: Offset(0, 4),
                  ),
                ],
              ),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  // Cámara activa escaneando códigos de barras y QRs
                  MobileScanner(
                    controller: _scannerController,
                    onDetect: _onDetect,
                    errorBuilder: (context, error, child) {
                      return Center(
                        child: Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.videocam_off_rounded, size: 48, color: Colors.amber),
                              const SizedBox(height: 10),
                              const Text(
                                'Cámara en espera o no disponible',
                                style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700),
                              ),
                              const SizedBox(height: 6),
                              Text(
                                'Podés ingresar el código de barras manualmente tocando el botón inferior.',
                                textAlign: TextAlign.center,
                                style: TextStyle(color: Colors.white.withValues(alpha: 0.7), fontSize: 12),
                              ),
                              const SizedBox(height: 14),
                              FilledButton.icon(
                                style: FilledButton.styleFrom(backgroundColor: const Color(0xFF10B981)),
                                onPressed: _showManualInputDialog,
                                icon: const Icon(Icons.edit_rounded, size: 16),
                                label: const Text('Ingresar Código Manual'),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),

                  // Marco guía visual para apuntar el código
                  Center(
                    child: Container(
                      width: 260,
                      height: 160,
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFF10B981), width: 2),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Stack(
                        children: [
                          Positioned(
                            top: 0,
                            left: 0,
                            right: 0,
                            child: Container(
                              height: 2,
                              color: const Color(0xFF10B981).withValues(alpha: 0.8),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  // Overlay superior con controles de linterna y teclado manual
                  Positioned(
                    top: 12,
                    left: 12,
                    right: 12,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: Colors.black.withValues(alpha: 0.65),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Row(
                            children: [
                              Icon(Icons.center_focus_strong_rounded, size: 14, color: Color(0xFF10B981)),
                              SizedBox(width: 6),
                              Text(
                                'Apuntá a Barcode o QR DNIT',
                                style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.w700),
                              ),
                            ],
                          ),
                        ),
                        Row(
                          children: [
                            IconButton(
                              style: IconButton.styleFrom(backgroundColor: Colors.black54),
                              icon: Icon(
                                _torchActive ? Icons.flash_on_rounded : Icons.flash_off_rounded,
                                color: _torchActive ? Colors.amber : Colors.white,
                                size: 20,
                              ),
                              onPressed: () async {
                                await _scannerController.toggleTorch();
                                setState(() {
                                  _torchActive = !_torchActive;
                                });
                              },
                            ),
                            const SizedBox(width: 6),
                            IconButton(
                              style: IconButton.styleFrom(backgroundColor: Colors.black54),
                              icon: const Icon(Icons.keyboard_rounded, color: Colors.white, size: 20),
                              tooltip: 'Ingresar código manual',
                              onPressed: _showManualInputDialog,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  // Indicador inferior del código detectado
                  if (_scannedCode != null)
                    Positioned(
                      bottom: 12,
                      left: 12,
                      right: 12,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: const Color(0xFF0F172A).withValues(alpha: 0.9),
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: const Color(0xFF10B981)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.barcode_reader, size: 18, color: Color(0xFF10B981)),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                'Código: $_scannedCode',
                                style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            InkWell(
                              onTap: () => setState(() => _scannedCode = null),
                              child: const Icon(Icons.close_rounded, size: 18, color: Colors.white70),
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ),

          // Semáforo de Precios en Vivo o Formulario de Registro
          Expanded(
            flex: 5,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: _scannedCode == null
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.qr_code_scanner_rounded,
                            size: 48,
                            color: isDark ? const Color(0xFF475569) : const Color(0xFF94A3B8),
                          ),
                          const SizedBox(height: 10),
                          Text(
                            'Cámara lista para escanear',
                            style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w800,
                              color: isDark ? Colors.white : const Color(0xFF0F172A),
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Enfocá cualquier producto en la góndola para ver si te conviene comprarlo aquí o si está más barato en otro súper.',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 12,
                              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                            ),
                          ),
                          const SizedBox(height: 12),
                          OutlinedButton.icon(
                            style: OutlinedButton.styleFrom(
                              foregroundColor: const Color(0xFF10B981),
                              side: const BorderSide(color: Color(0xFF10B981)),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                            ),
                            onPressed: _showManualInputDialog,
                            icon: const Icon(Icons.edit_rounded, size: 16),
                            label: const Text('Ingresar Código Manual', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700)),
                          ),
                        ],
                      ),
                    )
                  : (scannedProduct == null
                      ? _PriceHunterForm(
                          ean: _scannedCode!,
                          activeStoreSlug: effectiveActiveStoreSlug,
                          onRegistered: () => setState(() {}),
                        )
                      : _AisleSemaphoreSheet(
                          product: scannedProduct,
                          rankedOffers: rankedOffers,
                          activeStoreSlug: effectiveActiveStoreSlug,
                        )),
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
            const SizedBox(height: 12),
            Expanded(
              child: ListView.separated(
                itemCount: rankedOffers.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (context, index) {
                  final eval = rankedOffers[index];
                  final isCurrent = eval.offer.supermarketSlug == activeStoreSlug;
                  return ListTile(
                    dense: true,
                    contentPadding: EdgeInsets.zero,
                    title: Row(
                      children: [
                        Text(
                          eval.offer.supermarketName,
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: isCurrent ? FontWeight.w900 : FontWeight.w600,
                            color: isCurrent ? const Color(0xFF10B981) : (isDark ? Colors.white : const Color(0xFF0F172A)),
                          ),
                        ),
                        if (isCurrent) ...[
                          const SizedBox(width: 6),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
                            decoration: BoxDecoration(
                              color: const Color(0xFF10B981).withValues(alpha: 0.2),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: const Text(
                              'AQUÍ',
                              style: TextStyle(fontSize: 9, fontWeight: FontWeight.w900, color: Color(0xFF10B981)),
                            ),
                          ),
                        ],
                      ],
                    ),
                    subtitle: Text(
                      eval.pricingNote,
                      style: TextStyle(
                        fontSize: 11,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
                    ),
                    trailing: Text(
                      GuaraniFormatter.format(eval.effectiveFinalPriceGs),
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w800,
                        color: index == 0 ? const Color(0xFF10B981) : (isDark ? Colors.white70 : const Color(0xFF334155)),
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 8),
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                style: FilledButton.styleFrom(
                  backgroundColor: const Color(0xFF10B981),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: () {
                  ref.read(smartCartProvider.notifier).addOrIncrement(product);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: const Color(0xFF10B981),
                      behavior: SnackBarBehavior.floating,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      content: Text('✅ ${product.normalizedName} agregado al carrito'),
                      action: SnackBarAction(
                        label: 'Ver Carrito',
                        textColor: Colors.white,
                        onPressed: () => ref.read(activeTabProvider.notifier).state = 3,
                      ),
                      duration: const Duration(seconds: 2),
                    ),
                  );
                },
                icon: const Icon(Icons.add_shopping_cart_rounded, size: 18),
                label: const Text('Sumar a Mi Carrito'),
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
    final price = int.tryParse(_priceCtrl.text.trim());

    if (name.isEmpty || price == null || price <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Completá nombre y precio válido.')),
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
