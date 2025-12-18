from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url

    def open(self, path: str = ""):
        """Open a relative path on the base_url."""
        self.driver.get(self.base_url + path)

