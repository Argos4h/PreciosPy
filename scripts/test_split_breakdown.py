# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_split_and_promos():
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

        # 1. VERIFICAR ENLACES OFICIALES EN PROMOS
        print("--- TEST 1: ENLACES OFICIALES EN PROMOS ---")
        driver.execute_script("switchTab('viewPromos');")
        time.sleep(0.5)

        official_links = driver.find_elements(By.XPATH, "//a[contains(., 'Web Oficial')]")
        print(f"Total botones 'Web Oficial ↗' encontrados: {len(official_links)}")
        assert len(official_links) >= 11, f"Deben haber al menos 11 enlaces oficiales, encontrados: {len(official_links)}"

        for i, link in enumerate(official_links[:3]):
            href = link.get_attribute("href")
            target = link.get_attribute("target")
            rel = link.get_attribute("rel")
            print(f"  Link {i+1}: href={href} | target={target} | rel={rel}")
            assert href.startswith("https://www."), f"El link debe empezar con https://www., valor: {href}"
            assert target == "_blank", "Debe abrir en nueva pestaña (_blank)"
            assert "noopener" in rel, "Debe tener rel noopener"

        print("✓ Enlaces oficiales de promociones verificados correctamente")

        # 2. VERIFICAR CARRITO Y DESGLOSE DIVIDIDO EN 2 SUPERMERCADOS
        print("\n--- TEST 2: DESGLOSE DE COMPRA DIVIDIDA EN 2 SUPERMERCADOS ---")
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)

        container = driver.find_element(By.ID, "splitCartBreakdownContainer")
        assert "hidden" in container.get_attribute("class"), "Inicialmente debe estar oculto si split no está activo"

        # Activar el switch de Split-Cart
        split_toggle = driver.find_element(By.ID, "splitCartToggle")
        driver.execute_script("arguments[0].click();", split_toggle)
        time.sleep(0.5)

        assert "hidden" not in container.get_attribute("class"), "Al activar el toggle, el desglose debe ser visible"
        hint_text = driver.find_element(By.ID, "splitSavingsHint").text
        print("Split hint:", hint_text)
        assert "Modo Split Activo" in hint_text, "Debe mostrar 'Modo Split Activo'"
        assert "Biggie: 2 productos" in hint_text, "Debe indicar 2 productos en Biggie"
        assert "Superseis: 1 producto" in hint_text, "Debe indicar 1 producto en Superseis"

        container_html = container.get_attribute("innerHTML")
        assert "Biggie Express" in container_html, "Debe listar la sección Biggie Express"
        assert "Superseis" in container_html, "Debe listar la sección Superseis"
        assert "¿Por qué comprar acá?" in container_html, "Debe incluir el bloque '¿Por qué comprar acá?'"
        assert "Ahorras" in container_html, "Debe calcular la diferencia exacta en Guaraníes"

        # Verificar qué productos están en cada súper
        print("\nVerificando contenido de la división inteligente:")
        stores_headings = container.find_elements(By.XPATH, ".//h5")
        for h in stores_headings:
            print("  Súper:", h.text)

        assert len(stores_headings) == 2, f"Deben haber exactamente 2 súper divididos, encontrados: {len(stores_headings)}"

        why_blocks = container.find_elements(By.XPATH, ".//div[contains(., '¿Por qué comprar acá?')]//p")
        print(f"Total explicaciones '¿Por qué comprar acá?': {len(why_blocks)}")
        for idx, block in enumerate(why_blocks):
            print(f"  [{idx+1}] {block.text[:120]}...")

        # 3. VERIFICAR BOTÓN DE COMPARTIR Y COPIAR
        copy_btn = container.find_element(By.XPATH, ".//button[contains(., 'Copiar')]")
        assert copy_btn.is_displayed(), "El botón Copiar debe estar visible"
        driver.execute_script("arguments[0].click();", copy_btn)
        time.sleep(0.4)
        toast_el = driver.find_element(By.ID, "toastMsg")
        print("Toast al copiar:", toast_el.text)
        assert "copiado" in toast_el.text.lower(), "Debe mostrar toast de copiado"

        # 4. VERIFICAR BOTÓN WHATSAPP SPLIT
        wa_btn = container.find_element(By.XPATH, ".//button[contains(., 'Compartir Plan en WhatsApp')]")
        assert wa_btn.is_displayed(), "El botón WhatsApp debe estar visible"
        print("✓ Botón 'Compartir Plan en WhatsApp' verificado")

        print("\n>>> TEST SPLIT-CART Y ENLACES OFICIALES PASÓ CON ÉXITO TOTAL (100%) <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_split_and_promos()
