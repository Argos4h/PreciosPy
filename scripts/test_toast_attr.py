import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Force utf-8 output for windows console
sys.stdout.reconfigure(encoding='utf-8')

opt = Options()
opt.add_argument('--headless=new')
opt.add_argument('--window-size=1280,1000')
driver = webdriver.Chrome(options=opt)
try:
    file_path = os.path.abspath('preciospy_redesign_2026.html')
    driver.get('file:///' + file_path.replace(os.sep, '/'))
    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)

    btn = driver.find_element(By.XPATH, "//button[contains(., 'Enviar por WhatsApp')]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    time.sleep(0.3)
    btn.click()
    time.sleep(0.3)

    toast_elem = driver.find_element(By.ID, "toastMsg")
    text_content = toast_elem.get_attribute("textContent")
    print(f"textContent: {text_content}")
    print(f"Selenium text: {toast_elem.text}")
    print(f"Parent classes: {driver.find_element(By.ID, 'toastNotification').get_attribute('class')}")

finally:
    driver.quit()

