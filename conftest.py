"""Shared fixtures and hooks.

Run options:
    pytest --browser-name chrome|firefox|edge   (default: chrome)
    pytest --headless                      (no visible browser window, used in CI)
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from api.api_client import ApiClient
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import load_json


def pytest_addoption(parser):
    parser.addoption("--browser-name", action="store", default="chrome", choices=["chrome", "firefox", "edge"])
    parser.addoption("--headless", action="store_true", default=False, help="run the browser without a window")


def _chromium_options(options, headless: bool):
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-search-engine-choice-screen")
    # Chrome shows a "change your password" popup after login on demo sites; switch it off.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    return options


@pytest.fixture
def driver(request):
    """A fresh browser for every test, closed automatically afterwards."""
    browser = request.config.getoption("--browser-name")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        drv = webdriver.Chrome(options=_chromium_options(ChromeOptions(), headless))
    elif browser == "edge":
        drv = webdriver.Edge(options=_chromium_options(EdgeOptions(), headless))
    else:
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("-headless")
        drv = webdriver.Firefox(options=opts)

    drv.implicitly_wait(0)  # only explicit waits are used in this framework
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On a failed test, embed a screenshot in the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            try:
                from pytest_html import extras
                shot = drv.get_screenshot_as_base64()
                report.extras = getattr(report, "extras", []) + [extras.png(shot, "Screenshot on failure")]
            except Exception:
                pass


@pytest.fixture(scope="session")
def users():
    return load_json("users.json")


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver)


@pytest.fixture
def logged_in(login_page, users):
    """Open the site and log in with the valid user."""
    login_page.load()
    login_page.login(**users["valid"])


@pytest.fixture(scope="session")
def api():
    return ApiClient()
