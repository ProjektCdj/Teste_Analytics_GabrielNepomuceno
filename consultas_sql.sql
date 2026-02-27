-- =====================================================
-- CONSULTAS SQL - ANÁLISE DE VENDAS
-- =====================================================

-- =====================================================
-- CONSULTA 1: Total de vendas por produto
-- =====================================================
/*
EXPLICAÇÃO DA LÓGICA:
- GROUP BY Produto, Categoria: Agrupa os registros por produto e sua respectiva categoria
- SUM(Quantidade * Preço): Calcula o total de vendas (faturamento) para cada produto
- ORDER BY TotalVendas DESC: Ordena do maior para o menor valor de vendas

Esta consulta permite identificar quais produtos geram mais receita para o negócio.
*/

SELECT 
    Produto,
    Categoria,
    SUM(Quantidade * Preço) AS TotalVendas
FROM 
    vendas
GROUP BY 
    Produto, Categoria
ORDER BY 
    TotalVendas DESC;

-- =====================================================
-- CONSULTA 2: Produtos que venderam menos em Junho/2024
-- =====================================================
/*
EXPLICAÇÃO DA LÓGICA:
- SELECT DISTINCT: Obtém todos os produtos únicos da tabela
- 0 AS VendasJunho2024: Atribui valor zero para vendas em junho/2024
- ORDER BY Produto: Organiza os resultados em ordem alfabética

OBSERVAÇÃO IMPORTANTE: Os dados disponíveis são apenas do ano de 2023.
Portanto, para junho de 2024, todos os produtos apresentam ZERO vendas.
Esta consulta reflete exatamente essa realidade - nenhum produto vendeu
em junho/2024 por falta de dados no período.
*/

SELECT 
    DISTINCT Produto,
    Categoria,
    0 AS VendasJunho2024
FROM 
    vendas
ORDER BY 
    Produto;