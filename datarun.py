from dataset import simular_dados, limpar_dados
import os
import pandas as pd

# ----------------------
# EXECUÇÃO PRINCIPAL
# ----------------------
if __name__ == "__main__":
# Simulação e limpeza
	df = simular_dados()
	df = limpar_dados(df)
	print(df)
	df.to_csv("data_clean.csv", index=False, sep=';')

# --- Análise usando o arquivo data_clean.csv ---
if os.path.exists("data_clean.csv"):
	df_clean = pd.read_csv("data_clean.csv", sep=';')

# Garante que as colunas estejam no tipo correto
	df_clean['Quantidade'] = df_clean['Quantidade'].astype(int)
	df_clean['Preço'] = df_clean['Preço'].astype(float)
#

# Leitura dos Dados
def carregar_dados(path):
        df_clean = pd.read_csv(path, sep=';')
        df_clean['Data'] = pd.to_datetime(df_clean['Data'])
        if 'TotalVenda' not in df_clean.columns:
            df_clean['TotalVenda'] = df_clean['Quantidade'] * df_clean['Preço']
        return df_clean
if os.path.exists("data_clean.csv"):
    df_clean = carregar_dados("data_clean.csv")


def calcular_total_vendas_produto(df_clean):
    return (
        df_clean.groupby('Produto')['TotalVenda']
            .sum()
            .sort_values(ascending=False)
    )

total_vendas_produto = calcular_total_vendas_produto(df_clean)

# Calcula o total de vendas por produto e imprime
print(f"\nTotal de vendas por produto:\n{total_vendas_produto}\n")
produto_mais_vendas = total_vendas_produto.idxmax()
valor_mais_vendas = total_vendas_produto.max()
print(f"\nProduto com maior total de vendas: {produto_mais_vendas} (R$ {valor_mais_vendas:.2f})")
