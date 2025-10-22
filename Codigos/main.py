import random
import numpy as np
import matplotlib.pyplot as plt

from individuos import (
    algoritmo_genetico,
)


# Execução das 3 versões do Algoritmo Genético

if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)

    historicos_um_ponto, resultados_um_ponto = algoritmo_genetico("one_point")
    historicos_dois_pontos, resultados_dois_pontos = algoritmo_genetico("two_point")
    historicos_uniforme, resultados_uniforme = algoritmo_genetico("uniform")

    
    # Gráfico de convergência
    plt.figure(figsize=(10, 6))
    plt.plot(np.mean(historicos_um_ponto, axis=0), label="Crossover 1 ponto")
    plt.plot(np.mean(historicos_dois_pontos, axis=0), label="Crossover 2 pontos")
    plt.plot(np.mean(historicos_uniforme, axis=0), label="Crossover uniforme")
    plt.title("Convergência do AG para o problema Knapsack (20 dimensões)")
    plt.xlabel("Geração")
    plt.ylabel("Melhor fitness médio")
    plt.legend()
    plt.grid(True)
    caminho_arquivo = "../imagens/grafico_convergencia_ag.png"
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches="tight")
    plt.show()

    
    # Boxplot comparativo
    resultados_hc = [1042, 974, 1009, 1011, 1042, 1030, 1042, 1019, 1000, 1031, 1017, 942, 1042, 1024, 957, 1037, 1031, 898, 1042, 993,1031, 975, 997, 981, 973, 1019, 1042, 1000, 980, 1037]

    resultados_shc = [945, 784, 784, 960, 873, 766, 951, 823, 893, 909, 817, 1037, 936, 869, 788, 870, 927, 811, 878, 825, 911, 856, 811, 833, 871, 871, 898, 869, 897, 880]

    dados_boxplot = [
        resultados_um_ponto,
        resultados_dois_pontos,
        resultados_uniforme,
        resultados_hc,
        resultados_shc,
    ]
    labels = [
        "AG 1 ponto",
        "AG 2 pontos",
        "AG uniforme",
        "Hill Climbing",
        "Stochastic HC",
    ]

    plt.figure(figsize=(10, 6))
    plt.boxplot(dados_boxplot, patch_artist=True, labels=labels)
    plt.title("Comparação de desempenho - AGs vs Hill Climbing")
    plt.ylabel("Fitness final")
    plt.grid(True)
    caminho_arquivo = "../imagens/boxplot_comparativo_ag.png"
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches="tight")
    plt.show()



