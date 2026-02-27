import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datarun import total_vendas_produto, produto_mais_vendas, valor_mais_vendas


# Carrega o dataset limpo
df = pd.read_csv('data_clean.csv', sep=';')

# Garante que a coluna Data está como datetime
df['Data'] = pd.to_datetime(df['Data'])

# Garante que TotalVenda existe
if 'TotalVenda' not in df.columns:
    df['TotalVenda'] = df['Quantidade'] * df['Preço']



#TENDÊNCIA DE VENDAS MENSAIS

# Define data como índice
df_temp = df.copy()
df_temp.set_index('Data', inplace=True)

vendas_mensais = df_temp['TotalVenda'].resample('ME').sum()
vendas_mensais.index = vendas_mensais.index.strftime('%b/%Y')


# ----- SUBPLOTS (3 GRÁFICOS) -----

# Cria a figura com 3 gráficos (3 linhas, 1 coluna)
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# 1) Tendência de vendas mensais
axes[0].plot(vendas_mensais.index, vendas_mensais, marker='o')
axes[0].set_title('Tendência de Vendas Mensais')
axes[0].set_xlabel('Mês')
axes[0].set_ylabel('Total de Vendas')
axes[0].grid(True)

# 2) Total de vendas por produto (barra)
axes[1].bar(total_vendas_produto.index, total_vendas_produto)
axes[1].set_title('Total de Vendas por Produto')
axes[1].set_xlabel('Produto')
axes[1].set_ylabel('Total de Vendas')
axes[1].tick_params(axis='x', rotation=45)

# Ajusta espaçamento para não sobrepor
plt.tight_layout()

# Mostra tudo na mesma tela
plt.show()