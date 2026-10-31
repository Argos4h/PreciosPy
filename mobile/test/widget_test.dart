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

    // Verificar que los destinos de la barra de navegación inferior están presentes
    expect(find.text('Comparar'), findsOneWidget);
    expect(find.text('Escáner'), findsOneWidget);
    expect(find.text('Mi Lista PY'), findsOneWidget);
    expect(find.text('Mis Tarjetas'), findsOneWidget);
  });
}
