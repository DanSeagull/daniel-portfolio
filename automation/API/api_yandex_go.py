import pytest
import requests
import json
import time
import uuid
from datetime import datetime

BASE_URL = "https://test-api.yandex-go.ru/v3"
API_KEY = "****************"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "X-Request-Id": str(uuid.uuid4())
}

# ========== ТЕСТОВЫЕ ДАННЫЕ ==========
TEST_USER = {
    "user_id": "test_qa_001",
    "phone": "+79991234567",
    "payment_method": "card"
}

TEST_RIDE = {
    "pickup": {"lat": 55.751244, "lon": 37.618423, "address": "Тверская 1"},
    "dropoff": {"lat": 55.755864, "lon": 37.617698, "address": "Кремль"},
    "tariff": "economy"
}

INVALID_RIDE = {
    "pickup": {"lat": 999, "lon": 999},  # Невалидные координаты
    "dropoff": {"lat": 55.755864, "lon": 37.617698}
}


#FIXTURES
@pytest.fixture
def created_order():
    """Создает заказ и возвращает его ID. Удаляет после теста."""
    response = requests.post(
        f"{BASE_URL}/orders/create",
        json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
        headers=HEADERS
    )
    assert response.status_code == 201
    order_id = response.json()["order_id"]
    yield order_id
    
    # Отменяем заказ после теста
    requests.post(f"{BASE_URL}/orders/{order_id}/cancel", headers=HEADERS)


