import 'package:flutter/material.dart';
import 'features/cart/presentation/smart_cart_screen.dart';
import 'features/scanner/presentation/scanner_screen.dart';
import 'features/search/presentation/search_screen.dart';
import 'features/wallet/presentation/wallet_screen.dart';

class PreciosPyApp extends StatefulWidget {
  const PreciosPyApp({super.key});

  @override
  State<PreciosPyApp> createState() => _PreciosPyAppState();
}

class _PreciosPyAppState extends State<PreciosPyApp> {
  int _selectedIndex = 0;

  static const List<Widget> _screens = [
    SearchScreen(),
    ScannerScreen(),
    SmartCartScreen(),
    WalletScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PreciosPy',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00875A), // Verde ahorro de alto contraste
          brightness: Brightness.dark,
        ),
        scaffoldBackgroundColor: const Color(0xFF0D1117),
        cardTheme: CardThemeData(
          color: const Color(0xFF161B22),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF30363D)),
          ),
        ),
      ),
      home: Scaffold(
        body: IndexedStack(
          index: _selectedIndex,
          children: _screens,
        ),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _selectedIndex,
          onDestinationSelected: (idx) => setState(() => _selectedIndex = idx),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.search_rounded),
              label: 'Comparar',
            ),
            NavigationDestination(
              icon: Icon(Icons.qr_code_scanner_rounded),
              label: 'Escáner',
            ),
            NavigationDestination(
              icon: Icon(Icons.shopping_cart_checkout_rounded),
              label: 'Carrito PY',
            ),
            NavigationDestination(
              icon: Icon(Icons.credit_card_rounded),
              label: 'Mis Tarjetas',
            ),
          ],
        ),
      ),
    );
  }
}

