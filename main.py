from itertools import count
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import time
import importlib
from config import selenium_web_driver_path, after_post_sleep_timer, after_per_post_sleep_timer, account_url, delete_url
from check_connection import wait_for_page_load_or_reload


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
                        time.sleep(0.5)
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
            print(f"Skipping empty value for ")
            return
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(str(value))
            print(f"Set value '{value}' for element at XPath")
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
            except:
                print(f"Error setting minimum purchase quantity.")
                
                # Try an alternative approach with JavaScript if direct input fails
                try:
                    print("Trying alternative JavaScript approach for minimum purchase quantity...")
                    js_code = "document.evaluate('/html/body/div[1]/div/div[1]/main/div[3]/form/div/div[4]/div[1]/div/div/div[2]/div[2]/div[3]/div/div[2]/div[1]/div/div/div/div/span/label/div/div[1]/div[2]/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = '1';"
                    self.driver.execute_script(js_code)
                    print("Set minimum purchase quantity via JavaScript")
                except:
                    print(f"JavaScript approach also failed.")
                
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
            except:
                print(f"Error clicking minutes dropdown.")
                
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
                    time.sleep(0.5)
                except:
                    print(f"Alternative method also failed.")
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
                time.sleep(0.5)
            except Exception as e:
                print(f"Error selecting 10 minutes: {str(e)}")
                return False
            
            print("✅ Successfully set delivery speed parameters (1-1 quantity, 10 minutes)")
            return True
        except Exception as e:
            print(f"Error setting delivery speed: {str(e)}")
            return False

    def close_success_popup(self):
        """
        Close the success popup by clicking the 'Manage offer' or 'Add new offer' button
        
        Returns:
            bool: True if popup was closed, False otherwise
        """
        try:
            # Try to click "Manage offer" button to close popup
            manage_button_xpath = "//button[contains(., 'Manage offer')]"
            
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, manage_button_xpath))
                )
                print("✅ Post Success Check : Manage offer")
                return True
            except TimeoutException:
                print("⏰ Post Failed Check : Manage offer")

            # Alternative: Click "Add new offer" button
            add_new_xpath = "//button[contains(., 'Add new offer')]"
            
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, add_new_xpath))
                )
                print("✅ Post Success Check : Add new Account")
                return True
            except TimeoutException:
                print("❌ Post Failed Check : Add new Account")
                return False
                
        except:
            print(f"❌ Maybe Post is Failed.")
            return False

    

# URL constant
FORM_URL = account_url

# Multiple dictionaries defined outside class


def count_number_into_three(number):
    count = 0
    count += number
    return count
    


def test_connection_main(driver):
    try:
        result = wait_for_page_load_or_reload(
            driver, 
            FORM_URL, 
            timeout=20, 
            max_retries=3,
            check_internet_first=True
            )
        
        print(f"\n Final Result:")
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Attempts: {result['attempts']}")
        print(f"Final URL: {result['final_url']}")
        
        if result['success']:
            print("\n✅ Ready to proceed with automation!")
        else:
            print("\n❌ Page loading failed. Check internet connection and try again.")
            time.sleep(3)
    except:
        print("❌ Website or Internet Error.")



def run_post_command(driver):
    # Reload the data module to get the latest changes
    import data
    importlib.reload(data)
    from data import multi_config

    form_handler = FormHandler(driver)
    dropdown_handler = DropdownHandler(driver)
    media_handler = MediaHandler(driver)

    try:
        for config in multi_config:
            print(f"\n🔄 Processing new configuration: {config['name']}")

            test_connection_main(driver)
                
            # Set hero levels
            th_level = config["Town Hall Level"]
            kl_level = config["King Level"]
            ql_level = config["Queen Level"]
            wl_level = config["Warden Level"]
            cl_level = config["Champion Level"]


            while True:
                time.sleep(2)
                dropdown_handler.fill_form_based_on_dict(th_level, kl_level, ql_level, wl_level, cl_level)  # Wait for page load

                # Set basic form fields
                form_handler.set_title(config["name"])
                form_handler.set_description(config["description"])
                form_handler.set_price(config["price"])
                form_handler.select_manual_delivery()
                form_handler.set_delivery_speed()
                # time.sleep(1)   
                    

                # Add media items
                if "media" in config and isinstance(config["media"], dict):
                    media_handler.add_media_items(config["media"])
                else:
                    print("⚠️ No media found in configuration or invalid media format")

                # Click publish button
                form_handler.click_publish_button()
                time.sleep(2)  # Wait for submit action

                if form_handler.close_success_popup():
                    print("✅ Form submitted for this configuration.")
                    print("✅ Successfully posted configurations.")
                    break
                else:
                    set_post_retry_count = count_number_into_three(1)
                    try:
                        test_connection_main(driver)
                        time.sleep(3)
                    except:
                        print("Website or Internet Error.")
                    time.sleep(2)
                    print("\n" + "Retry Count : " + str(set_post_retry_count) + "\n")
                    if set_post_retry_count == 3:
                        print("❌ Post Failed. Please check the internet or website. Network maybe slow or website is not working perfectly.")
                        print("✌️  Please restart the bot to work again.")
                        break
                    continue
            print(f"\n🔔 Start Per Post Sleep : {after_per_post_sleep_timer}")
            time.sleep(after_per_post_sleep_timer)
    except:
        print("Data is not current")
        print(f"Failed Data Index : {count}")


        

            
    




