import os
import copy
import random
import numpy as np
import matplotlib.pyplot as plt

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


class HillClimbing:
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
            melhor_vizinho = None
            melhor_fitness_vizinho = fitness_atual

            for vizinho in vizinhos:
                fitness_vizinho = self.funcao_fitness(vizinho)
                eh_melhor = (
                    fitness_vizinho > melhor_fitness_vizinho
                    if self.maximizar
                    else fitness_vizinho < melhor_fitness_vizinho
                )
                if eh_melhor:
                    melhor_vizinho = vizinho
                    melhor_fitness_vizinho = fitness_vizinho

            if melhor_vizinho is not None:
                solucao_atual = copy.deepcopy(melhor_vizinho)
                fitness_atual = melhor_fitness_vizinho
            else:
                break

            self.historico.append(fitness_atual)

        return solucao_atual, fitness_atual, self.historico


if __name__ == "__main__":
    from Codigos import knapsack  # sua função já existente

    DIM = 20
    MAX_ITERACOES = 200
    N_SIMULACOES = 30

    resultados_finais = []

    for i in range(N_SIMULACOES):
        solucao_inicial = [int(random.random() > 0.8) for _ in range(DIM)]
        hill_climbing = HillClimbing(
            funcao_fitness=lambda sol: knapsack(sol, dim=DIM)[0],
            gerar_vizinhos=gerar_vizinhos_knapsack,
            maximizar=True,
        )
        _, melhor_fitness, historico = hill_climbing.executar(
            solucao_inicial, max_iteracoes=MAX_ITERACOES, verbose=False
        )

        # Média e desvio padrão do histórico da simulação
        media_exec = np.mean(historico)
        desvio_exec = np.std(historico)

        resultados_finais.append(melhor_fitness)

        print(f"\n=== Simulação {i+1} ===")
        print(f"Fitness final: {melhor_fitness}")
        print(f"Média do fitness (durante execução): {media_exec:.4f}")
        print(f"Desvio padrão do fitness (durante execução): {desvio_exec:.4f}")

    # Estatísticas globais (fitness finais das 30 execuções)
    media_global = np.mean(resultados_finais)
    desvio_global = np.std(resultados_finais)

    print("\n=== RESULTADOS GLOBAIS ===")
    print(f"Média dos fitness finais: {media_global:.4f}")
    print(f"Desvio padrão dos fitness finais: {desvio_global:.4f}")

    # Criar pasta "imagens" no Colab
    os.makedirs("../Imagens", exist_ok=True)

    # Boxplot dos fitness finais
    plt.boxplot(resultados_finais, vert=True, patch_artist=True)
    plt.title("Distribuição dos Fitness Finais - Hill Climbing (30 simulações)")
    plt.ylabel("Fitness")
    caminho_arquivo = "/content/imagens/boxplot_fitness.png"
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches="tight")

    print(f"\nBoxplot salvo em: {caminho_arquivo}")