import pygame
import sys
import random
import math
from itertools import combinations
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import shutil
import os

shutil.rmtree("fps", ignore_errors=True)
os.mkdir("fps")
shutil.rmtree("log", ignore_errors=True)
os.mkdir("log")

matplotlib.use("agg")

histograma = []
colisão = []
cada_mol = []

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 620, 608
x_grafico = 700
window = pygame.display.set_mode((WINDOW_WIDTH + x_grafico, WINDOW_HEIGHT))
pygame.display.set_caption("Particulas")


NUMERO_MOLECULAS = 2000

VEL = 50
RAIO = 2
MASSA = 1

VEL1 = 50
RAIO1 = 1
MASSA1 = 1


T_max = 2

chance = 0.7
cataliza = True
chance_catalize = 0.5
tempo_catalize = 10

# vel_maxima = max(VEL, VEL1)
vel_maxima = VEL


DT = 1 / (vel_maxima)


raio_maior = max(RAIO, RAIO1)
raio_maior *= 2

barra_cor = (0, 255, 0)

METADE = NUMERO_MOLECULAS // 2

cordenadas_possiveis = [(1.0, 1.0) for _ in range(NUMERO_MOLECULAS)]


WHITE = (255, 255, 255)


class Particle:
    def __init__(self, x, y, vel, raio, mass, color):
        self.x = x
        self.y = y

        self.raio = raio

        self.speed_x = random.uniform(-vel, vel)
        self.speed_y = random.uniform(-vel, vel)
        self.color = color
        self.tipo = 0
        self.massa = mass
        self.chance = chance
        self.catalizada = 0
        self.time_catalizador = 0

        self.existe = True

    def move(self):
        self.x += self.speed_x * DT
        self.y += self.speed_y * DT

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.raio)

    def colisao_parede(self):
        x_novo = self.x + self.speed_x
        y_novo = self.y + self.speed_y

        afasta_0_x = x_novo > self.x
        afasta_0_y = y_novo > self.y

        afasta_f_x = x_novo < self.x
        afasta_f_y = y_novo < self.y

        if ((self.x - self.raio) <= 0 and not afasta_0_x) or (
            (self.x + self.raio) >= WINDOW_WIDTH and not afasta_f_x
        ):
            self.speed_x *= -1
            if self.tipo == 0 and cataliza:
                self.color = (0, 255, 0)
                self.chance = chance_catalize
                self.time_catalizador = time.time()
                self.catalizada = 1

        if ((self.y - self.raio) <= 0 and not afasta_0_y) or (
            (self.y + self.raio) >= WINDOW_HEIGHT and not afasta_f_y
        ):
            self.speed_y *= -1
            if self.tipo == 0 and cataliza:
                self.color = (0, 255, 0)
                self.chance = chance_catalize
                self.catalizada = 1
                self.time_catalizador = time.time()

    def parar_catalização(self):
        if self.catalizada and (time.time() - self.time_catalizador) > tempo_catalize:
            self.catalizada = 0
            self.chance = chance
            self.color = (255, 0, 0)


