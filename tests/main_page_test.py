from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import pytest
import time
from conftest import link


@pytest.fixture(scope="function")
def browser():
    from conftest import valid_email, valid_password
    browser = webdriver.Chrome()

    browser.get(link)

    input_loginEmail = browser.find_element_by_id("loginEmail")
    input_loginEmail.send_keys(valid_email)

    input_loginPassword = browser.find_element_by_id("loginPassword")
    input_loginPassword.send_keys(valid_password)

    button = browser.find_element_by_id("authButton")
    button.click()

    yield browser
    browser.quit()

@pytest.mark.main
class TestMainPage():

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_main_page_correct_work_with_all_choices(self, browser):

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


    @pytest.mark.smoke
    @pytest.mark.negative
    def test_main_page_not_correct_work_without_any_choices(self, browser):

        input_dataEmail = browser.find_element_by_id("dataEmail")
        input_dataEmail.send_keys("")

        input_dataName = browser.find_element_by_id("dataName")
        input_dataName.send_keys("")

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

        actual_message = browser.find_element_by_id("emailFormatError").text

        assert actual_message == "Неверный формат E-Mail"

    
    @pytest.mark.parametrize(
        ["email", "error_message"],
        [
            ("абвгдеёжз@иклмн.опрст", "Ввод данных на кириллице"),
            ("123@456.789", "Ввод цифр"),
            ("not_correct_test@ru", "Отсутствует ."),
            ("not_correct_test.ru", "Отсутствует @"),
            ("not_correct_test@.", "Отсутствует текст после @ и ."),
            (" not_correct_test_with_space@ poitey.ru", "Пробел в начале домена"),
            ("not_correct_test with_space@poitey .ru", "Пробел посередине домена перед ."),
            ("not_correct_test with_space@poitey. ru", "Пробел посередине домена после ."),
            ("not_correct_test_with_space@poitey.ru ", "Пробел в конце адреса"),
        ],
    )
    @pytest.mark.positive
    def test_main_page_correct_work_without_any_choices(self, browser, email, error_message):
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
            ("alex@.ru", "Отсутсвует текст после @ и до ."),
            ("alex@protei.", "Отсутсвует текст после ."),
        ],
    )
    @pytest.mark.negative
    def test_message_for_emailFormatError_without_any_choices(
        self, browser, email, error_message
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
    @pytest.mark.positive
    def test_correct_work_with_different_data_for_names_without_any_choices(
        self, browser, name, error_message
    ):

        input_dataEmail = browser.find_element_by_id("dataEmail")
        input_dataEmail.send_keys("alex@poitey.ru")

        input_dataName = browser.find_element_by_id("dataName")
        input_dataName.send_keys(name)

        button = browser.find_element_by_id("dataSend")
        button.click()

        alert = browser.find_element_by_class_name("uk-modal-content")
        alert_text = alert.text

        assert alert_text == "Данные добавлены.", error_message

    @pytest.mark.smoke
    @pytest.mark.negative
    def test_message_for_blankNameError_without_any_choices(self, browser):

        input_dataEmail = browser.find_element_by_id("dataEmail")
        input_dataEmail.send_keys("alex@poitey.ru")

        input_dataName = browser.find_element_by_id("dataName")
        input_dataName.send_keys("")

        button = browser.find_element_by_id("dataSend")
        button.click()

        actual_message = browser.find_element_by_id("blankNameError").text

        assert actual_message == "Поле имя не может быть пустым", "Пустая строка"

    
    @pytest.mark.parametrize(
        "email",
            ("@protei.ru", ""),
    )
    @pytest.mark.alert
    def test_close_message_window_after_error(self, browser, email):

        input_dataEmail = browser.find_element_by_id("dataEmail")
        input_dataEmail.send_keys("alex@poitey.ru")

        input_dataName = browser.find_element_by_id("dataName")
        input_dataName.send_keys(email)

        button = browser.find_element_by_id("dataSend")
        button.click()

        actual_message = browser.find_element_by_tag_name("a")

        actual_message.click()
        time.sleep(0.2)

        with pytest.raises(NoSuchElementException):
            actual_message = browser.find_element_by_tag_name("a")

            actual_message.click()

            pytest.fail("Поле с сообщением об ошибке должно быть скрыто")

        assert True

    @pytest.mark.alert
    def test_multiple_data_addition(self, browser):
        for _ in range(4):
            input_dataEmail = browser.find_element_by_id("dataEmail")
            input_dataEmail.send_keys("alex@poitey.ru")

            input_dataName = browser.find_element_by_id("dataName")
            input_dataName.send_keys("alex")

            button = browser.find_element_by_id("dataSend")
            button.click()

            alert = browser.find_element_by_class_name("uk-modal-close")
            alert.click()
            time.sleep(0.2)

            with pytest.raises(NoSuchElementException):
                actual_message = browser.find_element_by_class_name("uk-modal-close")

                actual_message.click()

                pytest.fail(
                    "Поле с сообщением об успешном добавлении данных должно быть скрыто"
                )

            assert True
