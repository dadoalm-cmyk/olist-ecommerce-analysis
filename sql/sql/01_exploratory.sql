-- Visão geral do banco Olist

-- Total de pedidos
SELECT COUNT(*) AS total_orders FROM orders;

-- Total de clientes únicos
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM customers;

-- Total de produtos
SELECT COUNT(*) AS total_products FROM products;



-- Distribuição de status dos pedidos
SELECT 
    order_status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- Distribuição de Clientes por Estado
SELECT COUNT(*) AS total_customers, 
    customer_state
    from customers
    GROUP BY customer_state 
    ORDER BY total_customers  DESC;

-- Clientes "reais" e o total de registros
SELECT
  COUNT(DISTINCT customer_unique_id) AS clientes_reais,
  COUNT(*) AS registros
FROM customers;