# Delete handler
def delete_open_tab(driver):

    try:
        # # Create a new tab using JavaScript
        # driver.execute_script("window.open('');")
        
        # # Switch focus to the new tab
        # driver.switch_to.window(driver.window_handles[-1])
        
        # Navigate to the target URL
        driver.get(delete_url)
        
    except Exception as e:
        print(f"An error occurred: {e}")




def select_rows_with_title_starting_with_TH(driver):
    print("🔄 Selecting rows with title starting with 'TH '")
    """
    Selects rows in a G2G table where the Title starts with 'TH '.
    Clicks the checkbox in those rows.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    try:
        # Wait for the table body to be present and visible
        wait = WebDriverWait(driver, 10)
        table_body = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='q-table__middle scroll']//table/tbody"))
        )

        time.sleep(2)

        # Find all rows in the table body
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            # Locate the title element (inside the second column)
            title_element = row.find_element(By.XPATH, ".//td[2]//div[@class='text-body1']//span")
            title_text = title_element.text.strip()

            # Check if the title starts with 'TH ' (TH followed by a space)
            if title_text.startswith("TH "):
                # Locate the checkbox (first column)
                checkbox = row.find_element(By.XPATH, ".//td[1]//div[@role='checkbox']")
                # time.sleep(0.5)

                # Scroll the checkbox into view (to avoid click issues)
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", checkbox)

                # time.sleep(0.5)

                # Wait until the checkbox is clickable
                wait.until(EC.element_to_be_clickable((By.XPATH, ".//td[1]//div[@role='checkbox']")))

                # time.sleep(0.5)

                # Click the checkbox
                checkbox.click()

                # time.sleep(2)
            else:
                pass
                # print("👀 No TH Found")

    except:
        print("No TH Found")
        



def confirm_delete_offer(driver, timeout=10):
    """
    Clicks the delete button in the footer and confirms the ensuing popup.

    :param driver: Selenium WebDriver instance (already on the page with offers)
    :param timeout: How many seconds to wait for elements (default: 10)
    :raises TimeoutException: if either button isn't found/clickable in time
    """
    wait = WebDriverWait(driver, timeout)

    try:
        # 1) Click the trash/delete icon button
        delete_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "footer .q-btn.text-negative .material-icons"
        )))
        delete_btn.click()

        # 2) Wait for the confirmation popup’s “Confirm” button
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'q-pa-md')]//button[.//span[contains(.,'Confirm')]]"
        )))
        confirm_btn.click()
        time.sleep(5)

        print("✅ Confirmed deletion")
        return True

    except:
        print(f"No TH found or Error confirming deletion.")
        return False




def loop_page_and_delete_data(driver, operation_function=None, config_name=None):
    """
    Loops through all pages of pagination and performs an operation on each page.
    
    Args:
        driver: Selenium WebDriver instance
        operation_function: Function to perform on each page. If None, no operation is performed.
                           The function should accept the driver as an argument.
        config_name: Optional name of the configuration being processed, for better logging
    
    Returns:
        The total number of pages processed
    """


    config_label = f" [{config_name}]" if config_name else ""
    current_page = 1
    total_pages_processed = 0
    operation_performed = False
    
    try:
        # Wait for pagination to load initially
        time.sleep(1)
        
        # First check if pagination exists at all
        try:
            pagination_exists = driver.find_element(By.CSS_SELECTOR, "div.q-pagination, ul.pagination, nav.pagination")
        except NoSuchElementException:
            # If no pagination exists, just perform the operation once on the current page
            if operation_function:
                print(f"🔄 Performing operation{config_label} (single page)")
                operation_function(driver)
                operation_performed = True
            print(f"No pagination found. Processed single page.{config_label}")
            return 1
        
        while True:
            # Perform the operation on the current page if a function is provided
            if operation_function and not (operation_performed and current_page == 1):
                print(f"\n🔄 Performing operation on page {current_page}{config_label}")
                operation_function(driver)
                operation_performed = True
            
            total_pages_processed += 1
            
            # Wait a moment for any operations to complete
            time.sleep(0.5)
            
            # Find all pagination elements to determine if there are more pages
            try:
                # Try to find the next button (typically shows as ">" or "›")
                next_button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='>']"))
                )
            except:
                try:
                    # Alternative selector if text is not directly in the button
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page'], button.pagination-next")
                except:
                    try:
                        # Another alternative - look for any button with ">" or "›" character
                        next_button = driver.find_element(By.XPATH, "//button[contains(text(), '>') or contains(text(), '›')]")
                    except:
                        try:
                            # Find by position in the pagination container (last button)
                            pagination_container = driver.find_element(By.CSS_SELECTOR, "div.q-pagination, ul.pagination, nav.pagination")
                            buttons = pagination_container.find_elements(By.TAG_NAME, "button")
                            # Last button in pagination is typically the "Next" button
                            if len(buttons) > 1:
                                next_button = buttons[-1]
                            else:
                                print(f"No next button found. This appears to be the last page ({current_page}).{config_label}")
                                break
                        except:
                            print(f"Could not locate pagination controls. Stopping after page {current_page}.{config_label}")
                            break
            
            # Check if the next button is disabled or if we're on the last page
            try:
                is_disabled = next_button.get_attribute("disabled") == "true" or \
                              next_button.get_attribute("aria-disabled") == "true" or \
                              "disabled" in (next_button.get_attribute("class") or "") or \
                              not next_button.is_enabled()
                
                if is_disabled:
                    print(f"Next button is disabled. Reached the last page ({current_page}).{config_label}")
                    break
                
                # If we're here, the next button is clickable
                # Try to click the next button
                try:
                    # Scroll the button into view
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(0.5)  # Give it a moment to scroll
                    
                    # Try regular click
                    next_button.click()
                except ElementClickInterceptedException:
                    # If regular click fails, try JavaScript click
                    driver.execute_script("arguments[0].click();", next_button)
                    
                print(f"\nNavigated to page {current_page + 1}{config_label}")
                current_page += 1
                
                # Wait for the page to update
                time.sleep(2)
                
            except Exception as e:
                print(f"Error checking or clicking next button: {str(e)}{config_label}")
                print(f"Assuming this is the last page ({current_page}).{config_label}")
                break
    
    except Exception as e:
        print(f"Unexpected error in pagination loop: {str(e)}{config_label}")

    # Close the current tab
    print("\n🔄 Close Tab")


    
    print(f"Pagination loop completed. Processed {total_pages_processed} pages in total.{config_label}")
    return total_pages_processed




def delete_complete_operation(driver):
    """
    Performs the operation of selecting rows and deleting data.
    This fixed version doesn't recursively call loop_page_and_delete_data.
    """
    print("🔄 Select Rows")

    while True:
        try:
            time.sleep(2)
            select_rows_with_title_starting_with_TH(driver)
        except:
            print(f"Error selecting rows.")
            pass

        time.sleep(2)

        print("🔄 Delete Data")

        try:
            delet_data = confirm_delete_offer(driver)
            if delet_data:
                time.sleep(2)
                driver.get(driver.current_url)
                continue
            else:
                break
        except:
            print(f"Error in delete operation.")
            time.sleep(2)
            




# Main function to handle pagination and operations
def process_data_with_pagination(driver):
    """
    Main function to process all pages of data with proper pagination.
    This is what you should call from your main script.
    """
    # Now use loop_page_and_delete_data with our fixed delete_operation function
    return loop_page_and_delete_data(driver, delete_complete_operation)
       


def main():
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(selenium_web_driver_path)
    chrome_options.add_argument("--start-maximized")

    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        while True:
            
            print("\n🔄 Start Working. First Confirm Detele Data.")
            delete_open_tab(driver)
            time.sleep(3)
            
            process_data_with_pagination(driver)
            time.sleep(3)

            print("\n🔄 Start Working")
            run_post_command(driver)

            print("\n🕒 Start Interval Time")
            time.sleep(after_post_sleep_timer)
            print("\n🕒 Stop Interval Time")

            print("\n🔄 Tab Open")
            delete_open_tab(driver)
            time.sleep(3)

            process_data_with_pagination(driver)
            time.sleep(3)

            print("\n🎉 All configurations processed successfully!")
            
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user. Closing browser...")
    finally:
        driver.quit()




if __name__ == "__main__":
    main()