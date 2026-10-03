import re

import allure
import pytest
from playwright.sync_api import expect


@allure.title("TC-01: Открытие окна создания района, состояние полей")
def test_open_dialog_default_state(dialog):
    with allure.step("Проверить состав окна"):
        expect(dialog.title).to_be_visible()
        expect(dialog.name_input).to_be_visible()
        expect(dialog.number_input).to_be_visible()
        expect(dialog.params_title).to_be_visible()
        expect(dialog.params_empty).to_be_visible()

    with allure.step("Проверить значения полей по умолчанию"):
        expect(dialog.name_input).to_have_value("")
        expect(dialog.number_input).to_have_value(re.compile(r"^\d+$"))

    with allure.step("Ошибки под полем «Название района» нет"):
        expect(dialog.name_error).to_be_hidden()

    with allure.step("Кнопка «Отмена» активна"):
        expect(dialog.cancel_button).to_be_enabled()


@allure.title("TC-02: Район с пустым названием создать нельзя")
def test_empty_name_not_saved(dialog):
    if dialog.save_button.is_enabled():
        dialog.save()

    with allure.step("Окно осталось открытым, район не создан"):
        expect(dialog.title).to_be_visible()


@allure.title("TC-02: Валидация поля «Название района»")
def test_name_validation(dialog):
    dialog.touch_name()
    with allure.step("Пустое поле: ошибка показана, «Внести» неактивна"):
        expect(dialog.name_error).to_be_visible()
        expect(dialog.save_button).to_be_disabled()

    dialog.fill_name("Тест")
    with allure.step("Валидное название: ошибки нет, «Внести» активна"):
        expect(dialog.name_error).to_be_hidden()
        expect(dialog.save_button).to_be_enabled()


@allure.title("TC-02, шаг 2: название из одних пробелов не принимается")
@pytest.mark.xfail(
    reason="BUG-02: поле «Название района» принимает значение из одних пробелов",
    raises=AssertionError,
    strict=True,
)
def test_name_spaces_only(dialog):
    dialog.fill_name("   ")
    with allure.step("Ошибка показана, «Внести» неактивна"):
        expect(dialog.name_error).to_be_visible()
        expect(dialog.save_button).to_be_disabled()