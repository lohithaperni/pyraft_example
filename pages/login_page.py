from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class LoginPage(BasePage):
    # Revalu platform login page selectors
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Enter your email' or @type='email' or @name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Enter your password' or @type='password' or @name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Log In') or @type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[role='alert'], .error, [class*='error'], [class*='Error']")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Log in here')]")

    def open_login(self):
        """Navigate to login page"""
        self.open("/login")

    def navigate_to_login(self):
        """Click on 'Log in here' link if on home page"""
        try:
            login_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.LOGIN_LINK)
            )
            login_link.click()
        except:
            # Already on login page or link not found
            pass

    def login(self, email: str, password: str):
        """Login with email and password"""
        wait = WebDriverWait(self.driver, 10)
        
        # Wait for and fill email - try multiple selector strategies
        try:
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your email']")))
        except:
            try:
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
            except:
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
        
        email_input.clear()
        email_input.send_keys(email)
        
        # Wait for and fill password - try multiple selector strategies
        try:
            password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your password']")))
        except:
            try:
                password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
            except:
                password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        
        password_input.clear()
        password_input.send_keys(password)
        
        # Click login button - try multiple selector strategies
        try:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]")))
        except:
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        
        login_button.click()

    def is_logged_in(self) -> bool:
        """Check if login was successful by checking URL or page elements"""
        # Wait for redirect after login (up to 15 seconds)
        wait = WebDriverWait(self.driver, 15)
        
        try:
            # Wait until URL changes from login page
            wait.until(
                lambda d: "/login" not in d.current_url and d.current_url != self.base_url + "/login"
            )
            current_url = self.driver.current_url
            # Check if we're no longer on login page
            return "/login" not in current_url and current_url != self.base_url + "/login"
        except Exception as e:
            # If timeout, check current URL anyway
            current_url = self.driver.current_url
            # Also check if login form is still present (alternative check)
            try:
                # If we can't find login form elements, might be logged in
                self.driver.find_element(*self.EMAIL_INPUT)
                # If we found email input, still on login page
                return False
            except:
                # Can't find login elements, might be logged in
                return "/login" not in current_url

    def get_error_text(self) -> str:
        """Get error message text if login fails"""
        try:
            wait = WebDriverWait(self.driver, 3)
            error_element = wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE))
            return error_element.text
        except:
            elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            return elements[0].text if elements else ""

