from extracao import extrair_dados
from transformacao import transformar_dados

clientes, pedidos, produtos = extrair_dados()

if clientes is None:
    print("Extração falhou. Transformação não executada.")
else:
    print(f"Total de clientes extraídos: {len(clientes)}")
    clientes, pedidos, itens, produtos = transformar_dados(clientes, pedidos, produtos)
    print(f"Clientes: {len(clientes)} | Pedidos: {len(pedidos)} | Itens: {len(itens)} | Produtos: {len(produtos)}")