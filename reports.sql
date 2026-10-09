```sql
-- ============================================================
-- TASK 3 — REPORTS
-- Mamaearth Returns & Growth Intelligence Pipeline
-- Raw / uncleaned SQL data
-- ============================================================


-- ============================================================
-- a) ORDER TOTALS
-- COUNT(*), total revenue, and average order value
-- ============================================================

-- Expected Output:
-- total_orders | total_revenue | average_order_value
-- 180          | 99860.20      | 554.78

SELECT
    COUNT(*) AS total_orders,
    ROUND(
        SUM(
            quantity * price *
            (1 - COALESCE(discount_pct, 0) / 100)
        ), 2
    ) AS total_revenue,
    ROUND(
        AVG(
            quantity * price *
            (1 - COALESCE(discount_pct, 0) / 100)
        ), 2
    ) AS average_order_value
FROM orders
JOIN products
    ON orders.product_id = products.product_id;


-- ============================================================
-- b) COUNT(*) VS COUNT(rating)
-- ============================================================

-- Expected Output:
-- total_orders | rated_orders | missing_ratings
-- 180          | 165          | 15

SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS rated_orders,
    COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;


-- ============================================================
-- c) ZERO-ORDER CUSTOMER
-- Method 1: LEFT JOIN + HAVING
-- ============================================================

-- Expected Output:
-- customer_id | name
-- C045        | Vihaan

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.name
HAVING COUNT(o.order_id) = 0;


-- ============================================================
-- c) ZERO-ORDER CUSTOMER
-- Method 2: NOT IN
-- ============================================================

-- Expected Output:
-- customer_id | name
-- C045        | Vihaan

SELECT
    customer_id,
    name
FROM customers
WHERE customer_id NOT IN (
    SELECT customer_id
    FROM orders
);


-- ============================================================
-- d) CITY RETURN RATES > 20%
-- ============================================================

-- Expected Output:
-- city      | total_orders | returned_orders | return_rate_pct
-- Jaipur    | 19           | 8               | 42.1
-- Lucknow   | 49           | 15              | 30.6
-- Bangalore | 33           | 8               | 24.2

SELECT
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(100 * AVG(o.returned), 1) AS return_rate_pct
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.city
HAVING ROUND(100 * AVG(o.returned), 1) > 20
ORDER BY return_rate_pct DESC;


-- ============================================================
-- e) TOP 5 SPENDERS
-- ============================================================

-- Expected Output:
-- customer_id | name    | total_spend
-- C043        | Reyansh | 12920.00
-- C026        | Isha    | 8371.60
-- C008        | Meera   | 4564.60
-- C011        | Arjun   | 4111.00
-- C042        | Sanya   | 3785.00

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_spend DESC
LIMIT 5;


-- ============================================================
-- e) RANKS 3–5 USING LIMIT 3 OFFSET 2
-- ============================================================

-- Expected Output:
-- customer_id | name   | total_spend
-- C008        | Meera  | 4564.60
-- C011        | Arjun  | 4111.00
-- C042        | Sanya  | 3785.00

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_spend
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    c.customer_id,
    c.name
ORDER BY total_spend DESC
LIMIT 3 OFFSET 2;


-- ============================================================
-- f) CATEGORY-WISE ORDER COUNT AND REVENUE
-- ============================================================

-- Expected Output:
-- category     | order_count | total_revenue
-- Haircare     | 54          | 44956.10
-- Skincare     | 60          | 27346.00
-- Babycare     | 30          | 16805.00
-- PersonalCare | 36          | 10753.10

SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100)
        ), 2
    ) AS total_revenue
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- ============================================================
-- g) CUSTOMERS WHOSE NAME STARTS WITH 'A'
-- ============================================================

-- Expected Output:
-- Aarav
-- Aditi
-- Ananya
-- Arjun
-- Aryan
-- Aditya
-- Anika
-- Aisha
-- Ayaan
-- Aria
--
-- Total rows: 10

SELECT
    name
FROM customers
WHERE name LIKE 'A%'
ORDER BY name;


-- ============================================================
-- h) DISTINCT ACQUISITION SOURCES
-- ============================================================

-- Expected Output:
-- acquisition_source
-- Ad
-- Organic
-- Referral
-- Social

SELECT DISTINCT
    acquisition_source
FROM customers
ORDER BY acquisition_source;


-- ============================================================
-- i) ADD LOYALTY TIER
-- ============================================================

-- Add the loyalty_tier column.

ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);


-- Update loyalty tier:
-- City Tier 1 = Gold
-- Everything else = Silver

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;


-- ============================================================
-- i) VERIFY LOYALTY TIER COUNTS
-- ============================================================

-- Expected Output:
-- loyalty_tier | customer_count
-- Gold         | 28
-- Silver       | 17

SELECT
    loyalty_tier,
    COUNT(*) AS customer_count
FROM customers
GROUP BY loyalty_tier
ORDER BY loyalty_tier DESC;
```
