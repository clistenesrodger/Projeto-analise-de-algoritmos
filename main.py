import time
import csv
import os
from algoritmos import selection_sort, cycle_sort

# Estrutura dos arquivos (mantida igual).
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
    inicio = time.perf_counter()  # Mais preciso para intervalos curtos
    func(arr)
    return time.perf_counter() - inicio

def verificar_ordenacao(arr):
    # Verifica se o array está ordenado corretamente
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

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
            resultados = []

            # Warm-up: Executa cada algoritmo uma vez sem medir
            selection_sort(dados.copy())
            cycle_sort(dados.copy())

            for execucao in range(30):
                print(f"Executando {tamanho}-{tipo} - Execução {execucao+1}/30")
                
                # Intercala a ordem dos algoritmos a cada execução
                for algoritmo in [selection_sort, cycle_sort]:
                    arr_copia = dados.copy()  # Cópia superficial (rápida)
                    tempo = medir_tempo(algoritmo, arr_copia)
                    
                    # Valida a ordenação
                    if not verificar_ordenacao(arr_copia):
                        print(f"Erro: {algoritmo.__name__} não ordenou corretamente!")
                    
                    resultados.append({
                        "Algoritmo": algoritmo.__name__,
                        "Execucao": execucao + 1,
                        "Tempo": tempo
                    })

            # Salva os resultados no CSV
            with open(nome_csv, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Algoritmo", "Execucao", "Tempo(segundos)"])
                for r in resultados:
                    writer.writerow([r["Algoritmo"], r["Execucao"], f"{r['Tempo']:.6f}"])

            print(f"Resultados salvos em {nome_csv}")

if __name__ == "__main__":
    executar_testes()