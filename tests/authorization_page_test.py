from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pytest
import time
from conftest import link


@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

@pytest.mark.authorization
class TestAuthorizationPage():

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_correct_input_for_authorization_page(self, browser):
        from conftest import valid_email, valid_password

        browser.get(link)

        input_loginEmail = browser.find_element_by_id("loginEmail")
        input_loginEmail.send_keys(valid_email)

        input_loginPassword = browser.find_element_by_id("loginPassword")
        input_loginPassword.send_keys(valid_password)

        button = browser.find_element_by_id("authButton")
        button.click()

        authPage = browser.find_element_by_id("authPage")
        assert authPage.get_attribute("style") == "display: none;", f"!!!!!!!!\tlink:{link}"


    @pytest.mark.smoke
    @pytest.mark.negative
    def test_not_correct_authorization_page(self, browser):
        browser.get(link)

        input_loginEmail = browser.find_element_by_id("loginEmail")
        input_loginEmail.send_keys("not_correct_test@protei.ru")

        input_loginPassword = browser.find_element_by_id("loginPassword")
        input_loginPassword.send_keys("not_correct_test")

        button = browser.find_element_by_id("authButton")
        button.click()

        authPage = browser.find_element_by_id("authPage")
        assert authPage.get_attribute("style") == ""


    @pytest.mark.negative
    @pytest.mark.parametrize(
        ["email", "error_message"],
        [
            ("not_correct_test@poitey.ru", "Не логин из списка доступных для входа"),
            ("not_correct_test@ru", "Отсутствует ."),
            ("not_correct_test@.", "Отсутствует текст после @ и ."),
            ("not_correct_test@poitey.", "Отсутствует текст после ."),
            ("not_correct_test@.ru", "Отсутствует текст после @"),
        ],
    )
    def test_message_for_invalidEmailPassword(self, browser, email, error_message):
        browser.get(link)

        input_loginEmail = browser.find_element_by_id("loginEmail")
        input_loginEmail.send_keys(email)

        input_loginPassword = browser.find_element_by_id("loginPassword")
        input_loginPassword.send_keys("test")

        button = browser.find_element_by_id("authButton")
        button.click()

        actual_message = browser.find_element_by_id("invalidEmailPassword").text

        assert actual_message == "Неверный E-Mail или пароль", error_message


    @pytest.mark.negative
    @pytest.mark.parametrize(
        ["email", "error_message"],
        [
            ("not_correct_test", "Отсутствует @ и."),
            ("not_correct_test.ru", "Отсутствует @ "),
            ("@.", "Отсутствует текст"),
            ("", "Пустая строка"),
        ],
    )
    def test_message_for_emailFormatError(self, browser, email, error_message):
        browser.get(link)

        input_loginEmail = browser.find_element_by_id("loginEmail")
        input_loginEmail.send_keys(email)

        input_loginPassword = browser.find_element_by_id("loginPassword")
        input_loginPassword.send_keys("test")

        button = browser.find_element_by_id("authButton")
        button.click()

        actual_message = browser.find_element_by_id("emailFormatError").text

        assert actual_message == "Неверный формат E-Mail", error_message


    @pytest.mark.alert
    @pytest.mark.parametrize(
        "email",
        [
            "not_correct_test@protei.ru",
            "not_correct_test",
        ],
    )
    def test_close_message_window_after_error(self, browser, email):
        browser.get(link)

        input_loginEmail = browser.find_element_by_id("loginEmail")
        input_loginEmail.send_keys(email)

        input_loginPassword = browser.find_element_by_id("loginPassword")
        input_loginPassword.send_keys("test")

        button = browser.find_element_by_id("authButton")
        button.click()

        actual_message = browser.find_element_by_tag_name("a")

        actual_message.click()
        time.sleep(0.2)

        with pytest.raises(NoSuchElementException):
            actual_message = browser.find_element_by_tag_name("a")

            actual_message.click()

            pytest.fail("Поле с сообщением об ошибке должно быть скрыто")

        assert True
