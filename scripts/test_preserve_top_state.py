# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_preserve_top():
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

        # 1. ESTADO INICIAL: TOP 1 (STOCK) SELECCIONADO
        print("\n--- CASO 1: TOP 1 (STOCK) -> ACTIVAR SPLIT -> DESACTIVAR SPLIT ---")
        status_stock = driver.find_element(By.ID, "podiumStockStatus").text
        total_initial = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Estado inicial: Total={total_initial} | Status Stock={status_stock}")
        assert "Viendo" in status_stock, "Inicialmente debe estar seleccionado el TOP 1 (Stock)"
        assert total_initial == "Gs. 93.360", f"El total inicial debe ser Gs. 93.360, obtenido: {total_initial}"

        # Activar Ahorro Dividido
        split_toggle = driver.find_element(By.ID, "splitCartToggle")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)

        total_split = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Con Split activo: Total={total_split}")
        assert total_split == "Gs. 85.528"

        # DESACTIVAR AHORRO DIVIDIDO (EL CASO EXACTO DEL USUARIO)
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)

        total_after = driver.find_element(By.ID, "cartFinalTotal").text
        status_stock_after = driver.find_element(By.ID, "podiumStockStatus").text
        status_biggie_after = driver.find_element(By.ID, "podiumBiggieStatus").text

        print(f"Al desactivar Split: Total={total_after} | Status Stock={status_stock_after} | Status Biggie={status_biggie_after}")
        assert total_after == "Gs. 93.360", f"El total debe mantenerse en Gs. 93.360 (Top 1 Stock), pero fue: {total_after}"
        assert "Viendo" in status_stock_after, "Stock (Top 1) debe seguir seleccionado con '✓ Viendo aquí'"
        assert "Viendo" not in status_biggie_after, "Biggie (Top 3) NO debe quedarse seleccionado"
        print("✓ ÉXITO: Al desactivar el ahorro dividido se mantuvo en el TOP 1 (Stock) y no saltó al Top 3!")

        # 2. CASO 2: SELECCIONAR TOP 2 (SUPERSEIS) -> ACTIVAR SPLIT -> DESACTIVAR SPLIT
        print("\n--- CASO 2: TOP 2 (SUPERSEIS) -> ACTIVAR SPLIT -> DESACTIVAR SPLIT ---")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 94.720"

        # Activar Split
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 85.528"

        # Desactivar Split
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        total_back_super = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Al desactivar Split habiendo estado en Superseis: Total={total_back_super}")
        assert total_back_super == "Gs. 94.720", "Debe restaurar Superseis"
        print("✓ ÉXITO: Al desactivar el ahorro dividido se mantuvo en Superseis!")

        print("\n>>> TEST DE PERSISTENCIA DEL TOP AL ACTIVAR/DESACTIVAR SPLIT PASÓ 100%! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_preserve_top()