# ПОЗИТИВНЫЕ ТЕСТЫ
class TestPositiveAPI:
    
    def test_create_order_success(self):
        """[API-001] Успешное создание заказа"""
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        assert response.status_code == 201
        data = response.json()
        assert "order_id" in data
        assert data["status"] == "pending"
        assert data["tariff"] == "economy"
        assert data["estimated_price"] > 0
    
    def test_get_order_status(self, created_order):
        """[API-002] Получение статуса заказа"""
        response = requests.get(
            f"{BASE_URL}/orders/{created_order}/status",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert data["order_id"] == created_order
        assert data["status"] in ["pending", "searching", "driver_assigned"]
    
    def test_cancel_order_success(self, created_order):
        """[API-003] Успешная отмена заказа"""
        response = requests.post(
            f"{BASE_URL}/orders/{created_order}/cancel",
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"
        assert "cancellation_reason" in data
    
    def test_get_available_tariffs(self):
        """[API-004] Получение списка доступных тарифов"""
        response = requests.get(
            f"{BASE_URL}/tariffs",
            params={"lat": TEST_RIDE["pickup"]["lat"], "lon": TEST_RIDE["pickup"]["lon"]},
            headers=HEADERS
        )
        assert response.status_code == 200
        tariffs = response.json()["tariffs"]
        assert len(tariffs) >= 3
        tariff_names = [t["name"] for t in tariffs]
        assert "economy" in tariff_names
        assert "comfort" in tariff_names
    
    def test_apply_promo_success(self):
        """[API-005] Успешное применение промокода"""
        response = requests.post(
            f"{BASE_URL}/promo/validate",
            json={"promo_code": "TEST50", "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == True
        assert data["discount_percent"] == 50
        assert data["max_discount"] == 500


# НЕГАТИВНЫЕ ТЕСТЫ
class TestNegativeAPI:
    
    def test_create_order_missing_pickup(self):
        """[API-101] Создание заказа без точки отправления"""
        invalid_data = {"dropoff": TEST_RIDE["dropoff"]}
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=invalid_data,
            headers=HEADERS
        )
        assert response.status_code == 400
        error = response.json()
        assert "pickup" in str(error).lower() or "required" in str(error).lower()
    
    def test_create_order_invalid_coordinates(self):
        """[API-102] Создание заказа с невалидными координатами"""
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=INVALID_RIDE,
            headers=HEADERS
        )
        assert response.status_code == 400
        assert "coordinates" in response.json().get("error", "").lower()
    
    def test_cancel_already_cancelled_order(self):
        """[API-103] Отмена уже отмененного заказа"""
        # Создаем заказ
        create_resp = requests.post(
            f"{BASE_URL}/orders/create",
            json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        order_id = create_resp.json()["order_id"]
        
        # Отменяем первый раз
        requests.post(f"{BASE_URL}/orders/{order_id}/cancel", headers=HEADERS)
        
        # Отменяем второй раз
        response = requests.post(f"{BASE_URL}/orders/{order_id}/cancel", headers=HEADERS)
        assert response.status_code == 400
        assert "already cancelled" in response.json().get("message", "").lower()
    
    def test_invalid_promo_code(self):
        """[API-104] Невалидный промокод"""
        response = requests.post(
            f"{BASE_URL}/promo/validate",
            json={"promo_code": "INVALID123", "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        assert response.status_code == 200  # или 404 в зависимости от API
        data = response.json()
        assert data["valid"] == False
        assert "invalid" in data.get("reason", "").lower()
    
    def test_expired_promo_code(self):
        """[API-105] Просроченный промокод"""
        response = requests.post(
            f"{BASE_URL}/promo/validate",
            json={"promo_code": "EXPIRED2023", "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == False
        assert "expired" in data.get("reason", "").lower()
    
    def test_create_order_unauthorized(self):
        """[API-106] Создание заказа без авторизации"""
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=TEST_RIDE
            # Без заголовка Authorization
        )
        assert response.status_code == 401
        assert "unauthorized" in response.json().get("error", "").lower()


# ТЕСТЫ НА ГРАНИЧНЫЕ ЗНАЧЕНИЯ
class TestBoundaryAPI:
    
    @pytest.mark.parametrize("comment,should_pass", [
        ("", True),                                    # Пустой комментарий
        ("A" * 10, True),                              # Короткий
        ("A" * 255, True),                             # Максимальная длина
        ("A" * 256, False),                            # Превышение лимита
        ("🚗🚕🚙 Привет 🚲🛴", True),                  # С эмодзи (если поддерживается)
        ("<script>alert('xss')</script>", True),      # XSS попытка
    ])
    def test_comment_field_boundaries(self, comment, should_pass):
        """[API-201] Тестирование поля comment: граничные значения"""
        ride_with_comment = {**TEST_RIDE, "comment": comment}
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json={**ride_with_comment, "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        
        if should_pass:
            assert response.status_code == 201
        else:
            assert response.status_code == 400
    
    @pytest.mark.parametrize("lat,lon,expected_status", [
        (55.751244, 37.618423, 201),      # Валидные координаты
        (90.0, 180.0, 201),               # Максимальные допустимые
        (-90.0, -180.0, 201),             # Минимальные допустимые
        (91.0, 0.0, 400),                 # Широта за пределами
        (0.0, 181.0, 400),                # Долгота за пределами
        (999.0, 999.0, 400),              # Полный мусор
    ])
    def test_coordinates_boundaries(self, lat, lon, expected_status):
        """[API-202] Тестирование граничных значений координат"""
        ride_with_coords = {
            "pickup": {"lat": lat, "lon": lon},
            "dropoff": TEST_RIDE["dropoff"],
            "user_id": TEST_USER["user_id"]
        }
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=ride_with_coords,
            headers=HEADERS
        )
        assert response.status_code == expected_status


# ТЕСТЫ НА ИДЕМПОТЕНТНОСТЬ
class TestIdempotencyAPI:
    
    def test_same_request_idempotent(self):
        """[API-301] Повторный запрос с тем же ID не создает дубликат"""
        request_id = str(uuid.uuid4())
        headers_with_id = {**HEADERS, "X-Idempotency-Key": request_id}
        
        # Первый запрос
        resp1 = requests.post(
            f"{BASE_URL}/orders/create",
            json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
            headers=headers_with_id
        )
        order_id_1 = resp1.json()["order_id"]
        
        # Второй запрос (такой же)
        resp2 = requests.post(
            f"{BASE_URL}/orders/create",
            json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
            headers=headers_with_id
        )
        order_id_2 = resp2.json()["order_id"]
        
        # Должен вернуть тот же заказ, а не создавать новый
        assert order_id_1 == order_id_2
        assert resp2.status_code == 200  # Обычно 200 при повторном запросе


# ТЕСТЫ НА ВРЕМЯ
class TestTimingAPI:
    
    def test_price_calculation_response_time(self):
        """[API-401] Время ответа API расчета цены < 500ms"""
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/orders/price",
            json=TEST_RIDE,
            headers=HEADERS
        )
        elapsed = (time.time() - start) * 1000
        assert elapsed < 500, f"Response time: {elapsed}ms > 500ms"
        assert response.status_code == 200
    
    def test_order_status_websocket_timeout(self):
        """[API-402] Статус заказа обновляется не позже чем через 5 секунд"""
        # Создаем заказ
        create_resp = requests.post(
            f"{BASE_URL}/orders/create",
            json={**TEST_RIDE, "user_id": TEST_USER["user_id"]},
            headers=HEADERS
        )
        order_id = create_resp.json()["order_id"]
        
        # Ждем обновления статуса
        max_wait = 5  # секунд
        start = time.time()
        status = "pending"
        
        while time.time() - start < max_wait:
            resp = requests.get(f"{BASE_URL}/orders/{order_id}/status", headers=HEADERS)
            status = resp.json()["status"]
            if status != "pending":
                break
            time.sleep(0.5)
        
        assert status != "pending", f"Status didn't change within {max_wait} seconds"


# ЗАПУСК
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
