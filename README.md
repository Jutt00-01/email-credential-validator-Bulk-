# email-credential-validator-Bulk-
Email Credential Validator - Advanced Python automation tool for parallel testing of email credentials across Gmail, Outlook, and Yahoo. Features 25+ concurrent browser automation, intelligent security challenge detection, parallel threading, and detailed CSV/JSON reporting. Built for a  testing and educational learning. Licensed under MIT.

# 📧 Email Credential Validator

A Python automation tool for parallel testing of email credentials. Built for educational purposes and authorized security testing.

> **⚠️ DISCLAIMER**: This tool is designed for testing credentials on accounts you own or have explicit written permission to test. Unauthorized access to email accounts is illegal. Use responsibly.

---

## 🎯 Features

- ✅ **Parallel Testing** - Test multiple email accounts simultaneously (configurable 1-50+)
- ✅ **Multi-Provider Support** - Gmail, Outlook, Hotmail, Yahoo, and custom domains
- ✅ **Smart Detection** - Recognizes security challenges and 2FA as successful login
- ✅ **Detailed Logging** - Generates CSV and JSON reports with timestamps
- ✅ **Browser Automation** - Uses Selenium for real browser automation
- ✅ **Anti-Detection** - Built-in anti-automation features for stealth testing
- ✅ **Low Resource Mode** - Optimized for systems with limited CPU/RAM

---

## 📋 Requirements

- Python 3.10+ (Python 3.13 compatible)
- 8GB+ RAM (for parallel testing)
- Chrome/Chromium browser installed
- Linux/Windows/macOS

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/email-credential-validator.git
cd email-credential-validator
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Chrome is installed
```bash
# Linux
which google-chrome chromium

# macOS
which /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome

# Windows
where chrome.exe
```

---

## 📝 Setup: Credentials File

Create a `credentials.txt` file with format:
```
email1@gmail.com:password1
email2@outlook.com:password2
email3@yahoo.com:password3
```

**Example:**
```
user1@gmail.com:MyPassword123
user2@outlook.com:SecurePass456
user3@yahoo.com:AnotherPass789
```

---

## 🎮 Usage

### Basic Usage (5 parallel logins)
```bash
python multi_email_login.py credentials.txt
```

### With custom number of parallel logins
```bash
# Test 10 accounts at same time
python multi_email_login.py credentials.txt --workers 10

# Test 20 accounts at same time (need 16GB+ RAM)
python multi_email_login.py credentials.txt --workers 20
```

### Headless mode (no browser windows visible)
```bash
python multi_email_login.py credentials.txt --headless

# Headless + custom workers
python multi_email_login.py credentials.txt --headless --workers 5
```

### Split credentials by provider
First split your mixed credentials file:
```bash
python split_credentials.py credentials.txt
```

This creates:
- `credentials_gmail.txt`
- `credentials_outlook.txt`
- `credentials_yahoo.txt`
- `credentials_other.txt`

Then test each separately:
```bash
python multi_email_login.py credentials_gmail.txt --workers 5
python multi_email_login.py credentials_outlook.txt --workers 5
```

---

## 📊 Output

Results are saved in `email_login_logs/` folder:

### CSV Report
```
email,status,provider,timestamp,profile
user1@gmail.com,SUCCESS,gmail,2024-01-15T10:30:45,/tmp/chrome_profile_...
user2@outlook.com,FAILED,microsoft,2024-01-15T10:31:12,
user3@yahoo.com,SUCCESS,yahoo,2024-01-15T10:32:01,/tmp/chrome_profile_...
```

### JSON Report
```json
[
  {
    "email": "user1@gmail.com",
    "status": "SUCCESS",
    "provider": "gmail",
    "timestamp": "2024-01-15T10:30:45.123456",
    "profile": "/tmp/chrome_profile_..."
  },
  {
    "email": "user2@outlook.com",
    "status": "FAILED",
    "provider": "microsoft",
    "reason": "Verification failed",
    "timestamp": "2024-01-15T10:31:12.654321"
  }
]
```

---

## 🔧 Configuration

### Parallel Workers (by system specs)

| CPU | RAM | Recommended Workers |
|-----|-----|-------------------|
| Dual Core | 4GB | 2-3 |
| Quad Core | 8GB | 5 |
| 6-Core | 16GB | 10 |
| 8-Core | 16GB | 15 |
| Server | 32GB+ | 25+ |

**Monitor CPU/RAM:**
```bash
# Linux
htop

# macOS
top

# Windows Task Manager
Ctrl + Shift + Esc
```

---

## ⚡ Performance Tips

1. **Use Kali Linux headless mode** for better performance:
   ```bash
   python multi_email_login.py credentials.txt --headless
   ```

