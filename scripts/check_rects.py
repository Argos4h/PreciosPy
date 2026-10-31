import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

opt = Options()
opt.add_argument('--headless=new')
opt.add_argument('--window-size=1200,1000')
d = webdriver.Chrome(options=opt)
try:
    d.get('file:///' + os.path.abspath('preciospy_redesign_2026.html').replace(os.sep, '/'))
    d.execute_script("switchTab('viewCart');")
    nav = d.find_element(By.TAG_NAME, 'nav')
    print('Nav rect:', nav.rect)
    btns = d.find_elements(By.TAG_NAME, 'button')
    for b in btns:
        if 'Vaciar' in b.text or 'WhatsApp' in b.text:
            print(b.text, 'rect:', b.rect)
finally:
    d.quit()

