# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

def capture_redesign():
    html_path = os.path.abspath('preciospy_redesign_2026.html')
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--window-size=430,932')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)
    artifact_dir = "C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916"
    
    try:
        driver.get(file_url)
        time.sleep(1.2)

        # 1. Search view
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_1_search.png"))
        print("Captured 1_search")

        # 2. Cart view with TOP (Stock Gs. 93.360) selected in interactive podium
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_2_cart.png"))
        print("Captured 2_cart (TOP 1° Stock donde menos se gasta)")

        # 2b. Cart view with Superseis selected in interactive podium
        driver.execute_script("selectPodiumStore('Superseis');")
        time.sleep(0.5)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_9_superseis_selected.png"))
        print("Captured 9_superseis_selected")

        # 2c. Cart view with Split-Cart activated and breakdown visible
        driver.execute_script("const t = document.getElementById('splitCartToggle'); if (t && !t.checked) t.click();")
        time.sleep(0.6)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_8_split_breakdown.png"))
        print("Captured 8_split_breakdown (with active split breakdown)")

        # Reset
        driver.execute_script("selectPodiumStore('Supermercados Stock');")

        # 3. Scanner view with quick chips
        driver.execute_script("switchTab('viewScanner');")
        time.sleep(0.6)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_3_scanner.png"))
        print("Captured 3_scanner")

        # 4. Bank deals view with official links
        driver.execute_script("switchTab('viewPromos');")
        time.sleep(0.6)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_4_promos.png"))
        print("Captured 4_promos (with official URLs)")

        # 5. Profile view
        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.6)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_6_profile_wallet.png"))
        print("Captured 6_profile_wallet")

        # 6. Knasta Price History modal
        driver.execute_script("switchTab('viewSearch'); openProductDetail(0);")
        time.sleep(0.6)
        driver.save_screenshot(os.path.join(artifact_dir, "redesign_5_detail.png"))
        print("Captured 5_detail")

    finally:
        driver.quit()

if __name__ == '__main__':
    capture_redesign()
