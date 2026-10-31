# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_location_based_supermarkets():
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

        # --- CASO 1: CAACUPÉ ---
        print("\n--- CASO 1: VERIFICAR SUPERMERCADOS EN CAACUPÉ ---")
        driver.execute_script("selectCity('Caacupé');")
        time.sleep(0.4)

        # Abrir el selector de supermercados
        driver.execute_script("openSupermarketSheet();")
        time.sleep(0.3)
        sheet_container = driver.find_element(By.ID, "supermarketListContainer")
        sheet_html = sheet_container.get_attribute("innerHTML")

        print("Supermercados visibles en Caacupé:")
        assert "Supermercado San Vicente" in sheet_html, "Supermercado San Vicente DEBE aparecer en Caacupé"
        assert "Local • En Tienda" in sheet_html, "Debe tener badge 'Local • En Tienda'"
        assert "Supermercados Stock" in sheet_html, "Stock debe aparecer en Caacupé"
        assert "Superseis" in sheet_html, "Superseis debe aparecer en Caacupé"
        assert "Biggie Express" in sheet_html, "Biggie debe aparecer en Caacupé"
        assert "Tiendas Tuti" in sheet_html, "Tuti debe aparecer en Caacupé"
        
        # VERIFICAR QUE NO APARECEN CADENAS QUE NO EXISTEN EN CAACUPÉ
        assert "Casa Rica" not in sheet_html, "Casa Rica NO debe aparecer en Caacupé"
        assert "Fortis Mayorista" not in sheet_html, "Fortis Mayorista NO debe aparecer en Caacupé"
        print("✓ Caacupé tiene únicamente sus comercios locales (incluyendo Supermercado San Vicente)!")
        driver.execute_script("closeSupermarketSheet();")

        # Probar comparativa en Ficha Knasta en Caacupé
        print("\nVerificando Ficha Knasta en Caacupé...")
        driver.execute_script("openProductDetail(0);")
        time.sleep(0.5)
        modal_content = driver.find_element(By.ID, "modalProductContent").get_attribute("innerHTML")
        assert "Supermercado San Vicente" in modal_content, "San Vicente debe estar en la comparativa de Caacupé"
        assert "Local • En Tienda" in modal_content, "Debe tener la etiqueta Local"
        assert "Casa Rica" not in modal_content, "Casa Rica no debe estar en la comparativa de Caacupé"
        print("✓ Knasta en Caacupé compara solo comercios de Caacupé (incluyendo San Vicente).")
        driver.execute_script("closeProductModal();")
        time.sleep(0.3)

        # --- CASO 2: ASUNCIÓN ---
        print("\n--- CASO 2: CAMBIAR A ASUNCIÓN ---")
        driver.execute_script("selectCity('Asunción');")
        time.sleep(0.4)

        driver.execute_script("openSupermarketSheet();")
        time.sleep(0.3)
        sheet_html_asu = driver.find_element(By.ID, "supermarketListContainer").get_attribute("innerHTML")

        assert "Casa Rica" in sheet_html_asu, "Casa Rica DEBE aparecer en Asunción"
        assert "Supermercados Areté" in sheet_html_asu, "Areté DEBE aparecer en Asunción"
        assert "Delimarket" in sheet_html_asu, "Delimarket DEBE aparecer en Asunción"
        assert "Supermercado San Vicente" not in sheet_html_asu, "San Vicente NO debe aparecer en Asunción"
        print("✓ Asunción tiene Casa Rica, Areté, Delimarket y NO tiene a San Vicente.")
        driver.execute_script("closeSupermarketSheet();")

        # --- CASO 3: SAN LORENZO ---
        print("\n--- CASO 3: CAMBIAR A SAN LORENZO ---")
        driver.execute_script("selectCity('San Lorenzo');")
        time.sleep(0.4)

        driver.execute_script("openSupermarketSheet();")
        time.sleep(0.3)
        sheet_html_sl = driver.find_element(By.ID, "supermarketListContainer").get_attribute("innerHTML")

        assert "Supermercados Salemma" in sheet_html_sl, "Salemma DEBE aparecer en San Lorenzo"
        assert "Fortis Mayorista" in sheet_html_sl, "Fortis DEBE aparecer en San Lorenzo"
        assert "Casa Rica" not in sheet_html_sl, "Casa Rica NO debe aparecer en San Lorenzo"
        assert "Supermercado San Vicente" not in sheet_html_sl, "San Vicente NO debe aparecer en San Lorenzo"
        print("✓ San Lorenzo tiene Salemma, Fortis y NO tiene Casa Rica ni San Vicente.")
        driver.execute_script("closeSupermarketSheet();")

        # Captura de pantalla para artifact
        driver.execute_script("selectCity('Caacupé');")
        time.sleep(0.3)
        driver.execute_script("openProductDetail(0);")
        time.sleep(0.5)
        driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_15_caacupe_san_vicente_knasta.png')
        print("✓ Captura guardada como redesign_15_caacupe_san_vicente_knasta.png")

        print("\n>>> ¡TEST 'SUPERMERCADOS POR UBICACIÓN & SAN VICENTE' PASÓ 100%! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_location_based_supermarkets()

