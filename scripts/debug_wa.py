import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
    print("Button found, tag:", btn.tag_name)
    print("Button location before scroll:", btn.location)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    time.sleep(0.3)
    print("Button location after scroll:", btn.location)
    
    # Try clicking
    btn.click()
    time.sleep(0.3)
    toast = driver.find_element(By.ID, "toastMsg")
    toast_parent = driver.find_element(By.ID, "toastNotification")
    print("Toast innerHTML:", repr(toast.get_attribute("innerHTML")))
    print("Toast text:", repr(toast.text))
    print("Toast parent classes:", repr(toast_parent.get_attribute("class")))
    print("Window handles:", len(driver.window_handles))
    
    logs = driver.get_log('browser')
    print("Browser logs:", logs)

except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
