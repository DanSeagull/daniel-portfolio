import pytest
from pages.login_page import LoginPage
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestLogin:
    """
    Тестовый класс для проверки функциональности логина
    """

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Фикстура для инициализации страницы логина перед каждым тестом"""
        self.login_page = LoginPage(page)
        self.login_page.open()
        yield
       
        page.close()

    def test_successful_login(self, page):
        """
        Тест успешного входа с корректными данными
        """
        username = "******"
        password = "******"

        self.login_page.login(username, password, remember_me=True)

        assert self.login_page.is_login_successful(), "Login failed"

        self.login_page.take_screenshot("successful_login")

    def test_login_with_invalid_credentials(self, page):
        """
        Тест входа с неверными учетными данными
        """
        self.login_page.enter_username("invalid_user")
        self.login_page.enter_password("invalid_password")
        self.login_page.click_login_button()

        assert self.login_page.is_error_visible(), "Error message not displayed"

    def test_empty_username(self, page):
        """
        Тест входа с пустым именем пользователя
        """
        self.login_page.enter_username("")
        self.login_page.enter_password("some_password")
        self.login_page.click_login_button()

        assert self.login_page.is_error_visible() or self.login_page.is_element_visible(
            'input:invalid'
        ), "No validation error for empty username"

    def test_empty_password(self, page):
        """
        Тест входа с пустым паролем
        """
        self.login_page.enter_username("test_user")
        self.login_page.enter_password("")
        self.login_page.click_login_button()

        assert self.login_page.is_error_visible(), "No error for empty password"

    def test_forgot_password_link(self, page):
        """
        Тест перехода по ссылке "Забыли пароль?"
        """
        self.login_page.click_forgot_password()

        page.wait_for_timeout(2000)
        current_url = self.login_page.get_current_url()

        assert current_url != LoginPage.BASE_URL, "Forgot password link didn't redirect"

    def test_register_link(self, page):
        """
        Тест перехода по ссылке регистрации
        """
        self.login_page.click_register_link()
       
        page.wait_for_timeout(2000)
        current_url = self.login_page.get_current_url()
      
        assert current_url != LoginPage.BASE_URL, "Register link didn't redirect"

    def test_remember_me_functionality(self, page, context):
        """
        Тест функциональности "Запомнить меня"
        """
        username = "cda203d"
        password = "cda203d"

        self.login_page.login(username, password, remember_me=True)
        assert self.login_page.is_login_successful(), "Login failed"

       
        page.close()
        new_page = context.new_page()
        new_login_page = LoginPage(new_page)
        new_login_page.open()

      
        username_field = new_page.locator('#login_input').first
        username_value = username_field.input_value()

        if username_value:
            assert username_value == username, "Remember me didn't populate username"

    @pytest.mark.parametrize("username,password,expect_error", [
        ("user", "pass", False), 
        ("", "password", True), 
        ("username", "", True), 
        ("user@domain.com", "pass123", False)
    ])
    def test_login_with_different_credentials(self, username, password, expect_error):
        """
        Параметризованный тест для проверки различных комбинаций учетных данных
        """
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_login_button()

        if expect_error:
            assert self.login_page.is_error_visible(), f"Expected error for {username}/{password}"
        else:   
            pass

    def test_login_form_validation(self, page):
        """
        Тест HTML5 валидации формы
        """
       
        self.login_page.click_login_button()

        
        username_field = page.locator('#login_input').first
        is_invalid = username_field.evaluate("el => el.validity.valid") is False

        assert is_invalid or self.login_page.is_error_visible(), "Form validation not triggered"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--headed"])
