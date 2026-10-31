import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def test_bank_circle_toggles():
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

        # Navigate to viewProfile (Billetera & Niveles)
        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.5)

        # Check all 9 bank toggle buttons and their circle thumbs
        banks = ['ueno', 'itau', 'continental', 'zeta', 'familiar', 'atlas', 'sudameris', 'gnb', 'basa']
        for b in banks:
            btn = driver.find_element(By.ID, f"btn-{b}")
            thumb = driver.find_element(By.ID, f"thumb-{b}")
            assert btn is not None, f"Button btn-{b} missing"
            assert thumb is not None, f"Thumb thumb-{b} missing"
            btn_class = btn.get_attribute("class")
            thumb_class = thumb.get_attribute("class")
            assert "rounded-full" in btn_class, f"btn-{b} must be rounded-full"
            assert "rounded-full" in thumb_class, f"thumb-{b} must be rounded-full circle"
            print(f"Bank {b}: btn class contains rounded-full, thumb class contains rounded-full")

        # Initial check: ueno is enabled -> translate-x-6 & bg-emerald-500
        ueno_thumb = driver.find_element(By.ID, "thumb-ueno")
        assert "translate-x-6" in ueno_thumb.get_attribute("class"), "ueno thumb should be translated right"
        
        # Initial check: continental is disabled -> translate-x-0 & bg-slate-800
        conti_thumb = driver.find_element(By.ID, "thumb-continental")
        assert "translate-x-0" in conti_thumb.get_attribute("class"), "continental thumb should be translated left"

        # Toggle Continental on
        driver.find_element(By.ID, "btn-continental").click()
        time.sleep(0.3)
        conti_enabled = driver.execute_script("return bankProfiles.continental.enabled;")
        assert conti_enabled == True, "Continental should be enabled after click"
        conti_thumb_after = driver.find_element(By.ID, "thumb-continental")
        assert "translate-x-6" in conti_thumb_after.get_attribute("class"), "continental thumb should move right on activate"
        print("Continental toggled ON: circle moved right (translate-x-6) successfully!")

        # Toggle ueno off
        driver.find_element(By.ID, "btn-ueno").click()
        time.sleep(0.3)
        ueno_enabled = driver.execute_script("return bankProfiles.ueno.enabled;")
        assert ueno_enabled == False, "ueno should be disabled after click"
        ueno_thumb_after = driver.find_element(By.ID, "thumb-ueno")
        assert "translate-x-0" in ueno_thumb_after.get_attribute("class"), "ueno thumb should move left on deactivate"
        print("ueno toggled OFF: circle moved left (translate-x-0) successfully!")

        # Toggle ueno back ON
        driver.find_element(By.ID, "btn-ueno").click()
        time.sleep(0.3)
        assert driver.execute_script("return bankProfiles.ueno.enabled;") == True

        # Take screenshot of viewProfile for verification artifact
        artifact_path = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_16_cards_circle_toggles.png')
        driver.save_screenshot(artifact_path)
        print("Screenshot saved to:", artifact_path)

        print(">>> ALL CIRCLE TOGGLE TESTS PASSED WITH 100% SUCCESS! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_bank_circle_toggles()

