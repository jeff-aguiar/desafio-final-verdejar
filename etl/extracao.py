import json
import csv
import os
import requests

URL = "http://127.0.0.1:8000"

PASTA_PRINCIPAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def salvar_json(dados, nome):
    pasta = os.path.join(PASTA_PRINCIPAL, "brutos")
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"{nome}.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Arquivo salvo: {nome}.json")


def pegar_da_api(endpoint):
    lista = []
    pagina = 1
    total_paginas = 1

    try:
        while pagina <= total_paginas:
            resposta = requests.get(
                f"{URL}/{endpoint}",
                params={"page": pagina, "page_size": 200},
                timeout=30,
            )

            if resposta.status_code == 404:
                print(f"Erro: página {pagina} de {endpoint} não existe.")
                return None

            resposta.raise_for_status()
            resultado = resposta.json()

            total_paginas = resultado["total_pages"]
            lista.extend(resultado["items"])
            print(f"{endpoint}: página {pagina} de {total_paginas}")
            pagina += 1

    except requests.exceptions.ConnectionError:
        print("Erro: não foi possível conectar à API. Verifique se ela está rodando.")
        return None

    return lista


def extrair_dados():
    clientes = pegar_da_api("clientes")
    if clientes is None:
        return None, None, None
    salvar_json(clientes, "clientes")

    pedidos = pegar_da_api("pedidos")
    if pedidos is None:
        return None, None, None
    salvar_json(pedidos, "pedidos")

    caminho_csv = os.path.join(PASTA_PRINCIPAL, "insumos", "dados", "produtos.csv")
    with open(caminho_csv, "r", encoding="utf-8") as f:
        produtos = list(csv.DictReader(f))
    salvar_json(produtos, "produtos")

    print(f"Clientes: {len(clientes)} | Pedidos: {len(pedidos)} | Produtos: {len(produtos)}")
    return clientes, pedidos, produtos