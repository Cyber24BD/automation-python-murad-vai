import time
import requests
import socket
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException


def check_internet_connection(timeout=10, test_urls=None):
    """
    Check if internet connection is available using multiple methods
    
    Args:
        timeout (int): Timeout for each connectivity test
        test_urls (list): List of URLs to test (optional)
        
    Returns:
        bool: True if internet is available, False otherwise
    """
    if test_urls is None:
        test_urls = [
            "https://www.google.com",
            "https://www.cloudflare.com", 
            "https://httpbin.org/status/200",
        ]
    
    print("🌐 Checking internet connectivity...")
    
    # Method 1: Try to resolve DNS for google.com
    try:
        socket.setdefaulttimeout(timeout)
        socket.gethostbyname("google.com")
        print("✅ DNS resolution successful")
    except socket.gaierror:
        print("❌ DNS resolution failed")
        return False
    except Exception as e:
        print(f"❌ DNS check error: {str(e)}")
        return False
    
    # Method 2: Try HTTP requests to multiple reliable endpoints
    successful_requests = 0
    for url in test_urls:
        try:
            response = requests.get(url, timeout=timeout, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            if response.status_code == 200:
                successful_requests += 1
                print(f"✅ Successfully connected to {url}")
                break  # One successful connection is enough
            else:
                print(f"⚠️ Got status {response.status_code} from {url}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to connect to {url}: {str(e)}")
            continue
        except Exception as e:
            print(f"❌ Unexpected error with {url}: {str(e)}")
            continue
    
    if successful_requests > 0:
        print("🎉 Internet connection is available!")
        return True
    else:
        print("❌ No internet connection detected!")
        return False


def is_browser_showing_error_page(driver):
    """
    Check if browser is showing an error page (no internet, DNS error, etc.)
    
    Args:
        driver: Selenium WebDriver instance
        
    Returns:
        bool: True if error page is detected, False otherwise
    """
    try:
        # Get page title and URL
        current_url = driver.current_url
        page_title = driver.title.lower()
        
        # Check for common error page indicators
        error_indicators = [
            "this site can't be reached",
            "unable to connect",
            "internet disconnected",
            "dns_probe_finished_nxdomain",
            "err_internet_disconnected",
            "err_network_changed",
            "err_connection_timed_out",
            "check your internet connection",
            "no internet connection",
            "offline"
        ]
        
        # Check title for error indicators
        for indicator in error_indicators:
            if indicator in page_title:
                print(f"❌ Error page detected in title: {indicator}")
                return True
        
        # Check if URL contains error indicators
        if any(error in current_url.lower() for error in ["chrome-error://", "edge-error://", "about:neterror"]):
            print(f"❌ Error page detected in URL: {current_url}")
            return True
        
        # Check page source for error content
        try:
            page_source = driver.page_source.lower()
            for indicator in error_indicators:
                if indicator in page_source:
                    print(f"❌ Error page detected in content: {indicator}")
                    return True
        except Exception:
            pass  # Sometimes page source might not be accessible
        
        return False
        
    except Exception as e:
        print(f"⚠️ Could not check for error page: {str(e)}")
        return False


def is_page_fully_loaded(driver, timeout=15):
    """
    Enhanced page load check with error page detection
    
    Args:
        driver: Selenium WebDriver instance
        timeout (int): Maximum time to wait for page load
        
    Returns:
        bool: True if page is fully loaded, False otherwise
    """
    try:
        # First check if we're showing an error page
        if is_browser_showing_error_page(driver):
            print("❌ Browser is showing an error page")
            return False
        
        # Method 1: Wait for document ready state to be complete
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("📄 Document ready state: Complete")
        except TimeoutException:
            print("⏰ Document ready state timeout")
            return False
        except WebDriverException as e:
            print(f"❌ WebDriver error checking ready state: {str(e)}")
            return False
        
        # Method 2: Check if we can access basic page properties
        try:
            current_url = driver.current_url
            page_title = driver.title
            
            # Ensure we're not on a blank or error page
            if not current_url or current_url == "about:blank" or "data:" in current_url:
                print("❌ Page URL indicates no content loaded")
                return False
                
            print(f"📄 Page loaded: {current_url[:50]}... | Title: {page_title[:30]}...")
            
        except WebDriverException as e:
            print(f"❌ Cannot access page properties: {str(e)}")
            return False
        
        # Method 3: Wait for jQuery to be loaded and ready (if present)
        try:
            WebDriverWait(driver, 3).until(
                lambda d: d.execute_script("return typeof jQuery !== 'undefined' && jQuery.active == 0")
            )
            print("📄 jQuery loaded and ready")
        except (TimeoutException, WebDriverException):
            print("📄 jQuery not present or not ready (this is okay)")
        except Exception:
            pass  # Ignore other jQuery-related errors
        
        # Method 4: Check for common loading indicators to disappear
        loading_indicators = [
            "//div[contains(@class, 'loading')]",
            "//div[contains(@class, 'spinner')]", 
            "//div[contains(@class, 'loader')]",
            "//div[contains(@class, 'preloader')]",
            "//*[contains(text(), 'Loading')]",
            "//*[contains(text(), 'Please wait')]"
        ]
        
        for indicator in loading_indicators:
            try:
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.XPATH, indicator))
                )
                print(f"✅ Loading indicator disappeared: {indicator}")
            except TimeoutException:
                continue  # It's okay if loading indicator is not found
            except WebDriverException:
                continue  # Skip if we can't check this indicator
        
        # Method 5: Wait for main content to be present
        main_content_selectors = [
            "//body[count(*)>0]",  # Body with child elements
            "//form",  # Look for any form
            "//main",  # Look for main content
            "//div[@id]",  # Any div with an ID
            "//*[@class]"  # Any element with a class
        ]
        
        content_found = False
        for selector in main_content_selectors:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"✅ Main content found: {selector}")
                content_found = True
                break
            except (TimeoutException, WebDriverException):
                continue
        
        if not content_found:
            print("⏰ No meaningful content found on page")
            return False
        
        # Method 6: Final verification - check page has actual content
        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text.strip()
            if len(body_text) < 10:  # Page should have some meaningful text
                print("⚠️ Page has very little content")
                # Don't return False here as some valid pages might be minimal
        except (WebDriverException, Exception):
            print("⚠️ Could not verify page content")
        
        print("🎉 Page appears to be fully loaded!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking page load status: {str(e)}")
        return False


