# ETL da Verdejar

Projeto de ETL desenvolvido para o desafio final do bootcamp. O fluxo extrai clientes e pedidos de uma API local e produtos de um CSV, transforma os dados para tratar as inconsistências previstas no desafio e carrega o resultado em um banco PostgreSQL.

## Fluxo do ETL

1. **Extração** (`etl/extracao.py`): consulta as rotas paginadas `/clientes` e `/pedidos` da API em `http://127.0.0.1:8000` e lê `insumos/dados/produtos.csv`. As respostas são salvas em `brutos/`.
2. **Transformação** (`etl/transformacao.py`): aplica as regras de qualidade descritas abaixo e prepara pedidos e itens para as tabelas de destino.
3. **Carga** (`etl/carga.py`): conecta ao PostgreSQL usando as variáveis definidas no `.env`, limpa os dados existentes nas tabelas do ETL e carrega o novo conjunto.

## Regras de transformação

O ETL trata as seis armadilhas de qualidade dos dados:

| Armadilha                              | Tratamento                                                                                                                 |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| A1 — e-mail ausente ou vazio           | Substitui por `NULL` e mantém o cliente.                                                                                   |
| A2 — sigla de estado em caixa mista    | Remove espaços externos e converte para maiúsculas.                                                                        |
| A3 — datas em formatos diferentes      | Converte `DD/MM/AAAA` para `AAAA-MM-DD`; mantém datas já nesse formato.                                                    |
| A4 — valor decimal com vírgula         | Converte o texto para número com duas casas decimais.                                                                      |
| A5 — pedidos repetidos entre páginas   | Mantém a primeira ocorrência de cada pedido.                                                                               |
| A6 — total diferente da soma dos itens | Calcula `valor_itens` e marca `divergente` quando a diferença absoluta excede um centavo. Preserva `valor_total` recebido. |

O detalhamento dos campos e das regras está em [`CONTRATO_DE_DADOS.md`](CONTRATO_DE_DADOS.md).

## Estrutura do projeto

```text
etl/
  extracao.py            # Extração da API e do CSV
  transformacao.py       # Limpeza e transformação dos dados
  carga.py               # Carga no PostgreSQL
  main.py                # Orquestra as etapas do ETL
tests/
  test_transformacao.py  # Testes das regras A1 a A6
  test_reconciliacao.py  # Reconciliação com o banco e validação de consulta
insumos/
  dados/produtos.csv     # Produtos usados na carga
  schema.sql             # Esquema PostgreSQL
brutos/                  # JSON extraído; gerado durante a execução
consultas_validacao.sql  # Consultas de conferência dos resultados
resultado_consultas.txt  # Resultados registrados das consultas
```

## Como executar

### Pré-requisitos

- Python 3
- PostgreSQL em execução e um banco criado para o projeto
- API do desafio disponível em `http://127.0.0.1:8000`

O script `api_verdejar.py` é fornecido como parte dos insumos do desafio, mas não está incluído neste repositório. Inicie essa API separadamente antes de executar a extração.

### Instalar dependências

Na raiz do projeto, crie e ative um ambiente virtual e instale as bibliotecas utilizadas:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install requests psycopg2-binary python-dotenv pytest
```

### Preparar o banco

Crie um banco PostgreSQL e aplique o esquema:

```powershell
psql -U SEU_USUARIO -d SEU_BANCO -f insumos/schema.sql
```

Crie um arquivo `.env` na raiz com os dados de conexão:

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=SEU_BANCO
PGUSER=SEU_USUARIO
PGPASSWORD=SUA_SENHA
```

O `.env` é ignorado pelo Git; não compartilhe nem versione credenciais. A pasta `brutos/` também é gerada localmente e não é versionada.

### Executar

Com o PostgreSQL e a API do desafio em execução, rode na raiz:

```powershell
python etl/main.py
```

A carga apaga os registros atuais das tabelas `itens_pedido`, `pedidos`, `clientes` e `produtos` antes de inserir os dados extraídos. Execute em um banco destinado ao projeto, pois uma nova execução substitui o conteúdo dessas tabelas.

## Testes e validação

Com o ambiente virtual ativado e o banco já carregado, execute:

```powershell
pytest
```

Os testes incluem casos para as regras de transformação e testes de reconciliação entre os JSON extraídos e o banco. Os testes de reconciliação precisam de um PostgreSQL acessível com as variáveis do `.env` configuradas.

**Resultado registrado:** 11 testes passaram — 9 de transformação e 2 de reconciliação.

As consultas de conferência estão em [`consultas_validacao.sql`](consultas_validacao.sql), com os resultados registrados em [`resultado_consultas.txt`](resultado_consultas.txt).

### Consultas de validação

Arquivo: [`consultas_validacao.sql`](consultas_validacao.sql). Resultado completo em [`resultado_consultas.txt`](resultado_consultas.txt).

**(a) Total de vendas por mês**

| mês     |    total |
| ------- | -------: |
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
| ------ | ------: |
| MG     |     476 |
| PR     |     974 |
| RS     |    1543 |
| SC     |    1127 |
| SP     |     880 |

Total: 5000 pedidos.

**(c) Pedidos divergentes**

Total: 238 pedidos, igual ao contador `divergentes` da transformação. Primeiros registros:

|  id | valor_total | valor_itens |
| --: | ----------: | ----------: |
|   1 |      125.84 |      130.84 |
|  51 |       26.58 |       23.58 |
|  71 |      144.35 |      134.35 |
|  81 |       -1.84 |        3.16 |
| 106 |       47.78 |       44.78 |

### Observação sobre o pedido 81

O pedido 81 tem `valor_total` negativo (-1.84) e `valor_itens` 3.16. O valor já vinha negativo na origem (`brutos/pedidos.json`), então o ETL o gravou como recebido e o marcou como divergente, conforme a regra A6. Não foi tratado como erro de carga.
