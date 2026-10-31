import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:precios_py_mobile/app.dart';

void main() {
  testWidgets('PreciosPyApp smoke test y navegación inicial', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: PreciosPyApp(),
      ),
    );

    // Verificar que los 5 destinos al estilo Rebuscate están presentes en la navegación
    expect(find.text('Precios'), findsOneWidget);
    expect(find.text('Promos'), findsOneWidget);
    expect(find.text('Escáner'), findsOneWidget);
    expect(find.text('Listas'), findsOneWidget);
    expect(find.text('Perfil'), findsOneWidget);
  });

  testWidgets('Verificar filtros flotantes gemelos y vista en cuadrícula 2x2', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: PreciosPyApp(),
      ),
    );
    await tester.pumpAndSettle();

    // 1. Verificar botones gemelos de filtrado
    expect(find.text('Categorías ▾'), findsOneWidget);
    expect(find.text('Supermercados ▾'), findsOneWidget);

    // 2. Verificar que los chips sueltos ya NO están en la pantalla principal
    expect(find.byType(FilterChip), findsNothing);

    // 3. Verificar que la vista de productos es una cuadrícula (GridView)
    final gridFinder = find.byType(GridView);
    expect(gridFinder, findsOneWidget);

    final gridView = tester.widget<GridView>(gridFinder);
    final delegate = gridView.gridDelegate as SliverGridDelegateWithFixedCrossAxisCount;
    expect(delegate.crossAxisCount, equals(2)); // Cuadrícula 2x2
  });
}
