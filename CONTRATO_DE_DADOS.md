# Contrato de dados: verdejar

## Clientes

| Campo       | Tipo    | Aceita nulo | Regra de transformação                                |
| ----------- | ------- | ----------- | ----------------------------------------------------- |
| id          | INTEGER | não         | sem alteração                                         |
| nome        | TEXT    | não         | sem alteração                                         |
| email       | TEXT    | sim         | ausente ou vazio vira nulo e o cliente é mantido (A1) |
| cidade      | TEXT    | não         | sem alteração                                         |
| estado      | CHAR(2) | não         | sempre em maiúsculas (A2)                             |
| cadastro_em | DATE    | não         | sem alteração (já vem em AAAA-MM-DD)                  |

## Produtos

| Campo      | Tipo          | Aceita nulo | Regra de transformação                          |
| ---------- | ------------- | ----------- | ----------------------------------------------- |
| produto_id | INTEGER       | não         | texto do CSV convertido para inteiro            |
| nome       | TEXT          | não         | sem alteração                                   |
| categoria  | TEXT          | não         | sem alteração                                   |
| preco_base | NUMERIC(10,2) | não         | texto do CSV convertido para número com 2 casas |

## Pedidos

| Campo       | Tipo          | Aceita nulo | Regra de transformação                                                              |
| ----------- | ------------- | ----------- | ----------------------------------------------------------------------------------- |
| id          | INTEGER       | não         | pedidos repetidos descartados, fica a primeira ocorrência (A5)                      |
| cliente_id  | INTEGER       | não         | sem alteração                                                                       |
| data_pedido | DATE          | não         | DD/MM/AAAA convertido para AAAA-MM-DD (A3)                                          |
| status      | TEXT          | não         | sem alteração                                                                       |
| valor_total | NUMERIC(12,2) | não         | texto com vírgula decimal convertido para número com 2 casas (A4)                   |
| valor_itens | NUMERIC(12,2) | não         | soma de quantidade x preco_unitario dos itens do pedido (A6)                        |
| divergente  | BOOLEAN       | não         | verdadeiro quando a diferença entre valor_total e valor_itens é maior que 0,01 (A6) |

## itens_pedido

| Campo          | Tipo          | Aceita nulo | Regra de transformação                                                          |
| -------------- | ------------- | ----------- | ------------------------------------------------------------------------------- |
| pedido_id      | INTEGER       | não         | id do pedido ao qual o item pertence                                            |
| linha          | INTEGER       | não         | posição do item no pedido, começando em 1; com pedido_id forma a chave primária |
| produto_id     | INTEGER       | não         | convertido para inteiro                                                         |
| quantidade     | INTEGER       | não         | convertida para inteiro                                                         |
| preco_unitario | NUMERIC(10,2) | não         | convertido para número com 2 casas                                              |
