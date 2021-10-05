from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import pytest
from conftest import link


@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()

    browser.get(link)

    input_loginEmail = browser.find_element_by_id("loginEmail")
    input_loginEmail.send_keys("test@protei.ru")

    input_loginPassword = browser.find_element_by_id("loginPassword")
    input_loginPassword.send_keys("test")

    button = browser.find_element_by_id("authButton")
    button.click()

    yield browser
    browser.quit()


def test_main_page_correct_work_with_all_choices(browser):

    input_dataEmail = browser.find_element_by_id("dataEmail")
    input_dataEmail.send_keys("alex@poitey.ru")

    input_dataName = browser.find_element_by_id("dataName")
    input_dataName.send_keys("Alex")

    select = Select(browser.find_element_by_tag_name("select"))
    select.select_by_index(0)

    select = Select(browser.find_element_by_tag_name("select"))
    select.select_by_index(1)

    option1 = browser.find_element_by_id("dataCheck11")
    option1.click()

    option2 = browser.find_element_by_id("dataCheck12")
    option2.click()

    option3 = browser.find_element_by_id("dataSelect21")
    option3.click()

    option4 = browser.find_element_by_id("dataSelect22")
    option4.click()

    option5 = browser.find_element_by_id("dataSelect23")
    option5.click()

    button = browser.find_element_by_id("dataSend")
    button.click()

    alert = browser.find_element_by_class_name("uk-modal-content")
    alert_text = alert.text

    assert alert_text == "Данные добавлены."


@pytest.mark.parametrize(
    ["email", "error_message"],
    [
        ("alex@poitey.ru", "Ожидается корректная обработка данных"),
        ("абвгдеёжз@иклмн.опрст", "Ввод данных на кириллице"),
        ("123@456.789", "Ввод цифр"),
        ("not_correct_test@ru", "Отсутствует ."),
        ("not_correct_test@.", "Отсутствует текст после @ и ."),
        ("not_correct_test@poitey.", "Отсутствует текст после ."),
        ("not_correct_test@.ru", "Отсутствует текст после @"),
        ("not_correct_test_with space@ poitey.ru", "Пробел в начале домена"),
        ("not_correct_test with space@poitey .ru", "Пробел посередине домена перед ."),
        ("not_correct_test with space@poitey. ru", "Пробел посередине домена после ."),
        ("not_correct_test_with space@poitey.ru ", "Пробел в конце адреса"),
    ],
)
def test_main_page_correct_work_without_any_choices(browser, email, error_message):
    input_dataEmail = browser.find_element_by_id("dataEmail")
    input_dataEmail.send_keys(email)

    input_dataName = browser.find_element_by_id("dataName")
    input_dataName.send_keys("Alex")

    button = browser.find_element_by_id("dataSend")
    button.click()

    alert = browser.find_element_by_class_name("uk-modal-content")
    alert_text = alert.text

    assert alert_text == "Данные добавлены.", error_message


@pytest.mark.parametrize(
    ["email", "error_message"],
    [
        ("@protei.ru", "Отсутсвует текст до @ "),
        ("@.ru", "Отсутсвует текст до @ и до ."),
        ("@protei.", "Отсутсвует текст до @ и после ."),
    ],
)
def test_message_for_emailFormatError_without_any_choices(
    browser, email, error_message
):

    input_dataEmail = browser.find_element_by_id("dataEmail")
    input_dataEmail.send_keys(email)

    input_dataName = browser.find_element_by_id("dataName")
    input_dataName.send_keys("Alex")

    button = browser.find_element_by_id("dataSend")
    button.click()

    actual_message = browser.find_element_by_id("emailFormatError").text

    assert actual_message == "Неверный формат E-Mail", error_message


@pytest.mark.parametrize(
    ["name", "error_message"],
    [
        ("Иван", "Ввод данных на кириллице"),
        ("123", "Ввод цифр"),
        (".,?|/@", "Ввод знаков препинания"),
        (" Иван", "Пробел в начале имени"),
        ("Иван Иванов", "Пробел посередине имени"),
        ("Иван ", "Пробел в конце имени"),
        (" ", "Один проблел"),
    ],
)
def test_correct_work_with_different_data_for_names_without_any_choices(
    browser, name, error_message
):

    input_dataEmail = browser.find_element_by_id("dataEmail")
    input_dataEmail.send_keys("alex@poitey.ru")

    input_dataName = browser.find_element_by_id("dataName")
    input_dataName.send_keys(name)

    button = browser.find_element_by_id("dataSend")
    button.click()

    alert = browser.find_element_by_class_name("uk-modal-content")
    alert_text = alert.text

    assert alert_text == "Данные добавлены."


def test_message_for_blankNameError_without_any_choices(browser):

    input_dataEmail = browser.find_element_by_id("dataEmail")
    input_dataEmail.send_keys("alex@poitey.ru")

    input_dataName = browser.find_element_by_id("dataName")
    input_dataName.send_keys("")

    button = browser.find_element_by_id("dataSend")
    button.click()

    actual_message = browser.find_element_by_id("blankNameError").text

    assert actual_message == "Поле имя не может быть пустым", "Пустая строка"


def test_multiple_data_addition_without_any_choices(browser):
    for _ in range(5):
        input_dataEmail = browser.find_element_by_id("dataEmail")
        input_dataEmail.send_keys("alex@poitey.ru")

        input_dataName = browser.find_element_by_id("dataName")
        input_dataName.send_keys("alex")

        button = browser.find_element_by_id("dataSend")
        button.click()

        alert = browser.find_element_by_class_name("uk-modal-content")
        alert_text = alert.text

        assert alert_text == "Данные добавлены."
