import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
import glob
import os
import re

# Configurar o estilo dos gráficos
plt.style.use('default')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.figsize'] = (12, 8)

# Caminho dos arquivos
caminho = r"C:\Users\VICTOR\Documents\estudos\paa"
arquivos = glob.glob(os.path.join(caminho, "*.csv"))

# Criar pasta principal para salvar as imagens
pasta_principal = os.path.join(caminho, "analise_completa")
os.makedirs(pasta_principal, exist_ok=True)

# Dicionário para armazenar todos os dados organizados
dados_organizados = {
    'pequeno': {'crescente': {}, 'decrescente': {}, 'aleatorio': {}},
    'medio': {'crescente': {}, 'decrescente': {}, 'aleatorio': {}},
    'grande': {'crescente': {}, 'decrescente': {}, 'aleatorio': {}}
}

# Processar cada arquivo
for arquivo in arquivos:
    nome_arquivo = os.path.basename(arquivo).replace(".csv", "")
    print(f"Processando: {nome_arquivo}")
    
    # Extrair categoria e tipo do nome do arquivo
    categoria = None
    tipo = None
    
    if 'pequeno' in nome_arquivo:
        categoria = 'pequeno'
    elif 'medio' in nome_arquivo:
        categoria = 'medio'
    elif 'grande' in nome_arquivo:
        categoria = 'grande'
    
    # --- CORRIGIDO: decrescente vem antes de crescente ---
    if 'decrescente' in nome_arquivo:
        tipo = 'decrescente'
    elif 'crescente' in nome_arquivo:
        tipo = 'crescente'
    elif 'aleatorio' in nome_arquivo:
        tipo = 'aleatorio'
    
    if not categoria or not tipo:
        print(f"  Ignorando arquivo: {nome_arquivo} - não foi possível determinar categoria/tipo")
        continue
    
    try:
        # Ler e processar o arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        # Processar manualmente as linhas
        tempos_selection = []
        tempos_cycle = []
        
        for i, linha in enumerate(linhas):
            # Pular cabeçalho
            if i == 0:
                continue
                
            partes = linha.strip().split(',')
            if len(partes) >= 3:
                algoritmo = partes[0]
                # Limpar o valor do tempo (remover ;;; se existir)
                tempo_str = re.sub(r';+$', '', partes[2]).strip()
                try:
                    tempo = float(tempo_str)
                    if algoritmo == 'SelectionSort':
                        tempos_selection.append(tempo)
                    elif algoritmo == 'CycleSort':
                        tempos_cycle.append(tempo)
                except ValueError as e:
                    print(f"  Erro ao converter tempo: {tempo_str} - {e}")
                    continue
        
        # Armazenar os dados
        dados_organizados[categoria][tipo]['SelectionSort'] = tempos_selection
        dados_organizados[categoria][tipo]['CycleSort'] = tempos_cycle
        
        print(f"  {categoria} {tipo}: SelectionSort({len(tempos_selection)}), CycleSort({len(tempos_cycle)})")
            
    except Exception as e:
        print(f"Erro ao processar {nome_arquivo}: {e}")
        continue

