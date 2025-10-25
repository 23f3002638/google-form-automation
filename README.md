# Google Form Automation - Python Selenium Assignment

Automated Google Form filling and email submission using Python, Selenium WebDriver, and Flask-Mail.

## 🎯 Assignment Completion

This project fulfills all requirements:
1. ✅ Automatically fills Google Form using Selenium
2. ✅ Captures screenshot of confirmation page
3. ✅ Sends email automatically using Flask-Mail
4. ✅ Includes all 6 assignment requirements
5. ✅ Code pushed to GitHub

## 🚀 Features

- **Automatic ChromeDriver Management** - No manual driver download needed
- **Google Form Automation** - Fills all 8 fields automatically:
  - Full Name
  - Contact Number (10 digits)
  - Email ID
  - Full Address
  - Pin Code
  - Date of Birth
  - Gender
  - Verification Code (GNFPYC)
- **Screenshot Capture** - Timestamped confirmation screenshots
- **Email Automation** - Flask-Mail with Gmail SMTP
- **All 6 Requirements** - Automatically included in email:
  1. Screenshot attachment
  2. GitHub repository link
  3. Technical documentation
  4. Resume (optional)
  5. Work samples
  6. Availability confirmation

## 📋 Prerequisites

- Python 3.8 or higher
- Google Chrome Browser
- Gmail account with App Password
- Git

## 🛠️ Installation

### 1. Clone Repository
git clone https://github.com/yourusername/google-form-automation.git
cd google-form-automation

text

### 2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux

text

### 3. Install Dependencies
pip install -r requirements.txt

text

## ⚙️ Configuration

### 1. Get Gmail App Password
1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification → App passwords
3. Generate password for "Mail"
4. Copy 16-character password (remove spaces)

### 2. Update `.env` File
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your_16_char_app_password
YOUR_NAME=Your Full Name
CONTACT_NUMBER=9876543210
YOUR_EMAIL=your.email@gmail.com
YOUR_ADDRESS=Your Complete Address
PIN_CODE=110001
DATE_OF_BIRTH=15/08/2000
GENDER=Male
VERIFICATION_CODE=GNFPYC
GITHUB_REPO=

text

## 🚀 Usage

python main.py

text

### What Happens:
1.  Chrome browser opens automatically
2.  Navigates to Google Form
3.  Fills all 8 fields automatically
4.  Submits the form
5.  Captures screenshot
6.  Sends email to tech@themedius.ai with all requirements
7.  Browser closes

##  GitHub Setup

git init
git add .
git commit -m "Complete Google Form Automation with Flask-Mail"
git remote add origin https://github.com/YOUR_USERNAME/google-form-automation.git
git push -u origin main

text

## 🛠️ Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming language |
| Selenium | 4.15.2 | Browser automation |
| Flask-Mail | 0.9.1 | Email sending |
| webdriver-manager | 4.0.1 | ChromeDriver management |
| python-dotenv | 1.0.0 | Environment variables |

## 📧 Email Submission

Email automatically sent to:
- **TO:** tech@themedius.ai
- **CC:** hr@themedius.ai
- **Subject:** Python (Selenium) Assignment - [Your Name]

## 🐛 Troubleshooting

### Email Not Sending
- Use Gmail App Password (not regular password)
- Enable 2-Step Verification
- Remove spaces from app password

### Form Fields Not Filling
- Check internet connection
- Verify form URL
- Update form_data in main.py if form structure changed

### ChromeDriver Issues
- webdriver-manager handles this automatically
- Just ensure internet connection on first run

## 📝 License

Created for assignment purposes - The Medius.ai

## 👤 Author

**[Your Name]**
- Email: your.email@gmail.com
- GitHub: [@yourusername](https://github.com/yourusername)
