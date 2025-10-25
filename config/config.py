"""
Configuration module for Google Form Automation
Loads environment variables and provides configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to store all settings"""
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    
    # Email Recipients
    TO_EMAIL = os.getenv('TO_EMAIL', 'tech@themedius.ai')
    CC_EMAIL = os.getenv('CC_EMAIL', 'hr@themedius.ai')
    
    # Form Configuration
    FORM_URL = os.getenv('FORM_URL', 'https://forms.gle/WT68aV5UnPajeoSc8')
    
    # Personal Details - ALL FORM FIELDS
    YOUR_NAME = os.getenv('YOUR_NAME', 'Your Name')
    CONTACT_NUMBER = os.getenv('CONTACT_NUMBER', '0000000000')
    YOUR_EMAIL = os.getenv('YOUR_EMAIL', 'your.email@example.com')
    YOUR_ADDRESS = os.getenv('YOUR_ADDRESS', 'Your Address')
    PIN_CODE = os.getenv('PIN_CODE', '000000')
    DATE_OF_BIRTH = os.getenv('DATE_OF_BIRTH', '01/01/2000')
    GENDER = os.getenv('GENDER', 'Male')
    VERIFICATION_CODE = os.getenv('VERIFICATION_CODE', 'GNFPYC')
    GITHUB_REPO = os.getenv('GITHUB_REPO', 'https://github.com/yourusername/repo')
    
    # Resume Path
    RESUME_PATH = os.getenv('RESUME_PATH', '')
    
    # Screenshot Configuration
    SCREENSHOT_DIR = 'screenshots'
    SCREENSHOT_FILENAME = 'form_confirmation.png'
    
    @staticmethod
    def validate_config():
        """Validate that all required configuration is present"""
        required_vars = [
            'MAIL_USERNAME',
            'MAIL_PASSWORD',
            'YOUR_NAME',
            'GITHUB_REPO'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