class sistema:
    def __init__(self, particulas, DT):
        self.quantidade_vermelho = len(particulas)
        self.quantidade_azul = 0
        self.quantidade_vermelho_lista = []
        self.quantidade_azul_lista = []
        self.particulas = particulas
        self.DT=DT

    def velocidades(self):
        return np.array(
            [math.sqrt(p.speed_x**2 + p.speed_y**2) for p in self.particulas]
        )

    def massas(self):
        return np.array([p.massa for p in self.particulas])

    def simulacao_molecula(self, desenha):
        for particle in self.particulas:
            particle.move()
            particle.colisao_parede()
            particle.parar_catalização()
            if desenha:
                particle.draw()

    def colisoes_mol(self):
        combinacao = list(combinations(range(len(self.particulas)), 2))
        for index1, index2 in combinacao:
            mol1 = self.particulas[index1]
            mol2 = self.particulas[index2]
            if mol1.existe and mol2.existe:
                distancia = math.sqrt((mol1.x - mol2.x) ** 2 + (mol1.y - mol2.y) ** 2)
                if distancia <= (mol1.raio + mol2.raio):
                    chance_ = random.random()
                    distancia_futura = math.sqrt(
                        ((mol1.x + mol1.speed_x * self.DT) - (mol2.x + mol2.speed_x * self.DT))
                        ** 2
                        + ((mol1.y + mol1.speed_y * self.DT) - (mol2.y + mol2.speed_y * self.DT))
                        ** 2
                    )
                    aproximando = distancia_futura < distancia
                    if aproximando:
                        delta_r = (mol1.x - mol2.x, mol1.y - mol2.y)

                        delta_v = (
                            mol1.speed_x - mol2.speed_x,
                            mol1.speed_y - mol2.speed_y,
                        )

                        produto_interno = (
                            delta_v[0] * delta_r[0] + delta_v[1] * delta_r[1]
                        )

                        j = (2 * mol2.massa * mol1.massa * produto_interno) / (
                            distancia * (mol2.massa + mol1.massa)
                        )

                        j_x = (j * delta_r[0]) / distancia
                        j_y = (j * delta_r[1]) / distancia

                        mol1.speed_x -= j_x / mol1.massa
                        mol1.speed_y -= j_y / mol1.massa

                        mol2.speed_x += j_x / mol2.massa
                        mol2.speed_y += j_y / mol2.massa

                        chance_juntar = min((mol1.chance, mol2.chance))
                        if (
                            chance_ > chance_juntar
                            and mol1.tipo == 0
                            and mol2.tipo == 0
                        ):
                            self.quantidade_vermelho -= 2
                            self.quantidade_azul += 1
                            mol1.existe = False
                            mol2.color = (0, 0, 255)
                            mol2.tipo = 1
                            mol2.raio += 2
                            mol2.catalizada = 0
                            mol1.raio = 0

                            mol2.speed_x = (
                                mol2.speed_x * mol2.massa + mol1.speed_x * mol1.massa
                            ) / (mol1.massa + mol2.massa)

                            mol2.speed_y = (
                                mol2.speed_y * mol2.massa + mol1.speed_y * mol1.massa
                            ) / (mol1.massa + mol2.massa)
                            mol2.massa += mol1.massa

        self.particulas = [mol for mol in self.particulas if mol.existe]
        self.quantidade_azul_lista.append(self.quantidade_azul)
        self.quantidade_vermelho_lista.append(self.quantidade_vermelho)


def plot_dist_vel(axs, vels, vs, y_dist):
    # Crie um gráfico com o Matplotli
    axs[0, 0].hist(
        vels, density=True, label="Distribuição Verdadeira", bins=30
    )  # Exemplo de gráfico simples
    axs[0, 0].plot(vs, y_dist, c="0", label="Distribuição Maxwell-Boltzmann")

    axs[0, 0].set_ylim(0, np.max(y_dist) * 1.2)
    axs[0, 0].set_xlim(0, 100)
    axs[0, 0].set_yticks([])

    axs[0, 0].set_xlabel("Velocidade")


def plot_quantidade(axs, tempo, q_verm, q_azul):
    # Crie um gráfico com o Matplotlib
    axs[0, 1].plot(tempo, q_verm, "r")
    axs[0, 1].plot(tempo, q_azul, "b")
    axs[0, 1].set_xlabel("Tempo")
    axs[0, 1].set_ylabel("Quant.")


def plot_derivada(
    axs,
    tempo,
    list_deri_verm,
    list_deri_azul,
):
    axs[1, 1].plot(tempo[1:], list_deri_verm, "r")
    axs[1, 1].plot(tempo[1:], list_deri_azul, "b")
    axs[1, 1].set_xlabel("Tempo")
    axs[1, 1].set_ylabel("$d$ Quant./$dt$")


def plot_temp(axs, tempo, lista_tempo):
    axs[1, 0].plot(tempo, lista_tempo)
    axs[1, 0].set_xlabel("Tempo")
    axs[1, 0].set_ylabel("Temperatura")


def cria_dados_deriv(tempo, q_verm, q_azul, list_deri_verm, list_deri_azul):
    if len(tempo) > 1:
        derivada_verm = -((q_verm[-1] - q_verm[-2]) / (tempo[-1] - tempo[-2]))
        derivada_azul = (q_azul[-1] - q_azul[-2]) / (tempo[-1] - tempo[-2])
        list_deri_verm.append(derivada_verm)
        list_deri_azul.append(derivada_azul)


def cria_figura():
    fig, axs = plt.subplots(2, 2, figsize=(5, 6))
    return fig, axs


def extrai_dados(fig, axs):
    plt.tight_layout()

    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()

    axs[0, 0].clear()
    axs[0, 1].clear()
    axs[1, 0].clear()
    axs[1, 1].clear()
    imagem = pygame.image.fromstring(raw_data, size, "RGB")
    return imagem


def temperatura(meu_sistema, k):
    n_mol = len(meu_sistema.particulas)
    vels = meu_sistema.velocidades()
    massas = meu_sistema.massas()
    return ((1 / n_mol) * sum(massas * vels**2 / 2)) / k


def FMB(v, T, massa, k):
    mb = (
        massa
        * np.exp(-massa * v**2 / (2 * T * k))
        / (2 * np.pi * T * k)
        * 2
        * np.pi
        * v
    )
    return mb
