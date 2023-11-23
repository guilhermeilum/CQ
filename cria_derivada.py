import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


q_azul = np.load(r"log/quantidade_azul.npy")
q_verm = np.load(r"log/quantidade_vermelho.npy")
temp = np.load(r"log/tempo.npy")

cons_incial = q_verm[0]


def func_verm(t, k):
    return 1 / cons_incial + k * t


popt_verm, _ = curve_fit(func_verm, temp, 1 / q_verm)


def plot_quantidade_inv(ax, temp, popt_verm, lista_verm):
    funcao = func_verm(temp, *popt_verm)
    ax.scatter(temp, 1 / lista_verm, 0.1, c="r", label="Inverso da quantidade")
    ax.plot(temp, funcao, "r", label="Fit inverso")
    ax.text(
        max(temp) / 10 * 8,
        max(funcao) / 10 * 3,
        f"k = {round(popt_verm[0],6)}",
    )
    ax.legend()
    ax.set_xlabel("Tempo")
    ax.set_ylabel("1 / [A]")


def plot_quantidade(
    ax,
    tempo,
    list_verm,
    list_azul,
):
    ax.scatter(tempo, list_verm, 0.1, c="r", label="Quantidade vermelhos")
    ax.scatter(tempo, list_azul, 0.1, c="b", label="Quantidade azuis")
    ax.legend()
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Quant.")


def plot_derivada(ax, temp, lista_verm, popt):
    derivada_list = []
    for i in range(1, len(lista_verm)):
        derivada_list.append(
            -((lista_verm[i] - lista_verm[i - 1]) / (temp[i] - temp[i - 1]))
        )
    ax.plot(temp[1:], derivada_list, label="Derivada númerica")
    ax.plot(temp[1:], popt[0] * lista_verm[1:] ** 2, label="Derivada $A^2k$")
    ax.legend()
    ax.set_xlabel("Tempo")
    ax.set_ylabel("$d$ Quant./ $dt$")


fig, axs = plt.subplots(3, 1)
plot_quantidade(axs[0], temp, q_verm, q_azul)
plot_quantidade_inv(axs[1], temp, popt_verm, q_verm)
plot_derivada(axs[2], temp, q_verm, popt_verm)
plt.tight_layout()
plt.savefig("Fits_catalizado.png", dpi=600)

plt.show()
