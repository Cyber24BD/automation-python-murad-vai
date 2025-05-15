from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.option_locator))
            return True
        except Exception as e:
            print(f"Failed to open dropdown at index {index}: {e}")
            return False

    def close_dropdown(self):
        """Close the currently opened dropdown."""
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

    def fill_form_based_on_dict(self, th_level, kl_level, ql_level, wl_level, cl_level):
        """Fill form by accepting each field separately - only if provided"""
        if th_level:
            print(f"Setting Town Hall Level to: {th_level}")
            self.select_value(0, "Town Hall Level", th_level)

        if kl_level:
            print(f"Setting King Level to: {kl_level}")
            self.select_value(1, "King Level", kl_level)

        if ql_level:
            print(f"Setting Queen Level to: {ql_level}")
            self.select_value(2, "Queen Level", ql_level)

        if wl_level:
            print(f"Setting Warden Level to: {wl_level}")
            self.select_value(3, "Warden Level", wl_level)

        if cl_level:
            print(f"Setting Champion Level to: {cl_level}")
            self.select_value(4, "Champion Level", cl_level)


class FormHandler:
    def __init__(self, driver):
        self.driver = driver

    def set_title(self, value):
        """Set title using full XPath"""
        xpath = "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[1]/div[1]/div/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div/span/label/div/div[1]/div[2]/input"
        self._set_value(xpath, value)

    def set_description(self, value):
        """Set description using full XPath"""
        xpath = "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[1]/div[1]/div/div/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/span/label/div/div[1]/div[2]/textarea"
        self._set_value(xpath, value)

    def set_price(self, value):
        """Set price using full XPath"""
        xpath = "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div/div[2]/span/label/div/div/div[2]/input"
        self._set_value(xpath, value)

    def _set_value(self, xpath, value):
        """Reusable function to enter value into input field"""
        if value is None or str(value).strip() == "":
            print(f"Skipping empty value for: {xpath}")
            return
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(str(value))
            print(f"Set value '{value}' for element at XPath: {xpath}")
        except Exception as e:
            print(f"Error setting value for XPath {xpath}: {str(e)}")

    def select_manual_delivery(self):
        """Select manual delivery option by visible text using contains() in XPath"""
        try:
            xpath = "//div[contains(., 'Manual delivery')]"
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            print("Selected 'Manual delivery'")
        except Exception as e:
            print(f"Error selecting Manual delivery: {str(e)}")


# URL constant
FORM_URL = "https://www.g2g.com/offers/create?service_id=f6a1aba5-473a-4044-836a-8968bbab16d7&brand_id=lgc_game_19955&root_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_path=5830014a-b974-45c6-9672-b51e83112fb7&relation_id=98da2461-14bf-44bb-8e8d-011a4f06c187 "

# Multiple dictionaries defined outside class
multi_config = [
    {
        "name": "TH 15",
        "description": "Best TH 15 base for sale",
        "price": "100",
        "Town Hall Level": "15",
        "King Level": "95",
        "Queen Level": "85",
        "Warden Level": "45",
        "Champion Level": "45",
        "media": {
            "media1": "https://via.placeholder.com/350x150",
            "media2": "https://via.placeholder.com/350x150",
            "media3": "https://via.placeholder.com/350x150"
        }
    },
    {
        "name": "TH 16",
        "description": "TH 16 for sale with maxed out everything",
        "price": "200",
        "Town Hall Level": "16",
        "King Level": "85",
        "Queen Level": "75",
        "Warden Level": "75",
        "Champion Level": "45",
        "media": {
            "media1": "https://via.placeholder.com/350x150",
            "media2": "https://via.placeholder.com/350x150"
        }
    },
    {
        "name": "TH 17",
        "description": "TH 17 for sale with maxed out everything",
        "price": "300",
        "Town Hall Level": "17",
        "King Level": "55",
        "Queen Level": "85",
        "Warden Level": "60",
        "Champion Level": "40",
        "media": {
            "media1": "https://via.placeholder.com/350x150",
            "media2": "https://via.placeholder.com/350x150"
        }
    }
]


def main():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(r"user-data-dir=C:\Users\ayans\selenium-profile")
    chrome_options.add_argument("--start-maximized")

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    form_handler = FormHandler(driver)
    dropdown_handler = DropdownHandler(driver)

    for config in multi_config:
        print(f"\n🔄 Processing new configuration: {config['name']}")
        driver.get(FORM_URL)
        time.sleep(5)  # Wait for page load

        form_handler.set_title(config["name"])
        form_handler.set_description(config["description"])
        form_handler.set_price(config["price"])
        form_handler.select_manual_delivery()

        th_level = config["Town Hall Level"]
        kl_level = config["King Level"]
        ql_level = config["Queen Level"]
        wl_level = config["Warden Level"]
        cl_level = config["Champion Level"]

        dropdown_handler.fill_form_based_on_dict(th_level, kl_level, ql_level, wl_level, cl_level)

        print("✅ Form submitted for this configuration.")

    print("\n🎉 All configurations processed successfully!")
    input("Press Enter to close browser...")

    driver.quit()


if __name__ == "__main__":
    main()