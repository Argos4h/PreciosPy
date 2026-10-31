import 'package:flutter/material.dart';

class TutorialTourSheet extends StatefulWidget {
  final int initialStep;
  final VoidCallback? onCompleted;
  final ValueChanged<int>? onNavigateTab;

  const TutorialTourSheet({
    super.key,
    this.initialStep = 0,
    this.onCompleted,
    this.onNavigateTab,
  });

  static Future<void> show(
    BuildContext context, {
    int initialStep = 0,
    ValueChanged<int>? onNavigateTab,
  }) {
    return showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => TutorialTourSheet(
        initialStep: initialStep,
        onNavigateTab: onNavigateTab,
      ),
    );
  }

  @override
  State<TutorialTourSheet> createState() => _TutorialTourSheetState();
}

class _TutorialTourSheetState extends State<TutorialTourSheet> {
  late final PageController _pageController;
  late int _currentPage;

  static const List<Map<String, dynamic>> _steps = [
    {
      'tabIndex': 0,
      'badge': 'Paso 1 de 5 • Pestaña Precios',
      'title': 'Buscador y Comparador en Vivo',
      'subtitle': 'El catálogo más veloz de Paraguay (< 4 ms)',
      'icon': Icons.storefront_rounded,
      'color': Color(0xFF10B981),
      'highlights': [
        '🟢 Semáforo en vivo: el precio más bajo se resalta en verde.',
        '📈 Gráfico de 30 días: tocá cualquier producto para ver si la oferta es real o inflaron el precio antes.',
        '📍 Filtro por ciudad: solo ves supermercados con sucursales cercanas (Caacupé, Asunción, Luque, etc.).',
      ],
      'tip': 'Tip: Usá los chips rápidos como "🌿 Yerba" o "🥛 Lácteos" para comparar de inmediato.',
    },
    {
      'tabIndex': 1,
      'badge': 'Paso 2 de 5 • Pestaña Promos',
      'title': 'Calendario Semanal de Bancos',
      'subtitle': 'Descuentos y reintegros bancarios de Paraguay',
      'icon': Icons.local_offer_rounded,
      'color': Color(0xFF0284C7),
      'highlights': [
        '📅 Seleccioná cualquier día (Lun a Dom) para ver qué bancos tienen convenio hoy.',
        '💳 Filtro "Mis Tarjetas": mirá exclusivamente las promociones donde podés ahorrar con tus tarjetas activas.',
        '🏷️ Topes y condiciones: cálculo automático de reintegros máximos y compras con QR.',
      ],
      'tip': 'Tip: Tocá "Mis Tarjetas" para ocultar bancos que no usás y ahorrar tiempo.',
    },
    {
      'tabIndex': 2,
      'badge': 'Paso 3 de 5 • Pestaña Escáner',
      'title': 'Escáner de Pasillo & Facturas DNIT',
      'subtitle': 'Tu asistente de compras en la góndola',
      'icon': Icons.qr_code_scanner_rounded,
      'color': Color(0xFFF59E0B),
      'highlights': [
        '📸 Apuntá a cualquier código de barras en el supermercado y te dirá: "🟢 Compralo acá" o "🔴 Caro aquí".',
        '🧾 Lector de Factura Electrónica e-Kuatia: escaneá el QR fiscal del ticket de la DNIT para importar tu compra de una.',
        '⚡ Cazador de precios: si encontrás un precio nuevo, podés registrarlo para la comunidad.',
      ],
      'tip': 'Tip: Elegí en el selector arriba en qué súper estás parado para calibrar el semáforo.',
    },
    {
      'tabIndex': 3,
      'badge': 'Paso 4 de 5 • Pestaña Listas',
      'title': 'Carrito Inteligente & Ahorro',
      'subtitle': 'Dónde te conviene comprar hoy',
      'icon': Icons.format_list_bulleted_rounded,
      'color': Color(0xFF8B5CF6),
      'highlights': [
        '🎯 Tocá "Dónde te conviene comprar" para simular tu carrito completo en todas las cadenas.',
        '🔀 Compra Dividida (Split Cart): si te conviene hacer 2 paradas para duplicar tu ahorro, la app te dice exactamente qué comprar en cada lugar.',
        '📲 Botón WhatsApp: compartí el plan de compras con tu familia listo con emojis y montos.',
      ],
      'tip': 'Tip: Podés comparar el resultado en "Mis Tarjetas" o en "Solo Efectivo".',
    },
    {
      'tabIndex': 4,
      'badge': 'Paso 5 de 5 • Pestaña Perfil',
      'title': 'Mi Billetera PY & Ajustes',
      'subtitle': 'Configuración personalizada para ahorrar más',
      'icon': Icons.account_balance_wallet_rounded,
      'color': Color(0xFFEC4899),
      'highlights': [
        '💳 Mi Billetera: configurá tu nivel de ueno (1 al 5) y tus tarjetas (Itaú, Continental, Atlas, etc.).',
        '💵 Modo Solo Efectivo: si no usás tarjetas bancarias, activalo para comparar solo precios góndola.',
        '📡 GPS Automático: detectá tu ubicación para fijar tu ciudad con un solo clic.',
      ],
      'tip': 'Tip: Cambiá entre Modo Claro y Oscuro según tu preferencia en cualquier momento.',
    },
  ];

