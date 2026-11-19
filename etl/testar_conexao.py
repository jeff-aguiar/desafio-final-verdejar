
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conexao = psycopg2.connect(
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT"),
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD")
)

with conexao.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM clientes")
    quantidade = cursor.fetchone()[0]

print(f"Conexão bem-sucedida! Clientes: {quantidade}")

conexao.close()
