import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

class PreciosPyApp extends StatefulWidget {
  const PreciosPyApp({super.key});

  @override
  State<PreciosPyApp> createState() => _PreciosPyAppState();
}

class _PreciosPyAppState extends State<PreciosPyApp> {
  late final WebViewController _controller;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();

    SystemChrome.setSystemUIOverlayStyle(
      const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.light,
        systemNavigationBarColor: Color(0xFF020617),
        systemNavigationBarIconBrightness: Brightness.light,
      ),
    );

    final WebViewController controller = WebViewController();

    controller
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF020617))
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            setState(() {
              _isLoading = true;
            });
          },
          onPageFinished: (String url) {
            setState(() {
              _isLoading = false;
            });
          },
          onWebResourceError: (WebResourceError error) {
            debugPrint('Web resource error: ${error.description}');
          },
        ),
      )
      ..loadFlutterAsset('assets/www/index.html');

    _controller = controller;
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PreciosPy',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF020617),
      ),
      home: Scaffold(
        backgroundColor: const Color(0xFF020617),
        body: SafeArea(
          bottom: false,
          child: Stack(
            children: [
              WebViewWidget(controller: _controller),
              if (_isLoading)
                Container(
                  color: const Color(0xFF020617),
                  child: const Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          '🇵🇾 PreciosPy',
                          style: TextStyle(
                            fontSize: 26,
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF10B981),
                            letterSpacing: -0.5,
                          ),
                        ),
                        SizedBox(height: 14),
                        CircularProgressIndicator(
                          color: Color(0xFF10B981),
                          strokeWidth: 3,
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
