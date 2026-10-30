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

  @override
  Widget build(BuildContext context) {
    final repo = ref.watch(catalogRepositoryProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final weekday = ref.watch(selectedWeekdayProvider);
    final activeStoreSlug = ref.watch(activeStoreInAisleProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final supermarkets = ref.watch(supermarketsProvider);

    final scannedProduct = repo.findByBarcode(_currentBarcode);
    final rankedOffers = scannedProduct != null
        ? PromoCalculator.rankProductOffers(
            product: scannedProduct,
            allPromotions: promotions,
            userCardSlugs: wallet,
            isoWeekday: weekday,
          )
        : <EvaluatedOffer>[];

    return SafeArea(
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Escáner de Pasillo',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
                ),
                DropdownButton<String>(
                  value: activeStoreSlug,
                  underline: const SizedBox.shrink(),
                  items: supermarkets.entries
                      .map(
                        (e) => DropdownMenuItem(
                          value: e.key,
                          child: Text('Estoy en: ${e.value}'),
                        ),
                      )
                      .toList(),
                  onChanged: (val) {
                    if (val != null) {
                      ref.read(activeStoreInAisleProvider.notifier).state = val;
                    }
                  },
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
                color: const Color(0xFF161B22),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF30363D)),
              ),
              child: _cameraEnabled
                  ? MobileScanner(
                      onDetect: (capture) {
                        for (final barcode in capture.barcodes) {
                          final raw = barcode.rawValue;
                          if (raw != null && raw != _currentBarcode) {
                            setState(() => _currentBarcode = raw);
                            break;
                          }
                        }
                      },
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.qr_code_scanner_rounded, size: 64, color: Color(0xFF3FB950)),
                        const SizedBox(height: 12),
                        Text(
                          'EAN Simulado: $_currentBarcode',
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 8,
                          children: LocalCatalogRepository.initialCatalog.map((prod) {
                            return ActionChip(
                              label: Text(prod.brand ?? prod.normalizedName),
                              onPressed: () => setState(() => _currentBarcode = prod.ean ?? ''),
                            );
                          }).toList(),
                        ),
                        const SizedBox(height: 12),
                        FilledButton.icon(
                          onPressed: () => setState(() => _cameraEnabled = true),
                          icon: const Icon(Icons.camera_alt_rounded),
                          label: const Text('Activar Cámara en Vivo (60 FPS)'),
                        ),
                      ],
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
                      activeStoreSlug: activeStoreSlug,
                      onRegistered: () => setState(() {}),
                    )
                  : _AisleSemaphoreSheet(
                      product: scannedProduct,
                      rankedOffers: rankedOffers,
                      activeStoreSlug: activeStoreSlug,
                    ),
            ),
          ),
        ],
      ),
    );
  }
}

class _AisleSemaphoreSheet extends StatelessWidget {
  final ProductItem product;
  final List<EvaluatedOffer> rankedOffers;
  final String activeStoreSlug;

  const _AisleSemaphoreSheet({
    required this.product,
    required this.rankedOffers,
    required this.activeStoreSlug,
  });

  @override
  Widget build(BuildContext context) {
    if (rankedOffers.isEmpty) return const SizedBox.shrink();
    final cheapest = rankedOffers.first;
    final currentStoreMatches =
        rankedOffers.where((o) => o.offer.supermarketSlug == activeStoreSlug).toList();
    final currentStoreEval = currentStoreMatches.isNotEmpty ? currentStoreMatches.first : null;
    final isCheapestHere = currentStoreEval != null &&
        currentStoreEval.effectiveFinalPriceGs <= cheapest.effectiveFinalPriceGs;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              product.normalizedName,
              style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isCheapestHere
                    ? const Color(0x3300875A)
                    : const Color(0x26FF5252),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: isCheapestHere ? const Color(0xFF3FB950) : Colors.redAccent,
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    isCheapestHere ? Icons.check_circle_rounded : Icons.warning_amber_rounded,
                    color: isCheapestHere ? const Color(0xFF3FB950) : Colors.redAccent,
                    size: 28,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      isCheapestHere
                          ? '¡Llevalo! Estás en el súper más barato hoy (${GuaraniFormatter.format(cheapest.effectiveFinalPriceGs)}).'
                          : 'En ${cheapest.offer.supermarketName} te sale ${GuaraniFormatter.format(cheapest.effectiveFinalPriceGs)} (${cheapest.pricingNote}).',
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            if (currentStoreEval != null)
              Text(
                'Precio aquí (${currentStoreEval.offer.supermarketName}): ${GuaraniFormatter.format(currentStoreEval.effectiveFinalPriceGs)} • En caja: ${GuaraniFormatter.format(currentStoreEval.cashOutflowAtPosGs)}',
                style: const TextStyle(fontSize: 13, color: Colors.white70),
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
        backgroundColor: Color(0xFF00875A),
      ),
    );

    setState(() => _isSaving = false);
    widget.onRegistered();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          shrinkWrap: true,
          children: [
            Row(
              children: [
                const Icon(Icons.military_tech_rounded, color: Colors.amberAccent, size: 28),
                const SizedBox(width: 8),
                const Text(
                  '¡Modo Cazador de Precios!',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800),
                ),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: const Color(0x33FFC107),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.amberAccent),
                  ),
                  child: const Text(
                    '+50 PTS',
                    style: TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.amberAccent),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              'El código ${widget.ean} aún no está catalogado. Registralo para que toda la comunidad pueda comparar su precio.',
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _nameCtrl,
              decoration: InputDecoration(
                labelText: 'Nombre del Producto',
                hintText: 'Ej: Empanada de Carne, Yerba 500g...',
                filled: true,
                fillColor: const Color(0xFF0D1117),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _priceCtrl,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: 'Precio en Góndola (Gs.)',
                hintText: 'Ej: 14500',
                prefixText: 'Gs. ',
                filled: true,
                fillColor: const Color(0xFF0D1117),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
            const SizedBox(height: 14),
            FilledButton.icon(
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

