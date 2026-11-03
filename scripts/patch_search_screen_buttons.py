with open('mobile/lib/features/search/presentation/search_screen.dart', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = "    final supermarkets = ref.watch(supermarketsProvider);"
replacement1 = """    final supermarkets = ref.watch(supermarketsProvider);
    final selectedBrand = ref.watch(selectedBrandProvider);"""

if target1 in content:
    content = content.replace(target1, replacement1, 1)
    print("Replaced target1 successfully")
else:
    print("Target1 not found")

# Replace buttons row
target2 = """                // Botones gemelos flotantes: Categorías y Supermercados
                Row(
                  children: [
                    // Botón principal que abre la Ventana Flotante de Categorías
                    Expanded(
                      child: InkWell(
                        onTap: () => _showCategoriesBottomSheet(context, ref),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
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
                                style: const TextStyle(fontSize: 14),
                              ),
                              const SizedBox(width: 6),
                              Flexible(
                                child: Text(
                                  selectedCategory.isEmpty
                                      ? 'Categorías ▾'
                                      : '${activeCatMeta['label']} ▾',
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 12,
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
                                    size: 15,
                                    color: Color(0xFF10B981),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    // Botón que abre la Ventana Flotante de Supermercados
                    Expanded(
                      child: InkWell(
                        onTap: () => _showSupermarketsBottomSheet(context, ref),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
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
                                style: const TextStyle(fontSize: 14),
                              ),
                              const SizedBox(width: 6),
                              Flexible(
                                child: Text(
                                  selectedSupermarket.isEmpty
                                      ? 'Supermercados ▾'
                                      : '$selectedStoreName ▾',
                                  overflow: TextOverflow.ellipsis,
                                  style: TextStyle(
                                    fontSize: 12,
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
                                    size: 15,
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
                ),"""

replacement2 = """                // Botones triples flotantes: Categorías, Marcas y Supermercados
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
                ),"""

# Normalize \r\n to match
if target2.replace('\r\n', '\n') in content.replace('\r\n', '\n'):
    content = content.replace('\r\n', '\n').replace(target2.replace('\r\n', '\n'), replacement2)
    print("Replaced target2 successfully")
else:
    print("Target2 not found")

with open('mobile/lib/features/search/presentation/search_screen.dart', 'w', encoding='utf-8') as f:
    f.write(content)

