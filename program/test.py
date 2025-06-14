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
    """Select the maximum value from a dropdown."""
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



def get_dropdown_options(driver, button_index, label_name):
    """Get all available options from a dropdown."""
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
            print(f"Clicked {label_name} dropdown button to view options")
            
            # Wait for the dropdown options to be visible
            time.sleep(1.5)
            
            # Find all the options in the dropdown
            options = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.q-item__section--main"))
            )
            
            # Get the text values of all options
            option_values = [option.text.strip() for option in options]
            
            # Close the dropdown by clicking outside
            ActionChains(driver).move_by_offset(0, 100).click().perform()
            time.sleep(1)
            
            return option_values
        else:
            print(f"Could not find {label_name} dropdown button at index {button_index}")
            
    except Exception as e:
        print(f"Error getting options for {label_name}: {str(e)}")
        
    return []

def select_specific_value(driver, button_index, label_name, target_value):
    """Select a specific value from a dropdown based on user input."""
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
            
            # Try to find and click the option that matches the target value
            found = False
            for option in options:
                option_text = option.text.strip()
                if target_value in option_text:
                    option.click()
                    print(f"Selected value for {label_name}: {option_text}")
                    found = True
                    time.sleep(1)  # Wait for dropdown to close
                    break
            
            if not found:
                print(f"Could not find option '{target_value}' in {label_name} dropdown")
                # Close the dropdown by clicking outside
                ActionChains(driver).move_by_offset(0, 100).click().perform()
                time.sleep(1)
                return False
            
            return True
        else:
            print(f"Could not find {label_name} dropdown button at index {button_index}")
            
    except Exception as e:
        print(f"Error in {label_name} selection: {str(e)}")
        
    return False

def main():
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
        
        # Get Town Hall dropdown options first
        town_hall_options = get_dropdown_options(driver, 0, "Town Hall Level")
        
        if town_hall_options:
            print("\nAvailable Town Hall levels:")
            for i, option in enumerate(town_hall_options):
                print(f"{i+1}. {option}")
            
            while True:
                try:
                    # Get user input for Town Hall level
                    user_input = input("\nEnter Town Hall level (e.g. '15' or 'Town Hall 15'): ")
                    
                    # Check if input matches any available option
                    if select_specific_value(driver, 0, "Town Hall Level", user_input):
                        break
                    else:
                        print("Invalid input. Please choose from the available options.")
                except ValueError:
                    print("Invalid input. Please enter a valid Town Hall level.")
        else:
            print("Could not retrieve Town Hall level options. Using max value instead.")
            select_max_value(driver, 0, "Town Hall Level")
        
        # Process other dropdowns to max values
        other_dropdowns = [
            (1, "King Level"),
            (2, "Queen Level"),
            (3, "Warden Level"),
            (4, "Champion Level")
        ]
        
        for index, label in other_dropdowns:
            if not select_max_value(driver, index, label):
                print(f"Failed to process {label} dropdown")
        
        print("All dropdowns processed successfully!")
        
        # Keep the browser open for review
        input("\nPress Enter to close the browser...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        
    finally:    
        driver.quit()

if __name__ == "__main__":
    main()