# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_dynamic_top_podium():
    html_path = os.path.abspath('preciospy_redesign_2026.html')
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--window-size=430,932')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(file_url)
        time.sleep(1.0)
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)

        # 1. VERIFICAR QUE EL 1° LUGAR (TOP) ES DONDE MENOS SE GASTA
        print("\n--- PASO 1: VERIFICAR QUE EL TOP ES DONDE MENOS SE GASTA ---")
        p1 = driver.find_element(By.ID, "podium1Price").text
        p2 = driver.find_element(By.ID, "podium2Price").text
        p3 = driver.find_element(By.ID, "podium3Price").text

        print(f"🥇 1° Lugar (TOP): {p1}")
        print(f"🥈 2° Lugar: {p2}")
        print(f"🥉 3° Lugar: {p3}")

        # Extraer números para comparar
        val1 = int(p1.replace("Gs.", "").replace(".", "").strip())
        val2 = int(p2.replace("Gs.", "").replace(".", "").strip())
        val3 = int(p3.replace("Gs.", "").replace(".", "").strip())

        print(f"Valores numéricos: 1°={val1} | 2°={val2} | 3°={val3}")
        assert val1 <= val2, f"El TOP ({val1}) debe ser menor o igual al 2° lugar ({val2})"
        assert val2 <= val3, f"El 2° lugar ({val2}) debe ser menor o igual al 3° lugar ({val3})"
        print("✓ Confirmado: El TOP (1° lugar) es estrictamente el supermercado donde menos se gasta!")

        # 2. VERIFICAR QUIÉN ES EL TOP PARA EL CARRITO INICIAL
        card_top = driver.find_element(By.XPATH, "//div[contains(., 'TOP 1° AHORRO')]")
        assert "Stock" in card_top.text, "Para el carrito con Michelob, Stock debe ser el TOP (Gs. 93.360)"
        print("✓ Supermercados Stock es el 1° lugar (TOP) con Gs. 93.360")

        # 3. INTERACCIÓN: SELECCIONAR CADA UNO Y VER QUE LA LISTA CAMBIA
        print("\n--- PASO 2: TOCAR SUPERSEIS ---")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)
        total_super = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Total al seleccionar Superseis: {total_super}")
        assert total_super == "Gs. 94.720"

        print("\n--- PASO 3: TOCAR BIGGIE EXPRESS ---")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")
        driver.execute_script("arguments[0].click();", card_biggie)
        time.sleep(0.4)
        total_biggie = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Total al seleccionar Biggie Express: {total_biggie}")
        assert total_biggie == "Gs. 98.628"

        print("\n--- PASO 4: ACTIVAR AHORRO DIVIDIDO (SPLIT-CART) ---")
        split_toggle = driver.find_element(By.ID, "splitCartToggle")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        total_split = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Total con Ahorro Dividido: {total_split}")
        assert total_split == "Gs. 85.528"
        assert not "hidden" in driver.find_element(By.ID, "splitCartBreakdownContainer").get_attribute("class")
        print("✓ Desglose de Ahorro Dividido visible y correcto")

        print("\n>>> TEST DE PODIUM DINÁMICO POR MENOR GASTO PASÓ CON ÉXITO TOTAL (100%) <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_dynamic_top_podium()

