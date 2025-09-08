import time
import csv
import copy
import os
from algoritmos import selection_sort, cycle_sort

# Estrutura dos arquivos
arquivos = {
    "crescente": {
        "conjunto-pequeno": "conjunto-pequeno/crescente.txt",
        "conjunto-medio": "conjunto-medio/crescente.txt",
        "conjunto-grande": "conjunto-grande/crescente.txt"
    },
    "decrescente": {
        "conjunto-pequeno": "conjunto-pequeno/decrescente.txt",
        "conjunto-medio": "conjunto-medio/decrescente.txt",
        "conjunto-grande": "conjunto-grande/decrescente.txt"
    },
    "aleatorio": {
        "conjunto-pequeno": "conjunto-pequeno/aleatorio.txt",
        "conjunto-medio": "conjunto-medio/aleatorio.txt",
        "conjunto-grande": "conjunto-grande/aleatorio.txt"
    }
}

def carregar_arquivo(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {nome_arquivo}")
    with open(nome_arquivo, "r") as f:
        return list(map(int, f.read().split()))

def medir_tempo(func, arr):
    inicio = time.time()
    func(arr)
    fim = time.time()
    return fim - inicio

def executar_testes():
    for tipo, conj in arquivos.items():
        for tamanho, caminho in conj.items():
            try:
                dados = carregar_arquivo(caminho)
                print(f"Carregados {len(dados)} elementos de {caminho}")
            except FileNotFoundError as e:
                print(f"Erro: {e}")
                continue

            nome_csv = f"{tamanho}-{tipo}.csv"
            
            tempos_selection = []
            tempos_cycle = []
            
            for execucao in range(1, 31):
                print(f"Executando {tamanho}-{tipo} - Execução {execucao}/30")
                
                try:
                    # Selection Sort
                    arr1 = copy.deepcopy(dados)
                    tempo1 = medir_tempo(selection_sort, arr1)
                    tempos_selection.append(tempo1)
                    
                    # Cycle Sort
                    arr2 = copy.deepcopy(dados)
                    tempo2 = medir_tempo(cycle_sort, arr2)
                    tempos_cycle.append(tempo2)
                    
                except Exception as e:
                    print(f"Erro durante a execução {execucao}: {e}")
                    continue
            
            with open(nome_csv, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Algoritmo", "Execucao", "Tempo(segundos)"])
                
                for i, tempo in enumerate(tempos_selection, 1):
                    writer.writerow(["SelectionSort", i, f"{tempo:.6f}"])
                
                for i, tempo in enumerate(tempos_cycle, 1):
                    writer.writerow(["CycleSort", i, f"{tempo:.6f}"])

            print(f"Resultados salvos em {nome_csv}")

if __name__ == "__main__":
    executar_testes()