# Função para criar e salvar boxplots
def criar_boxplot(dados, categoria, tipo, pasta_destino):
    algoritmos = list(dados.keys())
    valores = [dados[algoritmo] for algoritmo in algoritmos]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    boxplot = ax.boxplot(valores, labels=algoritmos, patch_artist=True)
    
    # Adicionar cores
    colors = ['lightblue', 'lightcoral']
    for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.title(f'Boxplot - {categoria.capitalize()} {tipo.capitalize()}\nSelectionSort vs CycleSort', fontsize=14)
    plt.ylabel('Tempo (segundos)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salvar a imagem
    nome_arquivo = f"boxplot_{categoria}_{tipo}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Função para criar e salvar gráfico de barras (medianas)
def criar_barras_medianas(dados, categoria, tipo, pasta_destino):
    algoritmos = list(dados.keys())
    medianas = [statistics.median(dados[algoritmo]) for algoritmo in algoritmos]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.bar(algoritmos, medianas, color=['skyblue', 'lightcoral'])
    ax.set_title(f'Medianas - {categoria.capitalize()} {tipo.capitalize()}\nSelectionSort vs CycleSort', fontsize=14)
    ax.set_ylabel('Tempo (segundos)', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars, medianas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(medianas)*0.01, 
                f'{valor:.2f}s', ha='center', va='bottom', fontsize=11)
    
    plt.tight_layout()
    
    # Salvar a imagem
    nome_arquivo = f"medianas_{categoria}_{tipo}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Função para criar gráfico de distribuição
def criar_histograma(dados, categoria, tipo, pasta_destino):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['skyblue', 'lightcoral']
    for i, (algoritmo, tempos) in enumerate(dados.items()):
        ax.hist(tempos, alpha=0.7, label=algoritmo, bins=15, color=colors[i])
    
        ax.set_title(f'Distribuição - {categoria.capitalize()} {tipo.capitalize()}\nSelectionSort vs CycleSort', fontsize=14)
        ax.set_xlabel('Tempo (segundos)', fontsize=12)
        ax.set_ylabel('Frequência', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salvar a imagem
    nome_arquivo = f"histograma_{categoria}_{tipo}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Função para criar gráfico comparativo entre tipos de ordenação
def criar_comparacao_tipos(dados, categoria, pasta_destino):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    tipos = list(dados[categoria].keys())
    algoritmos = ['SelectionSort', 'CycleSort']
    colors = ['skyblue', 'lightcoral']
    
    # Preparar dados
    medianas_por_tipo = {tipo: [] for tipo in tipos}
    for tipo in tipos:
        for algoritmo in algoritmos:
            if algoritmo in dados[categoria][tipo]:
                medianas_por_tipo[tipo].append(statistics.median(dados[categoria][tipo][algoritmo]))
    
    # Configurar posições no gráfico
    x = np.arange(len(tipos))
    width = 0.35
    
    # Criar barras
    for i, algoritmo in enumerate(algoritmos):
        valores = [medianas_por_tipo[tipo][i] for tipo in tipos]
        ax.bar(x + i*width, valores, width, label=algoritmo, color=colors[i])
    
    ax.set_xlabel('Tipo de Ordenação', fontsize=12)
    ax.set_ylabel('Tempo Médio (segundos)', fontsize=12)
    ax.set_title(f'Comparação de Desempenho - {categoria.capitalize()}\nSelectionSort vs CycleSort', fontsize=14)
    ax.set_xticks(x + width/2)
    ax.set_xticklabels([t.capitalize() for t in tipos])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar a imagem
    nome_arquivo = f"comparacao_{categoria}.png"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo

# Criar gráficos para cada categoria e tipo
for categoria in dados_organizados:
    # Criar pasta para a categoria
    pasta_categoria = os.path.join(pasta_principal, categoria)
    os.makedirs(pasta_categoria, exist_ok=True)
    
    for tipo in dados_organizados[categoria]:
        if dados_organizados[categoria][tipo] and len(dados_organizados[categoria][tipo]) > 0:
            try:
                print(f"Criando gráficos para {categoria} {tipo}")
                
                # Criar boxplot
                criar_boxplot(
                    dados_organizados[categoria][tipo], 
                    categoria, 
                    tipo, 
                    pasta_categoria
                )
                
                # Criar gráfico de medianas
                criar_barras_medianas(
                    dados_organizados[categoria][tipo], 
                    categoria, 
                    tipo, 
                    pasta_categoria
                )
                
                # Criar histograma
                criar_histograma(
                    dados_organizados[categoria][tipo], 
                    categoria, 
                    tipo, 
                    pasta_categoria
                )
                
            except Exception as e:
                print(f"Erro ao criar gráficos para {categoria} {tipo}: {e}")
                continue

# Criar gráficos comparativos entre tipos de ordenação para cada categoria
for categoria in dados_organizados:
    try:
        print(f"Criando gráfico comparativo para {categoria}")
        criar_comparacao_tipos(dados_organizados, categoria, pasta_principal)
    except Exception as e:
        print(f"Erro ao criar gráfico comparativo para {categoria}: {e}")

# Criar resumo estatístico
resumo_estatistico = []
for categoria in dados_organizados:
    for tipo in dados_organizados[categoria]:
        for algoritmo in dados_organizados[categoria][tipo]:
            tempos = dados_organizados[categoria][tipo][algoritmo]
            if tempos and len(tempos) > 0:
                resumo_estatistico.append({
                    'Categoria': categoria,
                    'Tipo': tipo,
                    'Algoritmo': algoritmo,
                    'Média': statistics.mean(tempos),
                    'Mediana': statistics.median(tempos),
                    'Desvio Padrão': statistics.stdev(tempos) if len(tempos) > 1 else 0,
                    'Mínimo': min(tempos),
                    'Máximo': max(tempos),
                    'N': len(tempos)
                })

# Converter para DataFrame e salvar como CSV
if resumo_estatistico:
    df_resumo = pd.DataFrame(resumo_estatistico)
    df_resumo.to_csv(os.path.join(pasta_principal, "resumo_estatistico.csv"), index=False)
    
    # Criar tabela resumo formatada
    plt.figure(figsize=(14, 10))
    plt.axis('tight')
    plt.axis('off')
    table = plt.table(cellText=df_resumo.round(2).values,
                     colLabels=df_resumo.columns,
                     cellLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2)
    plt.title('Resumo Estatístico - SelectionSort vs CycleSort', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_principal, "tabela_resumo.png"), dpi=300, bbox_inches='tight')
    plt.close()

print(f"Análise concluída! Gráficos e estatísticas salvos em: {pasta_principal}")
