# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_only_one_top_selected():
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

        card_stock = driver.find_element(By.ID, "podiumCardStock")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")

        # --- CASO 1: ESTADO INICIAL -> SOLO TOP 1 (STOCK) SELECCIONADO ---
        print("\n--- PASO 1: VERIFICAR QUE INICIALMENTE SOLO STOCK ESTÁ SELECCIONADO ---")
        class_stock = card_stock.get_attribute("class")
        class_super = card_super.get_attribute("class")
        class_biggie = card_biggie.get_attribute("class")

        print(f"Stock class: {class_stock}")
        print(f"Superseis class: {class_super}")
        print(f"Biggie class: {class_biggie}")

        assert "scale-105" in class_stock, "Stock debe tener escala 105 (activo)"
        assert "border-2" in class_stock, "Stock debe tener borde-2"
        assert "scale-105" not in class_super, "Superseis NO debe tener escala 105"
        assert "border-2" not in class_super, "Superseis NO debe tener border-2"
        assert "scale-105" not in class_biggie, "Biggie NO debe tener escala 105"
        assert "border-2" not in class_biggie, "Biggie NO debe tener border-2"
        assert "Viendo" in driver.find_element(By.ID, "podiumStockStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumSuperseisStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumBiggieStatus").text
        print("✓ Inicialmente SOLO el Top 1 (Stock) se ve como seleccionado.")

        # --- CASO 2: SELECCIONAR TOP 2 (SUPERSEIS) ---
        print("\n--- PASO 2: TOCAR SUPERSEIS Y VERIFICAR QUE SOLO SUPERSEIS SE VE SELECCIONADO ---")
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)

        card_stock = driver.find_element(By.ID, "podiumCardStock")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")

        class_stock = card_stock.get_attribute("class")
        class_super = card_super.get_attribute("class")
        class_biggie = card_biggie.get_attribute("class")

        print(f"Superseis class (activo): {class_super}")
        print(f"Stock class (inactivo): {class_stock}")
        print(f"Biggie class (inactivo): {class_biggie}")

        assert "scale-105" in class_super, "Superseis debe tener escala 105"
        assert "border-2" in class_super, "Superseis debe tener border-2"
        assert "ring-2" in class_super, "Superseis debe tener ring-2"
        assert "scale-105" not in class_stock, "Stock YA NO debe tener escala 105"
        assert "border-2" not in class_stock, "Stock YA NO debe tener border-2"
        assert "ring-2" not in class_stock, "Stock YA NO debe tener ring-2"
        assert "scale-105" not in class_biggie, "Biggie NO debe tener escala 105"
        assert "border-2" not in class_biggie, "Biggie NO debe tener border-2"

        assert "Viendo" in driver.find_element(By.ID, "podiumSuperseisStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumStockStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumBiggieStatus").text
        print("✓ Al seleccionar Superseis: SOLO Superseis se ve seleccionado. Stock y Biggie se ven apagados/inactivos.")

        # --- CASO 3: SELECCIONAR TOP 3 (BIGGIE) ---
        print("\n--- PASO 3: TOCAR BIGGIE Y VERIFICAR QUE SOLO BIGGIE SE VE SELECCIONADO ---")
        driver.execute_script("arguments[0].click();", card_biggie)
        time.sleep(0.4)

        card_stock = driver.find_element(By.ID, "podiumCardStock")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")

        class_stock = card_stock.get_attribute("class")
        class_super = card_super.get_attribute("class")
        class_biggie = card_biggie.get_attribute("class")

        assert "scale-105" in class_biggie, "Biggie debe tener escala 105"
        assert "border-2" in class_biggie, "Biggie debe tener border-2"
        assert "scale-105" not in card_stock.get_attribute("class")
        assert "border-2" not in card_stock.get_attribute("class")
        assert "scale-105" not in card_super.get_attribute("class")
        assert "border-2" not in card_super.get_attribute("class")

        assert "Viendo" in driver.find_element(By.ID, "podiumBiggieStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumStockStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumSuperseisStatus").text
        print("✓ Al seleccionar Biggie: SOLO Biggie se ve seleccionado. Ni Stock ni Superseis se ven seleccionados.")

        # Tomar captura para artifact
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)
        driver.save_screenshot("C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_10_single_top_selected.png")
        print("✓ Captura guardada como redesign_10_single_top_selected.png")

        print("\n>>> ¡TEST 'SOLO UN TOP SELECCIONADO' PASÓ CON ÉXITO TOTAL (100%)! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_only_one_top_selected()

