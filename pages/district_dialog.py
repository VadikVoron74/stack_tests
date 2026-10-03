import allure
from pages.base_page import BasePage

class DistrictDialog(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title = page.get_by_text("Район (создание)")
        self.name_input = page.locator('[data-test-id="Название района"]')
        self.number_input = page.locator('[data-test-id="Номер в списке"]')
        self.name_error = page.get_by_text("Поле не может быть пустым")
        self.params_title = page.get_by_text("Параметры", exact=True)
        self.params_empty = page.get_by_text("Отсутствуют данные")
        self.save_button = page.locator('[data-cy="btn-save"]')
        self.cancel_button = page.locator('[data-cy="btn-cancel"]')

    @allure.step("Ввести название района: '{name}'")
    def fill_name(self, name: str):
        self.name_input.fill(name)

    @allure.step("Кликнуть в «Название района» и убрать из него фокус")
    def touch_name(self):
        self.name_input.click()
        self.number_input.click()

    @allure.step("Нажать 'Внести'")
    def save(self):
        self.save_button.click()

    def cancel(self):
        self.cancel_button.click()

