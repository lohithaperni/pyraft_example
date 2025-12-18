from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def create_driver(run_config: dict):
    browser = run_config.get("browser", "chrome").lower()

    if browser == "chrome":
        options = ChromeOptions()
        if run_config.get("headless", False):
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    implicit_wait = run_config.get("implicit_wait", 0)
    driver.implicitly_wait(implicit_wait)
    driver.maximize_window()
    return driver

