import os


class Config:
    # Environment
    BASE_URL = "https://www.saucedemo.com/"

    # Browser
    BROWSER = "chromium"
    HEADLESS = False
    SLOW_MO = 300

    # Timeout (milliseconds)
    TIMEOUT = 10000
    NAVIGATION_TIMEOUT = 30000

    # Screenshot
    SCREENSHOT_DIR = os.path.join("reports", "screenshots")

    # Report
    REPORT_DIR = "reports"

    # Test Account
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
