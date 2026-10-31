# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

chrome_options = Options()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--window-size=430,932')
driver = webdriver.Chrome(options=chrome_options)
try:
    file_url = 'file:///' + os.path.abspath('preciospy_redesign_2026.html').replace(os.sep, '/')
    driver.get(file_url)
    time.sleep(1.0)
    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.4)
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "splitCartToggle"))
    time.sleep(0.5)
    driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_8_split_breakdown.png')
    print("Updated redesign_8_split_breakdown.png successfully!")
finally:
    driver.quit()

