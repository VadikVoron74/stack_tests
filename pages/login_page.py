import allure
from playwright.sync_api import expect

from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.open_auth_button = page.get_by_role("button", name="Войти или зарегистрироваться")

    @allure.step("Войти под пользователем {login}")
    def login(self, login: str, password: str):
        with self.page.expect_popup() as popup_info:
            self.open_auth_button.click()
        sso = popup_info.value

        sso.get_by_placeholder("Логин").fill(login)
        sso.get_by_placeholder("Пароль").fill(password)
        with sso.expect_event("close"):
            sso.get_by_role("button", name="Войти", exact=True).click()

        expect(self.open_auth_button).to_be_hidden()
        self.page.wait_for_load_state("networkidle")





