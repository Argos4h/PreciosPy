# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_interactive_podium():
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

        # 1. ESTADO INICIAL: BIGGIE EXPRESS SELECCIONADO
        print("\n--- PASO 1: VERIFICAR MODO INICIAL BIGGIE EXPRESS ---")
        p1 = driver.find_element(By.ID, "podium1Price").text
        total_initial = driver.find_element(By.ID, "cartFinalTotal").text
        status_biggie = driver.find_element(By.ID, "podiumBiggieStatus").text
        print(f"Podium Biggie: {p1} | Total Final: {total_initial} | Status: {status_biggie}")
        assert "Viendo" in status_biggie, "Biggie debe estar activo inicialmente"
        assert total_initial == p1, f"El total {total_initial} debe coincidir con el podium de Biggie {p1}"

        first_prod_tag = driver.find_element(By.CSS_SELECTOR, "#cartItemsList p").text
        print(f"Tag del primer producto en lista: {first_prod_tag}")
        assert "Biggie Express" in first_prod_tag, "Todos los productos deben mostrar Biggie Express"

        # 2. CLICK EN SUPERSEIS EN EL PODIUM
        print("\n--- PASO 2: SELECCIONAR SUPERSEIS EN EL PODIUM ---")
        card_super = driver.find_element(By.ID, "podiumCardSuperseis")
        driver.execute_script("arguments[0].click();", card_super)
        time.sleep(0.4)

        status_super = driver.find_element(By.ID, "podiumSuperseisStatus").text
        p2 = driver.find_element(By.ID, "podium2Price").text
        total_super = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Podium Superseis: {p2} | Total Final: {total_super} | Status: {status_super}")
        assert "Viendo" in status_super, "Superseis debe estar activo ahora"
        assert total_super == p2, f"El total {total_super} debe coincidir con el podium de Superseis {p2}"

        all_item_tags = [el.text for el in driver.find_elements(By.CSS_SELECTOR, "#cartItemsList p")]
        print(f"Tags de productos en lista con Superseis activo: {all_item_tags}")
        for tag in all_item_tags:
            assert "Superseis" in tag, f"El producto con tag '{tag}' debe ser de Superseis"

        # 3. CLICK EN STOCK EN EL PODIUM
        print("\n--- PASO 3: SELECCIONAR STOCK EN EL PODIUM ---")
        card_stock = driver.find_element(By.ID, "podiumCardStock")
        driver.execute_script("arguments[0].click();", card_stock)
        time.sleep(0.4)

        status_stock = driver.find_element(By.ID, "podiumStockStatus").text
        p3 = driver.find_element(By.ID, "podium3Price").text
        total_stock = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Podium Stock: {p3} | Total Final: {total_stock} | Status: {status_stock}")
        assert "Viendo" in status_stock, "Stock debe estar activo ahora"
        assert total_stock == p3, f"El total {total_stock} debe coincidir con el podium de Stock {p3}"

        all_item_tags = [el.text for el in driver.find_elements(By.CSS_SELECTOR, "#cartItemsList p")]
        for tag in all_item_tags:
            assert "Stock" in tag, f"El producto con tag '{tag}' debe ser de Stock"

        # 4. ACTIVAR AHORRO DIVIDIDO (SPLIT-CART)
        print("\n--- PASO 4: ACTIVAR AHORRO DIVIDIDO (SPLIT-CART) ---")
        split_toggle = driver.find_element(By.ID, "splitCartToggle")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.5)

        split_container = driver.find_element(By.ID, "splitCartBreakdownContainer")
        assert "hidden" not in split_container.get_attribute("class"), "El desglose de split-cart debe ser visible"
        print("✓ Desglose de división en 2 supermercados se muestra correctamente")

        total_split = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Total Final con Split Activo: {total_split}")
        assert total_split == "Gs. 85.528", f"El total dividido debe ser Gs. 85.528, obtenido: {total_split}"

        # Verificar que en la lista hay productos asignados a Biggie y productos a Superseis
        split_item_tags = [el.text for el in driver.find_elements(By.CSS_SELECTOR, "#cartItemsList p")]
        print(f"Tags de productos con Split activo: {split_item_tags}")
        has_biggie = any("Biggie Express" in t for t in split_item_tags)
        has_super = any("Superseis" in t for t in split_item_tags)
        assert has_biggie and has_super, "En modo Split la lista debe mostrar productos de Biggie y de Superseis"

        # 5. DESDE SPLIT, TOCAR UN SÚPER EN EL PODIUM PARA VOLVER A MONOMARCA
        print("\n--- PASO 5: DESDE MODO SPLIT, TOCAR BIGGIE EN EL PODIUM ---")
        card_biggie = driver.find_element(By.ID, "podiumCardBiggie")
        driver.execute_script("arguments[0].click();", card_biggie)
        time.sleep(0.4)

        assert "hidden" in split_container.get_attribute("class"), "El desglose debe ocultarse al elegir un súper único"
        assert not split_toggle.is_selected(), "El switch de split debe apagarse"
        total_back_biggie = driver.find_element(By.ID, "cartFinalTotal").text
        print(f"Total de vuelta a Biggie: {total_back_biggie}")
        assert total_back_biggie == p1

        # 6. VOLVER A ACTIVAR SPLIT-CART
        print("\n--- PASO 6: VOLVER A ACTIVAR SPLIT-CART ---")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.4)
        assert "hidden" not in split_container.get_attribute("class"), "El desglose vuelve a mostrarse"
        assert driver.find_element(By.ID, "cartFinalTotal").text == "Gs. 85.528"
        print("✓ El switch de Ahorro Dividido vuelve a mostrar el desglose y el total dividido")

        print("\n>>> TODOS LOS PASOS DEL PODIUM INTERACTIVO PASARON AL 100%! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_interactive_podium()

