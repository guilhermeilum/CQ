import pygame
import sys
import random
import math
from itertools import combinations
import numpy as np
import imageio
import time


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

VEL1 = 40
RAIO1 = 5
MASSA1 = 1

vel_maxima = max(VEL, VEL1)

DT = 1 / (vel_maxima)


raio_maior = max(RAIO, RAIO1)
raio_maior *= 2

barra_cor = (0, 255, 0)

METADE = NUMERO_MOLECULAS // 2

cordenadas_possiveis = [(1.0, 1.0) for _ in range(NUMERO_MOLECULAS)]

cordenadas_possiveis1 = cordenadas_possiveis[:METADE]
cordenadas_possiveis2 = cordenadas_possiveis[METADE:]


WHITE = (255, 255, 255)


class Particle:
    def __init__(self, x, y, vel, raio, mass, color):
        self.x = x
        self.y = y
        self.radius = raio
        self.speed_x = random.uniform(-vel, vel)
        self.speed_y = random.uniform(-vel, vel)
        self.color = color
        self.massa = mass

    def move(self):
        self.x += self.speed_x * DT
        self.y += self.speed_y * DT

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def colisao_parede(self):
        x_novo = self.x + self.speed_x * DT
        y_novo = self.y + self.speed_y * DT

        afasta_0_x = x_novo > self.x
        afasta_0_y = y_novo > self.y

        afasta_f_x = x_novo < self.x
        afasta_f_y = y_novo < self.y

        if ((self.x - self.radius) <= 0 and not afasta_0_x) or (
            (self.x + self.radius) >= WINDOW_WIDTH and not afasta_f_x
        ):
            self.speed_x *= -1

        if ((self.y - self.radius) <= 0 and not afasta_0_y) or (
            (self.y + self.radius) >= WINDOW_HEIGHT and not afasta_f_y
        ):
            self.speed_y *= -1


class sistema:
    def __init__(self, particulas):
        self.particulas = particulas
        self.velocidades = [
            math.sqrt(p.speed_x**2 + p.speed_y**2) for p in particulas
        ]
        self.lista_combinacao = list(combinations(particulas, 2))
        print(self.lista_combinacao[0][0].x)

    def simulacao_molecula(self, desenha):
        for particle in self.particulas:
            particle.move()
            particle.colisao_parede()
            if desenha:
                particle.draw()

    def colisoes_mol(self):
        for mol1_2 in self.lista_combinacao:
            self.conta_colisao(mol1_2)

    def conta_colisao(self, mol1_2):
        mol1, mol2 = mol1_2
        distancia = math.sqrt((mol1.x - mol2.x) ** 2 + (mol1.y - mol2.y) ** 2)
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

                self.velocidades.remove(vel_media1)
                self.velocidades.remove(vel_media2)

                mol2.speed_x += j_x / mol2.massa
                mol2.speed_y += j_y / mol2.massa

                mol1.speed_x -= j_x / mol1.massa
                mol1.speed_y -= j_y / mol1.massa

                vel_media1 = math.sqrt(mol1.speed_x**2 + mol1.speed_y**2)
                vel_media2 = math.sqrt(mol2.speed_x**2 + mol2.speed_y**2)

                self.velocidades.append(vel_media1)
                self.velocidades.append(vel_media2)


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
        for x, y in cordenadas_possiveis1
    ]
    for x, y in cordenadas_possiveis2:
        particulas.append(
            Particle(
                x,
                y,
                VEL1,
                RAIO1,
                MASSA1,
                (0, 0, 255),
            )
        )
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
                    if D <= (particulas[i].radius + particulas[j].radius):
                        colidem = True
            if not colidem:
                break
        particulas[i].x = x
        particulas[i].y = y

    meu_sistema = sistema(particulas)

    clock = pygame.time.Clock()
    fps = 100

    frames = []
    T = 0
    T_max = 1

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
                elif event.key == pygame.K_d:
                    desenha = not desenha

        if not pausa:
            T += DT
            window.fill(WHITE)
            start = time.time()
            if v_hist:
                hist(meu_sistema.velocidades)
            end = time.time()
            histograma.append(start - end)

            start = time.time()
            meu_sistema.colisoes_mol()
            end = time.time()
            colisão.append(start - end)

            start = time.time()
            meu_sistema.simulacao_molecula(desenha)
            end = time.time()
            cada_mol.append(start - end)

            pygame.display.flip()
            clock.tick(fps)
            print(T)
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
