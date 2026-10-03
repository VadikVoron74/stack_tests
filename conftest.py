import time
import allure
import pytest

import config
from pages.addresses_page import AddressesPage
from pages.login_page import LoginPage
from pages.district_dialog import DistrictDialog

@pytest.fixture
def auth_page(page):
    login_page = LoginPage(page)
    login_page.open(config.BASE_URL)
    login_page.login(config.LOGIN, config.PASSWORD)
    return page


@pytest.fixture
def addresses(auth_page):
    addresses_page = AddressesPage(auth_page)
    addresses_page.open_section()
    return addresses_page


@pytest.fixture
def dialog(addresses):
    district_dialog = addresses.open_create_district()
    yield district_dialog
    if district_dialog.cancel_button.is_visible():
        district_dialog.cancel()


@pytest.fixture
def district_name():
    return f"Автотест {int(time.time())}"


@pytest.fixture
def cleanup(addresses):
    names = []
    yield names
    dialog = DistrictDialog(addresses.page)
    if dialog.cancel_button.is_visible():
        dialog.cancel()
    for name in names:
        if addresses.row(name).count() > 0:
            addresses.delete_district(name)

@pytest.fixture
def district(addresses, district_name, cleanup):
    addresses.create_district(district_name)
    cleanup.append(district_name)
    return district_name

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            allure.attach(
                page.screenshot(),
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG,
            )


