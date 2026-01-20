-- Categorias de produto com mais itens vendidos

-- Categorias com mais itens vendidos (pedidos entregues)
SELECT
  p.product_category_name,
  COUNT(oi.order_item_id) AS total_items_sold 
FROM order_items oi
JOIN orders o
  ON oi.order_id = o.order_id
JOIN products p
  ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_items_sold DESC
limit 10;

-- Tempo médio entre compra e entrega (em dias)
SELECT
  AVG(
    JULIANDAY(order_delivered_customer_date) -
    JULIANDAY(order_purchase_timestamp)
  ) AS avg_delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Tempo de entrega por pedido
SELECT
  order_id,
  (JULIANDAY(order_delivered_customer_date) -
   JULIANDAY(order_purchase_timestamp)) AS delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Receita total por estado
SELECT
  c.customer_state,
  SUM(p.payment_value) AS total_revenue
FROM orders o
JOIN customers c
  ON o.customer_id = c.customer_id
JOIN payments p
  ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

-- Ticket médio por pedido
SELECT
  AVG(order_total) AS avg_ticket
FROM (
  SELECT
    o.order_id,
    SUM(p.payment_value) AS order_total
  FROM orders o
  JOIN payments p
    ON o.order_id = p.order_id
  WHERE o.order_status = 'delivered'
  GROUP BY o.order_id
);

-- Produtos mais vendidos (itens entregues)
SELECT
  p.product_id,
  p.product_category_name,
  COUNT(oi.order_item_id) AS total_items_sold
FROM order_items oi
JOIN orders o
  ON oi.order_id = o.order_id
JOIN products p
  ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_id, p.product_category_name
ORDER BY total_items_sold DESC;
