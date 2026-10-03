import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page:Page):
        self.page = page

    def open(self, url: str):
        with allure.step(f'Открыть {url}'):
            self.page.goto(url, timeout=60000)

    def reload(self):
        with allure.step(f'Обновить страницу (F5)'):
            self.page.reload()



