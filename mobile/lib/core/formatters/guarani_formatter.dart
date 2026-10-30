/// Formateador de moneda para Guaraníes (PYG) sin decimales y con separador de miles con punto.
class GuaraniFormatter {
  const GuaraniFormatter._();

  /// Convierte `18500` -> `"Gs. 18.500"`
  static String format(int amountGs, {bool includePrefix = true}) {
    final isNegative = amountGs < 0;
    final digits = amountGs.abs().toString();
    final buffer = StringBuffer();

    for (var i = 0; i < digits.length; i++) {
      if (i > 0 && (digits.length - i) % 3 == 0) {
        buffer.write('.');
      }
      buffer.write(digits[i]);
    }

    final formatted = buffer.toString();
    final sign = isNegative ? '-' : '';
    return includePrefix ? '${sign}Gs. $formatted' : '$sign$formatted';
  }

  /// Convierte `22750` y `'KG'` -> `"Gs. 22.750 / KG"`
  static String formatPerBaseUnit(int pricePerUnitGs, String baseUnit) {
    return '${format(pricePerUnitGs)} / ${baseUnit.toUpperCase()}';
  }
}