2. **Start with fewer workers** and gradually increase:
   ```bash
   # Test with 3 workers first
   python multi_email_login.py credentials.txt --workers 3
   ```

3. **Split large files** - Don't test 1000 accounts at once:
   ```bash
   # Split by provider first
   python split_credentials.py large_credentials.txt
   
   # Test each in batches
   python multi_email_login.py credentials_gmail.txt
   ```

4. **Use different profiles** for different providers to avoid conflicts

---

## 🛡️ Security & Ethics

### ✅ Authorized Use:
- Testing your own email accounts
- Security research on accounts you own
- Authorized penetration testing (with written permission)
- Educational learning projects

### ❌ Unauthorized Use:
- Testing others' accounts without permission
- Credential stuffing attacks
- Unauthorized access
- Commercial credential harvesting

**Legal Notice**: Unauthorized access to computer systems is a federal crime under the Computer Fraud and Abuse Act (CFAA) in the USA and similar laws globally.

---

## 🐛 Troubleshooting

### Gmail accounts failing
**Problem:** Gmail blocks Selenium automation
**Solution:** 
1. Enable App Passwords on your Gmail account
2. Use App Password instead of account password
3. Or use Outlook/Yahoo for testing

**Steps:**
- Go to https://myaccount.google.com/security
- Enable 2-Step Verification
- Generate App Password
- Use that in credentials file

### CPU/Memory high
**Problem:** System is overloaded
**Solution:**
- Reduce `--workers` value
- Use `--headless` mode
- Test fewer accounts at a time

### Chrome/Chromium not found
**Problem:** Browser not installed
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# Fedora
sudo dnf install chromium

# macOS
brew install chromium

# Windows
Download from chrome.google.com
```

### "distutils not found" error
**Problem:** Python 3.13 compatibility issue
**Solution:**
```bash
pip install --upgrade undetected-chromedriver
# Or use Python 3.12
python3.12 multi_email_login.py credentials.txt
```

---

## 📚 Technical Stack

- **Selenium** - Browser automation
- **Python 3.10+** - Core language
- **ThreadPoolExecutor** - Parallel processing
- **webdriver-manager** - Chrome driver management
- **ChromeDriver** - Selenium web driver

---

## 🎓 Educational Resources

Learn more about the technologies used:

- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Python Threading](https://docs.python.org/3/library/threading.html)
- [Web Automation Basics](https://automatetheboringstuff.com/)
- [Email Provider APIs](https://developers.google.com/gmail/api)

---

## 📝 Changelog

### v1.0.0 (2024-01-15)
- Initial release
- Support for Gmail, Outlook, Yahoo
- Parallel testing up to 50+ workers
- CSV and JSON reporting
- Recovery/2FA detection as success

---

## 🤝 Contributing

Found a bug or have improvements? 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see `LICENSE` file for details.

**Key Points:**
- Free to use for educational purposes
- Must include license in distributions
- No warranty provided
- Author not liable for misuse

---

## ⚠️ Disclaimer

This tool is provided for **educational and authorized testing purposes only**. 

- **Users are responsible** for ensuring they have proper authorization before testing any email accounts
- The author is **not responsible** for any misuse, damage, or legal consequences
- **Use ethically and legally**
- Respect privacy and computer fraud laws

---

## 👨‍💻 Author

**Your Name**
- GitHub: [Jutt00-01](https://github.com/Jutt00-01)
- Email: sjsargana@example.com
- Learning: Cybersecurity & Python Automation

**Built with:** Claude AI + Selenium + Python

---

## 🙏 Acknowledgments

- Claude AI for code assistance
- Selenium community for browser automation tools
- Open source community for dependencies
- Educational institutions for cybersecurity knowledge

---

## 📞 Support

Issues? Questions?

1. Check the **Troubleshooting** section
2. Read the **FAQ** below
3. Open an **Issue** on GitHub

---

## ❓ FAQ

**Q: Is this legal to use?**
A: Only on accounts you own or have permission to test. Unauthorized access is illegal.

**Q: Why are my logins failing on Gmail?**
A: Gmail blocks Selenium. Use App Passwords instead.

**Q: How many workers should I use?**
A: Start with 5-10 based on your system specs. Monitor CPU/RAM usage.

**Q: Can I test against other email providers?**
A: This version supports Gmail, Outlook, Yahoo, and custom domains.

**Q: How long does testing take?**
A: Depends on number of accounts and workers. Usually 30 seconds per account.

**Q: Where are results saved?**
A: In `email_login_logs/` folder as CSV and JSON files.

---

## 🌟 Show Your Support

If this helped you learn, please:
- ⭐ Star this repository
- 📤 Share with fellow students
- 💬 Leave feedback

---

**Happy Learning! 🚀**
