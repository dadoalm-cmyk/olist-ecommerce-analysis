import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "olist.db"

# Conexão
conn = sqlite3.connect(DB_PATH)
query = """
SELECT
    p.product_category_name,
    COUNT(*) AS total_items_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_items_sold DESC
LIMIT 10;
"""

df_top_categories = pd.read_sql_query(query, conn)
print(df_top_categories)



plt.figure()
plt.barh(
    df_top_categories["product_category_name"],
    df_top_categories["total_items_sold"]
)
plt.xlabel("Quantidade vendida")
plt.ylabel("Categoria")
plt.title("Top 10 categorias mais vendidas")
plt.gca().invert_yaxis()
plt.show()


query = """
SELECT
    JULIANDAY(order_delivered_customer_date) -
    JULIANDAY(order_purchase_timestamp) AS delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;
"""

df_delivery = pd.read_sql_query(query, conn)

print(df_delivery.describe())

plt.figure()
plt.hist(df_delivery["delivery_days"], bins=30)
plt.xlabel("Dias para entrega")
plt.ylabel("Quantidade de pedidos")
plt.title("Distribuição do tempo de entrega")
plt.show()


query = """
SELECT
    c.customer_state,
    SUM(oi.price) AS total_revenue
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_revenue DESC;
"""

df_revenue_state = pd.read_sql_query(query, conn)
print(df_revenue_state.head())


top_states = df_revenue_state.head(10)

plt.figure()
plt.bar(
    top_states["customer_state"],
    top_states["total_revenue"]
)
plt.xlabel("Estado")
plt.ylabel("Receita total (R$)")
plt.title("Top 10 estados por receita")
plt.show()


# ============================
# TICKET MÉDIO POR PEDIDO
# ============================

query = """
SELECT
    order_id,
    SUM(price) AS order_total
FROM order_items
GROUP BY order_id;
"""

df_orders = pd.read_sql_query(query, conn)

ticket_medio = df_orders["order_total"].mean()

print(f"Ticket médio por pedido: R$ {ticket_medio:.2f}")


# ============================
# CLIENTES RECORRENTES 
# ============================
# Clientes que realizaram mais de uma compra Métrica usada para avaliar retenção básica


query = """
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id;
"""


df_customers = pd.read_sql_query(query, conn)

total_customers = len(df_customers)
recurring_customers = df_customers[df_customers["total_orders"] > 1]

recurrence_rate = len(recurring_customers) / total_customers * 100

print(f"Clientes recorrentes: {recurrence_rate:.2f}%")






# ============================
# TEMPO DE COMPRA
# ============================

query = """
SELECT
    c.customer_unique_id,
    o.order_purchase_timestamp
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY c.customer_unique_id, o.order_purchase_timestamp;
"""

df_purchases = pd.read_sql_query(query, conn)

# Converter para datetime
df_purchases["order_purchase_timestamp"] = pd.to_datetime(
    df_purchases["order_purchase_timestamp"]
)

# Diferença entre compras do mesmo cliente
df_purchases["days_since_last_purchase"] = (
    df_purchases
    .groupby("customer_unique_id")["order_purchase_timestamp"]
    .diff()
    .dt.days
)

# Remover primeira compra (NaN)
df_repurchase_time = df_purchases.dropna()

print(df_repurchase_time["days_since_last_purchase"].describe())

plt.figure()
plt.hist(df_repurchase_time["days_since_last_purchase"], bins=30)
plt.xlabel("Dias entre compras")
plt.ylabel("Quantidade de clientes")
plt.title("Tempo entre compras (recompra)")
plt.show()



# ============================
# LIFETIME VALUE (LTV)
# ============================


query = """
SELECT
    o.order_id,
    SUM(oi.price) AS order_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id;
"""

df_orders = pd.read_sql_query(query, conn)

ticket_medio = df_orders["order_revenue"].mean()
print(f"Ticket médio: R$ {ticket_medio:.2f}")

query = """
SELECT
    c.customer_unique_id,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id;
"""

df_frequency = pd.read_sql_query(query, conn)

frequencia_media = df_frequency["total_orders"].mean()
print(f"Frequência média de compra: {frequencia_media:.2f}")

ltv = ticket_medio * frequencia_media
print(f"LTV médio estimado: R$ {ltv:.2f}")

# ============================
# ANÁLISE DE COORTES
# ============================

