import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.stdout.reconfigure(encoding='utf-8')

opt = Options()
opt.add_argument('--headless=new')
opt.add_argument('--window-size=1280,1000')
driver = webdriver.Chrome(options=opt)

try:
    file_path = os.path.abspath('preciospy_redesign_2026.html')
    driver.get('file:///' + file_path.replace(os.sep, '/'))
    time.sleep(1)

    print("=== TEST 1: Live Clock in Status Bar ===")
    clock_text = driver.find_element(By.ID, "statusBarClock").text.strip()
    print(f"Status bar clock: '{clock_text}'")
    assert ":" in clock_text and len(clock_text) == 5, f"Clock should be HH:MM format, got: {clock_text}"
    print("PASS: Live clock working!")

    print("\n=== TEST 2: Dynamic Calendar Days with 'HOY' Badge ===")
    day_chips = driver.find_elements(By.CLASS_NAME, "day-chip")
    print(f"Total day chips: {len(day_chips)}")
    assert len(day_chips) == 7, "Should have 7 day chips"
    chip_texts = [c.text for c in day_chips]
    print(f"Day chips texts: {chip_texts}")
    assert any("HOY" in t for t in chip_texts), "At least one chip should have HOY badge"
    print("PASS: Calendar days dynamically rendered with HOY badge!")

    print("\n=== TEST 3: Favorites Filter Chip ===")
    fav_filter_btn = driver.find_element(By.ID, "btnFavFilter")
    fav_filter_btn.click()
    time.sleep(0.4)
    res_count = int(driver.find_element(By.ID, "resultsCount").text)
    print(f"Products shown in Favorites Only: {res_count}")
    assert res_count > 0, "Should show favored products"
    fav_filter_btn.click()
    time.sleep(0.4)
    all_count = int(driver.find_element(By.ID, "resultsCount").text)
    print(f"Products shown after disabling Favorites filter: {all_count}")
    assert all_count == 12, "Should show all 12 products"
    print("PASS: Favorites filter chip works bidirectionally!")

    print("\n=== TEST 4: Barcode Search ===")
    search_input = driver.find_element(By.ID, "searchInput")
    search_input.clear()
    search_input.send_keys("7840127000124")
    time.sleep(0.4)
    search_res = int(driver.find_element(By.ID, "resultsCount").text)
    print(f"Search results for EAN 7840127000124: {search_res}")
    assert search_res == 1, "Should find 1 product matching barcode"
    driver.find_element(By.ID, "clearSearchBtn").click()
    time.sleep(0.3)
    print("PASS: Barcode EAN search works!")

    print("\n=== TEST 5: Scanner View Quick Barcode Chips & 'Ver en 5 Súper' ===")
    driver.execute_script("switchTab('viewScanner');")
    time.sleep(0.5)
    # Click Lactolanda quick barcode chip
    lactolanda_chip = driver.find_element(By.XPATH, "//button[contains(., 'Lactolanda')]")
    lactolanda_chip.click()
    time.sleep(0.4)
    scanned_name = driver.find_element(By.ID, "scannedProductName").text
    print(f"Scanned product after clicking Lactolanda chip: '{scanned_name}'")
    assert "Lactolanda" in scanned_name, f"Expected Lactolanda, got: {scanned_name}"

    # Click "Ver en 5 Súper" from scanner view
    ver_super_btn = driver.find_element(By.XPATH, "//button[contains(., 'Ver en 5 Súper')]")
    ver_super_btn.click()
    time.sleep(0.5)
    modal = driver.find_element(By.ID, "productDetailModal")
    assert "hidden" not in modal.get_attribute("class"), "Knasta modal should open from Scanner view"
    print("PASS: Scanner quick barcode and direct 5 supermarkets comparison work!")

    print("\n=== TEST 6: Dismiss Modal with Escape Key ===")
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    time.sleep(0.4)
    assert "hidden" in modal.get_attribute("class"), "Modal should close with ESC"
    print("PASS: Escape key dismisses modals!")

    print("\n=== TEST 7: Dismiss Modal by Clicking Backdrop ===")
    driver.execute_script("openProductDetail(0);")
    time.sleep(0.4)
    assert "hidden" not in modal.get_attribute("class"), "Modal reopened"
    # Click outer backdrop
    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", modal)
    time.sleep(0.4)
    assert "hidden" in modal.get_attribute("class"), "Modal should close on backdrop click"
    print("PASS: Backdrop tap closes modal!")

    print("\n=== TEST 8: Reset Data Modal in Profile View ===")
    driver.execute_script("switchTab('viewProfile');")
    time.sleep(0.5)
    driver.execute_script("openResetDataModal();")
    time.sleep(0.4)
    reset_modal = driver.find_element(By.ID, "resetDataModal")
    assert "hidden" not in reset_modal.get_attribute("class"), "Reset modal should open"
    cancel_reset = reset_modal.find_element(By.XPATH, ".//button[contains(., 'Cancelar')]")
    cancel_reset.click()
    time.sleep(0.4)
    assert "hidden" in reset_modal.get_attribute("class"), "Reset modal should close on cancel"
    print("PASS: In-app Reset confirmation modal works safely!")

    print("\n=== TEST 9: Cash Mode Persistence ===")
    # Toggle cash mode
    driver.execute_script("toggleCashMode();")
    cash_val = driver.execute_script("return isCashOnly;")
    print(f"isCashOnly set to: {cash_val}")
    saved_cash = driver.execute_script("return localStorage.getItem('preciospy_2_cash_mode');")
    print(f"localStorage preciospy_2_cash_mode: {saved_cash}")
    assert "true" in saved_cash.lower(), "Cash mode must be saved to localStorage"
    # Toggle back
    driver.execute_script("toggleCashMode();")
    print("PASS: Cash mode persists to localStorage!")

    print("\n=== ALL 9 NEW ENHANCEMENTS TESTS PASSED 100%! ===")

finally:
    driver.quit()
