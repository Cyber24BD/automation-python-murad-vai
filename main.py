from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
from data import multi_config


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


class MediaHandler:
    def __init__(self, driver):
        self.driver = driver
        self.media_title_xpaths = [
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/span/label/div/div/div[2]/input",
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/span/label/div/div/div[2]/input",
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/span/label/div/div/div[2]/input"
        ]
        self.media_url_xpaths = [
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div[3]/span/label/div/div/div[2]/input",
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[3]/span/label/div/div/div[2]/input",
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[3]/span/label/div/div/div[2]/input"
        ]
        self.add_more_button_xpaths = [
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[2]/button",
            "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[2]/div[1]/div/div/div/div[2]/div[3]/button"
        ]
    
    def add_media_items(self, media_dict):
        """Add media items based on the provided dictionary."""
        try:
            media_count = len(media_dict)
            if media_count < 1 or media_count > 3:
                print(f"Warning: Invalid media count ({media_count}). Must be between 1-3.")
                return False
                
            print(f"\n📸 Adding {media_count} media items...")
            
            # Process first media item
            current_idx = 0
            for media_key, media_url in media_dict.items():
                if current_idx >= 3:
                    print("Maximum 3 media items allowed, skipping the rest.")
                    break
                    
                # Add 'Add more' button click for 2nd and 3rd items
                if current_idx > 0:
                    add_more_button_idx = current_idx - 1
                    try:
                        add_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, self.add_more_button_xpaths[add_more_button_idx]))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
                        add_button.click()
                        print(f"Clicked 'Add more' button #{add_more_button_idx+1}")
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error clicking 'Add more' button: {str(e)}")
                        return False
                
                # Set media title (using the media key or a generic name)
                try:
                    media_title = media_key.replace("media", "Media Item ")
                    title_input = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, self.media_title_xpaths[current_idx]))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    title_input.clear()
                    title_input.send_keys(media_title)
                    print(f"Set media title: {media_title}")
                except Exception as e:
                    print(f"Error setting media title for item #{current_idx+1}: {str(e)}")
                    return False
                
                # Set media URL
                try:
                    url_input = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, self.media_url_xpaths[current_idx]))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", url_input)
                    url_input.clear()
                    url_input.send_keys(media_url)
                    print(f"Set media URL: {media_url}")
                except Exception as e:
                    print(f"Error setting media URL for item #{current_idx+1}: {str(e)}")
                    return False
                
                current_idx += 1
                
            print(f"✅ Successfully added {current_idx} media items")
            return True
        except Exception as e:
            print(f"Error adding media items: {str(e)}")
            return False

    

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
        """Select manual delivery option using radio button"""
        try:
            # Try to find and click the manual delivery radio button
            manual_radio_xpath = "//div[contains(@class, 'q-radio__label') and contains(text(), 'Manual delivery')]"
            manual_radio = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, manual_radio_xpath))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manual_radio)
            manual_radio.click()
            print("Selected 'Manual delivery' option")
            
            # Verify selection (optional)
            time.sleep(1)
            # Check if the radio button now has the 'aria-checked="true"' attribute
            try:
                parent_radio = manual_radio.find_element(By.XPATH, "./ancestor::div[@role='radio']")
                is_checked = parent_radio.get_attribute("aria-checked")
                if is_checked == "true":
                    print("✅ Manual delivery option successfully selected")
                else:
                    print("⚠️ Manual delivery option may not be selected correctly")
            except:
                print("Could not verify if manual delivery option was selected")
                
            return True
        except Exception as e:
            print(f"Error selecting Manual delivery option: {str(e)}")
            
            # Backup method: try to find by role and label
            try:
                backup_xpath = "//div[@role='radio' and @aria-label='Manual delivery']"
                manual_radio_backup = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, backup_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", manual_radio_backup)
                manual_radio_backup.click()
                print("Selected 'Manual delivery' option using backup method")
                return True
            except Exception as backup_e:
                print(f"Backup method also failed: {str(backup_e)}")
                return False

            
    def click_publish_button(self):
        """Click the Publish button using multiple methods for reliability"""
        try:
            # First try using XPath
            xpath = "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[7]/div/div/div/div[2]/button"
            try:
                publish_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_button)
                publish_button.click()
                print("Successfully clicked Publish button using XPath")
                return True
            except Exception as e:
                print(f"Failed to click Publish using XPath: {str(e)}, trying CSS selector...")
                
            # Try using CSS selector as backup
            try:
                css_selector = "button.q-btn.bg-primary.text-white"
                publish_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_button)
                publish_button.click()
                print("Successfully clicked Publish button using CSS selector")
                return True
            except Exception as e:
                print(f"Failed to click Publish using CSS selector: {str(e)}, trying text search...")
                
            # Try finding by text content as last resort
            try:
                text_xpath = "//button[contains(., 'Publish')]"
                publish_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, text_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_button)
                publish_button.click()
                print("Successfully clicked Publish button by text content")
                return True
            except Exception as e:
                print(f"Failed to click Publish by text: {str(e)}")
                
            return False
        except Exception as e:
            print(f"Error clicking Publish button: {str(e)}")
            return False


    def set_delivery_speed(self):
        """Set purchase quantity range to 1-1 and delivery time to 10 minutes"""
        try:
            print("\n🕒 Setting delivery speed parameters...")
            
            # Set purchase quantity range (1-1)
            # Find and set the "From" field
            # try:
            #     from_xpath = "//input[@placeholder='From']"
            #     from_input = WebDriverWait(self.driver, 10).until(
            #         EC.visibility_of_element_located((By.XPATH, from_xpath))
            #     )
            #     self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", from_input)
            #     from_input.clear()
            #     from_input.send_keys("1")
            #     # Explicitly trigger blur event to ensure value is saved
            #     self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur'))", from_input)
            #     print("Set purchase quantity 'From' value to 1")
            # except Exception as e:
            #     print(f"Error setting 'From' field: {str(e)}")
            #     return False
                
            # Find and set the "To" field
            try:
                to_xpath = "//input[@placeholder='To']"
                to_input = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, to_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", to_input)
                to_input.clear()
                to_input.send_keys("1")
                # Explicitly trigger blur event to ensure value is saved
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur'))", to_input)
                print("Set purchase quantity 'To' value to 1")
            except Exception as e:
                print(f"Error setting 'To' field: {str(e)}")
                return False
                
            # Explicitly set the minimum purchase quantity
            try:
                # min_purchase_xpath = "/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[4]/div[1]/div/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div/span/label/div/div[1]/div[2]/input"
                # min_purchase_input = WebDriverWait(self.driver, 10).until(
                #     EC.visibility_of_element_located((By.XPATH, min_purchase_xpath))
                # )
                # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", min_purchase_input)
                # min_purchase_input.clear()
                # min_purchase_input.send_keys("1")
                # Explicitly trigger blur event to ensure value is saved
                # self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur'))", min_purchase_input)
                # Also try to trigger change event for good measure
                # self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", min_purchase_input)
                # print("Set minimum purchase quantity to 1")
                
                # Validate the field after setting it
                time.sleep(0.5)  # Give a moment for validation
                value = min_purchase_input.get_attribute("value")
                if value != "1":
                    print(f"Warning: Minimum purchase quantity field has value '{value}' instead of '1', trying again...")
                    min_purchase_input.clear()
                    min_purchase_input.send_keys("1")
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('blur'))", min_purchase_input)
                    time.sleep(0.5)
            except Exception as e:
                print(f"Error setting minimum purchase quantity: {str(e)}")
                
                # Try an alternative approach with JavaScript if direct input fails
                try:
                    print("Trying alternative JavaScript approach for minimum purchase quantity...")
                    js_code = "document.evaluate('/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[4]/div[1]/div/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div/span/label/div/div[1]/div[2]/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = '1';"
                    self.driver.execute_script(js_code)
                    print("Set minimum purchase quantity via JavaScript")
                except Exception as js_e:
                    print(f"JavaScript approach also failed: {str(js_e)}")
                
            # Click on the minutes dropdown
            try:
                # The minutes dropdown button - looking for the button containing "minute"
                minute_button_xpath = "//button[contains(@class, 'g-btn-outlined')]//div[contains(text(), 'minute')]"
                minute_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, minute_button_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", minute_button)
                minute_button.click()
                print("Clicked on minutes dropdown")
                time.sleep(1)  # Wait for dropdown to open
            except Exception as e:
                print(f"Error clicking minutes dropdown: {str(e)}")
                
                # Try alternative approach
                try:
                    # Try finding by the right side dropdown (second button)
                    alt_minute_xpath = "(//button[contains(@class, 'g-btn-outlined')])[2]"
                    alt_minute_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, alt_minute_xpath))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", alt_minute_button)
                    alt_minute_button.click()
                    print("Clicked on minutes dropdown using alternative method")
                    time.sleep(1)
                except Exception as alt_e:
                    print(f"Alternative method also failed: {str(alt_e)}")
                    return False
                    
            # Select 10 minutes from dropdown
            try:
                # Find the "10 minutes" option
                ten_min_xpath = "//div[contains(@class, 'q-item__section') and contains(text(), '10 minutes')]"
                ten_min_option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ten_min_xpath))
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ten_min_option)
                ten_min_option.click()
                print("Selected '10 minutes' from dropdown")
                time.sleep(1)
            except Exception as e:
                print(f"Error selecting 10 minutes: {str(e)}")
                return False
            
            print("✅ Successfully set delivery speed parameters (1-1 quantity, 10 minutes)")
            return True
        except Exception as e:
            print(f"Error setting delivery speed: {str(e)}")
            return False


