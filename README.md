# ETL da Verdejar

## Testes e reconciliação

### Como rodar

Na pasta principal do projeto, com o banco carregado (`python etl/main.py`):

```
pip install pytest
pytest
```

Os testes ficam na pasta `tests/`. O arquivo `conftest.py` (vazio) fica na raiz, para o pytest enxergar a pasta `etl/`.

### Resultado do pytest

```
11 passed in 0.36s
```

São 9 testes de transformação (cobrem as seis armadilhas, A1 a A6) e 2 de reconciliação.

### Primeiro erro: faltava o conftest.py

Na primeira execução, o `pytest` não coletou nenhum teste e deus o seguinte erro:

```
ModuleNotFoundError: No module named 'etl'
```

Os testes importam `etl.transformacao`, mas sem o `conftest.py` na raiz o Python não enxergava a pasta `etl/`. Corrigi criando o `conftest.py` vazio na raiz do projeto. Depois disso, os 11 testes passaram.

### Reconciliação

O arquivo `tests/test_reconciliacao.py` compara a origem com o banco:

- a contagem de pedidos únicos do `brutos/pedidos.json` (sem repetidos) com a contagem na tabela `pedidos`;
- a soma de `valor_itens` da origem com a soma no banco, com tolerância de um centavo.

### Teste de consulta

A soma dos totais de vendas por mês é igual à soma geral de `valor_total` da tabela `pedidos`.

### Consultas de validação

Arquivo: `consultas_validacao.sql`. Resultado completo em `resultado_consultas.txt`.

**(a) Total de vendas por mês**

| mês     | total    |
| ------- | -------- |
| 2026-01 | 30449.02 |
| 2026-02 | 33923.86 |
| 2026-03 | 30678.70 |
| 2026-04 | 31253.96 |
| 2026-05 | 30890.02 |
| 2026-06 | 31627.73 |
| 2026-07 | 32796.17 |
| 2026-08 | 29328.04 |
| 2026-09 | 29995.71 |
| 2026-10 | 31104.54 |

**(b) Pedidos por estado**

| estado | pedidos |
| ------ | ------- |
| MG     | 476     |
| PR     | 974     |
| RS     | 1543    |
| SC     | 1127    |
| SP     | 880     |

Total: 5000 pedidos.

**(c) Pedidos divergentes**

Total: 238 pedidos, igual ao contador `divergentes` da transformação. Primeiros registros:

| id  | valor_total | valor_itens |
| --- | ----------- | ----------- |
| 1   | 125.84      | 130.84      |
| 51  | 26.58       | 23.58       |
| 71  | 144.35      | 134.35      |
| 81  | -1.84       | 3.16        |
| 106 | 47.78       | 44.78       |

### Observação sobre o pedido 81

O pedido 81 tem `valor_total` negativo (-1.84) e `valor_itens` 3.16. O valor já vinha negativo na origem (`brutos/pedidos.json`), então o ETL o gravou como recebido e o marcou como divergente, conforme a regra da armadilha A6. Não foi tratado como erro de carga.
