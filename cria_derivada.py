import numpy as np
from scipy.interpolate import CubicSpline
from matplotlib import pyplot as plt


q_azul = np.load(r"log/quantidade_azul.npy")
q_verm = np.load(r"log/quantidade_vermelho.npy")
temp = np.load(r"log/tempo.npy")


min_temp = temp.min()
max_temp = temp.max()


temp_novo = np.linspace(min_temp, max_temp, len(temp) * 10)

spline_azul = CubicSpline(temp, q_azul)


q_azul_novo = spline_azul(temp_novo)

spline_verm = CubicSpline(temp, q_verm)


q_verm_novo = spline_verm(temp_novo)


def plot_derivada(
    tempo,
    list_verm,
    list_azul,
):
    list_derv_verm = []
    list_derv_azul = []
    for index in range(1, len(list_verm)):
        derivada_verm = (list_verm[index] - list_verm[index - 1]) / tempo[index]
        derivada_azul = (list_azul[index] - list_azul[index - 1]) / tempo[index]

        list_derv_verm.append(derivada_verm)
        list_derv_azul.append(derivada_azul)

    plt.plot(tempo[1:], list_derv_verm, "r")
    plt.plot(tempo[1:], list_derv_azul, "b")
    plt.xlabel("Tempo")
    plt.ylabel("$d$ Quant./$dt$")
    plt.show()


plot_derivada(temp_novo, q_verm_novo, q_azul_novo)
