from datetime import datetime, timedelta
import random
import pandas as pd

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
        produto, categoria = produtos[i % len(produtos)]
        quantidade = (i % 10) + 1
        preco = gerar_preco(produto)
        data = gerar_data(i).strftime('%d/%m/%Y')

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
    if df.isnull().values.any():
        produtos_list = [p[0] for p in produtos]
        categorias_dict = dict(produtos)

        # Produto faltante → usa o primeiro produto da lista (determinístico)
        if df['Produto'].isnull().any():
            produto_padrao = produtos_list[0]
            df['Produto'] = df['Produto'].fillna(produto_padrao)

        # Categoria faltante → baseada no produto
        if df['Categoria'].isnull().any():
            df['Categoria'] = df.apply(
                lambda row: categorias_dict.get(row['Produto'], "Outros")
                if pd.isnull(row['Categoria']) else row['Categoria'],
                axis=1
            )

        # Quantidade faltante → usa mediana (melhor que aleatório)
        if df['Quantidade'].isnull().any():
            quantidade_padrao = int(df['Quantidade'].median()) if df['Quantidade'].notnull().any() else 1
            df['Quantidade'] = df['Quantidade'].fillna(quantidade_padrao)

        # Preço faltante → preço médio por produto
        if df['Preço'].isnull().any():
            preco_medio = df.groupby('Produto')['Preço'].transform('mean')
            df['Preço'] = df['Preço'].fillna(preco_medio)
            df['Preço'] = df['Preço'].fillna(df['Preço'].mean())

        # Data faltante → sequência baseada no índice (sem random)
        if df['Data'].isnull().any():
            df['Data'] = df['Data'].fillna(
                pd.Series([
                    (datetime(2023, 1, 1) + timedelta(days=i)).strftime('%d/%m/%Y')
                    for i in range(len(df))
                ])
            )

        # ID faltante → sequência lógica (igual ao seu)
        if df['ID'].isnull().any():
            max_id = int(df['ID'].max()) if not df['ID'].isnull().all() else 0
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
