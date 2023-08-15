import pygame
import sys
import random
import math
from itertools import combinations
import numpy as np
import time

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Partículas")


NUMERO_MOLECULAS = 100

FPS = 300

VEL = 0.1
RAIO = 3
MASSA = 1

VEL1 = 0.2
RAIO1 = 5
MASSA1 = 10


raio_maior = max(RAIO,RAIO1)
raio_maior *= 2


METADE = NUMERO_MOLECULAS // 2

x_list = list(np.arange(raio_maior, WINDOW_WIDTH - raio_maior, raio_maior))
y_list = list(np.arange(raio_maior, WINDOW_HEIGHT - raio_maior, raio_maior))

cordenadas_possiveis = []

for _ in range(NUMERO_MOLECULAS):
    escolha1 = random.choice(x_list)
    escolha2 = random.choice(y_list)
    comb = (escolha1, escolha2)  # Cria a combinação escolhida

    # Verifica se a combinação já foi escolhida anteriormente
    while comb in cordenadas_possiveis:
        escolha1 = random.choice(x_list)
        escolha2 = random.choice(y_list)
        comb = (escolha1, escolha2)

    # Adiciona a combinação escolhida ao conjunto de combinações escolhidas
    cordenadas_possiveis.append(comb)

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
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def colisão_parede(self):
        if (self.x - self.radius) <= 0 or (self.x + self.radius) >= WINDOW_WIDTH:
            self.speed_x *= -1

        if (self.y - self.radius) <= 0 or (self.y + self.radius) >= WINDOW_HEIGHT:
            self.speed_y *= -1


def colisões_mol(moleculas_lista, list_vel):
    for mol1, mol2 in combinations(moleculas_lista, 2):
        distancia = math.sqrt((mol1.x - mol2.x) ** 2 + (mol1.y - mol2.y) ** 2)

        if distancia <= (mol1.radius + mol2.radius):
            delta_r = (mol1.x - mol2.x, mol1.y - mol2.y)

            delta_v = (mol1.speed_x - mol2.speed_x, mol1.speed_y - mol2.speed_y)

            produto_interno = delta_v[0] * delta_r[0] + delta_v[1] * delta_r[1]

            j = (2 * mol2.massa * mol1.massa * produto_interno) / (
                distancia * (mol2.massa + mol1.massa)
            )

            j_x = (j * delta_r[0]) / distancia
            j_y = (j * delta_r[1]) / distancia
            
            
            vel_media1 = math.sqrt(mol1.speed_x**2+mol1.speed_y**2)
            vel_media2 = math.sqrt(mol2.speed_x**2+mol2.speed_y**2)
            
            list_vel.remove(vel_media1)
            list_vel.remove(vel_media2)

            mol2.speed_x += j_x / mol2.massa
            mol2.speed_y += j_y / mol2.massa

            mol1.speed_x -= j_x / mol1.massa
            mol1.speed_y -= j_y / mol1.massa

            vel_media1 = math.sqrt(mol1.speed_x**2+mol1.speed_y**2)
            vel_media2 = math.sqrt(mol2.speed_x**2+mol2.speed_y**2)
            
            list_vel.append(vel_media1)
            list_vel.append(vel_media2)
            

def main():
    pausa = False

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
        
    list_vel_media = [math.sqrt(p.speed_x**2+p.speed_y**2) for p in particulas]

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa

        if not pausa:
            window.fill(WHITE)
            colisões_mol(particulas, list_vel_media)
            for particle in particulas:
                particle.move()
                particle.colisão_parede()
                particle.draw()

            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    main()
