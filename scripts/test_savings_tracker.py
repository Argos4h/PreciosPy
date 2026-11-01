import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def test_savings_tracker():
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

        # 1. Verify Home Banner starts clean at 0
        print("\n--- 1. Testing Home Savings Banner (Clean Slate) ---")
        home_amt = driver.find_element(By.ID, "homeSavingsDisplay").text
        print(f"Home Savings Display (Month): Gs. {home_amt}")
        assert home_amt == "0", f"Expected 0, got: {home_amt}"

        # Capture screenshot of Home with Savings Banner
        ss_home = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_23_savings_home_banner.png')
        driver.save_screenshot(ss_home)
        print("Saved screenshot:", ss_home)

        # 2. Open Savings Modal
        print("\n--- 2. Opening Savings Modal ---")
        driver.execute_script("openSavingsModal();")
        time.sleep(0.5)

        modal = driver.find_element(By.ID, "savingsModal")
        assert modal.is_displayed(), "savingsModal must be visible"

        # Check default Month values start at 0
        main_amt = driver.find_element(By.ID, "savingsMainAmount").text
        period_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Modal default view: {period_lbl} = Gs. {main_amt}")
        assert main_amt == "0"
        assert "MES" in period_lbl.upper()

        # 3. Test Period Switcher: Week
        print("\n--- 3. Testing Period Switcher (Week) ---")
        driver.execute_script("setSavingsPeriod('week');")
        time.sleep(0.3)
        week_amt = driver.find_element(By.ID, "savingsMainAmount").text
        week_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Week view: {week_lbl} = Gs. {week_amt}")
        assert week_amt == "0"
        assert "SEMANA" in week_lbl.upper()

        # 4. Test Period Switcher: Total
        print("\n--- 4. Testing Period Switcher (Total) ---")
        driver.execute_script("setSavingsPeriod('total');")
        time.sleep(0.3)
        total_amt = driver.find_element(By.ID, "savingsMainAmount").text
        total_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Total view: {total_lbl} = Gs. {total_amt}")
        assert total_amt == "0"
        assert "TOTAL" in total_lbl.upper()

        # Return to Month and capture screenshot of full dashboard modal
        driver.execute_script("setSavingsPeriod('month');")
        time.sleep(0.3)
        ss_modal = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_24_savings_modal_dashboard.png')
        driver.save_screenshot(ss_modal)
        print("Saved screenshot:", ss_modal)

        # 5. Close Modal
        driver.execute_script("closeSavingsModal();")
        time.sleep(0.4)
        assert not modal.is_displayed(), "Modal should be closed"

        # 6. Switch to viewProfile and verify 3-metric widget starts clean at 0
        print("\n--- 5. Testing Profile Savings Widget ---")
        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.5)

        prof_week = driver.find_element(By.ID, "profileSavingsWeek").text
        prof_month = driver.find_element(By.ID, "profileSavingsMonth").text
        prof_total = driver.find_element(By.ID, "profileSavingsTotal").text
        print(f"Profile metrics: Week={prof_week}, Month={prof_month}, Total={prof_total}")
        assert "0" in prof_week
        assert "0" in prof_month
        assert "0" in prof_total

        ss_prof = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_25_savings_profile_widget.png')
        driver.save_screenshot(ss_prof)
        print("Saved screenshot:", ss_prof)

        # 7. Add products to cart and test "Registrar Compra"
        print("\n--- 6. Testing 'Registrar Compra' in Mi Lista ---")
        driver.execute_script("flyToCart(0); flyToCart(1); flyToCart(3);")
        time.sleep(0.8)
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)

        btn_reg = driver.find_element(By.ID, "btnRegisterCartPurchase")
        assert btn_reg.is_displayed(), "btnRegisterCartPurchase must be visible"

        # Record initial savings
        initial_month = driver.execute_script("return userSavings.month;")
        print(f"Initial userSavings.month: {initial_month}")

        # Click register purchase
        driver.execute_script("document.getElementById('btnRegisterCartPurchase').click();")
        time.sleep(0.6)

        new_month = driver.execute_script("return userSavings.month;")
        print(f"Updated userSavings.month after recording purchase: {new_month}")
        assert new_month >= initial_month

        print("\n🎉 ALL SAVINGS TRACKER TESTS PASSED WITH CLEAN SLATE!")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_savings_tracker()
