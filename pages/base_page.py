from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.config import BASE_URL, DEFAULT_TIMEOUT


class BasePage:
    """Shared helpers. Every action waits explicitly, never with time.sleep()."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, path: str = "/"):
        self.driver.get(f"{BASE_URL}{path}")

    def find(self, locator):
        """Wait until the element is visible, then return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Return all matching elements (can be an empty list)."""
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str):
        element = self.find(locator)
        element.clear()
        if text:
            element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.find(locator).text

    def is_gone(self, locator) -> bool:
        """True when the element is not visible (or not in the page) within the timeout."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_count(self, locator, expected: int) -> bool:
        return self.wait.until(lambda d: len(d.find_elements(*locator)) == expected)

    def wait_for_text(self, locator, text: str) -> bool:
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))
