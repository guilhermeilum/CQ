import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


q_azul = np.load(r"log/quantidade_azul.npy")
q_verm = np.load(r"log/quantidade_vermelho.npy")
temp = np.load(r"log/tempo.npy")


min_temp = temp.min()
max_temp = temp.max()


temp_novo = np.linspace(min_temp, max_temp, (len(temp) * 1000) // 3 * 3)

spline_azul = CubicSpline(temp, q_azul)

q_azul_novo = spline_azul(temp_novo)

spline_verm = CubicSpline(temp, q_verm)

q_verm_novo = spline_verm(temp_novo)

cons_incial = q_verm_novo[0]


def func_verm(t, k):
    return 1 / cons_incial + k * t


popt_verm, _ = curve_fit(func_verm, temp_novo, 1 / q_verm_novo)


def plot_quantidade_inv(ax, temp, popt_verm, lista_verm):
    funcao = func_verm(temp, *popt_verm)
    ax.scatter(temp, 1 / lista_verm, 0.1, c="r")
    ax.plot(temp, funcao, "r")
    ax.text(
        min(temp),
        max(funcao),
        f"k = {round(popt_verm[0],6)}",
    )
    ax.set_xlabel("Tempo")
    ax.set_ylabel("1 / [A]")


def plot_quantidade(
    ax,
    tempo,
    list_verm,
    list_azul,
):
    ax.scatter(tempo, list_verm, 0.1, c="r")
    ax.scatter(tempo, list_azul, 0.1, c="b")
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Quant.")


def plot_derivada(ax, temp, lista_verm, popt):
    derivada_list = []
    for i in range(1, len(lista_verm)):
        derivada_list.append(
            -((lista_verm[i] - lista_verm[i - 1]) / (temp[i] - temp[i - 1]))
        )
    ax.scatter(temp[1:], derivada_list, 0.1, c="r")
    ax.plot(temp[1:], popt[0] * lista_verm[1:] ** 2)
    ax.set_xlabel("Tempo")
    ax.set_ylabel("$d$ Quant./ $dt$")




fig, axs = plt.subplots(1, 3)
plot_quantidade(axs[0], temp_novo, q_verm_novo, q_azul_novo)
plot_quantidade_inv(axs[1], temp, popt_verm, q_verm)
plot_derivada(axs[2], temp_novo, q_verm_novo, popt_verm)
plt.tight_layout()

plt.show()
