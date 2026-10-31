# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

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
    driver.execute_script("switchTab('viewCart');")
    time.sleep(0.5)

    p1 = driver.find_element(By.ID, "podium1Price").text
    p2 = driver.find_element(By.ID, "podium2Price").text
    p3 = driver.find_element(By.ID, "podium3Price").text

    subtotal_reg = driver.find_element(By.ID, "cartSubtotalRegular").text
    savings = driver.find_element(By.ID, "cartTotalSavings").text
    final_total = driver.find_element(By.ID, "cartFinalTotal").text

    print("=== PODIUM PRICES ===")
    print("Podium 1 (Biggie):", p1)
    print("Podium 2 (Superseis):", p2)
    print("Podium 3 (Stock):", p3)
    print("=== CART SUMMARY ===")
    print("Subtotal Regular:", subtotal_reg)
    print("Descuento:", savings)
    print("Total Final a Pagar:", final_total)

    # Now open split-cart
    split_toggle = driver.find_element(By.ID, "splitCartToggle")
    driver.execute_script("arguments[0].click();", split_toggle)
    time.sleep(0.5)

    split_container = driver.find_element(By.ID, "splitCartBreakdownContainer")
    print("=== SPLIT BREAKDOWN TEXT PREVIEW ===")
    print(split_container.text[:500])

finally:
    driver.quit()

