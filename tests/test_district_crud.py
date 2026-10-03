import allure
from playwright.sync_api import expect


@allure.title("TC-04: Создание района и сохранение после повторного открытия раздела")
def test_create_district(addresses, district_name, cleanup):
    cleanup.append(district_name)
    dialog = addresses.open_create_district()

    dialog.fill_name(district_name)
    dialog.save()

    with allure.step("Окно закрыто, запись появилась в таблице"):
        expect(dialog.title).to_be_hidden()
        expect(addresses.row(district_name)).to_be_visible()

    addresses.reopen_section()
    with allure.step("После повторного открытия раздела запись отображается"):
        expect(addresses.row(district_name)).to_be_visible()

@allure.title("TC-10: Редактирование района и сохранение изменений")
def test_edit_district(addresses, district, cleanup):
    new_name = district.replace("Автотест", "Автотест-изм")
    cleanup.append(new_name)

    dialog = addresses.open_edit_district(district)
    dialog.fill_name(new_name)
    dialog.name_input.press("Tab")
    dialog.save()

    with allure.step("В таблице новое название, старого нет"):
        expect(dialog.name_input).to_be_hidden()
        expect(addresses.row(new_name)).to_be_visible()
        expect(addresses.row(district)).to_have_count(0)

    addresses.reopen_section()
    with allure.step("После повторного открытия раздела изменения сохранились"):
        expect(addresses.row(new_name)).to_be_visible()


@allure.title("TC-12: Удаление района: отмена и подтверждение")
def test_delete_district(addresses, district):
    addresses.select_district(district)
    addresses.click_delete()

    with allure.step("Нажать «Нет»: район остался в таблице"):
        addresses.confirm_no.click()
        expect(addresses.row(district)).to_be_visible()

    addresses.click_delete()
    with allure.step("Нажать «Да»: район исчез из таблицы"):
        addresses.confirm_yes.click()
        expect(addresses.row(district)).to_have_count(0)

    addresses.reopen_section()
    with allure.step("После повторного открытия раздела района нет"):
        expect(addresses.row(district)).to_have_count(0)