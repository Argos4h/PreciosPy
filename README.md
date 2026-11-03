# PreciosPy - Comparador de Supermercados y Promociones Bancarias de Paraguay

PreciosPy es una aplicacion creada para ayudar a comparar precios de la canasta familiar paraguaya, optimizar listas de compras y calcular el beneficio real de tarjetas y billeteras digitales (ueno bank, Itau, Continental, Atlas, Familiar, Sudameris, BNF y compras en efectivo).

Funciona bajo una arquitectura nativa hibrida: respuesta inmediata sin conexion a internet (Offline-First en menos de 4 ms mediante SQLite FTS5) y actualizacion silenciosa automatica desde la nube sin necesidad de reinstalar la aplicacion.

---

## Modulos del Sistema

### 1. Comparador y Podio de Supermercados
- Permite comparar simultaneamente la canasta completa en las principales cadenas de Paraguay (Superseis, Supermercados Stock, Biggie Express, Casa Rica, Salemma, Cadena Real, Fortis, Box Mayorista, Tiendas Tuti, entre otros).
- Identifica el comercio mas economico para el total de la lista armada por el usuario, ordenando los resultados del primer al tercer puesto.

### 2. Ahorro Dividido (Split-Cart)
- Evalua si dividir la compra entre dos supermercados de una misma zona genera un ahorro neto relevante, detallando que productos conviene adquirir en cada tienda y con que medio de pago.

### 3. Escaner de Pasillo y Lector SIFEN e-Kuatia (DNIT)
- Camara fisica nativa a 60 FPS para escanear codigos de barra EAN-13 en la gondola del supermercado, mostrando un semaforo comparativo al instante.
- Deteccion automatica de codigos QR de facturas electronicas nacionales emitidas por la DNIT (e-Kuatia / SIFEN), extrayendo los productos del ticket e importandolos a la lista de compras.
- Soporte para ingreso manual de codigo por teclado.

### 4. Catalogo de 1.200 Productos Reales
- Base de datos con 1.200 productos autenticos de consumo masivo con fotografias oficiales de alta resolucion en correspondencia exacta uno a uno (Bebidas, Yerba Mate, Lacteos, Carniceria, Almacen, Limpieza, Frutas y Verduras).
- Modal emergente con mas de 380 marcas registradas para filtrado rapido por fabricante.

### 5. Configuracion de Billetera Bancaria
- Parametrizacion personal de tarjetas de credito, debito y pagos con QR.
- Calculo especifico para ueno bank segun el nivel del usuario (Niveles 1 al 5, del 10% al 40% de reintegro).
- Promociones vigentes por dia de la semana para Banco Itau, Continental, Familiar, Sudameris y Atlas.
- Modo Solo Efectivo para comparar unicamente precios de mostrador sin promociones financieras.

### 6. Sincronizacion Automatica en la Nube (Cloud Sync)
- El telefono descarga silenciosamente en segundo plano la ultima version de la base de datos de precios cuando dispone de conexion, validando la integridad del archivo antes de aplicarlo.
- El usuario no necesita desinstalar ni volver a descargar el archivo APK para recibir las listas de precios actualizadas.

---

## Estructura del Proyecto

```text
PreciosPy/
├── dist/                      # Instalador APK final de produccion (PreciosPy.apk)
├── mobile/                    # Aplicacion movil nativa en Flutter / Dart
│   ├── android/               # Configuracion y manifiesto de Android
│   ├── assets/db/             # Base de datos SQLite local empaquetada (catalog_latest.db)
│   └── lib/                   # Codigo fuente de la aplicacion
│       ├── core/              # Formateadores (Guarani) y utilidades de diseno
│       ├── data/local/        # Repositorio SQLite FTS5 y motor de sincronizacion remota
│       ├── domain/            # Modelos de catalogo y calculadora de promociones
│       ├── features/          # Pantallas: busqueda, escaner, carrito, billetera, perfil
│       └── state/             # Estado reactivo mediante Riverpod
├── database/                  # Esquemas relacionales y politicas de seguridad RLS
├── scraper/                   # Modulos de recoleccion de precios por cadena
├── scripts/                   # Herramientas de generacion y sincronizacion del catalogo
│   ├── sync_real_products_exact.py     # Extraccion de productos y fotos reales
│   └── populate_exact_catalog_sqlite.py # Migracion de ofertas hacia SQLite
└── README.md
```

---

## Rol de Supabase y Seguridad de Datos

Supabase actua como repositorio central de catalogacion y autenticacion:
1. **Esquema de Retail Central:** Administra las tablas normalizadas de categorias, cadenas comerciales, productos por codigo EAN-13, ofertas vigentes y calendario de descuentos bancarios.
2. **Seguridad mediante Row Level Security (RLS):**
   - **Lectura publica (SELECT):** Acceso habilitado a los datos de precios y comercios para cualquier cliente anonimo o autenticado.
   - **Escritura protegida:** Restringida exclusivamente al rol administrativo del sistema (`service_role`). Ningun usuario puede alterar precios ni ofertas.
   - **Datos personales:** Las tablas de favoritos y registros de ahorro aplican aislamiento estricto por identificador de usuario (`auth.uid() = user_id`).
3. **Privacidad del Dispositivo:** La configuracion de tarjetas bancarias, historial de simulaciones y listas de compra permanecen en el almacenamiento privado del telefono.

---

## Compilacion y Ejecucion

### Aplicacion Movil (Flutter)

Requisitos: Flutter 3.41 o superior, Dart 3.11+, Android SDK.

```bash
cd mobile

# Descarga de dependencias
flutter pub get

# Verificacion de codigo
flutter analyze

# Generacion del paquete instalable Android
flutter build apk --release
```

El binario compilado queda generado en `mobile/build/app/outputs/flutter-apk/app-release.apk` y se copia en `dist/PreciosPy.apk`.

### Sincronizacion del Catalogo de Precios

Para refrescar el archivo maestro de precios:
```bash
# Descargar productos, fotos y precios oficiales
py scripts/sync_real_products_exact.py

# Volcar los registros a la base SQLite
py scripts/populate_exact_catalog_sqlite.py
```

Al subir los cambios a la rama principal en GitHub, los dispositivos con la app instalada descargaran la nueva version automaticamente en su proxima apertura.

---

## Licencia

Proyecto desarrollado bajo licencia MIT. Libre para adaptacion y distribucion.
