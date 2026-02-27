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
-- CONSULTA 2: Produtos que venderam menos em Junho/2023
-- =====================================================
/*
EXPLICAÇÃO DA LÓGICA:
- WHERE Data LIKE '2023-06%': Filtra apenas as vendas do mês de junho de 2023
- GROUP BY Produto, Categoria: Agrupa por produto
- SUM(Quantidade * Preço): Calcula o total vendido em junho/2023
- ORDER BY VendasJunho2023 ASC: Ordena do menor para o maior (piores primeiro)

Esta consulta mostra quais produtos tiveram pior desempenho no mês de junho/2023.
*/

SELECT 
    Produto,
    Categoria,
    SUM(Quantidade * Preço) AS VendasJunho2023
FROM 
    vendas
WHERE 
    Data LIKE '2023-06%'
GROUP BY 
    Produto, Categoria
ORDER BY 
    VendasJunho2023 ASC;