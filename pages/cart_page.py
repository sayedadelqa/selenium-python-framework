from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")

    def wait_for_items(self, expected: int) -> bool:
        return self.wait_for_count(self.ITEMS, expected)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
