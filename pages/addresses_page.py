import re

import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

from pages.base_page import BasePage
from pages.district_dialog import DistrictDialog


class AddressesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.section_tile = page.get_by_text("Адреса проживающих", exact=True).first
        self.home_item = page.get_by_role("option", name="Главная", exact=True)
        self.add_button = page.locator('[data-cy="btn-add"]').first
        self.district_item = page.get_by_role("menuitem", name="Район", exact=True)
        self.records_counter = page.get_by_text(re.compile(r"Записей \d+-\d+ из \d+")).first
        self.delete_button = page.locator('[data-cy="btn-delete"]')
        self.confirm_yes = page.locator('[data-cy="btn-yes"]')
        self.confirm_no = page.get_by_role("button", name="Нет", exact=True)
        self.auth_button = page.get_by_role("button", name="Войти или зарегистрироваться")

    def row(self, name: str):
        return self.page.get_by_role("row").filter(
            has=self.page.get_by_role("cell", name=name, exact=True)
        )

    @allure.step("Открыть раздел «Адреса проживающих»")
    def open_section(self):
        self.section_tile.click()
        expect(self.add_button).to_be_visible()
        expect(self.records_counter).to_be_visible()
        self.page.wait_for_load_state("networkidle")

    @allure.step("Выйти на главную и снова открыть раздел")
    def reopen_section(self):
        self.home_item.click()
        self.open_section()

    def close_overlays(self):
        if self.auth_button.is_visible():
            self.auth_button.click()
            expect(self.auth_button).to_be_hidden(timeout=15000)
        else:
            self.page.keyboard.press("Escape")

    @allure.step("Нажать «+» и выбрать «Район»")
    def open_create_district(self) -> DistrictDialog:
        for attempt in range(5):
            try:
                self.add_button.click(timeout=5000)
                self.district_item.click(timeout=10000)
                break
            except PlaywrightTimeoutError:
                self.close_overlays()
        else:
            raise AssertionError("Не удалось выбрать пункт «Район» после 5 попыток")

        dialog = DistrictDialog(self.page)
        expect(dialog.title).to_be_visible()
        expect(dialog.number_input).to_have_value(re.compile(r"^\d+$"))
        self.page.wait_for_load_state("networkidle")
        return dialog

    @allure.step("Создать район «{name}»")
    def create_district(self, name: str):
        dialog = self.open_create_district()
        dialog.fill_name(name)
        dialog.save()
        expect(dialog.title).to_be_hidden()
        expect(self.row(name)).to_be_visible()

    @allure.step("Открыть район «{name}» на редактирование")
    def open_edit_district(self, name: str) -> DistrictDialog:
        row = self.row(name)
        row.hover()
        row.get_by_role("button").last.click()
        dialog = DistrictDialog(self.page)
        expect(dialog.name_input).to_have_value(name)
        return dialog

    @allure.step("Отметить чекбокс у района «{name}»")
    def select_district(self, name: str):
        row = self.row(name)
        row.hover()
        row.locator(".v-input--selection-controls__ripple").click()

    @allure.step("Нажать значок корзины")
    def click_delete(self):
        self.delete_button.click()

    @allure.step("Удалить район «{name}»")
    def delete_district(self, name: str):
        self.select_district(name)
        self.click_delete()
        self.confirm_yes.click()
        expect(self.row(name)).to_have_count(0)
