import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../domain/models/catalog_models.dart';

/// Servicio de persistencia local en dispositivo (SharedPreferences)
/// Garantiza que cada persona mantenga su carrito, tarjetas bancarias y configuración
class PreferencesService {
  static const String _keyWalletProfiles = 'preciospy_wallet_profiles_v1';
  static const String _keyCartItems = 'preciospy_cart_items_v1';
  static const String _keyFavorites = 'preciospy_favorites_v1';
  static const String _keySelectedCity = 'preciospy_selected_city_v1';
  static const String _keyCashOnly = 'preciospy_cash_only_v1';
  static const String _keyThemeMode = 'preciospy_theme_mode_v1';

  final SharedPreferences? _prefs;

  PreferencesService([this._prefs]);

  static Future<PreferencesService> create() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      return PreferencesService(prefs);
    } catch (_) {
      return PreferencesService(null);
    }
  }

  // --- Billetera de Tarjetas Bancarias ---
  Future<void> saveWalletProfiles(Map<String, UserCardProfile> profiles) async {
    if (_prefs == null) return;
    final map = profiles.map((k, v) => MapEntry(k, v.toJson()));
    await _prefs.setString(_keyWalletProfiles, jsonEncode(map));
  }

  Map<String, UserCardProfile>? loadWalletProfiles() {
    if (_prefs == null) return null;
    final raw = _prefs.getString(_keyWalletProfiles);
    if (raw == null) return null;
    try {
      final decoded = jsonDecode(raw) as Map<String, dynamic>;
      return decoded.map((k, v) => MapEntry(k, UserCardProfile.fromJson(v as Map<String, dynamic>)));
    } catch (_) {
      return null;
    }
  }

  // --- Carrito Inteligente (ID de Producto -> Cantidad) ---
  Future<void> saveCart(Map<int, int> cart) async {
    if (_prefs == null) return;
    final map = cart.map((k, v) => MapEntry(k.toString(), v));
    await _prefs.setString(_keyCartItems, jsonEncode(map));
  }

  Map<int, int>? loadCart() {
    if (_prefs == null) return null;
    final raw = _prefs.getString(_keyCartItems);
    if (raw == null) return null;
    try {
      final decoded = jsonDecode(raw) as Map<String, dynamic>;
      return decoded.map((k, v) => MapEntry(int.parse(k), v as int));
    } catch (_) {
      return null;
    }
  }

  // --- Alertas y Favoritos ---
  Future<void> saveFavorites(Set<int> favorites) async {
    if (_prefs == null) return;
    await _prefs.setStringList(_keyFavorites, favorites.map((e) => e.toString()).toList());
  }

  Set<int>? loadFavorites() {
    if (_prefs == null) return null;
    final list = _prefs.getStringList(_keyFavorites);
    if (list == null) return null;
    try {
      return list.map(int.parse).toSet();
    } catch (_) {
      return null;
    }
  }

  // --- Ciudad Seleccionada ---
  Future<void> saveCity(String city) async {
    if (_prefs == null) return;
    await _prefs.setString(_keySelectedCity, city);
  }

  String? loadCity() => _prefs?.getString(_keySelectedCity);

  // --- Modo Solo Efectivo ---
  Future<void> saveCashOnly(bool cashOnly) async {
    if (_prefs == null) return;
    await _prefs.setBool(_keyCashOnly, cashOnly);
  }

  bool? loadCashOnly() => _prefs?.getBool(_keyCashOnly);

  // --- Tema Claro / Oscuro ---
  Future<void> saveThemeMode(String mode) async {
    if (_prefs == null) return;
    await _prefs.setString(_keyThemeMode, mode);
  }

  String? loadThemeMode() => _prefs?.getString(_keyThemeMode);

  // --- Limpiar / Restablecer Datos de Fábrica ---
  Future<void> clearAll() async {
    if (_prefs == null) return;
    await _prefs.clear();
  }
}

