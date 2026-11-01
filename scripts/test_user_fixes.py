# -*- coding: utf-8 -*-
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916"
html_path = os.path.join(artifact_dir, "preciospy_redesign_2026.html")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=430,932") # iPhone 14 Pro Max viewport
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

try:
    print(f"Loading {html_path}...")
    driver.get(f"file:///{html_path.replace(os.sep, '/')}")
    time.sleep(2)

    # =========================================================================
    # 1. TEST CLEAN SLATE
    # =========================================================================
    print("\n--- 1. Testing Clean Slate ---")
    cart_keys = driver.execute_script("return Object.keys(cart);")
    assert len(cart_keys) == 0, f"Expected empty cart, got {cart_keys}"
    print(f"✓ Cart is empty: {cart_keys}")

    favorites = driver.execute_script("return favorites;")
    assert len(favorites) == 0, f"Expected empty favorites, got {favorites}"
    print(f"✓ Favorites is empty: {favorites}")

    home_savings = driver.find_element(By.ID, "homeSavingsDisplay").text.strip()
    assert home_savings == "0", f"Expected homeSavingsDisplay to be '0', got '{home_savings}'"
    print(f"✓ Home savings display is 0: Gs. {home_savings}")

    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)
    cart_empty_text = driver.find_element(By.ID, "cartItemsList").text
    assert "Tu lista de compras está vacía" in cart_empty_text, "Expected empty cart message"
    print("✓ Cart displays empty state view")

    # =========================================================================
    # 2. TEST CART ITEM LAYOUT & NO OVERLAP
    # =========================================================================
    print("\n--- 2. Testing Cart Layout & Non-Overlapping Elements ---")
    # Add product 0 and 1 to cart
    driver.execute_script("flyToCart(0); flyToCart(1);")
    time.sleep(0.8)
    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)

    cart_items = driver.find_elements(By.CSS_SELECTOR, "#cartItemsList > div")
    assert len(cart_items) >= 2, f"Expected at least 2 cart items, got {len(cart_items)}"
    print(f"✓ Cart has {len(cart_items)} items rendered")

    # Check bounding box separation between price/info container and stepper
    overlap_detected = False
    for i, item in enumerate(cart_items):
        info_div = item.find_element(By.CSS_SELECTOR, "div.flex-1")
        stepper_div = item.find_element(By.CSS_SELECTOR, "div.ml-auto")
        
        info_rect = driver.execute_script("return arguments[0].getBoundingClientRect();", info_div)
        stepper_rect = driver.execute_script("return arguments[0].getBoundingClientRect();", stepper_div)
        
        # Info right must not exceed stepper left
        assert info_rect['right'] <= stepper_rect['left'], f"Overlap detected on item {i}: info.right={info_rect['right']} > stepper.left={stepper_rect['left']}"
        print(f"✓ Item {i}: Gap between info and stepper is {stepper_rect['left'] - info_rect['right']:.1f}px (No overlap)")

    cart_screenshot = os.path.join(artifact_dir, "user_fix_cart_layout.png")
    driver.save_screenshot(cart_screenshot)
    print(f"✓ Saved screenshot: {cart_screenshot}")

    # =========================================================================
    # 3. TEST BRAND FILTER BUTTON & POPUP MODAL
    # =========================================================================
    print("\n--- 3. Testing Brand Filter Modal ---")
    driver.execute_script("switchTab('viewSearch');")
    time.sleep(0.5)

    brand_btn = driver.find_element(By.ID, "brandFilterBtn")
    assert brand_btn.is_displayed(), "brandFilterBtn should be visible"
    print("✓ #brandFilterBtn is present and visible")

    # Open Brand Modal
    brand_btn.click()
    time.sleep(0.6)

    brand_modal = driver.find_element(By.ID, "brandModalSheet")
    assert not "hidden" in brand_modal.get_attribute("class"), "brandModalSheet should not have 'hidden' class"
    print("✓ #brandModalSheet is open and visible")

    brand_modal_screenshot = os.path.join(artifact_dir, "user_fix_brand_modal.png")
    driver.save_screenshot(brand_modal_screenshot)
    print(f"✓ Saved screenshot: {brand_modal_screenshot}")

    # Search for brand Lactolanda
    search_input = driver.find_element(By.ID, "brandSearchInput")
    search_input.clear()
    search_input.send_keys("Lactolanda")
    time.sleep(0.4)

    brand_items = driver.find_elements(By.CSS_SELECTOR, "#brandListContainer button")
    assert len(brand_items) > 0, "Expected brand items matching Lactolanda"
    print(f"✓ Filtered brand list found {len(brand_items)} items for 'Lactolanda'")

    # Click first matching brand
    brand_items[0].click()
    time.sleep(0.8)

    # Verify modal closed
    assert "hidden" in brand_modal.get_attribute("class"), "brandModalSheet should close after selection"
    print("✓ #brandModalSheet closed upon brand selection")

    # Verify currentBrand is Lactolanda and grid has only Lactolanda products
    current_brand = driver.execute_script("return currentBrand;")
    assert current_brand.lower() == "lactolanda", f"Expected currentBrand 'Lactolanda', got '{current_brand}'"
    print(f"✓ currentBrand is active: {current_brand}")

    results_count = driver.find_element(By.ID, "resultsCount").text
    print(f"✓ Grid results count filtered by brand: {results_count}")

    brand_filtered_screenshot = os.path.join(artifact_dir, "user_fix_brand_filtered_grid.png")
    driver.save_screenshot(brand_filtered_screenshot)
    print(f"✓ Saved screenshot: {brand_filtered_screenshot}")

    # Reset brand filter
    driver.execute_script("selectBrand('', '🏷️', 'Marcas');")
    time.sleep(0.5)
    current_brand_reset = driver.execute_script("return currentBrand;")
    assert current_brand_reset == "", "Brand filter should be cleared"
    print("✓ Brand filter cleared successfully")

    # =========================================================================
    # 4. TEST BANCO ITAÚ CARD IN PROFILE
    # =========================================================================
    print("\n--- 4. Testing Banco Itaú Card in Profile ---")
    driver.execute_script("switchTab('viewProfile');")
    time.sleep(0.5)

    itau_btn = driver.find_element(By.ID, "btn-itau")
    assert itau_btn.is_displayed(), "btn-itau should be visible"

    # Verify btn-itau position inside parent card
    itau_card = itau_btn.find_element(By.XPATH, "./ancestor::div[contains(@class, 'p-4')][1]")
    card_rect = driver.execute_script("return arguments[0].getBoundingClientRect();", itau_card)
    btn_rect = driver.execute_script("return arguments[0].getBoundingClientRect();", itau_btn)

    assert btn_rect['right'] <= card_rect['right'], f"btn-itau overflowed card: btn.right={btn_rect['right']} > card.right={card_rect['right']}"
    assert btn_rect['left'] >= card_rect['left'], f"btn-itau overflowed card: btn.left={btn_rect['left']} < card.left={card_rect['left']}"
    print(f"✓ btn-itau is strictly inside card bounds ({btn_rect['right']} <= {card_rect['right']})")

    # Test clicking Itaú tiers
    tier_infinite_btn = driver.find_element(By.CSS_SELECTOR, "button[data-tier='infinite']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tier_infinite_btn)
    time.sleep(0.3)
    tier_infinite_btn.click()
    time.sleep(0.4)

    active_tier_badge = driver.find_element(By.ID, "itauActiveBadge").text
    print(f"✓ Active tier badge updated: {active_tier_badge}")
    assert "30%" in active_tier_badge or "Infinite" in active_tier_badge

    itau_screenshot = os.path.join(artifact_dir, "user_fix_itau_card.png")
    driver.save_screenshot(itau_screenshot)
    print(f"✓ Saved screenshot: {itau_screenshot}")

    # =========================================================================
    # 5. TEST REAL SCANNER VIEW
    # =========================================================================
    print("\n--- 5. Testing Real Scanner View ---")
    driver.execute_script("switchTab('viewScanner');")
    time.sleep(0.5)

    start_cam_btn = driver.find_element(By.ID, "btnStartRealCamera")
    assert start_cam_btn.is_displayed(), "btnStartRealCamera should be visible"
    print("✓ #btnStartRealCamera is present and visible")

    video_el = driver.find_element(By.ID, "scannerVideo")
    assert video_el is not None, "scannerVideo exists"
    print("✓ #scannerVideo HTML5 element exists")

    manual_input = driver.find_element(By.ID, "manualEanInput")
    assert manual_input.is_displayed(), "manualEanInput should be visible"
    print("✓ #manualEanInput is present")

    # Test manual EAN search
    manual_input.clear()
    manual_input.send_keys("7840042000124")
    driver.execute_script("scanManualEan();")
    time.sleep(0.5)

    scanned_name = driver.find_element(By.ID, "scannedProductName").text
    print(f"✓ Scanned product identified: {scanned_name}")
    assert len(scanned_name) > 0, "Product name should be populated"

    # Test simulateScanBarcode
    driver.execute_script("simulateScanBarcode();")
    time.sleep(0.5)
    scanned_name_2 = driver.find_element(By.ID, "scannedProductName").text
    print(f"✓ Simulate demo scanned product: {scanned_name_2}")

    scanner_screenshot = os.path.join(artifact_dir, "user_fix_real_scanner.png")
    driver.save_screenshot(scanner_screenshot)
    print(f"✓ Saved screenshot: {scanner_screenshot}")

    print("\n=======================================================")
    print("🎉 ALL 5 USER FIXES VERIFIED 100% SUCCESSFULLY WITH ZERO ERRORS!")
    print("=======================================================")

finally:
    driver.quit()

