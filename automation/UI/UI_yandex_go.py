import pytest
from playwright.sync_api import Page, expect, sync_playwright
import time


@pytest.fixture
def mobile_page():
    """Настройка эмуляции мобильного устройства"""
    with sync_playwright() as p:
        iphone_13 = p.devices['iPhone 13']
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            **iphone_13,
            locale='ru-RU',
            geolocation={'latitude': 55.751244, 'longitude': 37.618423},
            permissions=['geolocation']
        )
        page = context.new_page()
        yield page
        browser.close()


# UI ТЕСТЫ
class TestYandexGoUI:
    
    def test_main_screen_loads(self, mobile_page):
        """[UI-001] Главный экран загружается корректно"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Проверяем, что карта отображается
        expect(mobile_page.locator('[data-testid="map-canvas"]')).to_be_visible()
        
        # Проверяем, что поле "Откуда" отображается
        expect(mobile_page.locator('[data-testid="pickup-input"]')).to_be_visible()
        
        # Проверяем, что поле "Куда" отображается
        expect(mobile_page.locator('[data-testid="dropoff-input"]')).to_be_visible()
    
    def test_pickup_autodetect(self, mobile_page):
        """[UI-002] Автоопределение текущего адреса"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Кликаем на поле "Откуда"
        mobile_page.click('[data-testid="pickup-input"]')
        
        # Нажимаем кнопку "Определить"
        mobile_page.click('[data-testid="detect-location-btn"]')
        
        # Ждем, пока адрес определится
        mobile_page.wait_for_selector('[data-testid="pickup-suggestion"]', timeout=10000)
        
        # Проверяем, что адрес не пустой
        pickup_value = mobile_page.input_value('[data-testid="pickup-input"]')
        assert len(pickup_value) > 5, f"Pickup address is too short: {pickup_value}"
    
    def test_full_booking_flow(self, mobile_page):
        """[UI-003] Полный сценарий вызова такси"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Ввод адреса отправления
        mobile_page.click('[data-testid="pickup-input"]')
        mobile_page.fill('[data-testid="pickup-input"]', "Тверская 1")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        # Ввод адреса назначения
        mobile_page.click('[data-testid="dropoff-input"]')
        mobile_page.fill('[data-testid="dropoff-input"]', "Кремль")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        # Выбор тарифа
        mobile_page.click('[data-testid="tariff-selector"]')
        mobile_page.click('[data-testid="tariff-comfort"]')
        
        # Нажатие кнопки заказа
        mobile_page.click('[data-testid="order-button"]')
        
        # Ожидание появления карточки водителя
        expect(mobile_page.locator('[data-testid="driver-card"]')).to_be_visible(timeout=15000)
        
        # Проверка, что статус не ошибка
        status = mobile_page.text_content('[data-testid="order-status"]')
        assert "ошибк" not in status.lower(), f"Error in status: {status}"
    
    def test_tariff_switch_during_search(self, mobile_page):
        """[UI-004] Смена тарифа во время поиска водителя"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Ввод адресов
        mobile_page.fill('[data-testid="pickup-input"]', "Тверская 1")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        mobile_page.fill('[data-testid="dropoff-input"]', "Кремль")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        # Начинаем поиск
        mobile_page.click('[data-testid="order-button"]')
        
        # Ждем статуса "Ищем"
        mobile_page.wait_for_selector('[data-testid="searching-status"]', timeout=5000)
        
        # Меняем тариф
        mobile_page.click('[data-testid="change-tariff-btn"]')
        mobile_page.click('[data-testid="tariff-business"]')
        
        # Проверяем, что цена обновилась
        price_element = mobile_page.locator('[data-testid="current-price"]')
        price_text = price_element.text_content()
        assert "₽" in price_text
    
    def test_cancel_order(self, mobile_page):
        """[UI-005] Отмена заказа"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Ввод адресов и заказ
        mobile_page.fill('[data-testid="pickup-input"]', "Тверская 1")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        mobile_page.fill('[data-testid="dropoff-input"]', "Кремль")
        mobile_page.keyboard.press("Enter")
        mobile_page.click('[data-testid="suggestion-0"]')
        
        mobile_page.click('[data-testid="order-button"]')
        
        # Ждем появления кнопки отмены
        mobile_page.wait_for_selector('[data-testid="cancel-button"]', timeout=10000)
        
        # Отменяем заказ
        mobile_page.click('[data-testid="cancel-button"]')
        
        # Подтверждаем отмену
        mobile_page.click('[data-testid="confirm-cancel"]')
        
        # Проверяем, что вернулись на главный экран
        expect(mobile_page.locator('[data-testid="pickup-input"]')).to_be_visible()
    
    def test_alice_voice_input(self, mobile_page):
        """[UI-006] Голосовой ввод через Алису"""
        mobile_page.goto("https://test.go.yandex/")
        
        # Нажатие на микрофон
        mobile_page.click('[data-testid="voice-input-btn"]')
        
       
        # Здесь эмулируем успешное распознавание
        mobile_page.wait_for_selector('[data-testid="voice-recognized-text"]', timeout=5000)
        
        recognized_text = mobile_page.text_content('[data-testid="voice-recognized-text"]')
        assert len(recognized_text) > 0
    
    @pytest.mark.parametrize("tariff,expected_color", [
        ("economy", "green"),
        ("comfort", "blue"),
        ("business", "black")
    ])
    def test_tariff_color_coding(self, mobile_page, tariff, expected_color):
        """[UI-007] Цветовое кодирование тарифов"""
        mobile_page.goto("https://test.go.yandex/")
        
        mobile_page.click('[data-testid="tariff-selector"]')
        mobile_page.click(f'[data-testid="tariff-{tariff}"]')
        
        # Проверяем цвет выбранного тарифа
        tariff_element = mobile_page.locator(f'[data-testid="selected-tar
