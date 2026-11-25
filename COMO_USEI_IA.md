# Como usei IA

Usei IA principalmente como apoio pontual, mantendo as decisões e a validação do projeto sob minha responsabilidade. A maior parte da ajuda foi para receber dicas de bibliotecas adequadas ao ETL, organizar arquivos de texto como o README e o contrato de dados, e melhorar a apresentação das mensagens de `print` para que o andamento e os totais do processamento ficassem fáceis de acompanhar.

## Sugestões aceitas

- Usar `requests` para consultar a API local, `psycopg2` para conectar ao PostgreSQL e `python-dotenv` para carregar as configurações de conexão do arquivo de ambiente.
- Usar `pytest` para testar as transformações e a reconciliação. Os testes cobrem as seis armadilhas dos dados e verificam contagens e somas entre origem e banco.
- Organizar os `print` em mensagens identificáveis, com progresso da extração e contagens do processamento, para facilitar a conferência da execução.
- Estruturar a documentação em arquivos com objetivos distintos: instruções e resultados no README, e regras de transformação no contrato de dados.
- A IA me ajudou a escrever a função simples `converter_valor`, que troca a vírgula decimal por ponto e arredonda o resultado para duas casas:
  ```python
  def converter_valor(valor):
      if isinstance(valor, str):
          valor = valor.replace(",", ".")
      return round(float(valor), 2)
  ```

## Sugestões não adotadas

- Não acrescentei `pandas` só para ler o CSV de produtos. Como a entrada é simples, `csv.DictReader` atende ao caso sem adicionar mais uma dependência.
- Não alterei o `valor_total` dos pedidos para forçá-lo a coincidir com a soma dos itens. O valor original deve ser preservado e a diferença registrada como divergência, conforme a regra do desafio.
- Não tratei um valor negativo recebido na origem como falha de carga: o pedido foi mantido e marcado como divergente, em vez de modificar ou descartar os dados.

## Falhas e retrabalho

Na primeira execução, o `pytest` não conseguiu importar o módulo `etl` e terminou com `ModuleNotFoundError: No module named 'etl'`. Foi necessário criar o `conftest.py` vazio na raiz para que os testes encontrassem o pacote; depois, executei novamente e os 11 testes passaram.

Esse retrabalho reforçou que sugestões de código e configuração precisam ser verificadas no ambiente real do projeto. Também conferi os resultados das consultas SQL e preservei os dados de origem quando a regra pedia registrar uma divergência, em vez de corrigir o valor silenciosamente.
