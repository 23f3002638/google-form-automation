"""
Email Sender Module using Flask-Mail
Handles automated email sending with attachments
"""
import os
from flask import Flask
from flask_mail import Mail, Message
from config.config import Config


class EmailSender:
    """Class to handle email sending via Flask-Mail"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_mail()
        self.mail = Mail(self.app)
    
    def configure_mail(self):
        """Configure Flask-Mail with settings from Config"""
        self.app.config['MAIL_SERVER'] = Config.MAIL_SERVER
        self.app.config['MAIL_PORT'] = Config.MAIL_PORT
        self.app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
        self.app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
        self.app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
        self.app.config['MAIL_USE_SSL'] = Config.MAIL_USE_SSL
        self.app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_USERNAME
    
    def send_assignment_email(self, screenshot_path, github_repo, your_name, 
                             resume_path=None, work_samples=None):
        """Send assignment submission email with all requirements"""
        with self.app.app_context():
            try:
                subject = f"Python (Selenium) Assignment - {your_name}"
                
                body = f"""
Dear Team,

Please find my submission for the Python (Selenium) Assignment below:

1. Screenshot of Form Filled via Code:
   - Attached as 'form_confirmation.png'

2. Source Code (GitHub Repository):
   - {github_repo}

3. Brief Documentation of Approach:
   
   TECHNICAL APPROACH:
   
   • Automation Framework: Python with Selenium WebDriver 4.15.2
   • Browser: Google Chrome (automated using ChromeDriver)
   • Dependencies Management: webdriver-manager for automatic driver setup
   • Email Automation: Flask-Mail 0.9.1 for SMTP email sending
   • Configuration: Environment variables (.env) for secure credential storage
   
   IMPLEMENTATION STEPS:
   
   a) Form Filling Process:
      - Initialized Chrome WebDriver with appropriate options
      - Navigated to the Google Form URL
      - Identified form fields using multiple locator strategies (CSS selectors, XPath)
      - Filled all required fields programmatically:
        * Full Name
        * Contact Number (10 digits)
        * Email ID
        * Full Address
        * Pin Code
        * Date of Birth
        * Gender
        * Verification Code (GNFPYC)
      - Submitted the form and captured confirmation screenshot
   
   b) Email Automation:
      - Implemented Flask-Mail for SMTP email sending
      - Configured Gmail SMTP with TLS encryption
      - Automated email composition with all required attachments
      - Added proper error handling and logging
      - Included all 6 assignment requirements in email body
   
   c) Code Organization:
      - Modular structure with separate modules:
        * config/config.py - Configuration management
        * src/form_filler.py - Form automation logic
        * src/email_sender.py - Email sending logic
        * main.py - Main orchestration script
      - Configuration management using environment variables
      - Comprehensive error handling and logging
      - Clean, documented, and maintainable code
   
   FEATURES:
   - Automatic ChromeDriver management (no manual download needed)
   - Multiple fallback strategies for element location
   - Screenshot capture with timestamp
   - Secure credential management via .env file
   - Detailed console logging for debugging
   - All form fields automated including verification code

4. Resume:
   - Google Drive Link: https://drive.google.com/file/d/1ib9hvoLkRos9DqoP9SuzfCR4YDPSEwXT/view?usp=sharing

5. Links to Past Projects/Work Samples:
"""
                
                if work_samples:
                    for i, sample in enumerate(work_samples, 1):
                        body += f"\n   {i}. {sample}"
                else:
                    body += f"\n   - GitHub: {github_repo}"
                
                body += f"""

6. Availability Confirmation:
   Yes, I confirm my availability to work full time (10 AM to 7 PM) 
   for the next 3-6 months.

Technical Stack Used:
- Python 3.x
- Selenium WebDriver 4.15.2
- Flask 3.0.0
- Flask-Mail 0.9.1
- webdriver-manager 4.0.1
- python-dotenv 1.0.0
- Chrome Browser

Thank you for considering my submission. I look forward to hearing from you.

Best regards,
{your_name}
                """
                
                # Create message
                msg = Message(
                    subject=subject,
                    sender=Config.MAIL_USERNAME,
                    recipients=[Config.TO_EMAIL],
                    cc=[Config.CC_EMAIL],
                    body=body
                )
                
                # Attach screenshot
                if screenshot_path and os.path.exists(screenshot_path):
                    with open(screenshot_path, 'rb') as f:
                        msg.attach(
                            'form_confirmation.png',
                            'image/png',
                            f.read()
                        )
                    print("✓ Attached screenshot")
                else:
                    print("⚠ Warning: Screenshot file not found")
                
                # Attach resume if provided (local file)
                if resume_path and os.path.exists(resume_path):
                    filename = os.path.basename(resume_path)
                    with open(resume_path, 'rb') as f:
                        msg.attach(
                            filename,
                            'application/pdf',
                            f.read()
                        )
                    print("✓ Attached resume")
                
                # Send email
                self.mail.send(msg)
                print(f"\n✓ Email sent successfully to {Config.TO_EMAIL}")
                print(f"✓ CC: {Config.CC_EMAIL}")
                
                return True
                
            except Exception as e:
                print(f"\n✗ Error sending email: {str(e)}")
                print("\nPlease check:")
                print("  1. MAIL_USERNAME and MAIL_PASSWORD in .env file")
                print("  2. Gmail: Use 'App Password' (16 characters, not regular password)")
                print("  3. Enable 2-Step Verification in Google Account")
                print("  4. Generate App Password at: https://myaccount.google.com/apppasswords")
                print("  5. Internet connection")
                return False


def send_assignment_submission(screenshot_path, github_repo=None, your_name=None,
                               resume_path=None, work_samples=None):
    """Convenience function to send assignment email"""
    github_repo = github_repo or Config.GITHUB_REPO
    your_name = your_name or Config.YOUR_NAME
    
    sender = EmailSender()
    return sender.send_assignment_email(
        screenshot_path=screenshot_path,
        github_repo=github_repo,
        your_name=your_name,
        resume_path=resume_path,
        work_samples=work_samples
    )
