import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plotar_graficos(df, total_vendas_produto):
    """Gera os gráficos de análise"""
    
    df['Data'] = pd.to_datetime(df['Data'])
    
    if 'TotalVenda' not in df.columns:
        df['TotalVenda'] = df['Quantidade'] * df['Preço']
    
    # Vendas mensais
    df_temp = df.copy()
    df_temp.set_index('Data', inplace=True)
    vendas_mensais = df_temp['TotalVenda'].resample('ME').sum()
    
    # Gráficos
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # 1) Tendência mensal
    meses = vendas_mensais.index.strftime('%b/%Y')
    axes[0].plot(meses, vendas_mensais, marker='o', linewidth=2, markersize=8)
    axes[0].set_title('Tendência de Vendas Mensais', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Mês')
    axes[0].set_ylabel('Total de Vendas (R$)')
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # 2) Vendas por produto (já vem em ordem fixa do datamain)
    cores = plt.cm.viridis(np.linspace(0, 1, len(total_vendas_produto)))
    bars = axes[1].bar(total_vendas_produto.index, total_vendas_produto, color=cores)
    axes[1].set_title('Total de Vendas por Produto', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Produto')
    axes[1].set_ylabel('Total de Vendas (R$)')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()