import sqlite3
import pandas as pd
from pathlib import Path

#Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "olist.db"

DB_DIR.mkdir(exist_ok = True)

# Conexão com o banco
conn = sqlite3.connect(DB_PATH)

# Arquivos para carregar
files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "python -m pip install pandas
olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "payments": "olist_order_payments_dataset.csv"
}

for table, file in files.items():
    df = pd.read_csv(DATA_DIR / file)
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"Tabela {table} criada com sucesso!")

conn.close()
print("Banco de dados criado em database/olist.db")
