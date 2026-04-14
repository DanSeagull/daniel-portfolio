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


SELECT 
    r.ride_id,
    r.final_price AS ride_price,
    p.amount AS payment_amount,
    ABS(r.final_price - p.amount) AS difference
FROM rides r
JOIN payments p ON r.ride_id = p.ride_id
WHERE ABS(r.final_price - p.amount) > 0.01  -- Допуск 1 копейка
  AND p.status = 'completed';


SELECT 
    ride_id, 
    driver_id, 
    start_time, 
    CURRENT_TIMESTAMP - start_time AS duration
FROM rides
WHERE status = 'driving'
  AND start_time < NOW() - INTERVAL '4 hours';


INSERT INTO test_users (phone, email, payment_method, status)
VALUES ('+79991234567', 'test.yandex@example.com', 'card', 'active')
ON CONFLICT (phone) DO NOTHING;


DELETE FROM rides WHERE user_id IN (SELECT user_id FROM test_users WHERE email = 'test.yandex@example.com');
