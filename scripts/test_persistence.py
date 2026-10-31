import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_persistence():
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
        time.sleep(1.0)

        # 1. Check initial storage or defaults
        initial_cart = driver.execute_script("return JSON.stringify(cart);")
        print("Initial cart:", initial_cart)

        # 2. Modify cart and city in JS
        driver.execute_script("""
            quickAddToCart(0); // Add Kurupí
            quickAddToCart(0);
            selectCity('Asunción');
            toggleBankProfile('sudameris'); // Enable Sudameris
        """)
        time.sleep(0.5)

        # 3. Check localStorage content
        storage_val = driver.execute_script("return localStorage.getItem('preciospy_user_data_v1');")
        print("Saved to localStorage:", storage_val)
        assert storage_val is not None, "localStorage must have saved data!"
        assert "Asunción" in storage_val, "selectedCity must be Asunción!"
        assert "sudameris" in storage_val, "sudameris profile must be saved!"

        # 4. Reload page to simulate closing and reopening browser
        driver.refresh()
        time.sleep(1.5)

        # 5. Verify that restored state matches modified state!
        reloaded_city = driver.execute_script("return selectedCity;")
        reloaded_sudameris = driver.execute_script("return bankProfiles.sudameris.enabled;")
        reloaded_cart_kurupi = driver.execute_script("return cart[0];")

        print("After reload - City:", reloaded_city)
        print("After reload - Sudameris enabled:", reloaded_sudameris)
        print("After reload - Kurupi qty:", reloaded_cart_kurupi)

        assert reloaded_city == 'Asunción', f"Expected Asunción, got {reloaded_city}"
        assert reloaded_sudameris == True, f"Expected Sudameris enabled, got {reloaded_sudameris}"
        assert reloaded_cart_kurupi >= 3, f"Expected Kurupí qty >= 3, got {reloaded_cart_kurupi}"

        print("PERSISTENCE TEST PASSED: State survived page reload perfectly!")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_persistence()

