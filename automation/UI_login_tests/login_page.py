from pages.base_page import BasePage
from playwright.sync_api import Page
import logging


class LoginPage(BasePage):
    """
    Класс страницы авторизации
    """

    BASE_URL = "https://refactoring.dev.baionline.ru/points"

    LOCATORS = {
        'username_input': '#login_input',
        'password_input': 'input[type="password"]',
        'remember_me_checkbox': 'input[type="checkbox"]:visible',
        'forgot_password_link': 'a:has-text("Забыли пароль")',
        'login_button': 'button:has-text("Войти"), button[type="submit"]',
        'register_link': 'a:has-text("Зарегистрируйтесь")',
        'error_message': '//*[@id="baionline-root"]/div/div[2]/div[2]/form/div[2]/div',
        'success_element': '.dashboard, .MuiContainer-root, [role="main"]'
    }

    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(__name__)

    def open(self):
        """Открытие страницы логина"""
        self.logger.info("Opening login page")
        self.navigate(self.BASE_URL)
        self.wait_for_login_form()

    def wait_for_login_form(self, timeout: int = 15000):
        """Ожидание загрузки формы логина"""
        self.logger.info("Waiting for login form to load")
        self.wait_for_element('#login_input', timeout)
        self.wait_for_element('input[type="password"]', timeout)
        self.wait_for_element(self.LOCATORS['login_button'], timeout)

    def enter_username(self, username: str):
        """Ввод имени пользователя"""
        self.logger.info(f"Entering username: {username}")
        username_field = self.page.locator('#login_input').first
        username_field.scroll_into_view_if_needed()
        username_field.click()
        username_field.clear()
        username_field.fill(username)
        username_field.press("Tab")
        self.page.wait_for_timeout(500)  # Даем время на обработку

    def enter_password(self, password: str):
        """Ввод пароля"""
        self.logger.info("Entering password")
        password_field = self.page.locator('input[type="password"]').first
        password_field.scroll_into_view_if_needed()
        password_field.click()
        password_field.clear()
        password_field.fill(password)
        password_field.press("Tab")
        self.page.wait_for_timeout(500)

    def click_login_button(self):
        """Нажатие кнопки 'Войти'"""
        self.logger.info("Clicking login button")
        button = self.page.locator(self.LOCATORS['login_button']).first

        # Ждем, пока кнопка станет активной
        try:
            self.page.wait_for_function(
                """button => !button.disabled""",
                arg=button,
                timeout=10000
            )
            self.logger.info("✓ Button is enabled")
        except:
            self.logger.warning("Button may still be disabled")

        button.click()
        self.logger.info("✓ Button clicked")
        # Ждем ответа от сервера
        self.page.wait_for_timeout(3000)

    def login(self, username: str, password: str, remember_me: bool = False):
        """Полный процесс логина"""
        self.logger.info(f"Logging in as: {username}")
        self.enter_username(username)
        self.enter_password(password)
        if remember_me:
            checkbox = self.page.locator(self.LOCATORS['remember_me_checkbox']).first
            if checkbox.count() > 0:
                checkbox.check()
        self.click_login_button()

    def is_login_successful(self) -> bool:
        """
        Проверка успешности входа для SPA (URL не меняется)
        """
        self.logger.info("Checking if login was successful")

        # Ждем ответа от сервера
        self.page.wait_for_timeout(1000)

        # Если есть сообщение об ошибке - вход не удался
        if self.is_error_visible():
            error_text = self.get_error_message()
            self.logger.info(f"Error message: {error_text}")
            return False

        # Если форма логина исчезла или появились новые элементы - успех
        if not self.is_element_visible('#login_input'):
            self.logger.info("Login form disappeared - successful")
            return True

        # Проверяем наличие элементов дашборда
        success_selectors = [
            '.dashboard',
            '.MuiContainer-root',
            '[role="main"]',
            '.user-menu',
            '.profile'
        ]

        for selector in success_selectors:
            if self.is_element_visible(selector):
                self.logger.info(f"✅ Found success element: {selector}")
                return True

        self.logger.warning("No success indicators found")
        return False

    def is_error_visible(self) -> bool:
        """Проверка видимости сообщения об ошибке"""
        return self.is_element_visible(self.LOCATORS['error_message'])

    def get_error_message(self) -> str:
        """Получение текста сообщения об ошибке"""
        alert = self.page.locator(self.LOCATORS['error_message']).first
        if alert.count() > 0:
            return alert.text_content() or ""
        return ""

    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.page.url

    def is_element_visible(self, selector: str) -> bool:
        """Проверка видимости элемента"""
        try:
            return self.page.is_visible(selector)
        except:
            return False

    def click_forgot_password(self):
        """Нажатие на ссылку 'Забыли пароль?'"""
        link = self.page.locator(self.LOCATORS['forgot_password_link']).first
        if link.count() > 0:
            link.click()

    def click_register_link(self):
        """Нажатие на ссылку регистрации"""
        link = self.page.locator(self.LOCATORS['register_link']).first
        if link.count() > 0:
            link.click()

    def check_remember_me(self, check: bool = True):
        """Установка/снятие чекбокса 'Запомнить меня'"""
        checkbox = self.page.locator(self.LOCATORS['remember_me_checkbox']).first
        if checkbox.count() > 0:
            if check != checkbox.is_checked():
                checkbox.check()
