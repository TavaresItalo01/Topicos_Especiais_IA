
import random

import numpy as np

from knapsack import knapsack

class Individuo :
    #genes = list(range(10))
    #fitness = None
    def __init__(self, genes):
        self.genes = genes
        self.fitness = None
        print(f"Individuo criado") 

    def __repr__(self):
        return f"Genes : {self.genes}, Fiteness: {self.fitness}"

def criar_populacao_inicial(size) :
    populacao = list()

    for i in range(size) :
        ind = Individuo(list(random.randint(0, 1) for _ in range(20)))
        populacao.append(ind)
        
    for ind in populacao :
        print(ind.__repr__())

    return populacao

def roulette_wheel_selection(individuos, num_selecionados) :
    selecionados = list()
    total = 0

    for ind in individuos :
        total = total + ind.fitness

    i = 0 

    for i in range(num_selecionados) :

        ponteiro = random.randint(0, total)
        soma = 0
        j = 0 

        for j in range(len(individuos)) :
            soma = soma + individuos[j].fitness

            if ponteiro <= soma :
                selecionados.append(individuos[j])
                break
            
            j = j + 1
        
        i = i + 1

    return selecionados

def tournament_selection(population, tournament_size = 3) :
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda individuo: individuo.fitness)
        selected.append(winner)
    return selected      

def one_point_crossover(p1, p2, taxa_crossover=0.8):
    if random.random() < taxa_crossover :
        ponto = random.randint(1, len(p1) - 1) 
        filho1 = p1[:ponto] + p2[ponto:]
        filho2 =p2[:ponto] + p1[ponto:]
        return filho1, filho2
    else :
        return p1.copy(), p2.copy()
    
def two_point_crossover(p1, p2, taxa_crossover=0.8):

    if random.random() < taxa_crossover :
        ponto1 = random.randint(1, len(p1) - 2)
        ponto2 = random.randint(ponto1 + 1, len(p1) - 1)

        filho1 = p1[:ponto1] + p2[ponto1:ponto2] + p1[ponto2:]
        filho2 = p2[:ponto1] + p1[ponto1:ponto2] + p2[ponto2:]

        return filho1, filho2
    else :
        return p1.copy(), p2.copy()

def uniform_crossover(p1, p2, taxa_crossover=0.8):
    filho1 = []
    filho2 =[]

    for i in range(len(p1)) :
        if random.random() < taxa_crossover :
            filho1.append(p2[i])
            filho2.append(p1[i])
        else :
            filho1.append(p1[i])
            filho2.append(p2[i])

    return filho1, filho2

def mutation(ind, taxa_mutacao=0.02) :
    cromossomo_mutado = list(ind)

    for i in range(len(cromossomo_mutado)) :

        if random.random() < taxa_mutacao :
            if cromossomo_mutado[i] == 0:
                cromossomo_mutado[i] = 1
            else:
                cromossomo_mutado[i] = 0
    
    return cromossomo_mutado

def avaliar(populacao, dim=20):
    for ind in populacao:
        valor, _, valido = knapsack(ind.genes, dim)
        ind.fitness = valor if valido else 0


def elitismo(populacao, num_elites=2):
    return sorted(populacao, key=lambda x: x.fitness, reverse=True)[:num_elites]

def crossover(tipo, p1, p2):
    if tipo == "one_point":
        return one_point_crossover(p1, p2)
    elif tipo == "two_point":
        return two_point_crossover(p1, p2)
    else:
        return uniform_crossover(p1, p2)

def algoritmo_genetico(tipo_crossover, n_exec=30, geracoes=500, pop_size=50):
    
    resultados, historicos = [], []

    for _ in range(n_exec):
        pop = criar_populacao_inicial(pop_size)
        avaliar(pop)
        melhor_por_geracao = []

        for _ in range(geracoes):
            selecionados = tournament_selection(pop)
            filhos = []

            for i in range(0, pop_size, 2):
                f1, f2 = crossover(tipo_crossover, selecionados[i].genes, selecionados[i + 1].genes)
                f1 = mutation(f1, 0.02)
                f2 = mutation(f2, 0.02)
                filhos += [type(pop[0])(f1), type(pop[0])(f2)]

            avaliar(filhos)

            
            elites = elitismo(pop, 2)
            filhos = sorted(filhos, key=lambda x: x.fitness, reverse=True)
            filhos[-2:] = elites
            pop = filhos

            melhor_por_geracao.append(max(ind.fitness for ind in pop))

        historicos.append(melhor_por_geracao)
        resultados.append(melhor_por_geracao[-1])

    print(f"{tipo_crossover.upper()} | Média: {np.mean(resultados):.2f} | Desvio: {np.std(resultados):.2f}")
    return historicos, resultados

