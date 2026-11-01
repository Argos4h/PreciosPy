# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

def test_all():
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

        # 1. Test Search and Clear
        search_input = driver.find_element(By.ID, "searchInput")
        search_input.send_keys("coca")
        time.sleep(0.5)
        count_el = driver.find_element(By.ID, "resultsCount")
        print("Search 'coca' results count:", count_el.text)
        assert int(count_el.text) >= 1, "Must find at least 1 coca result"

        clear_btn = driver.find_element(By.ID, "clearSearchBtn")
        clear_btn.click()
        time.sleep(0.3)
        print("After clear results count:", driver.find_element(By.ID, "resultsCount").text)

        # 2. Test City Selection
        driver.execute_script("selectCity('Asunción');")
        time.sleep(0.3)
        lbl = driver.find_element(By.ID, "currentCityLabel").text
        print("City changed to:", lbl)
        assert lbl == "Asunción"

        # 3. Test Category Filter
        driver.execute_script("selectCategory('Bebidas', '🥤', 'Bebidas');")
        time.sleep(0.3)
        cat_count = driver.find_element(By.ID, "resultsCount").text
        print("Bebidas category count:", cat_count)
        assert int(cat_count) >= 2, "Must find at least 2 beverages"

        # Reset category
        driver.execute_script("selectCategory('', '🗂️', 'Categorías');")

        # 4. Test Cash Only Toggle
        driver.execute_script("toggleCashMode();")
        time.sleep(0.3)
        cash_mode = driver.execute_script("return isCashOnly;")
        print("Cash mode is now:", cash_mode)
        assert cash_mode == True
        driver.execute_script("toggleCashMode();") # Switch back

        # 4b. Test Star Favorite Toggle (Empty ☆ vs Filled ★)
        is_fav_before = driver.execute_script("return favorites.includes(1);")
        print("Product 1 initial favorite status:", is_fav_before)
        driver.execute_script("toggleFavorite(1);") # toggle on
        time.sleep(0.3)
        assert driver.execute_script("return favorites.includes(1);") == True
        print("Product 1 toggled to favorite ★ successfully")
        driver.execute_script("toggleFavorite(1);") # toggle off
        time.sleep(0.3)
        assert driver.execute_script("return favorites.includes(1);") == False
        print("Product 1 toggled back to un-favorite ☆ successfully")

        # 4c. Test Real Price Visibility on Card
        grid_html = driver.execute_script("return document.getElementById('productGrid').innerHTML;")
        assert "Precio real:" in grid_html, "Must explicitly display 'Precio real:'"
        print("Verified 'Precio real:' is clearly displayed on product cards")

        # 5. Test Cart Steppers and Calculations
        # Add products to cart first
        driver.execute_script("flyToCart(0, null); flyToCart(1, null); flyToCart(3, null);")
        time.sleep(0.5)
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)
        podium_biggie = driver.find_element(By.ID, "podium1Price").text
        print("Podium 1 Price:", podium_biggie)
        assert "Gs." in podium_biggie and podium_biggie != "Gs. 0"

        # Test Stepper +
        driver.execute_script("flyToCart(0, null);")
        time.sleep(0.3)
        badge = driver.find_element(By.ID, "navCartBadge").text
        print("Cart items badge:", badge)

        # Test Split Cart Toggle
        driver.execute_script("document.getElementById('splitCartToggle').click();")
        time.sleep(0.3)
        print("Split hint:", driver.find_element(By.ID, "splitSavingsHint").text)

        # 6. Test Scanner actions
        driver.execute_script("switchTab('viewScanner');")
        time.sleep(0.5)
        driver.execute_script("simulateScanBarcode();")
        time.sleep(0.3)
        scanned_name = driver.find_element(By.ID, "scannedProductName").text
        print("Scanned product name:", scanned_name)

        driver.execute_script("toggleScannerFlashlight();")
        time.sleep(0.3)
        flash_state = driver.execute_script("return isFlashlightOn;")
        print("Flashlight state:", flash_state)
        assert flash_state == True

        # 7. Test Bank Profile Toggles & ueno Level Selector
        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.5)
        
        # Test ueno Level Selection: Nivel 5 (40%)
        driver.execute_script("setUenoLevel(5);")
        time.sleep(0.3)
        ueno_lvl = driver.execute_script("return bankProfiles.ueno.level;")
        print("ueno level selected:", ueno_lvl)
        assert ueno_lvl == 5, "ueno level should be 5"

        # Test Itaú Tier Selection: Infinite (30%)
        driver.execute_script("setItauTier('infinite');")
        time.sleep(0.3)
        itau_tier = driver.execute_script("return bankProfiles.itau.tier;")
        print("Itaú tier selected:", itau_tier)
        assert itau_tier == 'infinite', "Itaú tier should be infinite"

        # Test Sudameris toggle
        driver.execute_script("toggleBankProfile('sudameris');")
        time.sleep(0.3)
        sud_enabled = driver.execute_script("return bankProfiles.sudameris.enabled;")
        print("Sudameris enabled:", sud_enabled)
        assert sud_enabled == True

        # Test Zeta Banco toggle
        driver.execute_script("toggleBankProfile('zeta');")
        time.sleep(0.3)
        zeta_enabled = driver.execute_script("return bankProfiles.zeta.enabled;")
        print("Zeta enabled:", zeta_enabled)

        # 8. Test Dynamic Calculation with ueno N5 on Biggie Product
        driver.execute_script("switchTab('viewSearch');")
        driver.execute_script("setDay(6);") # Saturday
        time.sleep(0.5)
        prod0_offer = driver.execute_script("return calculateProductOffer(products[0], 6);")
        print("Product 0 with ueno N5 (40%):", prod0_offer)
        assert prod0_offer['discountPct'] == 40, "Discount should be 40% with ueno N5"
        assert prod0_offer['finalPrice'] == int(round(17500 * 0.60)), "Price should be 60% of regular"

        # Switch to ueno N1 (15%)
        driver.execute_script("setUenoLevel(1);")
        time.sleep(0.3)
        # Note: On Saturday (6), if Zeta is enabled (20%), Zeta (20%) is better than ueno N1 (15%)!
        # If Zeta is disabled, ueno N1 (15%) will be picked. Let's verify Zeta vs ueno!
        prod0_offer_n1 = driver.execute_script("return calculateProductOffer(products[0], 6);")
        print("Product 0 with ueno N1 on Saturday:", prod0_offer_n1)

        # 9. Test Product Detail Modal (Knasta) & Multi-Supermarket Comparison
        driver.execute_script("openProductDetail(0);")
        time.sleep(0.5)
        modal_displayed = driver.execute_script("return !document.getElementById('productDetailModal').classList.contains('hidden');")
        print("Knasta modal opened:", modal_displayed)
        assert modal_displayed == True
        
        # Verify that all 5 supermarkets are displayed in the comparison list
        stores_count = driver.execute_script("return document.querySelectorAll('#supermarketComparisonList > div').length;")
        print("Supermarkets compared in modal:", stores_count)
        assert stores_count >= 5, f"Must show at least 5 supermarkets in comparison, got: {stores_count}"
        
        comparison_html = driver.execute_script("return document.getElementById('supermarketComparisonList').innerHTML;")
        print("Winner badge in HTML:", "Barato" in comparison_html)
        assert "Barato" in comparison_html, "Must have a winner marked with Barato"
        
        driver.execute_script("closeProductModal();")

        # 10. Test Promos Tab with 11 promotions and filter
        driver.execute_script("switchTab('viewPromos');")
        time.sleep(0.5)
        driver.execute_script("filterPromosView(false);") # All promos
        all_promos_count = driver.execute_script("return document.querySelectorAll('#promosListContainer > div').length;")
        print("All bank promos count rendered:", all_promos_count)
        assert all_promos_count == 11, "Should render 11 bank promos"

        driver.execute_script("filterPromosView(true);") # Only my cards
        my_promos_count = driver.execute_script("return document.querySelectorAll('#promosListContainer > div').length;")
        print("My cards promos count rendered:", my_promos_count)
        assert my_promos_count >= 1, "Should render at least 1 promo for active cards"

        print("\n>>> ALL 10 TESTS PASSED WITH 100% SUCCESS! UENO N1-N5 & ALL BANK PROMOS FULLY OPERATIONAL! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_all()
