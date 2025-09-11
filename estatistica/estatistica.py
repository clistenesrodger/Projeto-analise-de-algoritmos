import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminhos dos arquivos CSV
arquivos = {
    "conjunto-grande-crescente": r"C:\Users\VICTOR\Documents\estudos\paa\conjunto-grande-crescente.csv",
    "conjunto-medio-crescente": r"C:\Users\VICTOR\Documents\estudos\paa\conjunto-medio-crescente.csv",
    "conjunto-pequeno-crescente": r"C:\Users\VICTOR\Documents\estudos\paa\conjunto-pequeno-crescente.csv",
}

# Pasta de saída (mesma do script)
saida_dir = r"C:\Users\VICTOR\Documents\estudos\paa\estatistica"

# Ler os arquivos
dataframes = {}
for nome, caminho in arquivos.items():
    try:
        df = pd.read_csv(caminho)
        dataframes[nome] = df
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")

# Gerar histogramas e boxplots
for nome, df in dataframes.items():
    if isinstance(df, pd.DataFrame):
        # Histograma
        plt.figure(figsize=(10, 6))
        for alg in df["Algoritmo"].unique():
            subset = df[df["Algoritmo"] == alg]
            plt.hist(subset["Tempo(segundos)"], bins=10, alpha=0.6, label=alg)
        plt.title(f"Histograma dos Tempos - {nome}")
        plt.xlabel("Tempo (segundos)")
        plt.ylabel("Frequência")
        plt.legend()
        hist_path = os.path.join(saida_dir, f"histograma_{nome}.png")
        plt.savefig(hist_path)
        plt.close()

        # Boxplot
        plt.figure(figsize=(8, 6))
        df.boxplot(column="Tempo(segundos)", by="Algoritmo")
        plt.title(f"Boxplot dos Tempos - {nome}")
        plt.suptitle("")
        plt.ylabel("Tempo (segundos)")
        boxplot_path = os.path.join(saida_dir, f"boxplot_{nome}.png")
        plt.savefig(boxplot_path)
        plt.close()

        print(f"Arquivos salvos: {hist_path} e {boxplot_path}")
