import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def carregar_dados(clientes, pedidos, itens, produtos):
    conexao = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )
    cursor = conexao.cursor()

    # limpar as tabelas antes de inserir para nao duplicar os dados
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM clientes")
    cursor.execute("DELETE FROM produtos")

    cursor.executemany(
        "INSERT INTO produtos VALUES (%(produto_id)s, %(nome)s, %(categoria)s, %(preco_base)s)",
        produtos,
    )
    cursor.executemany(
        "INSERT INTO clientes VALUES (%(id)s, %(nome)s, %(email)s, %(cidade)s, %(estado)s, %(cadastro_em)s)",
        clientes,
    )
    cursor.executemany(
        "INSERT INTO pedidos VALUES (%(id)s, %(cliente_id)s, %(data_pedido)s, %(status)s, %(valor_total)s, %(valor_itens)s, %(divergente)s)",
        pedidos,
    )
    cursor.executemany(
        "INSERT INTO itens_pedido VALUES (%(pedido_id)s, %(linha)s, %(produto_id)s, %(quantidade)s, %(preco_unitario)s)",
        itens,
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    print(f"carga: clientes={len(clientes)} produtos={len(produtos)} pedidos={len(pedidos)} itens={len(itens)}")