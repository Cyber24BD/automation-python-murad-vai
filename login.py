from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from config import username_g2g, password_g2g
from config import selenium_web_driver_path

# Setup Chrome options
options = Options()
options.add_argument(selenium_web_driver_path)  # Safe custom profile

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the login page
    driver.get("https://www.g2g.com/login")
    
    # Wait for the username field to be present and fill it
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-attr='username-input']"))
    )
    # username_field.send_keys(username_g2g)  # Replace with your sample email
    
    # Find and fill the password field
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    # password_field.send_keys(password_g2g)  # Replace with your sample password
    
    # Find and click the login button
    login_button = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
    # login_button.click()
    time.sleep(3600)
    
    print("Login process completed!")
    
    # Keep the browser open for 10 seconds to see the result
    time.sleep(10)
    
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:    
    time.sleep(20)
