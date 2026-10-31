import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
try:
    file_path = os.path.abspath('preciospy_redesign_2026.html')
    driver.get('file:///' + file_path.replace(os.sep, '/'))
    time.sleep(1)

    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)

    # Check button for vaciar lista
    btns = driver.find_elements(By.TAG_NAME, "button")
    vaciar_btns = [b for b in btns if "Vaciar" in b.text or "vaciar" in b.text.lower()]
    print("Found vaciar buttons:", [b.text for b in vaciar_btns])

    # Check cart items
    cart_keys = driver.execute_script("return Object.keys(cart);")
    print("Cart keys initially:", cart_keys)

    # Click vaciar
    if vaciar_btns:
        print("Clicking vaciar button...")
        vaciar_btns[0].click()
        time.sleep(0.5)
        try:
            alert = driver.switch_to.alert
            print("Alert detected:", alert.text)
            alert.accept()
        except Exception as e:
            print("No alert or error handling alert:", e)
        time.sleep(0.5)
        cart_after = driver.execute_script("return Object.keys(cart);")
        print("Cart keys after clicking vaciar:", cart_after)

    # Check shareCartWhatsApp
    print("\nTesting shareCartWhatsApp...")
    whatsapp_btns = [b for b in btns if "WhatsApp" in b.text]
    print("WhatsApp buttons found:", [b.text for b in whatsapp_btns])
    if whatsapp_btns:
        print("Clicking WhatsApp button...")
        whatsapp_btns[0].click()
        time.sleep(1)
        print("Window handles:", len(driver.window_handles))

finally:
    driver.quit()

