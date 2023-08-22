import pygame
import sys
import random
import math
from itertools import combinations
import numpy as np
import imageio
import time
import numpy as np

histograma = []
colisão = []
cada_mol = []

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 620, 608
x_grafico = 500
window = pygame.display.set_mode((WINDOW_WIDTH + x_grafico, WINDOW_HEIGHT))
pygame.display.set_caption("Particulas")


NUMERO_MOLECULAS = 1000


VEL = 40
RAIO = 5
MASSA = 1
COR = (255, 0, 0)

VEL1 = 40
RAIO1 = 5
MASSA1 = 1
COR1 = (0, 0, 255)

vel_maxima = max(VEL, VEL1)

DT = 1 / (vel_maxima)


raio_maior = max(RAIO, RAIO1)
raio_maior *= 2

barra_cor = (0, 255, 0)

METADE = NUMERO_MOLECULAS // 2

WHITE = (255, 255, 255)


def move(coordenadas, velocidades, DT):
    coordenadas_novas = coordenadas + velocidades * DT
    return coordenadas_novas


def draw(window, cores, coordenadas, raios):
    [
        pygame.draw.circle(window, cor, xy, raio)
        for cor, xy, raio in zip(cores, coordenadas, raios)
    ]


def colisao_parede(coordenadas, raios, velocidades, DT):
    coordenadas_novas = move(coordenadas, velocidades, DT)

    afasta_0_x = coordenadas_novas[:, 0] > coordenadas[:, 0]
    afasta_0_y = coordenadas_novas[:, 1] > coordenadas[:, 1]

    afasta_f_x = coordenadas_novas[:, 0] < coordenadas[:, 0]
    afasta_f_y = coordenadas_novas[:, 1] < coordenadas[:, 1]

    coordenadas_mais_raio = coordenadas + raios[:, np.newaxis]
    coordenadas_menos_raio = coordenadas - raios[:, np.newaxis]

    velocidades_novas = np.zeros(velocidades.shape)

    velocidades_novas[:, 0] = np.where(
        np.logical_and(coordenadas_menos_raio[:, 0] <= 0, np.logical_not(afasta_0_x)),
        -velocidades[:, 0],
        velocidades[:, 0],
    )
    velocidades_novas[:, 0] = np.where(
        np.logical_and(
            coordenadas_mais_raio[:, 0] >= WINDOW_WIDTH, np.logical_not(afasta_f_x)
        ),
        -velocidades[:, 0],
        velocidades[:, 0],
    )
    velocidades_novas[:, 1] = np.where(
        np.logical_and(coordenadas_menos_raio[:, 1] <= 0, np.logical_not(afasta_0_y)),
        -velocidades[:, 1],
        velocidades[:, 1],
    )
    velocidades_novas[:, 1] = np.where(
        np.logical_and(
            coordenadas_mais_raio[:, 1] >= WINDOW_HEIGHT, np.logical_not(afasta_f_y)
        ),
        -velocidades[:, 1],
        velocidades[:, 1],
    )

    return velocidades_novas


def colisoes_mol(coordenadas, velocidades, DT):
    for mol in coordenadas:
        distancia = 
        if distancia <= (mol1.radius + mol2.radius):
            distancia_futura = math.sqrt(
                ((mol1.x + mol1.speed_x * DT) - (mol2.x + mol2.speed_x * DT)) ** 2
                + ((mol1.y + mol1.speed_y * DT) - (mol2.y + mol2.speed_y * DT)) ** 2
            )
            aproximando = distancia_futura < distancia
            if aproximando:
                delta_r = (mol1.x - mol2.x, mol1.y - mol2.y)

                delta_v = (mol1.speed_x - mol2.speed_x, mol1.speed_y - mol2.speed_y)

                produto_interno = delta_v[0] * delta_r[0] + delta_v[1] * delta_r[1]

                j = (2 * mol2.massa * mol1.massa * produto_interno) / (
                    distancia * (mol2.massa + mol1.massa)
                )

                j_x = (j * delta_r[0]) / distancia
                j_y = (j * delta_r[1]) / distancia

                vel_media1 = math.sqrt(mol1.speed_x**2 + mol1.speed_y**2)
                vel_media2 = math.sqrt(mol2.speed_x**2 + mol2.speed_y**2)

                velocidades.remove(vel_media1)
                velocidades.remove(vel_media2)

                mol2.speed_x += j_x / mol2.massa
                mol2.speed_y += j_y / mol2.massa

                mol1.speed_x -= j_x / mol1.massa
                mol1.speed_y -= j_y / mol1.massa

                vel_media1 = math.sqrt(mol1.speed_x**2 + mol1.speed_y**2)
                vel_media2 = math.sqrt(mol2.speed_x**2 + mol2.speed_y**2)

                velocidades.append(vel_media1)
                velocidades.append(vel_media2)


