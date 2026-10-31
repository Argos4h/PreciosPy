import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def verify_auto_day():
    html_path = os.path.abspath('precios_py_demo.html')
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--window-size=430,932')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(file_url)
        time.sleep(1.5)

        # Check JS state
        state = driver.execute_script("""
            return {
                selectedDay: typeof selectedDay !== 'undefined' ? selectedDay : null,
                promoSelectedDay: typeof promoSelectedDay !== 'undefined' ? promoSelectedDay : null,
                todayIso: typeof getTodayIsoDay === 'function' ? getTodayIsoDay() : null
            };
        """)
        print("JS Day State:", state)

        # Check Day Chips in Search Tab
        chips = driver.find_elements(By.CSS_SELECTOR, ".day-chip")
        for c in chips:
            day = c.get_attribute("data-day")
            text = c.text
            classes = c.get_attribute("class")
            is_active = "bg-emerald-500" in classes
            print(f"Search Day Chip [{day}]: text='{text}', active={is_active}")

        screenshot_path = os.path.abspath("C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/demo_auto_saturday_selected.png")
        driver.save_screenshot(screenshot_path)
        print("Search screenshot saved:", screenshot_path)

        # Switch to Promos Tab
        driver.execute_script("switchTab('viewPromos');")
        time.sleep(1.0)
        
        promo_sub = driver.find_element(By.ID, "promosSubtitle").text
        print("Promos Subtitle:", promo_sub)

        promo_chips = driver.find_elements(By.CSS_SELECTOR, ".promo-day-chip")
        for pc in promo_chips:
            day = pc.get_attribute("data-day")
            text = pc.text
            classes = pc.get_attribute("class")
            is_active = "bg-emerald-500" in classes
            print(f"Promo Day Chip [{day}]: text='{text}', active={is_active}")

        promo_screenshot = os.path.abspath("C:/Users/munic/.gemini/antigravity/brain/3ac93072-98c3-495f-ad02-c8cfc7984916/demo_promos_saturday_selected.png")
        driver.save_screenshot(promo_screenshot)
        print("Promos screenshot saved:", promo_screenshot)

    finally:
        driver.quit()

if __name__ == '__main__':
    verify_auto_day()
