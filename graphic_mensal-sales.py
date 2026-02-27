import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# Carrega o dataset limpo
df = pd.read_csv('data_clean.csv', sep=';')

# Garante que a coluna Data está como datetime
df['Data'] = pd.to_datetime(df['Data'])

# Garante a criação de um TotalVenda
if 'TotalVenda' not in df.columns:
    df['TotalVenda'] = df['Quantidade'] * df['Preço']


## TOTAL VENDAS POR PRODUTO
total_vendas_produto = (
    df.groupby('Produto')['TotalVenda']
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal de vendas por produto:\n")
print(total_vendas_produto.to_string())

# Plota gráfico de linha
#plt.figure(figsize=(10, 6))
#vendas_mensais.plot(kind='line', marker='o')
#plt.title('Tendência de vendas mensais')
#plt.xlabel('Mês')
#plt.ylabel('Total de vendas (R$)')
#plt.grid(True)
#plt.tight_layout()
#plt.show()
