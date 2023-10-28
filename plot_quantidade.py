import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import curve_fit
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


def plot_quantidade(axs, temp, lista_verm, lista_azul):
    axs[0].scatter(temp, lista_verm, 0.1, c="r")
    axs[0].scatter(temp, lista_azul, 0.1, c="b")
    axs[0].set_xlabel("Tempo")
    axs[0].set_ylabel("Quant.")


fig, axs = plt.subplots(2, 1)
plot_quantidade(axs, temp, q_verm, q_azul)
# plot_derivada(axs, temp_novo, q_verm_novo, q_azul_novo)
plt.tight_layout()

plt.show()
