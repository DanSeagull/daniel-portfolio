-- =============================================
-- SQL-запросы для проверки целостности поездок
-- Проект: Яндекс Go (тестирование дублей)
-- Автор: Fullstack тестировщик
-- =============================================

-- 1. Поиск дубликатов поездок (один пользователь, одинаковое время)
-- Ситуация: Баг, когда при плохом интернете кнопка "Заказать" отправляет 2 запроса
SELECT 
    user_id, 
    created_at, 
    pickup_address, 
    dropoff_address,
    COUNT(*) AS duplicate_count
FROM rides
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY user_id, created_at, pickup_address, dropoff_address
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- 2. Проверка, что сумма списания = сумме поездки (нет лишних комиссий)
SELECT 
    r.ride_id,
    r.final_price AS ride_price,
    p.amount AS payment_amount,
    ABS(r.final_price - p.amount) AS difference
FROM rides r
JOIN payments p ON r.ride_id = p.ride_id
WHERE ABS(r.final_price - p.amount) > 0.01  -- Допуск 1 копейка
  AND p.status = 'completed';

-- 3. Найти поездки без завершения (status = 'driving' дольше 4 часов)
-- Ожидается: не более 0.01% от всех поездок
SELECT 
    ride_id, 
    driver_id, 
    start_time, 
    CURRENT_TIMESTAMP - start_time AS duration
FROM rides
WHERE status = 'driving'
  AND start_time < NOW() - INTERVAL '4 hours';

-- 4. Вставить тестового пользователя для ручного тестирования
INSERT INTO test_users (phone, email, payment_method, status)
VALUES ('+79991234567', 'test.yandex@example.com', 'card', 'active')
ON CONFLICT (phone) DO NOTHING;

-- 5. Очистка тестовых данных после прогона
DELETE FROM rides WHERE user_id IN (SELECT user_id FROM test_users WHERE email = 'test.yandex@example.com');
