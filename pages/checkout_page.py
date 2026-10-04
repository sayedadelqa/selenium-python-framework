from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE = (By.CSS_SELECTOR, "[data-test='continue']")
    FINISH = (By.CSS_SELECTOR, "[data-test='finish']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)

    def finish(self):
        self.click(self.FINISH)

    def complete_text(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

    def error_text(self) -> str:
        return self.text_of(self.ERROR)
