# -*- coding: utf-8 -*-
import json

products = [
  {
    "id": 1,
    "name": "Yerba Kurupi Menta y Boldo 500g",
    "brand": "Kurupí",
    "category": "Yerbas",
    "image": "https://static.app.biggie.com.py/images/products/7840127000124.jpg",
    "regularPrice": 17500,
    "store": "Biggie Express",
    "unitPrice": "Gs. 22.750 / kg",
    "history": [18000, 17500, 17500, 16900, 17500, 11375],
    "stores": {
      "Biggie Express": 17500,
      "Superseis": 16900,
      "Supermercados Stock": 16750,
      "Casa Rica": 17900,
      "Fortis Mayorista": 15200
    }
  },
  {
    "id": 2,
    "name": "Leche Lactolanda Entera Ultra 1L Sachet",
    "brand": "Lactolanda",
    "category": "Lácteos",
    "image": "https://static.app.biggie.com.py/images/products/7840042000216.jpg",
    "regularPrice": 6250,
    "store": "Biggie Express",
    "unitPrice": "Gs. 4.060 / L",
    "history": [6500, 6250, 6250, 6000, 6250, 4060],
    "stores": {
      "Biggie Express": 6250,
      "Superseis": 6100,
      "Supermercados Stock": 5950,
      "Casa Rica": 6400,
      "Fortis Mayorista": 5800
    }
  },
  {
    "id": 3,
    "name": "Gaseosa Coca-Cola Original 2L",
    "brand": "Coca-Cola",
    "category": "Bebidas",
    "image": "https://static.app.biggie.com.py/images/products/7840058008084.jpg",
    "regularPrice": 14900,
    "store": "Biggie Express",
    "unitPrice": "Gs. 4.842 / L",
    "history": [15500, 14900, 14900, 14500, 14900, 9685],
    "stores": {
      "Biggie Express": 14900,
      "Superseis": 14500,
      "Supermercados Stock": 14300,
      "Casa Rica": 15200,
      "Fortis Mayorista": 13800
    }
  },
  {
    "id": 4,
    "name": "Cerveza Michelob Ultra 269ml Pack x12",
    "brand": "Michelob",
    "category": "Bebidas",
    "image": "https://static.app.biggie.com.py/images/products/7840050009881.png",
    "regularPrice": 48000,
    "store": "Superseis",
    "unitPrice": "Gs. 11.890 / L",
    "history": [50000, 48000, 48000, 47000, 48000, 38400],
    "stores": {
      "Biggie Express": 51500,
      "Superseis": 48000,
      "Supermercados Stock": 47500,
      "Casa Rica": 52900,
      "Fortis Mayorista": 45500
    }
  },
  {
    "id": 5,
    "name": "Costilla de Primera para Asado 1kg",
    "brand": "Carnes",
    "category": "Carnicería",
    "image": "https://static.app.biggie.com.py/images/products/60168.jpg",
    "regularPrice": 42950,
    "store": "Superseis",
    "unitPrice": "Gs. 34.360 / kg",
    "history": [44900, 42950, 42950, 41500, 42950, 34360],
    "stores": {
      "Biggie Express": 44900,
      "Superseis": 42950,
      "Supermercados Stock": 41900,
      "Casa Rica": 48500,
      "Fortis Mayorista": 39900
    }
  },
  {
    "id": 6,
    "name": "Galletitas Oreo Original Tubo 118g",
    "brand": "Oreo",
    "category": "Almacén",
    "image": "https://static.app.biggie.com.py/images/products/7622201759582.jpg",
    "regularPrice": 7400,
    "store": "Biggie Express",
    "unitPrice": "Gs. 40.762 / kg",
    "history": [7900, 7400, 7400, 7000, 7400, 4810],
    "stores": {
      "Biggie Express": 7400,
      "Superseis": 7200,
      "Supermercados Stock": 7050,
      "Casa Rica": 7750,
      "Fortis Mayorista": 6700
    }
  },
  {
    "id": 7,
    "name": "Café Nescafé Tradición Frasco 160g",
    "brand": "Nescafé",
    "category": "Desayuno",
    "image": "https://static.app.biggie.com.py/images/products/7891000414903.jpg",
    "regularPrice": 39900,
    "store": "Supermercados Stock",
    "unitPrice": "Gs. 199.500 / kg",
    "history": [42000, 39900, 39900, 38000, 39900, 31920],
    "stores": {
      "Biggie Express": 42500,
      "Superseis": 40500,
      "Supermercados Stock": 39900,
      "Casa Rica": 43500,
      "Fortis Mayorista": 38200
    }
  },
  {
    "id": 8,
    "name": "Papas Fritas Pringles Original 104g",
    "brand": "Pringles",
    "category": "Snacks",
    "image": "https://static.app.biggie.com.py/images/products/7896004006277.jpg",
    "regularPrice": 21800,
    "store": "Biggie Express",
    "unitPrice": "Gs. 136.250 / kg",
    "history": [23000, 21800, 21800, 21000, 21800, 14170],
    "stores": {
      "Biggie Express": 21800,
      "Superseis": 22500,
      "Supermercados Stock": 21950,
      "Casa Rica": 23900,
      "Fortis Mayorista": 19900
    }
  },
  {
    "id": 9,
    "name": "Arroz Primicia Parbolizado Tipo I 1kg",
    "brand": "Primicia",
    "category": "Almacén",
    "image": "https://static.app.biggie.com.py/images/products/7840045034102.jpg",
    "regularPrice": 9400,
    "store": "Supermercados Stock",
    "unitPrice": "Gs. 7.520 / kg",
    "history": [9800, 9400, 9400, 9000, 9400, 7520],
    "stores": {
      "Biggie Express": 10200,
      "Superseis": 9600,
      "Supermercados Stock": 9400,
      "Casa Rica": 10500,
      "Fortis Mayorista": 8900
    }
  },
  {
    "id": 10,
    "name": "Aceite de Soja Soya Botella 900ml",
    "brand": "Soya",
    "category": "Almacén",
    "image": "https://static.app.biggie.com.py/images/products/7891080806711.jpg",
    "regularPrice": 16550,
    "store": "Biggie Express",
    "unitPrice": "Gs. 11.952 / L",
    "history": [17500, 16550, 16550, 15900, 16550, 10757],
    "stores": {
      "Biggie Express": 16550,
      "Superseis": 16200,
      "Supermercados Stock": 15900,
      "Casa Rica": 16900,
      "Fortis Mayorista": 15100
    }
  },
  {
    "id": 11,
    "name": "Fideos Nissin Cup Noodles Pollo 71g",
    "brand": "Nissin",
    "category": "Almacén",
    "image": "https://static.app.biggie.com.py/images/products/7891079012895.jpg",
    "regularPrice": 12900,
    "store": "Biggie Express",
    "unitPrice": "Gs. 118.098 / kg",
    "history": [13500, 12900, 12900, 12000, 12900, 8385],
    "stores": {
      "Biggie Express": 12900,
      "Superseis": 13200,
      "Supermercados Stock": 12800,
      "Casa Rica": 13900,
      "Fortis Mayorista": 11900
    }
  },
  {
    "id": 12,
    "name": "Jabón Líquido Omo Lavado Perfecto 900ml",
    "brand": "Omo",
    "category": "Limpieza",
    "image": "https://static.app.biggie.com.py/images/products/7891150064928-29961185.jpg",
    "regularPrice": 23300,
    "store": "Superseis",
    "unitPrice": "Gs. 20.711 / L",
    "history": [24500, 23300, 23300, 22500, 23300, 18640],
    "stores": {
      "Biggie Express": 25500,
      "Superseis": 23300,
      "Supermercados Stock": 22900,
      "Casa Rica": 26200,
      "Fortis Mayorista": 21500
    }
  }
]

with open('scripts/verified_products_clean.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("Successfully enriched verified_products_clean.json with multi-store pricing across 5 chains!")

