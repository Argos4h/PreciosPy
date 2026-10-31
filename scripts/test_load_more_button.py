import os, time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_load_more_button():
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

        total_prods = driver.execute_script("return products.length;")
        print(f"Total products in catalog: {total_prods}")
        assert total_prods >= 1000, f"Expected at least 1000 products, got: {total_prods}"

        # 1. Filter by Supermercados Stock
        driver.execute_script("selectStore('Supermercados Stock', '🛒', 'Supermercados Stock');")
        time.sleep(0.5)

        initial_cards = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print(f"Initial rendered cards: {initial_cards}")
        assert initial_cards == 20, f"Expected 20 initial cards, got {initial_cards}"

        # 2. Check Load More button exists and has right text
        btn_load_more = driver.find_element(By.ID, "btnLoadMore")
        assert btn_load_more.is_displayed(), "btnLoadMore must be visible"
        btn_text = btn_load_more.text
        print(f"Button text: {btn_text}")
        assert "Ver más" in btn_text, f"Expected 'Ver más' in button text, got {btn_text}"
        assert "+20" in btn_text, f"Expected '+20' in button text, got {btn_text}"

        progress_el = driver.find_element(By.ID, "infiniteScrollProgress")
        print(f"Initial progress: {progress_el.text}")
        assert f"20 de {total_prods}" in progress_el.text

        # 3. Click #btnLoadMore
        print("\n--- Clicking '#btnLoadMore' to load next batch ---")
        driver.execute_script("document.getElementById('btnLoadMore').click();")
        time.sleep(0.6)

        cards_batch2 = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print(f"Cards after 1st click: {cards_batch2}")
        assert cards_batch2 == 40, f"Expected 40 cards after first click, got {cards_batch2}"

        progress_el2 = driver.find_element(By.ID, "infiniteScrollProgress")
        print(f"Progress after 1st click: {progress_el2.text}")
        assert f"40 de {total_prods}" in progress_el2.text

        # 4. Click #btnLoadMore second time
        print("\n--- Clicking '#btnLoadMore' again for 3rd batch ---")
        driver.execute_script("document.getElementById('btnLoadMore').click();")
        time.sleep(0.6)

        cards_batch3 = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print(f"Cards after 2nd click: {cards_batch3}")
        assert cards_batch3 == 60, f"Expected 60 cards after second click, got {cards_batch3}"

        # 5. Scroll main to bring button into view and take screenshot
        driver.execute_script("""
            const btn = document.getElementById('btnLoadMore');
            if (btn) btn.scrollIntoView({ behavior: 'instant', block: 'center' });
        """)
        time.sleep(0.5)

        ss_path = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_21_ver_mas_button.png')
        driver.save_screenshot(ss_path)
        print(f"Saved screenshot: {ss_path}")

        # Also take a screenshot showing the massive catalog count in header
        driver.execute_script("""
            const header = document.querySelector('header');
            if (header) header.scrollIntoView({ behavior: 'instant' });
        """)
        time.sleep(0.5)
        ss_path_massive = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_22_massive_catalog_1200.png')
        driver.save_screenshot(ss_path_massive)
        print(f"Saved massive catalog screenshot: {ss_path_massive}")

        print("\n>>> TEST 'VER MAS' BUTTON & MASSIVE CATALOG PASSED WITH 100% SUCCESS! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_load_more_button()
