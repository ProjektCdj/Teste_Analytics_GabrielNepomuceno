from datetime import datetime, timedelta
import random
import pandas as pd

# Seed fixa para garantir mesmos resultados sempre
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

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

# Lista de produtos em ordem fixa para referência
produtos_ordem = [p[0] for p in produtos]

# Dicionário de preços FIXOS (não aleatórios)
PRECOS_FIXOS = {
    "Notebook": 3500.00,
    "Smartphone": 2500.00,
    "Camiseta": 50.00,
    "Tênis": 300.00,
    "Geladeira": 2800.00,
    "Micro-ondas": 500.00,
    "Livro": 70.00,
    "Caneta": 8.00,
    "Bicicleta": 1800.00,
    "Bola": 120.00
}

# Geração de Data - sequencial
def gerar_data(i):
    """Gera datas sequenciais ao longo do ano"""
    data_inicial = datetime(2023, 1, 1)
    dias_desde_inicio = i * 6  # 6 dias entre cada registro
    dias_desde_inicio = min(dias_desde_inicio, 364)
    return data_inicial + timedelta(days=dias_desde_inicio)

# Geração de Preços - AGORA FIXO!
def gerar_preco(produto):
    """Retorna preço fixo para cada produto"""
    return PRECOS_FIXOS.get(produto, 100.00)

# Simulação dos dados
def simular_dados():
    dados = []
    for i in range(1, num_registros + 1):
        # Produto segue padrão cíclico mas previsível
        produto, categoria = produtos[i % len(produtos)]
        
        # Quantidade: padrão fixo baseado em i (1 a 10)
        quantidade = (i % 10) + 1
        
        # Preço FIXO por produto
        preco = gerar_preco(produto)
        
        # Data sequencial
        data = gerar_data(i).strftime('%Y-%m-%d')

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

        if df['Produto'].isnull().any():
            produto_padrao = produtos_list[0]
            df['Produto'] = df['Produto'].fillna(produto_padrao)

        if df['Categoria'].isnull().any():
            df['Categoria'] = df.apply(
                lambda row: categorias_dict.get(row['Produto'], "Outros")
                if pd.isnull(row['Categoria']) else row['Categoria'],
                axis=1
            )

        if df['Quantidade'].isnull().any():
            quantidade_padrao = int(df['Quantidade'].median()) if df['Quantidade'].notnull().any() else 1
            df['Quantidade'] = df['Quantidade'].fillna(quantidade_padrao)

        if df['Preço'].isnull().any():
            # Usar preços fixos
            df['Preço'] = df.apply(
                lambda row: PRECOS_FIXOS.get(row['Produto'], 100.00) 
                if pd.isnull(row['Preço']) else row['Preço'],
                axis=1
            )

        if df['Data'].isnull().any():
            df['Data'] = df['Data'].fillna(
                pd.Series([
                    (datetime(2023, 1, 1) + timedelta(days=i*6)).strftime('%Y-%m-%d')
                    for i in range(len(df))
                ])
            )

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
    df['Data'] = pd.to_datetime(df['Data'])
    return df