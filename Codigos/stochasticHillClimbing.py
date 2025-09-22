import copy
import random

def gerar_vizinhos_knapsack(solucao, n_vizinhos=10):
    vizinhos = []
    n_itens = len(solucao)
    sorted_pos = []

    for i in range(n_vizinhos):
        pos = random.randint(0, n_itens - 1)
        if pos in sorted_pos:
            continue
        vizinho = solucao.copy()
        vizinho[pos] = 1 - vizinho[pos]  # flip do bit
        vizinhos.append(vizinho)
        sorted_pos.append(pos)

    return vizinhos


# ---------------------------
# Stochastic Hill Climbing
# ---------------------------
class StochasticHillClimbing:
    def __init__(self, funcao_fitness, gerar_vizinhos, maximizar=True):
        self.funcao_fitness = funcao_fitness
        self.gerar_vizinhos = gerar_vizinhos
        self.maximizar = maximizar
        self.historico = []

    def executar(self, solucao_inicial, max_iteracoes=1000, verbose=False):
        solucao_atual = copy.deepcopy(solucao_inicial)
        fitness_atual = self.funcao_fitness(solucao_atual)
        self.historico = [fitness_atual]
        iteracao = 0

        while iteracao < max_iteracoes:
            iteracao += 1
            vizinhos = self.gerar_vizinhos(solucao_atual)
            candidatos_melhores = []

            # Seleciona todos os vizinhos que são melhores que a solução atual
            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)
                eh_melhor = (
                    fitness_vizinho > fitness_atual
                    if self.maximizar
                    else fitness_vizinho < fitness_atual
                )
                if eh_melhor:
                    candidatos_melhores.append((vizinho, fitness_vizinho))

            if candidatos_melhores:
                # Escolhe aleatoriamente um vizinho melhor
                vizinho_escolhido, fitness_vizinho = random.choice(candidatos_melhores)
                solucao_atual = copy.deepcopy(vizinho_escolhido)
                fitness_atual = fitness_vizinho
                self.historico.append(fitness_atual)
            else:
                break

        return solucao_atual, fitness_atual, self.historico