from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class DropdownHandler:
    def __init__(self, driver):
        self.driver = driver
        self.dropdown_buttons_locator = (By.CSS_SELECTOR, "button.g-btn-outlined")
        self.option_locator = (By.CSS_SELECTOR, "div.q-item__section--main")

    def _get_dropdown_button(self, index):
        """Helper to get a dropdown button by index."""
        buttons = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located(self.dropdown_buttons_locator)
        )
        if len(buttons) > index:
            return buttons[index]
        else:
            raise IndexError(f"Dropdown button not found at index {index}")

    def open_dropdown(self, index):
        """Open the dropdown at given index."""
        try:
            button = self._get_dropdown_button(index)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            ActionChains(self.driver).move_to_element(button).click().perform()
            time.sleep(1.5)  # Wait for dropdown to appear
            return True
        except Exception as e:
            print(f"Failed to open dropdown at index {index}: {e}")
            return False

    def close_dropdown(self):
        """Close the currently opened dropdown."""
        ActionChains(self.driver).move_by_offset(0, 100).click().perform()
        time.sleep(1)

    def select_max_value(self, index, label_name):
        """Select the first (max) option from dropdown."""
        try:
            if not self.open_dropdown(index):
                return False

            options = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.option_locator)
            )
            if options:
                options[0].click()
                print(f"Selected max value for {label_name}: {options[0].text.strip()}")
                time.sleep(1)
                return True
            else:
                print(f"No options found in {label_name} dropdown.")
                self.close_dropdown()
        except Exception as e:
            print(f"Error selecting max value for {label_name}: {str(e)}")
        return False

    def select_specific_value(self, index, label_name, target_value):
        """Select a specific value from the dropdown."""
        try:
            if not self.open_dropdown(index):
                return False

            options = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.option_locator)
            )

            found = False
            for option in options:
                text = option.text.strip()
                if target_value in text:
                    option.click()
                    print(f"Selected value for {label_name}: {text}")
                    found = True
                    break

            if not found:
                print(f"Could not find '{target_value}' in {label_name} dropdown.")
                self.close_dropdown()
                return False

            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error selecting specific value for {label_name}: {str(e)}")
        return False

    def get_dropdown_options(self, index, label_name):
        """Retrieve all available options from a dropdown."""
        try:
            if not self.open_dropdown(index):
                return []

            options = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.option_locator)
            )
            values = [option.text.strip() for option in options]
            self.close_dropdown()
            return values
        except Exception as e:
            print(f"Error fetching options for {label_name}: {str(e)}")
            return []


def main():
    # Setup Chrome options
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\ayans\selenium-profile")  # Safe custom profile
    options.add_argument("--start-maximized")  # Start with maximized window

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.g2g.com/offers/create?service_id=f6a1aba5-473a-4044-836a-8968bbab16d7&brand_id=lgc_game_19955&root_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_path=5830014a-b974-45c6-9672-b51e83112fb7&relation_id=98da2461-14bf-44bb-8e8d-011a4f06c187 ")

        time.sleep(5)  # Wait for initial page load

        handler = DropdownHandler(driver)

        townhall_dict = [
            {
                "Town Hall Level": "15",
                "King Level": "15",
                "Queen Level": "15",
                "Warden Level": "15",
                "Champion Level": "15"
            },
            {
                "Town Hall Level": "16",
                "King Level": "16",
                "Queen Level": "16",
                "Warden Level": "16",
                "Champion Level": "16"
            },
            {
                "Town Hall Level": "17",
                "King Level": "17",
                "Queen Level": "17",
                "Warden Level": "17",
                "Champion Level": "17"
            }
        ]

        # Select Town Hall level based on user input
        print("\nFetching Town Hall Levels...")
        th_options = handler.get_dropdown_options(0, "Town Hall Level")
        print("Available Town Hall levels:")
        for opt in th_options:
            print(opt)

        while True:
            user_input = input("\nEnter Town Hall level (e.g., '15' or 'Town Hall 15'): ").strip()
            if handler.select_specific_value(0, "Town Hall Level", user_input):
                break
            else:
                print("Invalid input. Please try again.")

        # Automatically set other levels to match selected TH level
        selected_th_level = next((item for item in townhall_dict if item["Town Hall Level"] in user_input), None)
        if selected_th_level:
            print("\nSetting dependent levels automatically...")
            for idx, key in enumerate(selected_th_level):
                if idx == 0:
                    continue  # Skip Town Hall since already selected
                val = selected_th_level[key]
                if not handler.select_specific_value(idx, key, val):
                    print(f"Failed to set {key} to {val}")
        else:
            print("Falling back to max values for dependent levels...")
            defaults = [
                (1, "King Level"),
                (2, "Queen Level"),
                (3, "Warden Level"),
                (4, "Champion Level")
            ]
            for idx, name in defaults:
                handler.select_max_value(idx, name)

        print("\n✅ All operations completed successfully!")
        input("\nPress Enter to close browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()