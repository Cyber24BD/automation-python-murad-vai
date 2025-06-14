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
        buttons = WebDriverWait(self.driver, 15).until(
            EC.presence_of_all_elements_located(self.dropdown_buttons_locator)
        )
        if len(buttons) > index:
            return buttons[index]
        else:
            raise IndexError(f"Dropdown button not found at index {index}")

    def open_dropdown(self, index):
        try:
            button = self._get_dropdown_button(index)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            ActionChains(self.driver).move_to_element(button).click().perform()
            time.sleep(1.5)
            return True
        except Exception as e:
            print(f"Failed to open dropdown at index {index}: {e}")
            return False

    def close_dropdown(self):
        ActionChains(self.driver).move_by_offset(0, 100).click().perform()
        time.sleep(1)

    def select_value(self, index, label_name, target_value=None):
        """Select either max value or specific value depending on input."""
        try:
            if not self.open_dropdown(index):
                return False

            options = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.option_locator)
            )

            if not options:
                print(f"No options found in {label_name} dropdown.")
                self.close_dropdown()
                return False

            if target_value is None:
                # Select max value (first option)
                options[0].click()
                print(f"Selected max value for {label_name}: {options[0].text.strip()}")
            else:
                # Try to find matching option
                found = False
                for option in options:
                    text = option.text.strip()
                    if str(target_value) in text:
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
            print(f"Error selecting value for {label_name}: {str(e)}")
        return False

    def fill_form_based_on_dict(self, townhall_level, others):
        """Fill the form using provided town hall level and other dropdown values."""
        print(f"\nSetting Town Hall Level to: {townhall_level}")
        if not self.select_value(0, "Town Hall Level", townhall_level):
            print("Failed to set Town Hall Level. Using max value instead.")
            self.select_value(0, "Town Hall Level")

        for idx, (key, value) in enumerate(others.items()):
            print(f"Setting {key} to: {value}")
            if not self.select_value(idx + 1, key, value):  # Skip index 0 (Town Hall)
                print(f"Failed to set {key}, falling back to max value...")
                self.select_value(idx + 1, key)


# Dictionary defined outside the class
townhall_dict = {
    "Town Hall Level": "15",
    "King Level": "15",
    "Queen Level": "15",
    "Warden Level": "15",
    "Champion Level": "15"
}

# Optional: You can also define multiple dicts and loop through them
multi_config = [
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


def main():
    # Setup Chrome options
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\ayans\selenium-profile")
    options.add_argument("--start-maximized")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        handler = DropdownHandler(driver)
        driver.get("https://www.g2g.com/offers/create?service_id=f6a1aba5-473a-4044-836a-8968bbab16d7&brand_id=lgc_game_19955&root_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_path=5830014a-b974-45c6-9672-b51e83112fb7&relation_id=98da2461-14bf-44bb-8e8d-011a4f06c187 ")
        time.sleep(5)  # Wait for initial page load

        # Extract town hall level from dict
        th_level = townhall_dict["Town Hall Level"]
        others = {k: v for k, v in townhall_dict.items() if k != "Town Hall Level"}

        # Fill form based on dict
        handler.fill_form_based_on_dict(th_level, others)

        print("\n✅ Form filled successfully!")
        input("\nPress Enter to close browser...")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()