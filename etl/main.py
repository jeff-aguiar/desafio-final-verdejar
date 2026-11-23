from extracao import extrair_dados

clientes, pedidos, produtos = extrair_dados()

print(f"Total de clientes extraídos: {len(clientes)}")