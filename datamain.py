from simulacao import simular_dados, limpar_dados
import os
import pandas as pd
import sqlite3
from gerar_excel import executar_consultas_e_gerar_excel
from graficos_mensais import plotar_graficos

def criar_banco_vendas(df, nome_banco="vendas.db"):
    """Cria banco SQLite e importa os dados"""
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        ID INTEGER PRIMARY KEY,
        Data TEXT,
        Produto TEXT,
        Categoria TEXT,
        Quantidade INTEGER,
        Preço REAL
    );
    ''')
    
    cursor.execute("DELETE FROM vendas;")
    for _, row in df.iterrows():
        cursor.execute('''
        INSERT INTO vendas (ID, Data, Produto, Categoria, Quantidade, Preço)
        VALUES (?, ?, ?, ?, ?, ?);
        ''', (
            int(row['ID']),
            row['Data'].strftime('%Y-%m-%d'),
            row['Produto'],
            row['Categoria'],
            int(row['Quantidade']),
            float(row['Preço'])
        ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    
    # 1. Simulação e limpeza
    df = simular_dados()
    df = limpar_dados(df)
    
    # 2. Salva CSV
    df.to_csv("data_clean.csv", index=False, sep=';', encoding='utf-8-sig')
    
    # 3. Cria banco
    criar_banco_vendas(df)
    
    # 4. Prepara dados para os gráficos
    df_clean = pd.read_csv("data_clean.csv", sep=';', encoding='utf-8-sig')
    df_clean['Data'] = pd.to_datetime(df_clean['Data'])
    df_clean['Quantidade'] = df_clean['Quantidade'].astype(int)
    df_clean['Preço'] = df_clean['Preço'].astype(float)
    df_clean['TotalVenda'] = df_clean['Quantidade'] * df_clean['Preço']
    
    ordem_fixa = sorted(df_clean['Produto'].unique())
    total_vendas_produto = (df_clean.groupby('Produto')['TotalVenda']
                                     .sum()
                                     .reindex(ordem_fixa))
    
    # 5. Executa consultas SQL e gera Excel com gráficos
    df_consulta1, df_consulta2 = executar_consultas_e_gerar_excel(df_clean, total_vendas_produto, "vendas.db")
    
    # 6. Mostra os gráficos
    plotar_graficos(df_clean, total_vendas_produto)