import numpy as np
import random

# Parâmetros do problema
cargas = {
    'C1': (480, 18, 310),  # (volume por tonelada, peso total, lucro por tonelada)
    'C2': (650, 15, 380),
    'C3': (580, 23, 350),
    'C4': (390, 12, 285)
}

compartimentos = {
    'D': (6800, 10),  # (volume máximo, peso máximo)
    'C': (8700, 16),
    'T': (5300, 8)
}

# Função de fitness
def fitness(individuo):
    lucro = 0
    penalidade = 0
    
    # Avaliando cada compartimento
    for compartimento, (volume_max, peso_max) in compartimentos.items():
        volume_total = 0
        peso_total = 0
        
        # Somando volumes e pesos para cada compartimento
        for carga, (volume_unit, peso_total_carga, lucro_por_ton) in cargas.items():
            qtd = individuo[carga + '_' + compartimento]
            volume_total += qtd * volume_unit
            peso_total += qtd
            
            lucro += qtd * lucro_por_ton
        
        # Penalidades se exceder o volume ou peso
        if volume_total > volume_max:
            penalidade += (volume_total - volume_max)
        if peso_total > peso_max:
            penalidade += (peso_total - peso_max)
    
    return lucro - penalidade * 1000  # Penalidade grande para soluções inválidas

# Inicializando a população
def inicializa_populacao(tamanho_pop):
    populacao = []
    for _ in range(tamanho_pop):
        individuo = {carga + '_' + compartimento: np.random.uniform(0, 5)
                     for carga in cargas for compartimento in compartimentos}
        populacao.append(individuo)
        # imprime_cromossomos(individuo)
    return populacao

# Seleção por torneio
def selecao_torneio(populacao, k=3):
    torneio = random.sample(populacao, k)
    melhor_individuo = max(torneio, key=fitness)
    return melhor_individuo

# Crossover de um ponto
def crossover(pai1, pai2):
    filho1, filho2 = pai1.copy(), pai2.copy()
    ponto_de_corte = random.randint(1, len(pai1) - 1)
    
    chaves = list(pai1.keys())
    for i in range(ponto_de_corte, len(pai1)):
        chave = chaves[i]
        filho1[chave], filho2[chave] = filho2[chave], filho1[chave]
    
    return filho1, filho2

# Mutação
def mutacao(individuo, taxa_mutacao=0.1):
    for gene in individuo:
        if random.random() < taxa_mutacao:
            individuo[gene] = np.random.uniform(0, 5)
    return individuo

# Algoritmo Genético
def algoritmo_genetico(tamanho_pop, geracoes, taxa_mutacao=0.1, taxa_crossover=0.8):
    # Inicializar população
    populacao = inicializa_populacao(tamanho_pop)
    
    # Executar por um número de gerações
    for geracao in range(geracoes):
        nova_populacao = []
        
        # Gerar nova população com seleção, crossover e mutação
        while len(nova_populacao) < tamanho_pop:
            pai1 = selecao_torneio(populacao)
            pai2 = selecao_torneio(populacao)
            
            # Crossover
            if random.random() < taxa_crossover:
                filho1, filho2 = crossover(pai1, pai2)
            else:
                filho1, filho2 = pai1.copy(), pai2.copy()
            
            # Mutação
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            
            # Adicionar filhos na nova população
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        
        # Substituir a população anterior
        populacao = nova_populacao[:tamanho_pop]
        
        # Melhor indivíduo da geração
        melhor_individuo = max(populacao, key=fitness)
        melhor_aptidao = fitness(melhor_individuo)
        
        print(f'Geração {geracao + 1}: Melhor aptidão = {melhor_aptidao:.2f}')
    
    # Melhor solução encontrada
    melhor_individuo = max(populacao, key=fitness)
    return melhor_individuo

# Exibir cromossomos
def imprime_cromossomos(individuo):
    print("Melhor solução encontrada:")
    for carga in cargas:
        print(f'  {carga}:')
        for compartimento in compartimentos:
            qtd = individuo[carga + '_' + compartimento]
            print(f'    {compartimento}: {qtd:.2f} toneladas')

# Executar o algoritmo genético
melhor_solucao = algoritmo_genetico(tamanho_pop=50, geracoes=50, taxa_mutacao=0.1, taxa_crossover=0.8)

# Imprimir a melhor solução encontrada
imprime_cromossomos(melhor_solucao)