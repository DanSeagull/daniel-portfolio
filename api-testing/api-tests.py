"""
API автотесты для Яндекс Go (учебный проект)
"""

import requests
import pytest

BASE_URL = "https://test-api.yandex-go.ru/v1"
API_KEY = "***************"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Тестовые данные
test_ride = {
    "pickup": {"lat": 55.751244, "lon": 37.618423},
    "dropoff": {"lat": 55.755864, "lon": 37.617698},
    "tariff": "economy"
}


class TestTaxiAPI:
    
    def test_create_ride_success(self):  """API: Успешное создание заказа"""
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=test_ride,
            headers=HEADERS
        )
        assert response.status_code == 201
        data = response.json()
        assert "order_id" in data
        assert data["status"] == "pending"
    
    def test_create_ride_missing_pickup(self):  """API: Негативный тест — нет точки отправления"""
        invalid_ride = {"dropoff": test_ride["dropoff"]}
        response = requests.post(
            f"{BASE_URL}/orders/create",
            json=invalid_ride,
            headers=HEADERS
        )
        assert response.status_code == 400
        assert "pickup" in response.json()["error"]["field"]
    
    def test_cancel_ride(self): """API: Отмена созданного заказа"""
        
        # Сначала создаем заказ
        create_resp = requests.post(f"{BASE_URL}/orders/create", json=test_ride, headers=HEADERS)
        order_id = create_resp.json()["order_id"]
        
        # Отменяем
        cancel_resp = requests.post(
            f"{BASE_URL}/orders/{order_id}/cancel",
            headers=HEADERS
        )
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "cancelled"
    
    @pytest.mark.parametrize("tariff,expected_price_range", [
        ("economy", (150, 300)),
        ("comfort", (300, 500)),
        ("business", (800, 1500))
    ])
    def test_price_calculation(self, tariff, expected_price_range):  """API: Проверка расчета цены для разных тарифов"""
        ride_with_tariff = {**test_ride, "tariff": tariff}
        response = requests.post(
            f"{BASE_URL}/orders/price",
            json=ride_with_tariff,
            headers=HEADERS
        )
        assert response.status_code == 200
        price = response.json()["estimated_price"]
        assert expected_price_range[0] <= price <= expected_price_range[1]
