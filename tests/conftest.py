import os
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import pytest
from playwright.sync_api import sync_playwright

from config.config import Config


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="function")
def browser(playwright_instance):
    browser = getattr(playwright_instance, Config.BROWSER).launch(
        headless=Config.HEADLESS,
        slow_mo=Config.SLOW_MO
    )

    yield browser

    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()

    yield context

    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()

    page.set_default_timeout(Config.TIMEOUT)
    page.set_default_navigation_timeout(
        Config.NAVIGATION_TIMEOUT
    )

    yield page

    screenshot_dir = Config.SCREENSHOT_DIR
    os.makedirs(screenshot_dir, exist_ok=True)

    page.close()

@pytest.fixture
def inventory_page(page):
    login = LoginPage(page)
    inventory = InventoryPage(page)

    login.open(Config.BASE_URL)
    login.login_as_standard_user()
    inventory.verify_inventory_page_loaded()

    return inventory
