def tratar_email(cliente):
    cliente = dict(cliente)
    email = cliente.get("email")
    if email is None or str(email).strip() == "":
        cliente["email"] = None
    return cliente


def padronizar_estado(cliente):
    cliente = dict(cliente)
    cliente["estado"] = cliente["estado"].strip().upper()
    return cliente


def converter_data(texto):
    texto = texto.strip()
    if "/" in texto:
        dia, mes, ano = texto.split("/")
        return f"{ano}-{mes}-{dia}"
    return texto


def converter_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace(",", ".")
    return round(float(valor), 2)


def calcular_valor_itens(itens):
    total = 0
    for item in itens:
        total += int(item["quantidade"]) * converter_valor(item["preco_unitario"])
    return round(total, 2)


def marcar_divergencia(pedido):
    pedido = dict(pedido)
    diferenca = abs(pedido["valor_total"] - pedido["valor_itens"])
    pedido["divergente"] = round(diferenca, 2) > 0.01
    return pedido


def tratar_cliente(cliente):
    cliente = tratar_email(cliente)
    cliente = padronizar_estado(cliente)
    return cliente


def tratar_pedido(pedido):
    pedido = dict(pedido)
    pedido["data_pedido"] = converter_data(pedido["data_pedido"])
    pedido["valor_total"] = converter_valor(pedido["valor_total"])
    pedido["valor_itens"] = calcular_valor_itens(pedido["itens"])
    pedido = marcar_divergencia(pedido)
    del pedido["itens"]  # os itens vão para a tabela itens_pedido
    return pedido


def montar_itens(pedido):
    itens = []
    linha = 1
    for item in pedido["itens"]:
        itens.append({
            "pedido_id": pedido["id"],
            "linha": linha,
            "produto_id": int(item["produto_id"]),
            "quantidade": int(item["quantidade"]),
            "preco_unitario": converter_valor(item["preco_unitario"]),
        })
        linha += 1
    return itens


def tratar_produto(produto):
    produto = dict(produto)
    produto["produto_id"] = int(produto["produto_id"])
    produto["preco_base"] = converter_valor(produto["preco_base"])
    return produto


def remover_repetidos(pedidos):
    vistos = set()
    unicos = []
    for pedido in pedidos:
        if pedido["id"] not in vistos:
            vistos.add(pedido["id"])
            unicos.append(pedido)
    return unicos


def transformar_dados(clientes, pedidos, produtos):
    # clientes
    clientes_ok = []
    emails_nulos = 0
    estados_padronizados = 0
    for cliente in clientes:
        novo = tratar_cliente(cliente)
        if novo["email"] is None:
            emails_nulos += 1
        if novo["estado"] != cliente["estado"]:
            estados_padronizados += 1
        clientes_ok.append(novo)

    # pedidos e itens
    unicos = remover_repetidos(pedidos)
    repetidos_descartados = len(pedidos) - len(unicos)

    pedidos_ok = []
    itens_ok = []
    datas_convertidas = 0
    valores_convertidos = 0
    divergentes = 0
    for pedido in unicos:
        novo = tratar_pedido(pedido)
        if "/" in pedido["data_pedido"]:
            datas_convertidas += 1
        if isinstance(pedido["valor_total"], str):
            valores_convertidos += 1
        if novo["divergente"]:
            divergentes += 1
        pedidos_ok.append(novo)
        itens_ok.extend(montar_itens(pedido))

    # produtos
    produtos_ok = [tratar_produto(p) for p in produtos]

    print(f"transformacao: pedidos_unicos={len(unicos)} repetidos_descartados={repetidos_descartados}")
    print(f"transformacao: emails_nulos={emails_nulos} estados_padronizados={estados_padronizados} datas_convertidas={datas_convertidas} valores_convertidos={valores_convertidos}")
    print(f"divergentes: {divergentes} pedidos com valor_total diferente da soma dos itens")

    return clientes_ok, pedidos_ok, itens_ok, produtos_ok