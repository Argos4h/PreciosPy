# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_split_keeps_selected_top():
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

        split_toggle = driver.find_element(By.ID, "splitCartToggle")
        card_stock = driver.find_element(By.ID, "podiumCardStock")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")

        # --- CASO 1: ESTADO INICIAL TOP 1 (STOCK) ---
        print("\n--- CASO 1: VERIFICAR TOP 1 (STOCK) INICIAL ---")
        assert "scale-105" in card_stock.get_attribute("class")
        assert "Viendo" in driver.find_element(By.ID, "podiumStockStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumSuperseisStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumBiggieStatus").text
        print("✓ Inicialmente Stock está seleccionado.")

        # --- CASO 2: ACTIVAR AHORRO DIVIDIDO -> STOCK DEBE MANTENERSE SELECCIONADO ---
        print("\n--- CASO 2: ACTIVAR AHORRO DIVIDIDO (EL CASO REPORTADO POR EL USUARIO) ---")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)

        card_stock = driver.find_element(By.ID, "podiumCardStock")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")

        print("Total con Split:", driver.find_element(By.ID, "cartFinalTotal").text)
        print("Stock status:", driver.find_element(By.ID, "podiumStockStatus").text)
        print("Superseis status:", driver.find_element(By.ID, "podiumSuperseisStatus").text)
        print("Biggie status:", driver.find_element(By.ID, "podiumBiggieStatus").text)

        # Verificar que el total es Gs. 85.528
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 85.528"

        # ¡VERIFICAR QUE STOCK SIGUE SELECCIONADO Y NINGÚN OTRO TOP SE SELECCIONÓ!
        assert "scale-105" in card_stock.get_attribute("class"), "Stock debe mantener escala 105"
        assert "border-2" in card_stock.get_attribute("class"), "Stock debe mantener borde-2 activo"
        assert "Viendo" in driver.find_element(By.ID, "podiumStockStatus").text, "Stock debe mantener '✓ Viendo aquí'"

        assert "scale-105" not in card_super.get_attribute("class"), "Superseis NO debe ganar escala 105"
        assert "border-2" not in card_super.get_attribute("class"), "Superseis NO debe ganar border-2"
        assert "Tocar" in driver.find_element(By.ID, "podiumSuperseisStatus").text, "Superseis debe ser 'Tocar para ver'"

        assert "scale-105" not in card_biggie.get_attribute("class"), "Biggie NO debe ganar escala 105"
        assert "border-2" not in card_biggie.get_attribute("class"), "Biggie NO debe ganar border-2"
        assert "Tocar" in driver.find_element(By.ID, "podiumBiggieStatus").text, "Biggie debe ser 'Tocar para ver'"
        print("✓ ¡ÉXITO TOTAL: Al activar Ahorro Dividido NINGÚN otro top se seleccionó y se mantuvo SOLO Stock!")

        # --- CASO 3: DESACTIVAR AHORRO DIVIDIDO ---
        print("\n--- CASO 3: DESACTIVAR AHORRO DIVIDIDO ---")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 93.360"
        assert "Viendo" in driver.find_element(By.ID, "podiumStockStatus").text
        print("✓ Al desactivar Ahorro Dividido Stock sigue seleccionado con Gs. 93.360.")

        # --- CASO 4: SELECCIONAR TOP 2 (SUPERSEIS) Y ACTIVAR SPLIT ---
        print("\n--- CASO 4: SELECCIONAR TOP 2 (SUPERSEIS) Y ACTIVAR SPLIT ---")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)
        assert "Viendo" in driver.find_element(By.ID, "podiumSuperseisStatus").text

        # Activar Split
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 85.528"
        assert "Viendo" in driver.find_element(By.ID, "podiumSuperseisStatus").text, "Superseis debe seguir seleccionado"
        assert "Tocar" in driver.find_element(By.ID, "podiumStockStatus").text
        assert "Tocar" in driver.find_element(By.ID, "podiumBiggieStatus").text
        print("✓ ¡ÉXITO: Con Superseis activo, al activar Split SE MANTIENE SUPERSEIS SELECCIONADO!")

        # Desactivar Split
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 94.720"
        assert "Viendo" in driver.find_element(By.ID, "podiumSuperseisStatus").text
        print("✓ Al desactivar vuelve al total de Superseis Gs. 94.720.")

        # Captura de pantalla para artifact
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_14_split_keeps_selected_top.png')
        print("✓ Captura guardada como redesign_14_split_keeps_selected_top.png")

        print("\n>>> ¡TEST 'EL SPLIT MANTIENE EL TOP SELECCIONADO' PASÓ 100%! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_split_keeps_selected_top()

