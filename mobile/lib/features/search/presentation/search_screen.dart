import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/formatters/guarani_formatter.dart';
import '../../../data/local/local_catalog_repository.dart';
import '../../../domain/models/catalog_models.dart';
import '../../../domain/services/promo_calculator.dart';
import '../../../state/app_providers.dart';
import '../../onboarding/presentation/tutorial_tour_sheet.dart';
import 'product_detail_sheet.dart';

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  late final TextEditingController _searchController;
  late final FocusNode _searchFocusNode;
  Timer? _debounceTimer;

  @override
  void initState() {
    super.initState();
    _searchController = TextEditingController();
    _searchFocusNode = FocusNode();
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _searchController.dispose();
    _searchFocusNode.dispose();
    super.dispose();
  }

  void _onSearchInputChanged(String value) {
    ref.read(searchQueryProvider.notifier).state = value;
    _debounceTimer?.cancel();
    final clean = value.trim();
    if (clean.length >= 3) {
      // Si la búsqueda local no arroja resultados, consultar automáticamente en línea en 600ms
      _debounceTimer = Timer(const Duration(milliseconds: 600), () {
        final currentProducts = ref.read(filteredProductsProvider);
        if (currentProducts.isEmpty && clean.isNotEmpty) {
          ref.read(onlineSearchActionProvider)(clean);
        }
      });
    }
  }

  static const Map<int, String> _weekdayLabels = {
    1: 'Lun',
    2: 'Mar',
    3: 'Mié',
    4: 'Jue',
    5: 'Vie',
    6: 'Sáb',
    7: 'Dom',
  };

  static const List<Map<String, dynamic>> productCategories = [
    {
      'key': '',
      'label': 'Todos los Productos',
      'icon': '🛒',
      'subtitle': 'Catálogo completo de ofertas y precios',
      'color': Color(0xFF10B981),
    },
    {
      'key': 'yerba',
      'label': 'Yerba Mate',
      'icon': '🌿',
      'subtitle': 'Kurupí, Campesino, Pajarito, Selecta',
      'color': Color(0xFF16A34A),
    },
    {
      'key': 'lacteos',
      'label': 'Lácteos y Quesos',
      'icon': '🥛',
      'subtitle': 'Trébol, Lactolanda, Yogures, Queso Py, Manteca',
      'color': Color(0xFF0284C7),
    },
    {
      'key': 'carniceria',
      'label': 'Carnicería y Granja',
      'icon': '🥩',
      'subtitle': 'Costilla al vacío Chortitzer, Pechuga Pechugon',
      'color': Color(0xFFDC2626),
    },
    {
      'key': 'bebidas',
      'label': 'Bebidas y Jugos',
      'icon': '🥤',
      'subtitle': 'Coca-Cola, Pulp Pomelo, Sprite, Jugo Puro Sol',
      'color': Color(0xFFEA580C),
    },
    {
      'key': 'cerveza',
      'label': 'Cervezas y Vinos',
      'icon': '🍺',
      'subtitle': 'Pilsen 940ml, Brahma Chopp, Santa Helena Cabernet',
      'color': Color(0xFFD97706),
    },
    {
      'key': 'almacen',
      'label': 'Almacén y Despensa',
      'icon': '🌾',
      'subtitle': 'Arroz Tío Nico, Fideos Anita, Harina, Azúcar, Café',
      'color': Color(0xFF7C3AED),
    },
    {
      'key': 'panaderia',
      'label': 'Panadería Fresca',
      'icon': '🥖',
      'subtitle': 'Pan Felipe francés tradicional, Galleta cuartel',
      'color': Color(0xFFB45309),
    },
    {
      'key': 'limpieza',
      'label': 'Limpieza del Hogar',
      'icon': '🧼',
      'subtitle': 'Jabón líquido Omo Matic 3L, Detergente Zorro',
      'color': Color(0xFF0D9488),
    },
    {
      'key': 'galletitas',
      'label': 'Snacks y Galletitas',
      'icon': '🍪',
      'subtitle': 'Galletitas Oreo rellenas, Papas fritas Lay\'s',
      'color': Color(0xFFE11D48),
    },
    {
      'key': 'frutas',
      'label': 'Frutas y Verduras',
      'icon': '🍎',
      'subtitle': 'Tomate Santa Cruz selección, Banana Karape',
      'color': Color(0xFF65A30D),
    },
  ];

  void _showCategoriesBottomSheet(BuildContext context, WidgetRef ref) {
    final currentCat = ref.read(selectedCategoryProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          constraints: BoxConstraints(
            maxHeight: MediaQuery.of(context).size.height * 0.80,
          ),
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
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.category_rounded, color: Color(0xFF10B981), size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Categorías de Productos',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          'Elegí un rubro para filtrar los precios al instante',
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
                child: ListView.separated(
                  itemCount: productCategories.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 8),
                  itemBuilder: (context, index) {
                    final cat = productCategories[index];
                    final key = cat['key'] as String;
                    final label = cat['label'] as String;
                    final icon = cat['icon'] as String;
                    final subtitle = cat['subtitle'] as String;
                    final color = cat['color'] as Color;
                    final isSelected = currentCat == key;

                    return Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: () {
                          ref.read(selectedCategoryProvider.notifier).state = key;
                          Navigator.of(ctx).pop();
                        },
                        borderRadius: BorderRadius.circular(16),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? color.withValues(alpha: isDark ? 0.25 : 0.12)
                                : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: isSelected
                                  ? color
                                  : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                              width: isSelected ? 1.5 : 1,
                            ),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 44,
                                height: 44,
                                alignment: Alignment.center,
                                decoration: BoxDecoration(
                                  color: color.withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  icon,
                                  style: const TextStyle(fontSize: 22),
                                ),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      label,
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w800,
                                        color: isSelected
                                            ? color
                                            : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                      ),
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      subtitle,
                                      style: TextStyle(
                                        fontSize: 11,
                                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ],
                                ),
                              ),
                              if (isSelected)
                                Icon(Icons.check_circle_rounded, color: color, size: 22)
                              else
                                Icon(
                                  Icons.chevron_right_rounded,
                                  color: isDark ? const Color(0xFF475569) : const Color(0xFFCBD5E1),
                                  size: 20,
                                ),
                            ],
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

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
                          'Solo verás supermercados con sucursal física cercana',
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
              // Botón de Detección GPS Automática
              Container(
                width: double.infinity,
                margin: const EdgeInsets.only(bottom: 12),
                child: FilledButton.icon(
                  style: FilledButton.styleFrom(
                    backgroundColor: const Color(0xFF0284C7).withValues(alpha: isDark ? 0.25 : 0.12),
                    foregroundColor: const Color(0xFF0284C7),
                    elevation: 0,
                    padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                      side: BorderSide(color: const Color(0xFF0284C7).withValues(alpha: 0.4)),
                    ),
                  ),
                  onPressed: () {
                    ref.read(selectedCityProvider.notifier).state = 'Caacupé';
                    Navigator.of(ctx).pop();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        backgroundColor: const Color(0xFF0284C7),
                        behavior: SnackBarBehavior.floating,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        content: const Row(
                          children: [
                            Icon(Icons.my_location_rounded, color: Colors.white, size: 20),
                            SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                '📍 GPS activado: Ubicación fijada en Caacupé (Cordillera)',
                                style: TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                              ),
                            ),
                          ],
                        ),
                        duration: const Duration(seconds: 3),
                      ),
                    );
                  },
                  icon: const Icon(Icons.my_location_rounded, size: 18),
                  label: const Text(
                    'Detectar mi ubicación automáticamente (GPS)',
                    style: TextStyle(fontSize: 13, fontWeight: FontWeight.w800),
                  ),
                ),
              ),
              ...LocalCatalogRepository.paraguayCities.map((item) {
                final cityName = item['city']!;
                final dept = item['dept']!;
                final badge = item['badge']!;
                final isSelected = cityName.toLowerCase() == currentCity.toLowerCase();

                return Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(14),
                    onTap: () {
                      ref.read(selectedCityProvider.notifier).state = cityName;
                      Navigator.of(ctx).pop();
                    },
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? (isDark ? const Color(0x260284C7) : const Color(0xFFE0F2FE))
                            : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(
                          color: isSelected
                              ? const Color(0xFF0284C7)
                              : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                          width: isSelected ? 1.5 : 1.0,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            cityName == 'Todas' ? Icons.public_rounded : Icons.location_city_rounded,
                            color: isSelected ? const Color(0xFF0284C7) : const Color(0xFF64748B),
                            size: 20,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Text(
                                      cityName,
                                      style: TextStyle(
                                        fontSize: 15,
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

  String _getSupermarketEmoji(String slug) {
    switch (slug) {
      case 'biggie':
        return '🟡';
      case 'superseis':
        return '🟢';
      case 'stock':
        return '🔴';
      case 'fortis':
        return '🔵';
      case 'tuti':
        return '🟠';
      case 'real':
        return '🟣';
      case 'casarica':
        return '⚪';
      case 'arete':
        return '🟢';
      case 'box':
        return '🔵';
      case 'salemma':
        return '🟤';
      case 'labomba':
        return '🔴';
      default:
        return '🏪';
    }
  }

  void _showBrandsBottomSheet(BuildContext context, WidgetRef ref) {
    final currentBrand = ref.read(selectedBrandProvider);
    final repo = ref.read(catalogRepositoryProvider);
    final brandsMap = repo.getUniqueBrands();
    final brandsList = brandsMap.keys.toList();
    final isDark = Theme.of(context).brightness == Brightness.dark;
    String brandSearch = '';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            final filtered = brandsList.where((b) {
              if (brandSearch.isEmpty) return true;
              return b.toLowerCase().contains(brandSearch.toLowerCase());
            }).toList();

            return Container(
              constraints: BoxConstraints(
                maxHeight: MediaQuery.of(context).size.height * 0.82,
              ),
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF0F172A) : Colors.white,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
                boxShadow: const [
                  BoxShadow(color: Colors.black45, blurRadius: 20, offset: Offset(0, -4)),
                ],
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
                          color: const Color(0xFFF59E0B).withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(Icons.sell_rounded, color: Color(0xFFF59E0B), size: 24),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Marcas del Catálogo',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            Text(
                              '${brandsList.length} marcas registradas con precios en vivo',
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
                  const SizedBox(height: 12),
                  // Barra de búsqueda dentro del modal de marcas
                  TextField(
                    onChanged: (val) {
                      setModalState(() {
                        brandSearch = val.trim();
                      });
                    },
                    style: TextStyle(color: isDark ? Colors.white : const Color(0xFF0F172A), fontSize: 13),
                    decoration: InputDecoration(
                      hintText: 'Filtrar marca (ej: Campesino, Coca Cola, Trebol)...',
                      hintStyle: TextStyle(color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8), fontSize: 13),
                      prefixIcon: const Icon(Icons.search_rounded, size: 20, color: Color(0xFFF59E0B)),
                      isDense: true,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                      filled: true,
                      fillColor: isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: ListView(
                      children: [
                        // Opción de "Todas las marcas"
                        Material(
                          color: Colors.transparent,
                          child: InkWell(
                            onTap: () {
                              ref.read(selectedBrandProvider.notifier).state = null;
                              Navigator.of(ctx).pop();
                            },
                            borderRadius: BorderRadius.circular(16),
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                              margin: const EdgeInsets.only(bottom: 8),
                              decoration: BoxDecoration(
                                color: currentBrand == null
                                    ? const Color(0xFF10B981).withValues(alpha: isDark ? 0.25 : 0.12)
                                    : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC)),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(
                                  color: currentBrand == null
                                      ? const Color(0xFF10B981)
                                      : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                                  width: currentBrand == null ? 1.5 : 1,
                                ),
                              ),
                              child: Row(
                                children: [
                                  Container(
                                    width: 40,
                                    height: 40,
                                    alignment: Alignment.center,
                                    decoration: BoxDecoration(
                                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                                      borderRadius: BorderRadius.circular(10),
                                    ),
                                    child: const Text('🏷️', style: TextStyle(fontSize: 18)),
                                  ),
                                  const SizedBox(width: 14),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Todas las Marcas',
                                          style: TextStyle(
                                            fontSize: 14,
                                            fontWeight: FontWeight.w800,
                                            color: currentBrand == null
                                                ? const Color(0xFF10B981)
                                                : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                          ),
                                        ),
                                        Text(
                                          'Ver productos sin filtro de fabricante',
                                          style: TextStyle(
                                            fontSize: 11,
                                            color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  if (currentBrand == null)
                                    const Icon(Icons.check_circle_rounded, color: Color(0xFF10B981), size: 22),
                                ],
                              ),
                            ),
                          ),
                        ),
                        // Marcas de la lista
                        ...filtered.map((b) {
                          final count = brandsMap[b] ?? 1;
                          final isSelected = currentBrand != null &&
                              currentBrand.toLowerCase() == b.toLowerCase();

                          return Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: () {
                                ref.read(selectedBrandProvider.notifier).state = b;
                                Navigator.of(ctx).pop();
                              },
                              borderRadius: BorderRadius.circular(14),
                              child: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                                margin: const EdgeInsets.only(bottom: 6),
                                decoration: BoxDecoration(
                                  color: isSelected
                                      ? const Color(0xFFF59E0B).withValues(alpha: isDark ? 0.25 : 0.12)
                                      : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF8FAFC)),
                                  borderRadius: BorderRadius.circular(14),
                                  border: Border.all(
                                    color: isSelected
                                        ? const Color(0xFFF59E0B)
                                        : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                                    width: isSelected ? 1.5 : 1,
                                  ),
                                ),
                                child: Row(
                                  children: [
                                    Container(
                                      width: 36,
                                      height: 36,
                                      alignment: Alignment.center,
                                      decoration: BoxDecoration(
                                        color: const Color(0xFFF59E0B).withValues(alpha: 0.12),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: const Text('✨', style: TextStyle(fontSize: 15)),
                                    ),
                                    const SizedBox(width: 12),
                                    Expanded(
                                      child: Text(
                                        b,
                                        style: TextStyle(
                                          fontSize: 13,
                                          fontWeight: FontWeight.w700,
                                          color: isSelected
                                              ? const Color(0xFFF59E0B)
                                              : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                        ),
                                      ),
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                      decoration: BoxDecoration(
                                        color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Text(
                                        '$count prod.',
                                        style: TextStyle(
                                          fontSize: 11,
                                          fontWeight: FontWeight.w600,
                                          color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                        ),
                                      ),
                                    ),
                                    if (isSelected) ...[
                                      const SizedBox(width: 8),
                                      const Icon(Icons.check_circle_rounded, color: Color(0xFFF59E0B), size: 20),
                                    ],
                                  ],
                                ),
                              ),
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
      },
    );
  }

  void _showSupermarketsBottomSheet(BuildContext context, WidgetRef ref) {
    final currentStore = ref.read(selectedSupermarketFilterProvider);
    final allStores = ref.read(supermarketsProvider);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) {
        return Container(
          constraints: BoxConstraints(
            maxHeight: MediaQuery.of(context).size.height * 0.80,
          ),
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
                    child: const Icon(Icons.storefront_rounded, color: Color(0xFF0284C7), size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Filtrar por Supermercado',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w900,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        Text(
                          'Ver solo los productos vendidos en tu súper elegido',
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
                    // Opción: Todos los supermercados
                    Material(
                      color: Colors.transparent,
                      child: InkWell(
                        onTap: () {
                          ref.read(selectedSupermarketFilterProvider.notifier).state = '';
                          Navigator.of(ctx).pop();
                        },
                        borderRadius: BorderRadius.circular(16),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                          margin: const EdgeInsets.only(bottom: 8),
                          decoration: BoxDecoration(
                            color: currentStore.isEmpty
                                ? const Color(0xFF10B981).withValues(alpha: isDark ? 0.25 : 0.12)
                                : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: currentStore.isEmpty
                                  ? const Color(0xFF10B981)
                                  : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                              width: currentStore.isEmpty ? 1.5 : 1,
                            ),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 44,
                                height: 44,
                                alignment: Alignment.center,
                                decoration: BoxDecoration(
                                  color: const Color(0xFF10B981).withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: const Text('🏪', style: TextStyle(fontSize: 22)),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Todos los Supermercados',
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w800,
                                        color: currentStore.isEmpty
                                            ? const Color(0xFF10B981)
                                            : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                      ),
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      'Comparar precios y encontrar el más barato',
                                      style: TextStyle(
                                        fontSize: 11,
                                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              if (currentStore.isEmpty)
                                const Icon(Icons.check_circle_rounded, color: Color(0xFF10B981), size: 22),
                            ],
                          ),
                        ),
                      ),
                    ),
                    // Lista de cada supermercado
                    ...allStores.entries.map((entry) {
                      final slug = entry.key;
                      final name = entry.value;
                      final isSelected = currentStore == slug;
                      String emoji = '🏪';
                      if (slug == 'biggie') emoji = '🟡';
                      if (slug == 'superseis') emoji = '🟢';
                      if (slug == 'stock') emoji = '🔴';
                      if (slug == 'fortis') emoji = '🔵';
                      if (slug == 'tuti') emoji = '🟠';
                      if (slug == 'real') emoji = '🟣';
                      if (slug == 'casarica') emoji = '⚪';
                      if (slug == 'arete') emoji = '🟢';
                      if (slug == 'box') emoji = '🔵';
                      if (slug == 'salemma') emoji = '🟤';
                      if (slug == 'labomba') emoji = '🔴';

                      return Material(
                        color: Colors.transparent,
                        child: InkWell(
                          onTap: () {
                            ref.read(selectedSupermarketFilterProvider.notifier).state = slug;
                            Navigator.of(ctx).pop();
                          },
                          borderRadius: BorderRadius.circular(16),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                            margin: const EdgeInsets.only(bottom: 8),
                            decoration: BoxDecoration(
                              color: isSelected
                                  ? const Color(0xFF0284C7).withValues(alpha: isDark ? 0.25 : 0.12)
                                  : (isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC)),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                color: isSelected
                                    ? const Color(0xFF0284C7)
                                    : (isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                                width: isSelected ? 1.5 : 1,
                              ),
                            ),
                            child: Row(
                              children: [
                                Container(
                                  width: 44,
                                  height: 44,
                                  alignment: Alignment.center,
                                  decoration: BoxDecoration(
                                    color: const Color(0xFF0284C7).withValues(alpha: 0.15),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: Text(emoji, style: const TextStyle(fontSize: 22)),
                                ),
                                const SizedBox(width: 14),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        name,
                                        style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.w800,
                                          color: isSelected
                                              ? const Color(0xFF0284C7)
                                              : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                        ),
                                      ),
                                      const SizedBox(height: 2),
                                      Text(
                                        'Ver solo catálogo y precios de $name',
                                        style: TextStyle(
                                          fontSize: 11,
                                          color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
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
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final searchQuery = ref.watch(searchQueryProvider);
    final products = ref.watch(filteredProductsProvider);
    final isSearchingOnline = ref.watch(isSearchingOnlineProvider);
    final onlineResults = ref.watch(onlineSearchResultsProvider);
    final wallet = ref.watch(userWalletCardsProvider);
    final isCashOnly = ref.watch(cashOnlyModeProvider);
    final selectedWeekday = ref.watch(selectedWeekdayProvider);
    final promotions = ref.watch(bankPromotionsProvider);
    final selectedCity = ref.watch(selectedCityProvider);
    final cityStores = ref.watch(currentCitySupermarketsProvider);
    final themeMode = ref.watch(themeModeProvider);
    final favorites = ref.watch(favoritesProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);
    final selectedSupermarket = ref.watch(selectedSupermarketFilterProvider);
    final supermarkets = ref.watch(supermarketsProvider);
    final selectedBrand = ref.watch(selectedBrandProvider);
    final activeCatMeta = productCategories.firstWhere(
      (c) => c['key'] == selectedCategory,
      orElse: () => productCategories.first,
    );
    final selectedStoreName = selectedSupermarket.isNotEmpty
        ? (supermarkets[selectedSupermarket] ?? selectedSupermarket)
        : '';
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return SafeArea(
      child: Column(
        children: [
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
                          child: const Icon(Icons.shopping_bag_rounded, color: Color(0xFF10B981), size: 22),
                        ),
                        const SizedBox(width: 10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'PreciosPy',
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            InkWell(
                              onTap: () => _showCityPicker(context, ref),
                              borderRadius: BorderRadius.circular(6),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(Icons.location_on_rounded, size: 12, color: Color(0xFF0284C7)),
                                  const SizedBox(width: 2),
                                  Text(
                                    selectedCity == 'Todas' ? 'Todo Paraguay' : selectedCity,
                                    style: const TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.w700,
                                      color: Color(0xFF0284C7),
                                    ),
                                  ),
                                  const Icon(Icons.arrow_drop_down_rounded, size: 16, color: Color(0xFF0284C7)),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        InkWell(
                          onTap: () {
                            final next = !ref.read(cashOnlyModeProvider);
                            ref.read(cashOnlyModeProvider.notifier).state = next;
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                backgroundColor: next ? const Color(0xFF10B981) : const Color(0xFF0284C7),
                                behavior: SnackBarBehavior.floating,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                content: Text(
                                  next
                                      ? '💵 Modo Solo Efectivo: precios de góndola sin tarjetas'
                                      : '💳 Modo Tarjetas: aplicando tus promociones bancarias',
                                  style: const TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                                ),
                                duration: const Duration(milliseconds: 1400),
                              ),
                            );
                          },
                          borderRadius: BorderRadius.circular(16),
                          child: Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                            decoration: BoxDecoration(
                              color: isCashOnly
                                  ? const Color(0xFF10B981).withValues(alpha: 0.22)
                                  : const Color(0xFF10B981).withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                color: isCashOnly
                                    ? const Color(0xFF10B981)
                                    : const Color(0xFF10B981).withValues(alpha: 0.3),
                                width: isCashOnly ? 1.5 : 1.0,
                              ),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(
                                  isCashOnly ? Icons.payments_rounded : Icons.credit_card_rounded,
                                  size: 14,
                                  color: const Color(0xFF10B981),
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  isCashOnly ? '💵 Efectivo' : '${wallet.length} tarjetas',
                                  style: const TextStyle(
                                    fontSize: 11,
                                    color: Color(0xFF10B981),
                                    fontWeight: FontWeight.w700,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(width: 6),
                        IconButton(
                          tooltip: isDark ? 'Cambiar a Modo Claro' : 'Cambiar a Modo Oscuro',
                          icon: Icon(
                            isDark ? Icons.light_mode_rounded : Icons.dark_mode_rounded,
                            color: isDark ? Colors.amber : const Color(0xFF475569),
                          ),
                          onPressed: () {
                            ref.read(themeModeProvider.notifier).state =
                                themeMode == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
                          },
                        ),
                        IconButton(
                          tooltip: 'Guía Rápida y Tutorial',
                          icon: const Icon(
                            Icons.help_outline_rounded,
                            color: Color(0xFF10B981),
                          ),
                          onPressed: () {
                            TutorialTourSheet.show(
                              context,
                              onNavigateTab: (tabIdx) {
                                ref.read(activeTabProvider.notifier).state = tabIdx;
                              },
                            );
                          },
                        ),
                      ],
                    ),
                  ],
                ),
                if (isCashOnly)
                  Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.12),
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.3)),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.payments_rounded, size: 14, color: Color(0xFF10B981)),
                        const SizedBox(width: 6),
                        const Expanded(
                          child: Text(
                            'Modo Solo Efectivo: precios directos de góndola',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                              color: Color(0xFF10B981),
                            ),
                          ),
                        ),
                        InkWell(
                          onTap: () => ref.read(cashOnlyModeProvider.notifier).state = false,
                          child: const Text(
                            'Usar Tarjetas',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              color: Color(0xFF10B981),
                              decoration: TextDecoration.underline,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                const SizedBox(height: 12),
                TextField(
                  controller: _searchController,
                  focusNode: _searchFocusNode,
                  onChanged: _onSearchInputChanged,
                  decoration: InputDecoration(
                    hintText: 'Buscar yerba, leche trébol, cerveza o EAN...',
                    prefixIcon: const Icon(Icons.search_rounded, color: Color(0xFF10B981)),
                    suffixIcon: ref.watch(searchQueryProvider).isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear_rounded, size: 18),
                            onPressed: () {
                              _searchController.clear();
                              _debounceTimer?.cancel();
                              ref.read(searchQueryProvider.notifier).state = '';
                              _searchFocusNode.unfocus();
                            },
                          )
                        : null,
                  ),
                ),
                const SizedBox(height: 10),
                // Botones triples flotantes: Categorías, Marcas y Supermercados
                Row(
                  children: [
                    // Botón de Categorías
                    Expanded(
                      flex: 4,
                      child: InkWell(
                        onTap: () => _showCategoriesBottomSheet(context, ref),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                          decoration: BoxDecoration(
                            color: selectedCategory.isNotEmpty
                                ? const Color(0xFF10B981).withValues(alpha: isDark ? 0.25 : 0.15)
                                : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9)),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: selectedCategory.isNotEmpty
                                  ? const Color(0xFF10B981)
                                  : (isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1)),
                              width: selectedCategory.isNotEmpty ? 1.5 : 1.0,
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                activeCatMeta['icon'] as String,
                                style: const TextStyle(fontSize: 13),
                              ),
                              const SizedBox(width: 4),
                              Flexible(
                                child: Text(
                                  selectedCategory.isEmpty
                                      ? 'Categorías ▾'
                                      : '${activeCatMeta['label']} ▾',
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w800,
                                    color: selectedCategory.isNotEmpty
                                        ? const Color(0xFF10B981)
                                        : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                  ),
                                ),
                              ),
                              if (selectedCategory.isNotEmpty) ...[
                                const SizedBox(width: 4),
                                GestureDetector(
                                  onTap: () => ref.read(selectedCategoryProvider.notifier).state = '',
                                  child: const Icon(
                                    Icons.close_rounded,
                                    size: 14,
                                    color: Color(0xFF10B981),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 6),
                    // Botón de Marcas (Emergente)
                    Expanded(
                      flex: 3,
                      child: InkWell(
                        onTap: () => _showBrandsBottomSheet(context, ref),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                          decoration: BoxDecoration(
                            color: selectedBrand != null && selectedBrand.isNotEmpty
                                ? const Color(0xFFF59E0B).withValues(alpha: isDark ? 0.25 : 0.15)
                                : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9)),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: selectedBrand != null && selectedBrand.isNotEmpty
                                  ? const Color(0xFFF59E0B)
                                  : (isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1)),
                              width: selectedBrand != null && selectedBrand.isNotEmpty ? 1.5 : 1.0,
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text('🏷️', style: TextStyle(fontSize: 13)),
                              const SizedBox(width: 4),
                              Flexible(
                                child: Text(
                                  selectedBrand == null || selectedBrand.isEmpty
                                      ? 'Marcas ▾'
                                      : '$selectedBrand ▾',
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w800,
                                    color: selectedBrand != null && selectedBrand.isNotEmpty
                                        ? const Color(0xFFF59E0B)
                                        : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                  ),
                                ),
                              ),
                              if (selectedBrand != null && selectedBrand.isNotEmpty) ...[
                                const SizedBox(width: 4),
                                GestureDetector(
                                  onTap: () => ref.read(selectedBrandProvider.notifier).state = null,
                                  child: const Icon(
                                    Icons.close_rounded,
                                    size: 14,
                                    color: Color(0xFFF59E0B),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 6),
                    // Botón de Supermercados
                    Expanded(
                      flex: 4,
                      child: InkWell(
                        onTap: () => _showSupermarketsBottomSheet(context, ref),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                          decoration: BoxDecoration(
                            color: selectedSupermarket.isNotEmpty
                                ? const Color(0xFF0284C7).withValues(alpha: isDark ? 0.25 : 0.15)
                                : (isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9)),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: selectedSupermarket.isNotEmpty
                                  ? const Color(0xFF0284C7)
                                  : (isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1)),
                              width: selectedSupermarket.isNotEmpty ? 1.5 : 1.0,
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text(
                                selectedSupermarket.isEmpty
                                    ? '🏪'
                                    : _getSupermarketEmoji(selectedSupermarket),
                                style: const TextStyle(fontSize: 13),
                              ),
                              const SizedBox(width: 4),
                              Flexible(
                                child: Text(
                                  selectedSupermarket.isEmpty
                                      ? 'Supermercados ▾'
                                      : '$selectedStoreName ▾',
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w800,
                                    color: selectedSupermarket.isNotEmpty
                                        ? const Color(0xFF0284C7)
                                        : (isDark ? Colors.white : const Color(0xFF0F172A)),
                                  ),
                                ),
                              ),
                              if (selectedSupermarket.isNotEmpty) ...[
                                const SizedBox(width: 4),
                                GestureDetector(
                                  onTap: () => ref.read(selectedSupermarketFilterProvider.notifier).state = '',
                                  child: const Icon(
                                    Icons.close_rounded,
                                    size: 14,
                                    color: Color(0xFF0284C7),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                // Selector de día para aplicar descuentos vigentes
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today_rounded,
                      size: 13,
                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                    ),
                    const SizedBox(width: 6),
                    Text(
                      'Promos de:',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: _weekdayLabels.entries.map((entry) {
                            final isSelected = entry.key == selectedWeekday;
                            final isToday = entry.key == DateTime.now().weekday;
                            final label = isToday ? ' • Hoy' : entry.value;
                            return Padding(
                              padding: const EdgeInsets.only(right: 4),
                              child: ChoiceChip(
                                visualDensity: VisualDensity.compact,
                                label: Text(
                                  label,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                                  ),
                                ),
                                selected: isSelected,
                                onSelected: (_) =>
                                    ref.read(selectedWeekdayProvider.notifier).state = entry.key,
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
                if (searchQuery.trim().isEmpty && selectedCategory.isEmpty && selectedSupermarket.isEmpty)
                  _DailyDealsCarousel(
                    isoWeekday: selectedWeekday,
                    isDark: isDark,
                  ),
          Expanded(
            child: products.isEmpty
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          if (isSearchingOnline) ...[
                            const SizedBox(
                              width: 44,
                              height: 44,
                              child: CircularProgressIndicator(
                                strokeWidth: 3.5,
                                color: Color(0xFF10B981),
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'Buscando en vivo en los supermercados...',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w800,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              'Consultando góndolas y precios de Biggie y cadenas asociadas',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: 12,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                              ),
                            ),
                          ] else ...[
                            Icon(
                              Icons.search_off_rounded,
                              size: 48,
                              color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8),
                            ),
                            const SizedBox(height: 10),
                            Text(
                              'No encontramos "$searchQuery" en el catálogo local',
                              style: TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w700,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            const SizedBox(height: 6),
                            Text(
                              selectedCategory.isNotEmpty
                                  ? 'En la categoría "${activeCatMeta['label']}" no hay coincidencias locales.'
                                  : 'Podés consultar en vivo a los servidores de los supermercados para encontrarlo.',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: 12,
                                color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                              ),
                            ),
                            if (searchQuery.trim().isNotEmpty) ...[
                              const SizedBox(height: 18),
                              ElevatedButton.icon(
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: const Color(0xFF10B981),
                                  foregroundColor: Colors.white,
                                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 13),
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                                  elevation: 3,
                                ),
                                onPressed: () {
                                  ref.read(onlineSearchActionProvider)(searchQuery.trim());
                                },
                                icon: const Icon(Icons.travel_explore_rounded, size: 20),
                                label: Text(
                                  'Buscar "${searchQuery.trim()}" en vivo en supermercados',
                                  style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13),
                                ),
                              ),
                            ],
                          ],
                          if (selectedCategory.isNotEmpty || selectedSupermarket.isNotEmpty) ...[
                            const SizedBox(height: 16),
                            Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              alignment: WrapAlignment.center,
                              children: [
                                if (selectedCategory.isNotEmpty)
                                  FilledButton.tonalIcon(
                                    style: FilledButton.styleFrom(
                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                    ),
                                    onPressed: () {
                                      ref.read(selectedCategoryProvider.notifier).state = '';
                                    },
                                    icon: const Icon(Icons.clear_all_rounded, size: 16),
                                    label: const Text('Limpiar categoría'),
                                  ),
                                if (selectedSupermarket.isNotEmpty)
                                  FilledButton.tonalIcon(
                                    style: FilledButton.styleFrom(
                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                    ),
                                    onPressed: () {
                                      ref.read(selectedSupermarketFilterProvider.notifier).state = '';
                                    },
                                    icon: const Icon(Icons.storefront_rounded, size: 16),
                                    label: const Text('Ver todos los súper'),
                                  ),
                              ],
                            ),
                          ],
                        ],
                      ),
                    ),
                  )
                : Column(
                    children: [
                      if (onlineResults.isNotEmpty && searchQuery.trim().isNotEmpty)
                        Container(
                          margin: const EdgeInsets.fromLTRB(14, 0, 14, 8),
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            color: const Color(0xFF10B981).withValues(alpha: isDark ? 0.2 : 0.1),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: const Color(0xFF10B981).withValues(alpha: 0.4)),
                          ),
                          child: Row(
                            children: [
                              const Text('🌐', style: TextStyle(fontSize: 16)),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  'Encontramos ${onlineResults.length} productos en vivo de los supermercados (guardados en tu teléfono)',
                                  style: TextStyle(
                                    fontSize: 11.5,
                                    fontWeight: FontWeight.w700,
                                    color: isDark ? const Color(0xFF34D399) : const Color(0xFF047857),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      Expanded(
                        child: GridView.builder(
                          padding: const EdgeInsets.fromLTRB(14, 6, 14, 24),
                          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 2,
                            crossAxisSpacing: 10,
                            mainAxisSpacing: 10,
                            childAspectRatio: 0.60,
                          ),
                          itemCount: products.length,
                          itemBuilder: (context, index) {
                            final product = products[index];
                            final isFavorite = favorites.contains(product.id);
                            final ranked = PromoCalculator.rankProductOffers(
                              product: product,
                              allPromotions: promotions,
                              userCardSlugs: isCashOnly ? const <String>{} : wallet,
                              isoWeekday: selectedWeekday,
                              availableSupermarketSlugs: cityStores.keys.toSet(),
                            );

                            return _ProductGridCard(
                              product: product,
                              rankedOffers: ranked,
                              selectedSupermarketSlug: selectedSupermarket,
                              isFavorite: isFavorite,
                              onToggleFavorite: () {
                                ref.read(favoritesProvider.notifier).toggleFavorite(product.id);
                              },
                              onAddToCart: () {
                                ref.read(smartCartProvider.notifier).addOrIncrement(product);
                                ScaffoldMessenger.of(context).showSnackBar(
                                  SnackBar(
                                    backgroundColor: const Color(0xFF10B981),
                                    behavior: SnackBarBehavior.floating,
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                    content: Text(
                                      '${product.normalizedName} agregado a tu lista',
                                      style: const TextStyle(fontWeight: FontWeight.w700, color: Colors.white),
                                    ),
                                    duration: const Duration(milliseconds: 900),
                                  ),
                                );
                              },
                            );
                          },
                        ),
                      ),
                    ],
                  ),
          ),
        ],
      ),
    );
  }
}

class _ProductGridCard extends StatelessWidget {
  final ProductItem product;
  final List<EvaluatedOffer> rankedOffers;
  final String selectedSupermarketSlug;
  final VoidCallback onAddToCart;
  final bool isFavorite;
  final VoidCallback onToggleFavorite;

  const _ProductGridCard({
    required this.product,
    required this.rankedOffers,
    required this.selectedSupermarketSlug,
    required this.onAddToCart,
    required this.isFavorite,
    required this.onToggleFavorite,
  });

  Widget _buildCategoryThumbnail(BuildContext context, String? category) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cat = (category ?? '').toLowerCase();
    String emoji = '🛒';
    if (cat.contains('yerba')) emoji = '🌿';
    if (cat.contains('lácteo') || cat.contains('lacteo') || cat.contains('leche')) emoji = '🥛';
    if (cat.contains('cerveza')) emoji = '🍺';
    if (cat.contains('bebida') || cat.contains('gaseosa')) emoji = '🥤';
    if (cat.contains('carne') || cat.contains('pollo') || cat.contains('carnicería')) emoji = '🥩';
    if (cat.contains('pan') || cat.contains('baguette')) emoji = '🥖';
    if (cat.contains('snack') || cat.contains('papa')) emoji = '🍟';
    if (cat.contains('limpieza')) emoji = '🧼';

    return Container(
      color: isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
      child: Center(
        child: Text(emoji, style: const TextStyle(fontSize: 34)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (rankedOffers.isEmpty) return const SizedBox.shrink();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    EvaluatedOffer activeOffer;
    if (selectedSupermarketSlug.isNotEmpty) {
      activeOffer = rankedOffers.firstWhere(
        (o) => o.offer.supermarketSlug == selectedSupermarketSlug,
        orElse: () => rankedOffers.first,
      );
    } else {
      activeOffer = rankedOffers.first;
    }

    final gondolaPriceGs = activeOffer.offer.promoPriceGs ?? activeOffer.offer.regularPriceGs;
    final hasGondolaDiscount = activeOffer.offer.promoPriceGs != null &&
        activeOffer.offer.promoPriceGs! < activeOffer.offer.regularPriceGs;
    final hasCardDiscount = activeOffer.effectiveFinalPriceGs < gondolaPriceGs;
    final cardDiscountPct = hasCardDiscount
        ? (((gondolaPriceGs - activeOffer.effectiveFinalPriceGs) / gondolaPriceGs) * 100).round()
        : 0;
    final isSingleSuper = selectedSupermarketSlug.isNotEmpty;

    final badgeColor = hasGondolaDiscount
        ? const Color(0xFFF59E0B)
        : (hasCardDiscount
            ? const Color(0xFF10B981)
            : (isSingleSuper ? const Color(0xFF0284C7) : const Color(0xFF475569)));

    final badgeLabel = hasGondolaDiscount
        ? 'OFERTA GÓNDOLA'
        : (hasCardDiscount
            ? '-$cardDiscountPct% TARJETA'
            : (isSingleSuper ? activeOffer.offer.supermarketName : 'MÁS BAJO'));

    return Card(
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(
          color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
          width: 1,
        ),
      ),
      child: InkWell(
        onTap: () {
          FocusScope.of(context).unfocus();
          showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            backgroundColor: Colors.transparent,
            builder: (_) => ProductDetailSheet(
              product: product,
              rankedOffers: rankedOffers,
            ),
          );
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Thumbnail / Foto del producto con badge de ahorro y corazón
            Stack(
              children: [
                Container(
                  height: 100,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1E293B) : Colors.white,
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(12)),
                  ),
                  padding: const EdgeInsets.all(4),
                  child: (product.imageUrl != null && product.imageUrl!.isNotEmpty)
                      ? Image.network(
                          product.imageUrl!,
                          fit: BoxFit.contain,
                          errorBuilder: (ctx, _, __) => _buildCategoryThumbnail(context, product.category),
                        )
                      : _buildCategoryThumbnail(context, product.category),
                ),
                // Badge de descuento o supermercado
                Positioned(
                  top: 6,
                  left: 6,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: badgeColor,
                      borderRadius: BorderRadius.circular(6),
                      boxShadow: const [
                        BoxShadow(color: Colors.black26, blurRadius: 2, offset: Offset(0, 1)),
                      ],
                    ),
                    child: Text(
                      badgeLabel,
                      style: const TextStyle(
                        fontSize: 8,
                        fontWeight: FontWeight.w900,
                        color: Colors.white,
                        letterSpacing: 0.3,
                      ),
                    ),
                  ),
                ),
                // Botón favorito
                Positioned(
                  top: 5,
                  right: 5,
                  child: InkWell(
                    onTap: onToggleFavorite,
                    borderRadius: BorderRadius.circular(14),
                    child: Container(
                      padding: const EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: isDark ? const Color(0xCC0F172A) : const Color(0xCCFFFFFF),
                        shape: BoxShape.circle,
                        boxShadow: const [
                          BoxShadow(color: Colors.black12, blurRadius: 3),
                        ],
                      ),
                      child: Icon(
                        isFavorite ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                        color: isFavorite ? const Color(0xFFEF4444) : const Color(0xFF64748B),
                        size: 15,
                      ),
                    ),
                  ),
                ),
              ],
            ),

            // Contenido de detalles
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(8, 6, 8, 8),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Nombre
                        Text(
                          product.normalizedName,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                            height: 1.15,
                            color: isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                        const SizedBox(height: 3),
                        // Supermercado / Comparación
                        Row(
                          children: [
                            Text(
                              activeOffer.offer.supermarketName,
                              style: TextStyle(
                                fontSize: 9.5,
                                fontWeight: FontWeight.w700,
                                color: isDark ? const Color(0xFF38BDF8) : const Color(0xFF0284C7),
                              ),
                            ),
                            if (!isSingleSuper && rankedOffers.length > 1) ...[
                              Text(
                                ' (${rankedOffers.length})',
                                style: TextStyle(
                                  fontSize: 8.5,
                                  color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                ),
                              ),
                            ],
                          ],
                        ),
                      ],
                    ),

                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // 1. Precio Real de Góndola (el monto en el súper)
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.baseline,
                          textBaseline: TextBaseline.alphabetic,
                          children: [
                            Text(
                              GuaraniFormatter.format(gondolaPriceGs),
                              style: TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w900,
                                color: isDark ? Colors.white : const Color(0xFF0F172A),
                              ),
                            ),
                            if (hasGondolaDiscount) ...[
                              const SizedBox(width: 4),
                              Text(
                                GuaraniFormatter.format(activeOffer.offer.regularPriceGs),
                                style: TextStyle(
                                  fontSize: 9,
                                  color: isDark ? const Color(0xFF64748B) : const Color(0xFF94A3B8),
                                  decoration: TextDecoration.lineThrough,
                                ),
                              ),
                            ],
                          ],
                        ),

                        // 2. Precio con Descuento de Tarjeta (Reintegro) o Precio por Unidad Base
                        if (hasCardDiscount)
                          Container(
                            margin: const EdgeInsets.only(top: 2),
                            padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1.5),
                            decoration: BoxDecoration(
                              color: const Color(0xFF10B981).withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(5),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Text('💳 ', style: TextStyle(fontSize: 8)),
                                Flexible(
                                  child: Text(
                                    'Con tarjeta: ${GuaraniFormatter.format(activeOffer.effectiveFinalPriceGs)} (-$cardDiscountPct%)',
                                    overflow: TextOverflow.ellipsis,
                                    style: const TextStyle(
                                      fontSize: 8.5,
                                      fontWeight: FontWeight.w800,
                                      color: Color(0xFF10B981),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          )
                        else
                          Text(
                            GuaraniFormatter.formatPerBaseUnit(activeOffer.pricePerBaseUnitGs, activeOffer.baseUnit),
                            style: TextStyle(
                              fontSize: 8.5,
                              color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                            ),
                          ),
                        const SizedBox(height: 5),
                        // Botón "+ Lista"
                        SizedBox(
                          width: double.infinity,
                          height: 27,
                          child: FilledButton.tonal(
                            onPressed: onAddToCart,
                            style: FilledButton.styleFrom(
                              backgroundColor: const Color(0xFF10B981).withValues(alpha: 0.12),
                              foregroundColor: const Color(0xFF10B981),
                              padding: EdgeInsets.zero,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            child: const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.add_shopping_cart_rounded, size: 12),
                                SizedBox(width: 4),
                                Text(
                                  '+ Lista',
                                  style: TextStyle(fontSize: 10, fontWeight: FontWeight.w800),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


class _DailyDealsCarousel extends ConsumerStatefulWidget {
  final int isoWeekday;
  final bool isDark;

  const _DailyDealsCarousel({
    required this.isoWeekday,
    required this.isDark,
  });

  @override
  ConsumerState<_DailyDealsCarousel> createState() => _DailyDealsCarouselState();
}

class _DailyDealsCarouselState extends ConsumerState<_DailyDealsCarousel> {
  late final PageController _pageController;
  Timer? _autoSlideTimer;
  int _currentPage = 0;

  @override
  void initState() {
    super.initState();
    _pageController = PageController(viewportFraction: 0.92);
    _startAutoSlide();
  }

  @override
  void dispose() {
    _autoSlideTimer?.cancel();
    _pageController.dispose();
    super.dispose();
  }

  void _startAutoSlide() {
    _autoSlideTimer?.cancel();
    _autoSlideTimer = Timer.periodic(const Duration(seconds: 4), (timer) {
      if (!mounted) return;
      if (_pageController.hasClients) {
        final nextPage = (_currentPage + 1) % 4;
        _pageController.animateToPage(
          nextPage,
          duration: const Duration(milliseconds: 450),
          curve: Curves.easeInOutCubic,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final promos = ref.watch(bankPromotionsProvider);
    final todayPromos = promos.where((p) => p.daysOfWeek.contains(widget.isoWeekday)).toList();
    todayPromos.sort((a, b) => b.discountPct.compareTo(a.discountPct));

    final slides = <Widget>[
      // Slide 1: Oferta estrella de Banco / Reintegro del día
      _buildSlideCard(
        title: todayPromos.isNotEmpty
            ? '% DE AHORRO HOY'
            : 'HASTA 40% REINTEGRO',
        subtitle: todayPromos.isNotEmpty
            ? todayPromos.first.title
            : 'Pagando con tarjetas y QR seleccionados',
        badge: 'OFERTA DEL DÍA',
        gradientColors: const [Color(0xFF047857), Color(0xFF10B981)],
        icon: Icons.percent_rounded,
        actionLabel: 'Ver Promos',
        onTap: () => ref.read(activeTabProvider.notifier).state = 1,
      ),
      // Slide 2: Supermercados y Pasillo Barato
      _buildSlideCard(
        title: 'COMPARADOR DE GÓNDOLAS',
        subtitle: 'Más de 1.700 productos relevados en Asunción, CDE y Encarnación',
        badge: 'PRECIOS EN VIVO',
        gradientColors: const [Color(0xFF0369A1), Color(0xFF0284C7)],
        icon: Icons.storefront_rounded,
        actionLabel: 'Escanear',
        onTap: () => ref.read(activeTabProvider.notifier).state = 2,
      ),
      // Slide 3: Smart Cart y Ahorro en Carrito
      _buildSlideCard(
        title: 'ARMÁ TU LISTA INTELIGENTE',
        subtitle: 'Te calculamos automáticamente qué súper te conviene más',
        badge: 'OPTIMIZADOR',
        gradientColors: const [Color(0xFF7C3AED), Color(0xFF8B5CF6)],
        icon: Icons.checklist_rounded,
        actionLabel: 'Ver Listas',
        onTap: () => ref.read(activeTabProvider.notifier).state = 3,
      ),
      // Slide 4: Modo Efectivo vs Tarjetas
      _buildSlideCard(
        title: 'CAZADOR DE PRECIOS DNIT',
        subtitle: 'Escaneá facturas electrónicas e-Kuatia para sumar productos al instante',
        badge: 'SIFEN DNIT',
        gradientColors: const [Color(0xFFB45309), Color(0xFFF59E0B)],
        icon: Icons.receipt_long_rounded,
        actionLabel: 'Ver QR',
        onTap: () => ref.read(activeTabProvider.notifier).state = 2,
      ),
    ];

    return Container(
      margin: const EdgeInsets.only(top: 8, bottom: 6),
      height: 108,
      child: Stack(
        alignment: Alignment.bottomCenter,
        children: [
          PageView.builder(
            controller: _pageController,
            onPageChanged: (idx) {
              setState(() => _currentPage = idx);
              _startAutoSlide();
            },
            itemCount: slides.length,
            itemBuilder: (context, index) {
              return slides[index];
            },
          ),
          Positioned(
            bottom: 6,
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: List.generate(slides.length, (idx) {
                final isActive = idx == _currentPage;
                return AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  margin: const EdgeInsets.symmetric(horizontal: 2.5),
                  height: 4,
                  width: isActive ? 16 : 5,
                  decoration: BoxDecoration(
                    color: isActive ? Colors.white : Colors.white54,
                    borderRadius: BorderRadius.circular(2),
                  ),
                );
              }),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSlideCard({
    required String title,
    required String subtitle,
    required String badge,
    required List<Color> gradientColors,
    required IconData icon,
    required String actionLabel,
    required VoidCallback onTap,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: LinearGradient(
          colors: gradientColors,
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        boxShadow: [
          BoxShadow(
            color: gradientColors.last.withValues(alpha: 0.3),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(14, 10, 14, 16),
            child: Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: Colors.white.withValues(alpha: 0.25),
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              badge,
                              style: const TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                                letterSpacing: 0.5,
                              ),
                            ),
                          ),
                          const SizedBox(width: 6),
                          Flexible(
                            child: Text(
                              title,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w900,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        subtitle,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                          color: Colors.white.withValues(alpha: 0.9),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(icon, color: Colors.white, size: 20),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
