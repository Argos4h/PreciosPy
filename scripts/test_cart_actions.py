import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

opt = Options()
opt.add_argument('--headless=new')
opt.add_argument('--window-size=1280,1000')
driver = webdriver.Chrome(options=opt)

try:
    file_path = os.path.abspath('preciospy_redesign_2026.html')
    driver.get('file:///' + file_path.replace(os.sep, '/'))
    time.sleep(1)

    print("=== TEST 1: Switch to viewCart ===")
    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)

    cart_keys = driver.execute_script("return Object.keys(cart).filter(k => cart[k] > 0);")
    print(f"Initial cart items: {cart_keys}")
    assert len(cart_keys) > 0, "Cart should initially have items"

    print("\n=== TEST 2: Click Vaciar Lista Button (Opens in-app Modal) ===")
    vaciar_btn = driver.find_element(By.XPATH, "//button[contains(., 'Vaciar lista')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", vaciar_btn)
    time.sleep(0.3)
    vaciar_btn.click()
    time.sleep(0.5)

    modal = driver.find_element(By.ID, "clearCartModal")
    modal_classes = modal.get_attribute("class")
    print(f"Modal classes after clicking Vaciar: {modal_classes}")
    assert "hidden" not in modal_classes, "Modal should NOT have 'hidden' class"
    print("PASS: clearCartModal is visible!")

    print("\n=== TEST 3: Click 'Cancelar' in Modal ===")
    cancel_btn = driver.find_element(By.XPATH, "//button[contains(., 'Cancelar')]")
    cancel_btn.click()
    time.sleep(0.3)
    modal_classes_after_cancel = modal.get_attribute("class")
    print(f"Modal classes after Cancel: {modal_classes_after_cancel}")
    assert "hidden" in modal_classes_after_cancel, "Modal should be hidden after cancel"
    cart_still = driver.execute_script("return Object.keys(cart).filter(k => cart[k] > 0);")
    assert len(cart_still) > 0, "Cart should still have items after cancel"
    print("PASS: Cancel kept items intact and hid modal!")

    print("\n=== TEST 4: Test WhatsApp with items in cart ===")
    wa_btn = driver.find_element(By.XPATH, "//button[contains(., 'Enviar por WhatsApp')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wa_btn)
    time.sleep(0.3)
    wa_btn.click()
    time.sleep(0.4)

    toast_msg = driver.find_element(By.ID, "toastMsg").get_attribute("textContent")
    print(f"Toast message after clicking WhatsApp: '{toast_msg}'")
    assert "WhatsApp" in toast_msg, f"Toast should mention WhatsApp, got: {toast_msg}"
    print("PASS: WhatsApp sharing triggered successfully!")

    print("\n=== TEST 5: Re-open Modal and Confirm Vaciar ===")
    vaciar_btn.click()
    time.sleep(0.3)
    confirm_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sí, Vaciar')]")
    confirm_btn.click()
    time.sleep(0.5)

    cart_empty = driver.execute_script("return Object.keys(cart).filter(k => cart[k] > 0);")
    print(f"Cart keys after confirm vaciar: {cart_empty}")
    assert len(cart_empty) == 0, "Cart should be completely empty"

    toast_msg = driver.find_element(By.ID, "toastMsg").get_attribute("textContent")
    print(f"Toast message after confirm vaciar: '{toast_msg}'")
    assert "vaciada" in toast_msg, f"Toast should confirm list cleared, got: {toast_msg}"

    cart_list = driver.find_element(By.ID, "cartItemsList")
    print(f"Cart list text: '{cart_list.get_attribute('textContent').strip()}'")
    assert "vacía" in cart_list.get_attribute("textContent"), "Cart UI should show empty state"
    print("PASS: Cart completely cleared and UI updated!")

    print("\n=== TEST 6: Test WhatsApp with EMPTY cart ===")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", wa_btn)
    time.sleep(0.2)
    wa_btn.click()
    time.sleep(0.4)
    toast_msg = driver.find_element(By.ID, "toastMsg").get_attribute("textContent")
    print(f"Toast message when cart is empty: '{toast_msg}'")
    assert "vacía" in toast_msg, f"Toast should warn cart is empty, got: {toast_msg}"
    print("PASS: WhatsApp correctly guards against empty cart!")

    print("\n=== TEST 7: Test Vaciar with EMPTY cart ===")
    vaciar_btn.click()
    time.sleep(0.4)
    toast_msg = driver.find_element(By.ID, "toastMsg").get_attribute("textContent")
    print(f"Toast message when clicking Vaciar with empty cart: '{toast_msg}'")
    assert "vacía" in toast_msg, f"Toast should warn list is already empty, got: {toast_msg}"
    assert "hidden" in modal.get_attribute("class"), "Modal should remain hidden when cart already empty"
    print("PASS: Vaciar button correctly informs user when cart is already empty!")

    print("\n=== ALL 7 CART & WHATSAPP TESTS PASSED WITH 100% SUCCESS! ===")

finally:
    driver.quit()