def wait_for_page_load_or_reload(driver, url, timeout=15, max_retries=3, check_internet_first=True):
    """
    Enhanced function to navigate to URL and wait for page to fully load with internet connectivity check
    
    Args:
        driver: Selenium WebDriver instance
        url (str): URL to navigate to
        timeout (int): Maximum time to wait for page load (default: 15 seconds)
        max_retries (int): Maximum number of reload attempts (default: 3)
        check_internet_first (bool): Whether to check internet connectivity first
        
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'attempts': int,
            'final_url': str
        }
    """
    
    # First check internet connectivity if requested
    if check_internet_first:
        if not check_internet_connection():
            while True:
                print("📱 Checking internet connection...")
                input("Press Enter to retry...")
                if check_internet_connection():
                    print("✅ Internet connection found!")
                    break
                else:
                    print("❌ Internet connection not found. Retrying...")
                
    
    for attempt in range(max_retries + 1):  # +1 for initial attempt
        try:
            print(f"🌐 Loading page (Attempt {attempt + 1}/{max_retries + 1}): {url}")
            
            # Navigate to the URL
            driver.get(url)
            
            # Give page a moment to start loading
            time.sleep(3)
            
            # Check for internet connectivity issues after navigation
            if is_browser_showing_error_page(driver):
                if attempt < max_retries:
                    print("❌ Error page detected. Checking internet and retrying...")
                    # Quick internet check before retry
                    if not check_internet_connection(timeout=5):
                        return {
                            'success': False,
                            'message': 'Internet connection lost during page load',
                            'attempts': attempt + 1,
                            'final_url': driver.current_url
                        }
                    continue
                else:
                    return {
                        'success': False,
                        'message': f'Error page displayed after {max_retries + 1} attempts',
                        'attempts': attempt + 1,
                        'final_url': driver.current_url
                    }
            
            # Check if page is fully loaded
            if is_page_fully_loaded(driver, timeout):
                print("✅ Page loaded successfully!")
                return {
                    'success': True,
                    'message': 'Page loaded successfully',
                    'attempts': attempt + 1,
                    'final_url': driver.current_url
                }
            else:
                if attempt < max_retries:
                    print(f"⏰ Page not loaded within {timeout} seconds. Reloading...")
                    continue
                else:
                    return {
                        'success': False,
                        'message': f'Page failed to load properly after {max_retries + 1} attempts',
                        'attempts': attempt + 1,
                        'final_url': driver.current_url
                    }
                    
        except WebDriverException as e:
            error_msg = str(e).lower()
            if "net::" in error_msg or "dns" in error_msg or "resolve" in error_msg:
                print(f"❌ Network error detected: {str(e)}")
                return {
                    'success': False,
                    'message': f'Network connectivity error: {str(e)}',
                    'attempts': attempt + 1,
                    'final_url': None
                }
            
            if attempt < max_retries:
                print(f"❌ WebDriver error: {str(e)}. Retrying...")
                continue
            else:
                return {
                    'success': False,
                    'message': f'WebDriver error after {max_retries + 1} attempts: {str(e)}',
                    'attempts': attempt + 1,
                    'final_url': None
                }
                
        except Exception as e:
            if attempt < max_retries:
                print(f"❌ Unexpected error: {str(e)}. Retrying...")
                continue
            else:
                return {
                    'success': False,
                    'message': f'Unexpected error after {max_retries + 1} attempts: {str(e)}',
                    'attempts': attempt + 1,
                    'final_url': None
                }
    
    return {
        'success': False,
        'message': 'Maximum retries exceeded',
        'attempts': max_retries + 1,
        'final_url': None
    }