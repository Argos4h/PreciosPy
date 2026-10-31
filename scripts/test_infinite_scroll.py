import os, time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_infinite_scroll():
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
        print("Total products in master catalog:", total_prods)
        assert total_prods >= 200, f"Expected at least 200 products, got: {total_prods}"

        # 1. Filter by Supermercados Stock
        driver.execute_script("selectStore('Supermercados Stock', '🛒', 'Supermercados Stock');")
        time.sleep(0.5)

        initial_cards = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print("Initial batch rendered in Stock filter:", initial_cards)
        assert initial_cards == 20, f"Initial batch must be 20 cards, got: {initial_cards}"

        btn_load_more = driver.find_element(By.ID, "btnLoadMore")
        assert btn_load_more.is_displayed(), "btnLoadMore must be displayed"
        progress_txt = driver.find_element(By.ID, "infiniteScrollProgress").text
        print("Initial progress:", progress_txt)
        assert "20 de 210" in progress_txt or "20 de" in progress_txt

        # 2. Simulate scrolling down inside <main> to trigger Batch 2
        print("\n--- Scrolling down inside <main> to trigger Batch 2 ---")
        driver.execute_script("""
            const main = document.querySelector('main');
            main.scrollTop = main.scrollHeight;
        """)
        time.sleep(0.8)

        cards_after_scroll1 = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print("Cards after 1st scroll:", cards_after_scroll1)
        assert cards_after_scroll1 == 40, f"Expected 40 cards after first scroll, got: {cards_after_scroll1}"
        
        progress_txt2 = driver.find_element(By.ID, "infiniteScrollProgress").text
        print("Progress after 1st scroll:", progress_txt2)
        assert "40 de" in progress_txt2

        # 3. Click #btnLoadMore to trigger Batch 3
        print("\n--- Clicking '#btnLoadMore' to trigger Batch 3 ---")
        driver.execute_script("document.getElementById('btnLoadMore').click();")
        time.sleep(0.6)

        cards_after_scroll2 = len(driver.find_elements(By.CSS_SELECTOR, "#productGrid > div:not(#loadMoreSection)"))
        print("Cards after 2nd trigger:", cards_after_scroll2)
        assert cards_after_scroll2 == 60, f"Expected 60 cards after click, got: {cards_after_scroll2}"

        # Take screenshot of load more button
        ss_path = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_20_stock_infinite_scroll.png')
        driver.save_screenshot(ss_path)
        print("Saved screenshot of Load More in Stock:", ss_path)

        print("\n>>> INFINITE SCROLL & LOAD MORE TEST PASSED WITH 100% SUCCESS! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_infinite_scroll()