# URL constant
FORM_URL = "https://www.g2g.com/offers/create?service_id=f6a1aba5-473a-4044-836a-8968bbab16d7&brand_id=lgc_game_19955&root_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_id=5830014a-b974-45c6-9672-b51e83112fb7&cat_path=5830014a-b974-45c6-9672-b51e83112fb7&relation_id=98da2461-14bf-44bb-8e8d-011a4f06c187 "

# Multiple dictionaries defined outside class




# multi_config = [
#     {
#         "name": "TH 15",
#         "description": "Best TH 15 base for sale",
#         "price": "100",
#         "Town Hall Level": "15",
#         "King Level": "95",
#         "Queen Level": "85",
#         "Warden Level": "45",
#         "Champion Level": "45",
#         "media": {
#             "media1": "https://imgur.com/a/9IEgqMn",
#             "media2": "https://imgur.com/a/9IIoqMn",
#             "media3": "https://imgur.com/a/9IIpqMn"
#         }
#     },
#     {
#         "name": "TH 16",
#         "description": "TH 16 for sale with maxed out everything",
#         "price": "200",
#         "Town Hall Level": "16",
#         "King Level": "85",
#         "Queen Level": "75",
#         "Warden Level": "75",
#         "Champion Level": "45",
#         "media": {
#             "media1": "https://imgur.com/a/9IEIkMn",
#             "media2": "https://imgur.com/a/9IEIlMn"
#         }
#     },
#     {
#         "name": "TH 17",
#         "description": "TH 17 for sale with maxed out everything",
#         "price": "300",
#         "Town Hall Level": "17",
#         "King Level": "55",
#         "Queen Level": "85",
#         "Warden Level": "60",
#         "Champion Level": "40",
#         "media": {
#             "media1": "https://imgur.com/a/9IEIhMn",
#             "media2": "https://imgur.com/a/9IEIdMn"
#         }
#     }
# ]





