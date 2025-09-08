import random

# Defina aqui a quantidade de números que você quer gerar
qtd_numeros = 60000  

# Geração do vetor crescente
crescente = list(range(1, qtd_numeros + 1))

# Geração do vetor decrescente
decrescente = list(range(qtd_numeros, 0, -1))

# Geração do vetor aleatório
aleatorio = [random.randint(1, qtd_numeros) for _ in range(qtd_numeros)]

# Salvando nos arquivos
with open("crescente.txt", "w") as f:
    f.write(" ".join(map(str, crescente)))

with open("decrescente.txt", "w") as f:
    f.write(" ".join(map(str, decrescente)))

with open("aleatorio.txt", "w") as f:
    f.write(" ".join(map(str, aleatorio)))

print("Arquivos gerados com sucesso!")
