import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_scrolled_screenshot():
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

        driver.execute_script("switchTab('viewProfile');")
        time.sleep(0.5)

        driver.execute_script("document.querySelector('main').scrollTop = 600;")
        time.sleep(0.5)

        artifact_path = os.path.abspath(r'C:\Users\munic\.gemini\antigravity\brain\3ac93072-98c3-495f-ad02-c8cfc7984916\redesign_17_cards_scrolled_toggles.png')
        driver.save_screenshot(artifact_path)
        print("Scrolled screenshot saved:", artifact_path)

    finally:
        driver.quit()

if __name__ == '__main__':
    take_scrolled_screenshot()
