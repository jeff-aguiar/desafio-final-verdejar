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


def pegar_da_api(endpoint, nome_registros):
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

            if resposta.status_code != 200:
                print(f"Erro: a API retornou o status {resposta.status_code} em {endpoint}, página {pagina}.")
                return None

            resultado = resposta.json()
            total_paginas = resultado["total_pages"]
            lista.extend(resultado["items"])
            pagina += 1

    except requests.exceptions.ConnectionError:
        print("Erro: não foi possível conectar à API. Verifique se ela está rodando.")
        return None

    print(f"extracao: {endpoint} paginas={total_paginas} {nome_registros}={len(lista)}")
    return lista


def extrair_dados():
    clientes = pegar_da_api("clientes", "registros")
    if clientes is None:
        return None, None, None
    salvar_json(clientes, "clientes")

    pedidos = pegar_da_api("pedidos", "registros_brutos")
    if pedidos is None:
        return None, None, None
    salvar_json(pedidos, "pedidos")

    caminho_csv = os.path.join(PASTA_PRINCIPAL, "insumos", "dados", "produtos.csv")
    try:
        with open(caminho_csv, "r", encoding="utf-8") as f:
            produtos = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Erro: arquivo não encontrado: {caminho_csv}")
        return None, None, None
    salvar_json(produtos, "produtos")

    return clientes, pedidos, produtos