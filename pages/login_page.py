from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        self.open("/")

    def login(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_text(self) -> str:
        return self.text_of(self.ERROR)
