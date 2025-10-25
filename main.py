"""
Main execution script for Google Form Automation Assignment
Orchestrates form filling and email sending
"""
import os
import sys
from config.config import Config
from src.form_filler import automate_google_form
from src.email_sender import send_assignment_submission


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("  GOOGLE FORM AUTOMATION & EMAIL SUBMISSION")
    print("  Python (Selenium) Assignment - The Medius.ai")
    print("=" * 80)
    
    # Validate configuration
    try:
        Config.validate_config()
        print("\n✓ Configuration validated successfully")
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease update the .env file with your details")
        sys.exit(1)
    
    # Display configuration
    print("\n" + "-" * 80)
    print("CONFIGURATION:")
    print("-" * 80)
    print(f"Form URL: {Config.FORM_URL}")
    print(f"Your Name: {Config.YOUR_NAME}")
    print(f"Your Email: {Config.YOUR_EMAIL}")
    print(f"Contact: {Config.CONTACT_NUMBER}")
    print(f"GitHub Repo: {Config.GITHUB_REPO}")
    print(f"To: {Config.TO_EMAIL}")
    print(f"CC: {Config.CC_EMAIL}")
    print("-" * 80)
    
    # Prepare form data - IN CORRECT ORDER
    form_data = {
        'Full Name': Config.YOUR_NAME,
        'Contact Number': Config.CONTACT_NUMBER,
        'Email ID': Config.YOUR_EMAIL,
        'Full Address': Config.YOUR_ADDRESS,
        'Pin Code': Config.PIN_CODE,
        'Date of Birth': Config.DATE_OF_BIRTH,  # Will be handled separately
        'Gender': Config.GENDER,
        'Verification Code': Config.VERIFICATION_CODE,
    }
    
    print("\n" + "=" * 80)
    print("STEP 1: FILLING GOOGLE FORM AUTOMATICALLY")
    print("=" * 80)
    
    # Fill and submit form
    screenshot_path = automate_google_form(Config.FORM_URL, form_data)
    
    if not screenshot_path:
        print("\n✗ Failed to complete form automation")
        sys.exit(1)
    
    print(f"\n✅ Form automation completed!")
    print(f"✓ Screenshot saved: {screenshot_path}")
    
    # Prepare additional info with resume and past projects
    resume_path = Config.RESUME_PATH if Config.RESUME_PATH else None
    work_samples = [
        Config.GITHUB_REPO,  # Current project
        "https://github.com/ar4002?tab=repositories",  # All past projects
        "https://github.com/23f3002638",  # Current IIT profile
    ]
    
    print("\n" + "=" * 80)
    print("STEP 2: SENDING EMAIL SUBMISSION AUTOMATICALLY")
    print("=" * 80)
    
    # Send email
    email_sent = send_assignment_submission(
        screenshot_path=screenshot_path,
        github_repo=Config.GITHUB_REPO,
        your_name=Config.YOUR_NAME,
        resume_path=resume_path,
        work_samples=work_samples
    )
    
    if email_sent:
        print("\n" + "=" * 80)
        print("  ✅ ASSIGNMENT SUBMISSION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nYour submission includes:")
        print("  ✓ Screenshot of form confirmation")
        print("  ✓ GitHub repository link")
        print("  ✓ Complete documentation of approach")
        print("  ✓ Work samples from both GitHub accounts")
        print("  ✓ Availability confirmation (10 AM - 7 PM for 3-6 months)")
        if resume_path:
            print("  ✓ Resume attached")
        print("\nEmail sent to:")
        print(f"  • TO: {Config.TO_EMAIL}")
        print(f"  • CC: {Config.CC_EMAIL}")
        print("=" * 80)
    else:
        print("\n✗ Failed to send email")
        print(f"\nScreenshot saved at: {screenshot_path}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
