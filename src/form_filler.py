"""
Google Form Automation - FINAL WORKING VERSION
Finds each question block and fills the input/textarea/date field inside it.
"""
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class GoogleFormFiller:
    def __init__(self, form_url, screenshot_dir='screenshots'):
        self.form_url = form_url
        self.screenshot_dir = screenshot_dir
        self.driver = None
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def setup_driver(self):
        try:
            print("\n🔧 Setting up Chrome...")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                # Try to use webdriver_manager to automatically get the driver
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.os_manager import ChromeType
                driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except ImportError:
                # Fallback if webdriver_manager is not installed
                print("ℹ webdriver_manager not found. Assuming chromedriver is in PATH.")
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                # Fallback for other manager errors
                print(f"ℹ Webdriver manager failed ({e}). Assuming chromedriver is in PATH.")
                self.driver = webdriver.Chrome(options=chrome_options)
            
            print("✓ Ready")
            return True
        except Exception as e:
            print(f"✗ Error setting up driver: {str(e)}")
            return False
    
    def fill_field(self, label, value):
        """
        Fill a text input, textarea, or date field.
        Finds the question block by its label, then finds the input within it.
        """
        # Don't try to fill if no value is provided
        if not str(value):
            print(f"ℹ Skipping {label} (no value provided).")
            return True
        
        try:
            # 1. Find the main question block that contains the label text
            xpath_base = f"//div[@role='listitem' and .//*[contains(text(), '{label}')]]"
            question_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_base))
            )
            
            # 2. Scroll to the block
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", question_block)
            time.sleep(0.7)
            
            # 3. Find the input or textarea *within* that block
            field = None
            try:
                # Find any <input> that is NOT a radio button or checkbox
                # This works for text, email, number, and date fields
                field = question_block.find_element(By.XPATH, ".//input[not(@type='radio') and not(@type='checkbox')]")
            except NoSuchElementException:
                try:
                    # If not, find a <textarea> (e.g., for "Full Address")
                    field = question_block.find_element(By.XPATH, ".//textarea")
                except NoSuchElementException:
                    print(f"⚠ Could not find an input or textarea for {label}.")
                    return False
            
            # 4. Fill the found field
            if field:
                field.clear()
                field.send_keys(str(value))
                print(f"✓ {label} = {value}")
                return True
            
        except TimeoutException:
            print(f"⚠ Could not find question block for: {label}")
            return False
        except Exception as e:
            print(f"⚠ Error filling {label}: {str(e)}")
            return False
    
    def fill_form(self, form_data):
        try:
            print(f"\n🌐 Opening form...")
            self.driver.get(self.form_url)
            # Wait for the first field to be ready
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Full Name')]"))
            )
            
            print("✓ Form loaded\n📝 Filling fields...\n")
            
            # Fill in order of appearance
            if not self.fill_field("Full Name", form_data.get('Full Name', '')): return False
            time.sleep(0.8)
            
            if not self.fill_field("Contact Number", form_data.get('Contact Number', '')): return False
            time.sleep(0.8)
            
            if not self.fill_field("Email ID", form_data.get('Email ID', '')): return False
            time.sleep(0.8)
            
            if not self.fill_field("Full Address", form_data.get('Full Address', '')): return False
            time.sleep(0.8)
            
            if not self.fill_field("Pin Code", form_data.get('Pin Code', '')): return False
            time.sleep(0.8)
            
            # Date of Birth
            dob = form_data.get('Date of Birth', '')
            if '/' in dob:
                parts = dob.split('/')
                if len(parts) == 3:
                    # Form placeholder is mm/dd/yyyy. This assumes input is dd/mm/yyyy
                    formatted = f"{parts[1]}/{parts[0]}/{parts[2]}" # Reformat to mm/dd/yyyy
                    if not self.fill_field("Date of Birth", formatted): return False
                    time.sleep(0.8)
            
            # Gender (now treated as a text field)
            if not self.fill_field("Gender", form_data.get('Gender', '')): return False
            time.sleep(0.8)
            
            # Captcha (if it appears)
            if not self.fill_field("Type this code", form_data.get('Verification Code', '')): return False
            time.sleep(0.8)
            
            print("\n✅ All fields filled\n")
            
            # Screenshots
            print("📸 Taking screenshots...")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            self.capture_screenshot("2_filled")
            
            return True
        except Exception as e:
            print(f"✗ Error during form fill: {str(e)}")
            return False
    
    def capture_screenshot(self, name):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(self.screenshot_dir, f'{name}_{timestamp}.png')
            self.driver.save_screenshot(path)
            print(f"✓ Screenshot saved: {path}")
            return path
        except:
            print("⚠ Could not save screenshot.")
            return None
    
    def submit_form(self):
        try:
            print("\n🔍 Submitting...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Submit')]"))
            )
            
            submit_button.click()
            print("✓ Submitted!")
            time.sleep(7) # Wait for confirmation page
            
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            return self.capture_screenshot("5_confirmation")
        except Exception as e:
            print(f"⚠ Submit error: {str(e)}")
            # Capture what went wrong (e.g., validation error)
            return self.capture_screenshot("5_submit_error")
    
    def close(self):
        if self.driver:
            print("\nShutting down browser...")
            time.sleep(3)
            self.driver.quit()
            print("✓ Done")


def automate_google_form(form_url, form_data):
    filler = GoogleFormFiller(form_url)
    try:
        if not filler.setup_driver():
            print("✗ Failed to setup driver. Exiting.")
            return None
        if not filler.fill_form(form_data):
            print("✗ Failed to fill form. Exiting.")
            filler.capture_screenshot("4_fill_error")
            return None
        
        return filler.submit_form()
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
        filler.capture_screenshot("9_unexpected_error")
        return None
    finally:
        filler.close()

# --- HOW TO RUN ---
if __name__ == "__main__":
    
    # 1. SET YOUR FORM URL HERE
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScf1-TC-mrclF-Ihv-v8-ucMh-3-P-E-RGLv-b-XJ-b-Q/viewform" # Example URL
    
    # 2. SET YOUR DATA HERE
    my_data = {
        "Full Name": "John Doe",
        "Contact Number": "1234567890",
        "Email ID": "john.doe@example.com",
        "Full Address": "123 Main Street, Anytown, USA",
        "Pin Code": "10001",
        "Date of Birth": "25/12/1990",  # dd/mm/yyyy format
        "Gender": "Male",               # This is now a text field
        "Verification Code": ""         # Only if there's a simple text captcha
    }
    
    print("--- Starting Form Automation ---")
    
    # Check your URL before running
    if "docs.google.com/forms/d/e/1FAIpQLScf1-TC-mrclF-Ihv-v8-ucMh-3-P-E-RGLv-b-XJ-b-Q" in FORM_URL:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! PLEASE REPLACE THE EXAMPLE_URL WITH YOUR    !!!")
        print("!!! OWN GOOGLE FORM URL IN THE __main__ BLOCK   !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        automate_google_form(FORM_URL, my_data)
        
    print("--- Script Finished ---")