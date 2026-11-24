from etl.transformacao import (
    tratar_email,
    padronizar_estado,
    converter_data,
    converter_valor,
    remover_repetidos,
    calcular_valor_itens,
    marcar_divergencia,
)


# A1: e-mail ausente
def test_email_ausente_vira_nulo():
    cliente = {"id": 1, "email": None}
    assert tratar_email(cliente)["email"] is None


# A2: estado em minúsculas
def test_estado_minusculo_vira_maiusculo():
    cliente = {"estado": "mg"}
    assert padronizar_estado(cliente)["estado"] == "MG"


# A3: data nos dois formatos
def test_data_com_barras_vira_iso():
    assert converter_data("19/02/2026") == "2026-02-19"


def test_data_iso_permanece():
    assert converter_data("2026-02-19") == "2026-02-19"


# A4: valor com vírgula
def test_valor_com_virgula_vira_numero():
    assert converter_valor("125,84") == 125.84


def test_valor_numerico_permanece():
    assert converter_valor(94.34) == 94.34


# A5: pedido repetido
def test_pedido_repetido_fica_so_um():
    pedidos = [{"id": 1}, {"id": 2}, {"id": 1}]
    resultado = remover_repetidos(pedidos)
    assert len(resultado) == 2
    assert [p["id"] for p in resultado] == [1, 2]


# A6: valor total diferente da soma dos itens
def test_soma_dos_itens():
    itens = [
        {"quantidade": 3, "preco_unitario": 4.3},
        {"quantidade": 5, "preco_unitario": 15.86},
        {"quantidade": 4, "preco_unitario": 9.66},
    ]
    assert calcular_valor_itens(itens) == 130.84


def test_pedido_divergente_e_marcado():
    pedido = {"valor_total": 125.84, "valor_itens": 130.84}
    assert marcar_divergencia(pedido)["divergente"] is True