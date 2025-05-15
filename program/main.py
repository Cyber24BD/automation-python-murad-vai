from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

def select_max_value(driver, button_index, label_name):
    try:
        # Find all dropdown buttons
        dropdown_buttons = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.g-btn-outlined"))
        )
        
        if len(dropdown_buttons) > button_index:
            # Scroll to the button to make it clickable
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_buttons[button_index])
            time.sleep(1)
            
            # Click the dropdown button
            ActionChains(driver).move_to_element(dropdown_buttons[button_index]).click().perform()
            print(f"Clicked {label_name} dropdown button")
            
            # Wait for the dropdown options to be visible
            time.sleep(1.5)
            
            # Find all the options in the dropdown
            options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.q-item__section--main"))
            )
            
            if options:
                # Select the first option (maximum value)
                options[0].click()
                print(f"Selected max value for {label_name}: {options[0].text.strip()}")
                time.sleep(1)  # Wait for dropdown to close
                return True
            else:
                print(f"No options found in {label_name} dropdown")
        else:
            print(f"Could not find {label_name} dropdown button at index {button_index}")
            
    except Exception as e:
        print(f"Error in {label_name} selection: {str(e)}")
        
    return False

# Setup Chrome options
options = Options()
options.add_argument(r"user-data-dir=C:\Users\ayans\selenium-profile")  # Safe custom profile
options.add_argument("--start-maximized")  # Start with maximized window

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open the page
    driver.get("https://www.g2g.com/offers/create?service_id=f6a1aba5-473a-4044-836a-8968bbab16d7&brand_id=lgc_game_19955&root_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_path=5830014a-b974-45c6-9672-b51e83112fb7&relation_id=98da2461-14bf-44bb-8e8d-011a4f06c187")
    
    # Wait for the page to load completely
    time.sleep(5)
    
    # List of dropdown labels and their expected indices
    dropdowns = [
        (0, "Town Hall Level"),
        (1, "King Level"),
        (2, "Queen Level"),
        (3, "Warden Level"),
        (4, "Champion Level")
    ]
    
    # Process each dropdown
    for index, label in dropdowns:
        if not select_max_value(driver, index, label):
            print(f"Failed to process {label} dropdown")
    
    print("All dropdowns processed successfully!")
    
    # Keep the browser open for 10 seconds to see the result
    time.sleep(10)
    
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()
    
finally:    
    time.sleep(5)
    driver.quit()