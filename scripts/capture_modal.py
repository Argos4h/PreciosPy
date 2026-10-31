import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--window-size=430,932')
driver = webdriver.Chrome(options=chrome_options)
try:
    file_path = os.path.abspath('preciospy_redesign_2026.html')
    driver.get('file:///' + file_path.replace(os.sep, '/'))
    time.sleep(1)
    driver.execute_script("switchTab('viewCart'); openClearCartModal();")
    time.sleep(0.6)
    artifact_dir = r"C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916"
    p = os.path.join(artifact_dir, "redesign_7_clear_modal.png")
    driver.save_screenshot(p)
    print("Captured clear modal successfully:", p)
finally:
    driver.quit()

