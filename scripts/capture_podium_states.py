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
    time.sleep(0.5)

    # 1. Top 1 Stock
    driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_11_top1_stock_only.png')

    # 2. Top 2 Superseis
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "podiumCardSuperseis"))
    time.sleep(0.4)
    driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_12_top2_superseis_only.png')

    # 3. Top 3 Biggie
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "podiumCardBiggie"))
    time.sleep(0.4)
    driver.save_screenshot('C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/redesign_13_top3_biggie_only.png')

    print("Podium screenshots taken successfully!")
finally:
    driver.quit()