  @override
  void initState() {
    super.initState();
    _currentPage = widget.initialStep.clamp(0, _steps.length - 1);
    _pageController = PageController(initialPage: _currentPage);
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _nextPage() {
    if (_currentPage < _steps.length - 1) {
      _pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    } else {
      Navigator.of(context).pop();
      widget.onCompleted?.call();
    }
  }

  void _prevPage() {
    if (_currentPage > 0) {
      _pageController.previousPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardBg = isDark ? const Color(0xFF1E293B) : Colors.white;

    return Container(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.85,
      ),
      padding: const EdgeInsets.fromLTRB(20, 14, 20, 24),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(28)),
      ),
      child: Column(
        children: [
          // Handle superior
          Center(
            child: Container(
              width: 44,
              height: 4,
              margin: const EdgeInsets.only(bottom: 12),
              decoration: BoxDecoration(
                color: isDark ? const Color(0xFF475569) : const Color(0xFFCBD5E1),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),

          // Header con Título y botón Saltar
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(7),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: const Icon(Icons.school_rounded, color: Color(0xFF10B981), size: 20),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Guía de Uso — PreciosPy',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w900,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                ],
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: Text(
                  'Cerrar',
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),

          // Contenido de los Pasos (PageView)
          Expanded(
            child: PageView.builder(
              controller: _pageController,
              onPageChanged: (index) => setState(() => _currentPage = index),
              itemCount: _steps.length,
              itemBuilder: (ctx, index) {
                final step = _steps[index];
                final color = step['color'] as Color;
                final icon = step['icon'] as IconData;
                final highlights = step['highlights'] as List<String>;

                return SingleChildScrollView(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Badge del paso
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: color.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: color.withValues(alpha: 0.3)),
                          ),
                          child: Text(
                            step['badge'] as String,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              color: color,
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),

                        // Icono y Título
                        Row(
                          children: [
                            Container(
                              width: 48,
                              height: 48,
                              decoration: BoxDecoration(
                                color: color.withValues(alpha: 0.15),
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: Icon(icon, color: color, size: 28),
                            ),
                            const SizedBox(width: 14),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    step['title'] as String,
                                    style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w900,
                                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                                    ),
                                  ),
                                  Text(
                                    step['subtitle'] as String,
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                      color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 16),

                        // Puntos destacados
                        Container(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC),
                            borderRadius: BorderRadius.circular(18),
                            border: Border.all(
                              color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: highlights.map((text) {
                              return Padding(
                                padding: const EdgeInsets.symmetric(vertical: 4),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    const Text('• ', style: TextStyle(fontWeight: FontWeight.bold)),
                                    Expanded(
                                      child: Text(
                                        text,
                                        style: TextStyle(
                                          fontSize: 13,
                                          height: 1.35,
                                          color: isDark ? const Color(0xFFE2E8F0) : const Color(0xFF334155),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              );
                            }).toList(),
                          ),
                        ),
                        const SizedBox(height: 12),

                        // Cuadro de Consejo / Tip
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0284C7).withValues(alpha: isDark ? 0.2 : 0.1),
                            borderRadius: BorderRadius.circular(14),
                            border: Border.all(color: const Color(0xFF0284C7).withValues(alpha: 0.3)),
                          ),
                          child: Row(
                            children: [
                              const Text('💡', style: TextStyle(fontSize: 18)),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  step['tip'] as String,
                                  style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w600,
                                    color: isDark ? const Color(0xFFE0F2FE) : const Color(0xFF0369A1),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 14),

                        // Botón de acceso directo a la pestaña
                        if (widget.onNavigateTab != null) ...[
                          Center(
                            child: TextButton.icon(
                              onPressed: () {
                                Navigator.of(context).pop();
                                widget.onNavigateTab!(step['tabIndex'] as int);
                              },
                              icon: const Icon(Icons.arrow_forward_rounded, size: 16),
                              label: Text(
                                'Ir a la pestaña "${step['title'].toString().split(' ').first}" ahora',
                                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700),
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                );
              },
            ),
          ),

          // Barra inferior: Indicadores de Puntos y Botones
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Indicadores (dots)
              Row(
                children: List.generate(_steps.length, (i) {
                  final isSelected = i == _currentPage;
                  return AnimatedContainer(
                    duration: const Duration(milliseconds: 250),
                    margin: const EdgeInsets.only(right: 6),
                    width: isSelected ? 22 : 7,
                    height: 7,
                    decoration: BoxDecoration(
                      color: isSelected
                          ? const Color(0xFF10B981)
                          : (isDark ? const Color(0xFF475569) : const Color(0xFFCBD5E1)),
                      borderRadius: BorderRadius.circular(4),
                    ),
                  );
                }),
              ),

              // Botones Anterior / Siguiente
              Row(
                children: [
                  if (_currentPage > 0) ...[
                    IconButton(
                      onPressed: _prevPage,
                      icon: const Icon(Icons.arrow_back_ios_new_rounded, size: 16),
                      tooltip: 'Anterior',
                    ),
                    const SizedBox(width: 4),
                  ],
                  FilledButton.icon(
                    style: FilledButton.styleFrom(
                      backgroundColor: const Color(0xFF10B981),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                    ),
                    onPressed: _nextPage,
                    icon: Icon(
                      _currentPage == _steps.length - 1 ? Icons.check_rounded : Icons.arrow_forward_rounded,
                      size: 16,
                    ),
                    label: Text(
                      _currentPage == _steps.length - 1 ? '¡Listo para Ahorrar!' : 'Siguiente',
                      style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

