-- (a) total de vendas por mês
SELECT DATE_TRUNC('month', data_pedido) AS mes, SUM(valor_total) AS total
FROM pedidos
GROUP BY mes
ORDER BY mes;

-- (b) quantidade de pedidos por estado
SELECT c.estado, COUNT(*) AS pedidos
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
GROUP BY c.estado
ORDER BY c.estado;

-- (c) pedidos divergentes
SELECT id, valor_total, valor_itens
FROM pedidos
WHERE divergente
ORDER BY id;