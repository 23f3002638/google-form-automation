"""
Google Form Automation Module
Handles automated form filling using Selenium WebDriver
"""
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class GoogleFormFiller:
    """Class to handle Google Form automation"""
    
    def __init__(self, form_url, screenshot_dir='screenshots'):
        self.form_url = form_url
        self.screenshot_dir = screenshot_dir
        self.driver = None
        
        # Create screenshot directory
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            print("\n🔧 Setting up Chrome WebDriver...")
            
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Try with webdriver-manager
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                from webdriver_manager.core.os_manager import ChromeType
                
                driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
                print("✓ Chrome WebDriver initialized successfully")
                return True
                
            except Exception as e1:
                # Fallback method
                self.driver = webdriver.Chrome(options=chrome_options)
                print("✓ Chrome WebDriver initialized successfully (alternative method)")
                return True
            
        except Exception as e:
            print(f"✗ Error setting up WebDriver: {str(e)}")
            return False
    
    def fill_form(self, form_data):
        """Fill the Google Form with provided data"""
        try:
            print(f"\n🌐 Navigating to form: {self.form_url}")
            self.driver.get(self.form_url)
            time.sleep(4)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            print("✓ Form loaded successfully")
            
            # Scroll to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # Find all input fields BY TYPE (separate date fields)
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            text_areas = self.driver.find_elements(By.TAG_NAME, "textarea")
            email_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
            date_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='date']")
            
            print(f"\n📝 Found {len(text_inputs)} text, {len(email_inputs)} email, {len(text_areas)} textarea, {len(date_inputs)} date fields")
            print("Filling form fields...\n")
            
            # Combine text fields (but NOT date fields)
            all_text_inputs = text_inputs + text_areas + email_inputs
            
            # Fill text fields (excluding Date of Birth and Gender)
            field_index = 0
            for field_name, field_value in form_data.items():
                # Skip Date of Birth and Gender - handle separately
                if field_name == 'Date of Birth' or field_name == 'Gender':
                    continue
                    
                try:
                    if field_index < len(all_text_inputs):
                        element = all_text_inputs[field_index]
                        
                        # Scroll to element
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(0.5)
                        
                        if element.is_displayed() and element.is_enabled():
                            element.clear()
                            element.send_keys(str(field_value))
                            print(f"✓ Filled: {field_name} = {field_value}")
                            field_index += 1
                            time.sleep(0.7)
                except Exception as e:
                    print(f"⚠ Warning: Could not fill '{field_name}': {str(e)}")
                    field_index += 1
            
            # Handle Date of Birth separately (date picker field)
            try:
                if 'Date of Birth' in form_data and date_inputs:
                    dob_value = form_data['Date of Birth']
                    
                    # Convert date format from DD/MM/YYYY to MM/DD/YYYY
                    if '/' in dob_value:
                        parts = dob_value.split('/')
                        if len(parts) == 3:
                            # Rearrange to MM/DD/YYYY for Google Forms
                            formatted_date = f"{parts[1]}/{parts[0]}/{parts[2]}"
                            
                            date_field = date_inputs[0]
                            
                            # Scroll to date field
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", date_field)
                            time.sleep(0.5)
                            
                            if date_field.is_displayed() and date_field.is_enabled():
                                date_field.clear()
                                date_field.send_keys(formatted_date)
                                print(f"✓ Filled: Date of Birth = {formatted_date} (MM/DD/YYYY format)")
                                time.sleep(0.7)
            except Exception as e:
                print(f"⚠ Warning: Could not fill Date of Birth: {str(e)}")
            
            # Handle Gender radio buttons
            try:
                gender_value = form_data.get('Gender', '')
                if gender_value:
                    gender_elements = self.driver.find_elements(By.XPATH, 
                        f"//span[contains(text(),'{gender_value}')]")
                    
                    for elem in gender_elements:
                        if elem.is_displayed():
                            # Scroll to element
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                            time.sleep(0.5)
                            elem.click()
                            print(f"✓ Selected Gender: {gender_value}")
                            time.sleep(0.7)
                            break
            except Exception as e:
                print(f"⚠ Note: Gender field handling: {str(e)}")
            
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            print("\n✅ All fields filled successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error filling form: {str(e)}")
            return False
    
    def submit_form(self):
        """Submit the form and capture screenshot"""
        try:
            submit_button = None
            
            print("\n🔍 Looking for Submit button...")
            
            # Scroll to bottom where submit button usually is
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            # Try multiple methods to find submit button
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, 
                        "//span[contains(text(),'Submit') or contains(text(),'submit')]"))
                )
            except TimeoutException:
                pass
            
            if not submit_button:
                try:
                    submit_button = self.driver.find_element(By.XPATH, 
                        "//div[@role='button']//span[contains(text(),'Submit')]")
                except:
                    pass
            
            if submit_button:
                print("✓ Found Submit button, clicking...")
                
                # Scroll to submit button
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                time.sleep(1)
                
                submit_button.click()
                print("✓ Form submitted!")
                
                # Wait for confirmation page to load
                time.sleep(5)
                
                # Scroll to top to capture full confirmation message
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                # Capture screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(self.screenshot_dir, 
                    f'form_confirmation_{timestamp}.png')
                
                self.driver.save_screenshot(screenshot_path)
                print(f"✓ Screenshot saved: {screenshot_path}")
                
                return screenshot_path
            else:
                print("⚠ Could not find submit button automatically")
                print("Please click Submit manually...")
                input("Press Enter after clicking Submit...")
                
                time.sleep(3)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(self.screenshot_dir, 
                    f'form_confirmation_{timestamp}.png')
                self.driver.save_screenshot(screenshot_path)
                print(f"✓ Screenshot saved: {screenshot_path}")
                
                return screenshot_path
                
        except Exception as e:
            print(f"✗ Error submitting form: {str(e)}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            time.sleep(3)
            self.driver.quit()
            print("\n✓ Browser closed")


def automate_google_form(form_url, form_data):
    """Main function to automate Google Form filling"""
    filler = GoogleFormFiller(form_url)
    
    try:
        if not filler.setup_driver():
            return None
        
        if not filler.fill_form(form_data):
            return None
        
        screenshot_path = filler.submit_form()
        return screenshot_path
        
    finally:
        filler.close()
