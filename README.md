
# Projeto de Análise de Vendas

Este projeto consiste em um sistema completo para simulação, limpeza, armazenamento e análise de dados de vendas. Os dados são gerados sinteticamente, processados, armazenados em banco SQLite e visualizados através de gráficos e consultas SQL, com exportação para Excel formatado profissionalmente.

## Estrutura do Repositório

├── datamain.py # Script principal - orquestra toda a execução
├── simulacao.py # Geração e limpeza dos dados simulados
├── graficos_mensais.py # Geração dos gráficos de análise
├── gerar_excel.py # Geração do Excel com gráficos e formatação
├── consultas_sql.sql # Consultas SQL com explicações
├── relatorio_insights.md # Relatório final com insights e recomendações
├── README.md # Este arquivo - documentação do projeto
├── data_clean.csv # Dados limpos gerados (criado na execução)
├── vendas.db # Banco de dados SQLite (criado na execução)
├── resultado_consulta1.csv # Resultado da Consulta 1 (criado na execução)
├── resultado_consulta2.csv # Resultado da Consulta 2 (criado na execução)
└── resultado_completo.xlsx # Excel com todas as abas e gráficos (criado na execução)


## Dependências Necessárias

- Python 3.8+
- Bibliotecas Python:

```bash
pip install pandas matplotlib numpy openpyxl
```

* SQLite3 (já incluso no Python)

---

## Como Executar

**bash**

```
python datamain.py
```

### O que acontece durante a execução:

1. Gera 60 registros simulados de vendas para 2023
2. Aplica limpeza e padronização nos dados
3. Salva `data_clean.csv`
4. Cria o banco SQLite `vendas.db` e importa os dados
5. Executa as consultas SQL
6. Gera `resultado_consulta1.csv` e `resultado_consulta2.csv`
7. Gera arquivo Excel `resultado_completo.xlsx` com 4 abas formatadas
8. Plota os gráficos de análise na tela

---

## Arquivo Excel Gerado

O arquivo `resultado_completo.xlsx` contém:

| Aba                         | Conteúdo                                                             |
| --------------------------- | --------------------------------------------------------------------- |
| **Total por Produto** | Consulta 1 - Total de vendas por produto (ordenado decrescente)       |
| **Junho2023**         | Consulta 2 - Produtos que venderam em junho/2023 (ordenado crescente) |
| **Dados Brutos**      | Todos os 60 registros de vendas                                       |
| **Resumo**            | Estatísticas gerais + gráficos incorporados                         |

### Formatação aplicada:

* Cabeçalhos coloridos
* Linhas zebradas
* Colunas auto-ajustadas
* Valores monetários formatados (R$ 1.234,56)
* Gráficos incorporados na aba Resumo

---

## Consultas SQL

Arquivo: `consultas_sql.sql`

### Consulta 1: Total de vendas por produto

**sql**

```
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
```

### Consulta 2: Produtos que venderam menos em Junho/2023

**sql**

```
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
```

Para executar manualmente:

**bash**

```
sqlite3 vendas.db
.read consultas_sql.sql
```

---

## Visualizações

O script `graficos_mensais.py` gera dois gráficos:

1. **Tendência de Vendas Mensais** - Evolução do faturamento em 2023
2. **Total de Vendas por Produto** - Comparativo por produto (ordem alfabética)

Os mesmos gráficos são incorporados na aba **Resumo** do Excel.

---

## Relatório de Insights

O arquivo `relatorio_insights.md` contém:

* Principais insights identificados
* Padrões de sazonalidade
* Concentração de receita
* Ações recomendadas para o negócio

---

## Observações Importantes

* Dados são **simulados** (não reais)
* Período coberto: **apenas 2023**
* Execução **determinística** - mesmos resultados sempre (preços fixos)
* O Excel gerado já vem **formatado profissionalmente** com gráficos

---

## Personalização

No arquivo `simulacao.py` você pode ajustar:

| Variável         | Descrição                    | Padrão              |
| ----------------- | ------------------------------ | -------------------- |
| `num_registros` | Quantidade de registros        | 60                   |
| `produtos`      | Lista de produtos e categorias | 10 produtos          |
| `PRECOS_FIXOS`  | Valores fixos por produto      | Definidos no código |

---

## Licença

Uso livre para fins educacionais.
