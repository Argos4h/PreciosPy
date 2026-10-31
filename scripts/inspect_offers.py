# -*- coding: utf-8 -*-
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.abspath('preciospy_redesign_2026.html')
file_url = f"file:///{html_path.replace(os.sep, '/')}"

chrome_options = Options()
chrome_options.add_argument('--headless=new')
driver = webdriver.Chrome(options=chrome_options)
try:
    driver.get(file_url)
    print('offer 0 (Kurupí):', driver.execute_script('return calculateProductOffer(products[0], selectedDay);'))
    print('offer 1 (Lactolanda):', driver.execute_script('return calculateProductOffer(products[1], selectedDay);'))
    print('offer 3 (Michelob):', driver.execute_script('return calculateProductOffer(products[3], selectedDay);'))
    print('prod 3 store:', driver.execute_script('return products[3].store;'))
finally:
    driver.quit()