def open_new_tab_and_process_table(driver):
    
    # Get current window handles
    original_handles = driver.window_handles
    
    # Open new tab using JavaScript
    driver.execute_script("window.open('about:blank', '_blank');")
    
    
    # Wait for new tab to open
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: len(d.window_handles) > len(original_handles))
    
    # Switch to new tab
    new_window = [window for window in driver.window_handles if window not in original_handles][0]
    driver.switch_to.window(new_window)
    
    # Navigate to URL
    url = "https://www.g2g.com/offers/list?cat_id=5830014a-b974-45c6-9672-b51e83112fb7"
    driver.get(url)
    print("Navigated to G2G website")

    # Wait for page to load
    time.sleep(5)

    try:
        # Wait for the table to be present
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.q-table")))
        
        # Find all data rows (skip header)
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]
        print(f"Found {len(rows)} data rows in the table")

        target_rows = []

        # Filter rows where Sale == 0 AND account name is "Clash Of Clans (Global)"
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 6:
                # Check if sales is 0
                sale_cell = cells[5]
                sale_text = sale_cell.text.strip()
                
                # Check account name
                title_cell = cells[1]
                account_name_element = title_cell.find_element(By.XPATH, ".//div[contains(@class, 'text-font-2nd') and contains(text(), 'Accounts -')]")
                account_name_text = account_name_element.text.strip()
                
                # Extract just the account name part
                if "Accounts -" in account_name_text:
                    account_name = account_name_text.split("Accounts -")[1].strip()
                    
                    if sale_text == "0" and "Clash Of Clans (Global)" in account_name:
                        target_rows.append(row)

        if not target_rows:
            print("No rows found matching criteria: Sale = 0 AND 'Clash Of Clans (Global)'")
            # Close tab and return to original
            driver.close()
            driver.switch_to.window(original_handles[0])
            return 0

        # Select the last matching row
        last_row = target_rows[-1]
        print("Processing last matching row...")

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", last_row)
        time.sleep(1)

        # Locate action cell (last td)
        action_cell = last_row.find_element(By.CSS_SELECTOR, "td.q-px-sm.q-td.text-center")
        more_button = action_cell.find_element(By.TAG_NAME, "button")

        # Click more_vert button
        try:
            more_button.click()
            print("Clicked more_vert button")
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", more_button)
            print("Forced click on more_vert button")
        time.sleep(2)

        # Click Remove from dropdown
        # Wait for dropdown to appear
        try:
            remove_option = wait.until(EC.visibility_of_element_located((By.XPATH,
                "//div[contains(@class, 'q-menu')]//div[contains(@class, 'q-item') and contains(., 'Remove')]")))
            
            # Try regular click first
            remove_option.click()
        except Exception as e:
            print("Normal click failed, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", remove_option)
        print("Clicked Remove option")
        time.sleep(2)

        # Click Confirm in the modal
        confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class, 'g-btn-min') and contains(., 'Confirm')]")))
        confirm_button.click()
        print("Clicked Confirm")
        time.sleep(4)

        print("Successfully deleted the selected item.")
        processed_count = 1

        # Close tab and return to original
        driver.close()
        driver.switch_to.window(original_handles[0])
        print("Closed new tab and returned to original window")

        return processed_count

    except Exception as e:
        print(f"Error processing table: {str(e)}")
        driver.save_screenshot("table_error.png")

        # Attempt cleanup
        try:
            driver.close()
            driver.switch_to.window(original_handles[0])
            print("Closed tab after error and returned to original window")
        except Exception as close_error:
            print(f"Error closing tab: {str(close_error)}")

        return 0




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
    media_handler = MediaHandler(driver)

    while True:
        for config in multi_config:
            print(f"\n🔄 Processing new configuration: {config['name']}")
            driver.get(FORM_URL)
            time.sleep(5)
            
            # Set hero levels
            th_level = config["Town Hall Level"]
            kl_level = config["King Level"]
            ql_level = config["Queen Level"]
            wl_level = config["Warden Level"]
            cl_level = config["Champion Level"]

            dropdown_handler.fill_form_based_on_dict(th_level, kl_level, ql_level, wl_level, cl_level)  # Wait for page load

            

            # Set basic form fields
            form_handler.set_title(config["name"])
            form_handler.set_description(config["description"])
            form_handler.set_price(config["price"])
            form_handler.select_manual_delivery()
            form_handler.set_delivery_speed()
            time.sleep(1)   
            

            # Add media items
            if "media" in config and isinstance(config["media"], dict):
                media_handler.add_media_items(config["media"])
            else:
                print("⚠️ No media found in configuration or invalid media format")

            
            # Click publish button
            form_handler.click_publish_button()
            time.sleep(3)  # Wait for submit action
            
            print("✅ Form submitted for this configuration.")
            open_new_tab_and_process_table(driver)
            time.sleep(1)

    print("\n🎉 All configurations processed successfully!")
    print("\n🎉 Table Data Deleted successfully!")
    input("Press Enter to close browser...")
    

    driver.quit()


if __name__ == "__main__":
    main()