import os
import json
import psycopg2
from dotenv import load_dotenv

from etl.transformacao import remover_repetidos, tratar_pedido

load_dotenv()


def abrir_conexao():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )


def test_reconciliacao_pedidos():
    with open("brutos/pedidos.json", encoding="utf-8") as f:
        brutos = json.load(f)

    unicos = remover_repetidos(brutos)
    soma_origem = sum(tratar_pedido(p)["valor_itens"] for p in unicos)

    cursor = abrir_conexao().cursor()
    cursor.execute("SELECT COUNT(*), SUM(valor_itens) FROM pedidos")
    quantidade_destino, soma_destino = cursor.fetchone()

    assert len(unicos) == quantidade_destino
    assert abs(soma_origem - float(soma_destino)) <= 0.01


def test_consulta_vendas_por_mes():
    cursor = abrir_conexao().cursor()

    cursor.execute("SELECT SUM(valor_total) FROM pedidos")
    soma_geral = cursor.fetchone()[0]

    cursor.execute("""
        SELECT SUM(total) FROM (
            SELECT DATE_TRUNC('month', data_pedido) AS mes, SUM(valor_total) AS total
            FROM pedidos
            GROUP BY mes
        ) AS meses
    """)
    soma_meses = cursor.fetchone()[0]

    assert abs(float(soma_meses) - float(soma_geral)) <= 0.01