query = """
SELECT
    c.customer_unique_id,
    MIN(o.order_purchase_timestamp) AS first_purchase_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_unique_id;
"""
df_first_purchase = pd.read_sql_query(query, conn)
df_first_purchase["first_purchase_date"] = pd.to_datetime(
    df_first_purchase["first_purchase_date"]
)
query = """
SELECT
    c.customer_unique_id,
    o.order_purchase_timestamp
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
"""
df_orders = pd.read_sql_query(query, conn)
df_orders["order_purchase_timestamp"] = pd.to_datetime(
    df_orders["order_purchase_timestamp"]
)

df_orders = df_orders.merge(
    df_first_purchase,
    on="customer_unique_id",
    how="left"
)

df_orders["cohort_month"] = (
    df_orders["first_purchase_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

df_orders["order_month"] = (
    df_orders["order_purchase_timestamp"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

df_orders["cohort_index"] = (
    (df_orders["order_month"].dt.year - df_orders["cohort_month"].dt.year) * 12 +
    (df_orders["order_month"].dt.month - df_orders["cohort_month"].dt.month)
)

cohort_data = (
    df_orders
    .groupby(["cohort_month", "cohort_index"])["customer_unique_id"]
    .nunique()
    .reset_index()
)

cohort_pivot = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="customer_unique_id"
)

cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0)

print(retention_matrix.head())




_ = plt.subplots(figsize = (12,8))

_= sns.heatmap(
    data = retention_matrix,
    mask = retention_matrix.isnull(),
    annot = True,
    fmt = '.0%',
    cmap = 'RdYlGn'
)

plt.title("Matriz de Retenção", size=14)
plt.xlabel("Meses desde a primeira compra")
plt.ylabel("Mês da primeira compra")

plt.show()

# ============================
# ANÁLISE DE CHURN
# ============================


churn_threshold = 90
df_repurchase_time["churn"] = (
    df_repurchase_time["days_since_last_purchase"] > churn_threshold
)
churn_rate = df_repurchase_time["churn"].mean()
print(f"Taxa de churn (90 dias): {churn_rate:.2%}")

# ============================
# CHURN POR SEGMENTO
# ============================

# CHURN POR ESTADO

query = """
SELECT
    c.customer_unique_id,
    c.customer_state,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id, c.customer_state;
"""
df_customer_orders = pd.read_sql_query(query, conn)

df_customer_orders["churn"] = df_customer_orders["total_orders"] == 1
churn_by_state = (
    df_customer_orders
    .groupby("customer_state")["churn"]
    .mean()
    .sort_values(ascending=False)
)

print(churn_by_state.head())


top_states_churn = churn_by_state.head(10)

plt.figure()
top_states_churn.plot(kind="bar")
plt.ylabel("Taxa de churn")
plt.title("Churn por estado (Top 10)")
plt.show()

# CHURN POR CATEGORIA DE PRODUTO

query = """
SELECT
    c.customer_unique_id,
    p.product_category_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers c
JOIN orders o 
ON c.customer_id = o.customer_id
JOIN order_items oi 
ON o.order_id = oi.order_id
JOIN products p 
ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY c.customer_unique_id, p.product_category_name;
"""
df_category_orders = pd.read_sql_query(query, conn)
df_category_orders["churn"] = df_category_orders["total_orders"] == 1
churn_by_category = (
    df_category_orders
    .groupby("product_category_name")["churn"]
    .mean()
    .sort_values(ascending=False)
)

print(churn_by_category.head(10))


top_churn_categories = churn_by_category.head(10)

plt.figure(figsize=(10, 5))
top_churn_categories.plot(kind="bar")
plt.ylabel("Taxa de churn")
plt.title("Churn por categoria de produto (Top 10)")
plt.show()

# CHURN VS TEMPO DE ENTREGA


query = """
SELECT
    c.customer_unique_id,
    AVG(
        JULIANDAY(o.order_delivered_customer_date) -
        JULIANDAY(o.order_purchase_timestamp)
    ) AS avg_delivery_days,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_unique_id;
"""
df_delivery_churn = pd.read_sql_query(query, conn)
df_delivery_churn["churn"] = df_delivery_churn["total_orders"] == 1
delivery_comparison = (
    df_delivery_churn
    .groupby("churn")["avg_delivery_days"]
    .mean()
)

print(delivery_comparison)

plt.figure()
delivery_comparison.plot(kind="bar")
plt.ylabel("Dias médios de entrega")
plt.title("Tempo de entrega vs Churn")
plt.xticks([0, 1], ["Retidos", "Churn"])
plt.show()



conn.close()
