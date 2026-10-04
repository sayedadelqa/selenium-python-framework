from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

    def title_text(self) -> str:
        return self.text_of(self.TITLE)

    def add_to_cart(self, product_slug: str):
        """product_slug example: 'sauce-labs-backpack'"""
        self.click((By.CSS_SELECTOR, f"[data-test='add-to-cart-{product_slug}']"))

    def remove_from_cart(self, product_slug: str):
        self.click((By.CSS_SELECTOR, f"[data-test='remove-{product_slug}']"))

    def cart_badge_text(self) -> str:
        return self.text_of(self.CART_BADGE)

    def cart_badge_gone(self) -> bool:
        return self.is_gone(self.CART_BADGE)

    def sort_by(self, option_value: str):
        """option_value: az, za, lohi, hilo"""
        Select(self.find(self.SORT)).select_by_value(option_value)

    def price_values(self):
        self.find(self.PRICES)  # wait until prices are on the page
        return [float(e.text.replace("$", "")) for e in self.find_all(self.PRICES)]

    def open_cart(self):
        self.click(self.CART_LINK)
