import os, time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

sys.stdout.reconfigure(encoding='utf-8')

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

        # 1. Verify Home Banner
        print("\n--- 1. Testing Home Savings Banner ---")
        home_amt = driver.find_element(By.ID, "homeSavingsDisplay").text
        print(f"Home Savings Display (Month): Gs. {home_amt}")
        assert home_amt == "542.000", f"Expected 542.000, got: {home_amt}"

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

        # Check default Month values
        main_amt = driver.find_element(By.ID, "savingsMainAmount").text
        period_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Modal default view: {period_lbl} = Gs. {main_amt}")
        assert main_amt == "542.000"
        assert "MES" in period_lbl.upper()

        # 3. Test Period Switcher: Week
        print("\n--- 3. Testing Period Switcher (Week) ---")
        driver.execute_script("setSavingsPeriod('week');")
        time.sleep(0.3)
        week_amt = driver.find_element(By.ID, "savingsMainAmount").text
        week_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Week view: {week_lbl} = Gs. {week_amt}")
        assert week_amt == "128.500"
        assert "SEMANA" in week_lbl.upper()

        # 4. Test Period Switcher: Total
        print("\n--- 4. Testing Period Switcher (Total) ---")
        driver.execute_script("setSavingsPeriod('total');")
        time.sleep(0.3)
        total_amt = driver.find_element(By.ID, "savingsMainAmount").text
        total_lbl = driver.find_element(By.ID, "savingsPeriodLabel").text
        print(f"Total view: {total_lbl} = Gs. {total_amt}")
        assert total_amt == "1.845.000"
        assert "TOTAL" in total_lbl.upper()

        # Return to Month and capture screenshot of full dashboard modal
        driver.execute_script("setSavingsPeriod('month');")
        time.sleep(0.3)
        ss_modal = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_24_savings_modal_dashboard.png')
        driver.save_screenshot(ss_modal)
        print("Saved screenshot:", ss_modal)

        # Check breakdown percentages exist
        bank_share = driver.find_element(By.ID, "savingsBankShare").text
        store_share = driver.find_element(By.ID, "savingsStoreShare").text
        split_share = driver.find_element(By.ID, "savingsSplitShare").text
        print(f"Breakdown: Bank={bank_share}, Store={store_share}, Split={split_share}")
        assert "58%" in bank_share
        assert "28%" in store_share
        assert "14%" in split_share

        # 5. Close Modal
        driver.execute_script("closeSavingsModal();")
        time.sleep(0.4)
        assert not modal.is_displayed(), "Modal should be closed"

        # 6. Switch to viewProfile and verify 3-metric widget
        print("\n--- 5. Testing Profile Savings Widget ---")
        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.5)

        prof_week = driver.find_element(By.ID, "profileSavingsWeek").text
        prof_month = driver.find_element(By.ID, "profileSavingsMonth").text
        prof_total = driver.find_element(By.ID, "profileSavingsTotal").text
        print(f"Profile metrics: Week={prof_week}, Month={prof_month}, Total={prof_total}")
        assert "128.500" in prof_week
        assert "542.000" in prof_month
        assert "1.845.000" in prof_total

        ss_prof = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_25_savings_profile_widget.png')
        driver.save_screenshot(ss_prof)
        print("Saved screenshot:", ss_prof)

        # 7. Switch to viewCart and test "Registrar Compra"
        print("\n--- 6. Testing 'Registrar Compra' in Mi Lista ---")
        driver.execute_script("switchTab('viewCart');")
        time.sleep(0.5)

        btn_reg = driver.find_element(By.ID, "btnRegisterCartPurchase")
        assert btn_reg.is_displayed(), "btnRegisterCartPurchase must be visible"

        # Record initial savings
        initial_month = driver.execute_script("return userSavings.month;")
        print(f"Initial userSavings.month before cart registration: {initial_month}")

        # Click register purchase
        driver.execute_script("document.getElementById('btnRegisterCartPurchase').click();")
        time.sleep(1.0)

        new_month = driver.execute_script("return userSavings.month;")
        print(f"New userSavings.month after cart registration: {new_month}")
        assert new_month > initial_month, f"Savings should have increased from {initial_month}, now {new_month}"

        # Verify history updated
        hist_len = driver.execute_script("return userSavings.history.length;")
        print(f"History entries count: {hist_len}")
        assert hist_len >= 6, f"Expected at least 6 history entries, got {hist_len}"

        print("\n>>> ALL SAVINGS TRACKER TESTS PASSED WITH 100% SUCCESS! <<<")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_savings_tracker()
