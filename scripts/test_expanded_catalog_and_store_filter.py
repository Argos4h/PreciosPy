import os, time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_expanded_catalog_and_store_filter():
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

        # 1. Total products initially visible (all stores)
        total_prods = driver.execute_script("return products.length;")
        print("Total products in catalog:", total_prods)
        assert total_prods >= 50, f"Catalog must have at least 50 products, got: {total_prods}"

        initial_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Initial products displayed in grid:", initial_count)
        assert initial_count == total_prods, f"Grid must display all {total_prods} products initially"

        # 2. Select Superseis
        print("\n--- Testing Supermarket Filter: Superseis ---")
        driver.execute_script("selectStore('Superseis', '🏪', 'Superseis');")
        time.sleep(0.5)

        s6_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Products displayed for Superseis:", s6_count)
        assert s6_count == total_prods, f"Superseis must show ALL {total_prods} products, got {s6_count}"

        grid_cards = driver.find_elements(By.CSS_SELECTOR, "#productGrid > div")
        assert len(grid_cards) == total_prods, f"Must render {total_prods} cards in grid"
        
        # Verify first card shows Superseis
        first_card_text = grid_cards[0].text
        print("First card sample text in Superseis filter:\n", first_card_text)
        assert "Superseis" in first_card_text, "Card must indicate Superseis"

        # Take screenshot for Superseis filter
        ss_s6 = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_18_superseis_all_products.png')
        driver.save_screenshot(ss_s6)
        print("Saved screenshot:", ss_s6)

        # 3. Select Supermercado San Vicente (Local Caacupé)
        print("\n--- Testing Supermarket Filter: Supermercado San Vicente ---")
        driver.execute_script("selectStore('Supermercado San Vicente', '🏷️', 'Supermercado San Vicente');")
        time.sleep(0.5)

        sv_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Products displayed for San Vicente:", sv_count)
        assert sv_count == total_prods, f"San Vicente must show ALL {total_prods} products, got {sv_count}"

        grid_cards_sv = driver.find_elements(By.CSS_SELECTOR, "#productGrid > div")
        first_sv_card = grid_cards_sv[0].text
        assert "San Vicente" in first_sv_card, "Card must indicate San Vicente"

        # Take screenshot for San Vicente filter
        ss_sv = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_19_san_vicente_all_products.png')
        driver.save_screenshot(ss_sv)
        print("Saved screenshot:", ss_sv)

        # 4. Select Supermercados Stock
        print("\n--- Testing Supermarket Filter: Supermercados Stock ---")
        driver.execute_script("selectStore('Supermercados Stock', '🛒', 'Supermercados Stock');")
        time.sleep(0.5)

        stock_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Products displayed for Stock:", stock_count)
        assert stock_count == total_prods, f"Stock must show ALL {total_prods} products, got {stock_count}"

        # 5. Select Biggie Express
        print("\n--- Testing Supermarket Filter: Biggie Express ---")
        driver.execute_script("selectStore('Biggie Express', '⚡', 'Biggie Express');")
        time.sleep(0.5)

        bg_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Products displayed for Biggie:", bg_count)
        assert bg_count == total_prods, f"Biggie must show ALL {total_prods} products, got {bg_count}"

        # 6. Combined filter: Superseis + Category 'Bebidas'
        print("\n--- Testing Superseis + Category Bebidas ---")
        driver.execute_script("selectStore('Superseis', '🏪', 'Superseis');")
        driver.execute_script("selectCategory('Bebidas', '🥤', 'Bebidas');")
        time.sleep(0.5)

        s6_bebidas_count = int(driver.find_element(By.ID, "resultsCount").text)
        print("Superseis Bebidas count:", s6_bebidas_count)
        assert s6_bebidas_count >= 10, f"Expected at least 10 beverages, got: {s6_bebidas_count}"

        # 7. Reset filters
        driver.execute_script("selectStore('', '🏬', 'Supermercados');")
        driver.execute_script("selectCategory('', '🗂️', 'Categorías');")
        time.sleep(0.5)
        reset_count = int(driver.find_element(By.ID, "resultsCount").text)
        assert reset_count == total_prods

        print("\n>>> ALL EXPANDED CATALOG & STORE FILTER TESTS PASSED 100%! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_expanded_catalog_and_store_filter()