def definir_x_y(particulas, WINDOW_HEIGHT, WINDOW_WIDTH):
    for i in range(len(particulas)):
        while True:
            colidem = False
            x = random.uniform(10, WINDOW_HEIGHT - 10)
            y = random.uniform(10, WINDOW_WIDTH - 10)

            for j in range(len(particulas)):
                if j != i:
                    D = ((x - particulas[j].x) ** 2 + (y - particulas[j].y) ** 2) ** (
                        1 / 2
                    )

                    if D <= (particulas[i].raio + particulas[j].raio):
                        colidem = True
            if not colidem:
                break
        particulas[i].x = x
        particulas[i].y = y

def main():
    pausa = False
    v_hist = True
    desenha = True

    particulas = [
        Particle(
            x,
            y,
            VEL,
            RAIO,
            MASSA,
            (255, 0, 0),
        )
        for x, y in cordenadas_possiveis
    ]
    # for x, y in cordenadas_possiveis2:
    #     particulas.append(
    #         Particle(
    #             x,
    #             y,
    #             VEL1,
    #             RAIO1,
    #             MASSA1,
    #             (0, 0, 255),
    #         )
    #     )

    definir_x_y(particulas,WINDOW_HEIGHT,WINDOW_WIDTH)

    meu_sistema = sistema(particulas,DT)

    clock = pygame.time.Clock()
    fps = 100

    frames = []

    T = 0.0
    tempo = []
    list_deri_verm = []
    list_deri_azul = []
    k = 1.38064852e-23

    vs = np.linspace(0, vel_maxima * 5, NUMERO_MOLECULAS)

    fig, axs = cria_figura()
    list_temp = []

    while True:
        frame_data = pygame.surfarray.array3d(window)
        frame_data = frame_data.swapaxes(0, 1)

        np.save(rf"fps/fps_{T}.npy", frame_data)
        # Append the frame_data to the file

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa
                elif event.key == pygame.K_h:
                    v_hist = not v_hist
                elif (
                    event.key == pygame.K_PLUS
                    or event.key == pygame.K_KP_PLUS
                    or event.key == pygame.K_EQUALS
                ):
                    fps += 10
                    print(fps)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    fps = max(10, fps - 10)
                    print(fps)
                elif event.key == pygame.K_d:
                    desenha = not desenha

        if not pausa:
            tempo.append(T)
            window.fill(WHITE)

            start = time.time()
            meu_sistema.colisoes_mol()
            end = time.time()
            colisão.append(start - end)

            start = time.time()
            meu_sistema.simulacao_molecula(desenha)
            end = time.time()
            cada_mol.append(start - end)

            cria_dados_deriv(
                tempo,
                meu_sistema.quantidade_vermelho_lista,
                meu_sistema.quantidade_azul_lista,
                list_deri_verm,
                list_deri_azul,
            )

            temp = temperatura(meu_sistema, k)
            list_temp.append(temp)
            y_dist = FMB(vs, temp, MASSA, k)
            start = time.time()

            if v_hist:
                # hist(meu_sistema.velocidades)

                plot_dist_vel(axs, meu_sistema.velocidades(), vs, y_dist)

                # Crie uma imagem a partir dos dados renderizados e desenhe-a na tela do Pygame

                plot_temp(axs, tempo, list_temp)

                plot_quantidade(
                    axs,
                    tempo,
                    meu_sistema.quantidade_vermelho_lista,
                    meu_sistema.quantidade_azul_lista,
                )
                plot_derivada(
                    axs,
                    tempo,
                    list_deri_verm,
                    list_deri_azul,
                )

                image_hist = extrai_dados(fig, axs)
                window.blit(image_hist, (x_grafico + 100, 0))

            end = time.time()
            histograma.append(start - end)
            pygame.display.flip()
            clock.tick(fps)
            # print(T)
            T += DT
            np.save(r"fps\tempo.npy", np.array(tempo + [DT]))
            np.save(r"log\tempo.npy", np.array(tempo))
            np.save(r"log\temperatura.npy", np.array(temp))
            np.save(
                r"log\quantidade_vermelho.npy",
                np.array(meu_sistema.quantidade_vermelho_lista),
            )
            np.save(
                r"log\quantidade_azul.npy", np.array(meu_sistema.quantidade_azul_lista)
            )

        if T >= T_max:
            print(f"colisão demora:{sum(colisão)/len(colisão)}")
            print(f"hist demora:{sum(histograma)/len(histograma)}")
            print(f"mol demora:{sum(cada_mol)/len(cada_mol)}")

            pygame.quit()

            break




if __name__ == "__main__":
    main()
