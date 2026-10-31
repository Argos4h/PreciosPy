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
}