def coordenadas(quantidade, raios):
    """Cria as coordenadas sem conhecidir o local de cada particula.

    Args:
        quantidade (int): Quantidade de particulas
        raios (np.array): Matriz de raios das particulas

    Returns:
        coordenadas_matriz (np.array): Matriz de coordenadas sendo x,y cada linha.
    """
    coordenadas_matriz = np.zeros((quantidade, 2))
    for i in range(quantidade):
        raio = raios[i]
        while True:
            x = random.uniform(10, WINDOW_WIDTH - 10)
            y = random.uniform(10, WINDOW_HEIGHT - 10)
            cordenada = np.array([x, y])

            distancia = np.sqrt(np.sum((coordenadas_matriz - cordenada) ** 2, axis=1))
            if all(distancia > (raio + raios)):
                break

        coordenadas_matriz[i][0] = x
        coordenadas_matriz[i][1] = y
    return coordenadas_matriz


def cria_particulas(quantidade, vel, raio, massa, cor):
    """Cria as matrizes nescessarias para a simulação, menos a matriz de coordenadas.

    Args:
        quantidade (int): Quantidade de particulas com determinadas propriedades.
        vel (int): Velociade modulo maximo da velociadas
        raio (int): Raio da particula.
        massa (int): Massa da paticula
        cor (tupla): Tupla de RGB das particulas.

    Returns:
        matriz_vels: Matriz das velocidades sendo x,y.
        matriz_raios: Matriz de raios.
        matriz_massas: Matriz de massas.
        matriz_cores: Matriz de cores.
    """
    matriz_vels = np.array(
        [
            [random.uniform(-vel, vel), random.uniform(-vel, vel)]
            for _ in range(quantidade)
        ]
    )

    matriz_raios = np.array([raio for _ in range(quantidade)])

    matriz_massas = np.array([massa for _ in range(quantidade)])

    matriz_cores = np.array([cor for _ in range(quantidade)])

    return matriz_vels, matriz_raios, matriz_massas, matriz_cores


def hist(lista_vel):
    bins = 200
    hist, _ = np.histogram(lista_vel, bins=bins, range=(0, 1400))
    bin_width = x_grafico / bins

    # Desenhar o histograma
    for i, count in enumerate(hist):
        bar_height = int((count / 20) * WINDOW_HEIGHT)

        bar_rect = pygame.Rect(
            WINDOW_WIDTH + (i * bin_width),
            WINDOW_HEIGHT - bar_height,
            bin_width,
            bar_height,
        )
        pygame.draw.rect(window, barra_cor, bar_rect)


def main():
    pausa = False
    v_hist = True

    clock = pygame.time.Clock()
    fps = 100

    frames = []
    T = 0
    T_max = 1

    (
        matriz_vels0,
        matriz_raios0,
        matriz_massas0,
        matriz_cores0,
    ) = cria_particulas(METADE, VEL, RAIO, MASSA, COR)

    (
        matriz_vels1,
        matriz_raios1,
        matriz_massas1,
        matriz_cores1,
    ) = cria_particulas(METADE, VEL1, RAIO1, MASSA1, COR1)

    matriz_vels = np.concatenate((matriz_vels0, matriz_vels1))
    matriz_raios = np.concatenate((matriz_raios0, matriz_raios1))
    matriz_massas = np.concatenate((matriz_massas0, matriz_massas1))
    matriz_cores = np.concatenate((matriz_cores0, matriz_cores1))

    matriz_coordenadas = coordenadas(NUMERO_MOLECULAS, matriz_raios)

    del matriz_vels0
    del matriz_vels1
    del matriz_raios0
    del matriz_raios1
    del matriz_massas0
    del matriz_massas1
    del matriz_cores0
    del matriz_cores1

    while True:
        frame_data = pygame.surfarray.array3d(window)
        frame_data = frame_data.swapaxes(0, 1)
        frames.append(frame_data)

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

        if not pausa:
            T += DT
            window.fill(WHITE)
            # start = time.time()
            # if v_hist:
            #     hist(meu_sistema.veloci dades)
            # end = time.time()
            # histograma.append(start - end)

            # start = time.time()
            # meu_sistema.colisoes_mol()
            # end = time.time()
            # colisão.append(start - end)

            # start = time.time()
            # meu_sistema.simulacao_molecula(desenha)
            # end = time.time()
            # cada_mol.append(start - end)

            draw(window, matriz_cores, matriz_coordenadas, matriz_raios)

            matriz_coordenadas = move(matriz_coordenadas, matriz_vels, DT)

            matriz_vels = colisao_parede(
                matriz_coordenadas, matriz_raios, matriz_vels, DT
            )

            pygame.display.flip()
            clock.tick(fps)
        if T >= T_max:
            print(f"colisão demora:{sum(colisão)/len(colisão)}")
            print(f"hist demora:{sum(histograma)/len(histograma)}")
            print(f"mol demora:{sum(cada_mol)/len(cada_mol)}")

            output_video_path = f"simulation_{DT}_{vel_maxima}.mp4"
            imageio.mimsave(output_video_path, frames, fps=int(1 / DT))
            pygame.quit()
            break


if __name__ == "__main__":
    main()
