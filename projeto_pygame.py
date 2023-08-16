import pygame
import sys
import random
import math
from itertools import combinations
import numpy as np
import time

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
x_grafico = 500
window = pygame.display.set_mode((WINDOW_WIDTH + x_grafico, WINDOW_HEIGHT))
pygame.display.set_caption("Partículas")


NUMERO_MOLECULAS = 1000


VEL = 30
RAIO = 2
MASSA = 1

VEL1 = 30
RAIO1 = 5
MASSA1 = 3

DT = 0.1

vel_maxima = max(VEL, VEL1)

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

    def colisão_parede(self):
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


def colisões_mol(moleculas_lista, list_vel):
    for mol1, mol2 in combinations(moleculas_lista, 2):
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

                list_vel.remove(vel_media1)
                list_vel.remove(vel_media2)

                mol2.speed_x += j_x / mol2.massa
                mol2.speed_y += j_y / mol2.massa

                mol1.speed_x -= j_x / mol1.massa
                mol1.speed_y -= j_y / mol1.massa

                vel_media1 = math.sqrt(mol1.speed_x**2 + mol1.speed_y**2)
                vel_media2 = math.sqrt(mol2.speed_x**2 + mol2.speed_y**2)

                list_vel.append(vel_media1)
                list_vel.append(vel_media2)


def hist(lista_vel, maxima):
    bins = 200
    hist, _ = np.histogram(lista_vel, bins=bins, range=(0, maxima*2.5))
    bin_width = x_grafico/bins
    
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
    list_vel_media = [math.sqrt(p.speed_x**2 + p.speed_y**2) for p in particulas]
    maxima_vel_media = max(list_vel_media)
    
    clock = pygame.time.Clock()
    fps = 60
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa
                elif event.key == pygame.K_h:
                    v_hist = not v_hist
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    fps += 10
                    print(fps)
                elif (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS):
                    fps = max(10, fps - 10)
                    print(fps)
                elif event.key == pygame.K_d:
                    desenha = not desenha

        if not pausa:
            window.fill(WHITE)
            if v_hist:
                hist(list_vel_media,maxima_vel_media)
            colisões_mol(particulas, list_vel_media)
            for particle in particulas:
                particle.move()
                particle.colisão_parede()
                if desenha:
                    particle.draw()

            pygame.display.flip()
            clock.tick(fps)


if __name__ == "__main__":
    main()
