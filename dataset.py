# --- Análise usando o arquivo data_clean.csv ---

# ----------------------
# SIMULAÇÃO DE DADOS
# ----------------------
import random
import pandas as pd
from datetime import datetime, timedelta
import os

# Parâmetros e listas de produtos
num_registros = 60
produtos = [
	("Notebook", "Eletrônicos"),
	("Smartphone", "Eletrônicos"),
	("Camiseta", "Vestuário"),
	("Tênis", "Vestuário"),
	("Geladeira", "Eletrodomésticos"),
	("Micro-ondas", "Eletrodomésticos"),
	("Livro", "Papelaria"),
	("Caneta", "Papelaria"),
	("Bicicleta", "Esportes"),
	("Bola", "Esportes")
]

# Geração de Data
def gerar_data():
	data_inicial = datetime(2023, 1, 1)
	data_final = datetime(2023, 12, 31)
	dias = (data_final - data_inicial).days
	return data_inicial + timedelta(days=random.randint(0, dias))

# Geração de Preços
def gerar_preco(produto):
	precos = {
		"Notebook": (2500, 6000),
		"Smartphone": (1000, 4000),
		"Camiseta": (30, 120),
		"Tênis": (120, 600),
		"Geladeira": (1500, 4000),
		"Micro-ondas": (300, 900),
		"Livro": (20, 120),
		"Caneta": (2, 15),
		"Bicicleta": (400, 2500),
		"Bola": (30, 200)
	}
	faixa = precos.get(produto, (10, 100))
	return round(random.uniform(*faixa), 2)

# Simulação dos dados
def simular_dados():
	dados = []
	for i in range(1, num_registros + 1):
		produto, categoria = random.choice(produtos)
		quantidade = random.randint(1, 10)
		preco = gerar_preco(produto)
		data = gerar_data().strftime('%d/%m/%Y')
		dados.append({
			"ID": i,
			"Data": data,
			"Produto": produto,
			"Categoria": categoria,
			"Quantidade": quantidade,
			"Preço": preco
		})
	return pd.DataFrame(dados)

# ----------------------
# LIMPEZA DE DADOS
# ----------------------
def limpar_dados(df):
# Preencher valores faltantes com aleatórios compatíveis
	if df.isnull().values.any():
		produtos_list = [p[0] for p in produtos]
		categorias_dict = dict(produtos)
		if df['Produto'].isnull().any():
			df['Produto'] = df['Produto'].apply(lambda x: random.choice(produtos_list) if pd.isnull(x) else x)
		if df['Categoria'].isnull().any():
			df['Categoria'] = df.apply(lambda row: categorias_dict.get(row['Produto'], random.choice([p[1] for p in produtos])) if pd.isnull(row['Categoria']) else row['Categoria'], axis=1)
		if df['Quantidade'].isnull().any():
			df['Quantidade'] = df['Quantidade'].apply(lambda x: random.randint(1, 10) if pd.isnull(x) else x)
		if df['Preço'].isnull().any():
			df['Preço'] = df.apply(lambda row: gerar_preco(row['Produto']) if pd.isnull(row['Preço']) else row['Preço'], axis=1)
		if df['Data'].isnull().any():
			df['Data'] = df['Data'].apply(lambda x: gerar_data().strftime('%d/%m/%Y') if pd.isnull(x) else x)
		if df['ID'].isnull().any():
			max_id = df['ID'].max() if not df['ID'].isnull().all() else 0
			novos_ids = list(range(max_id + 1, max_id + 1 + df['ID'].isnull().sum()))
			df.loc[df['ID'].isnull(), 'ID'] = novos_ids
# Remover duplicatas
	df = df.drop_duplicates()
# Conversão de tipos
	df['ID'] = df['ID'].astype(int)
	df['Quantidade'] = df['Quantidade'].astype(int)
	df['Preço'] = df['Preço'].astype(float)
	df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
	return df

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
		
    # Cria a coluna TotalVenda se não existir
		if 'TotalVenda' not in df_clean.columns:
			df_clean['TotalVenda'] = df_clean['Quantidade'] * df_clean['Preço']
		
    # Calcula o total de vendas por produto e imprime
		total_vendas_produto = df_clean.groupby('Produto')['TotalVenda'].sum().sort_values(ascending=False)
		print("\nTotal de vendas por produto (usando data_clean.csv):")
		print(total_vendas_produto)
		produto_mais_vendas = total_vendas_produto.idxmax()
		valor_mais_vendas = total_vendas_produto.max()
		print(f"\nProduto com maior total de vendas: {produto_mais_vendas} (R$ {valor_mais_vendas:.2f})")
