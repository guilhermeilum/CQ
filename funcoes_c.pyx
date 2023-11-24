from itertools import combinations
import math
import random
import numpy as np


class sistema:
    def __init__(self, particulas, DT):
        self.quantidade_vermelho = len(particulas)
        self.quantidade_azul = 0
        self.quantidade_vermelho_lista = []
        self.quantidade_azul_lista = []
        self.particulas = particulas
        self.DT = DT

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
        for  i in range(len(combinacao)):
            index1, index2 = combinacao[i]
            mol1 = self.particulas[index1]
            mol2 = self.particulas[index2]
            if mol1.existe and mol2.existe:
                distancia = math.sqrt((mol1.x - mol2.x) ** 2 + (mol1.y - mol2.y) ** 2)
                if distancia <= (mol1.raio + mol2.raio):
                    chance_ = random.random()
                    distancia_futura = math.sqrt(
                        (
                            (mol1.x + mol1.speed_x * self.DT)
                            - (mol2.x + mol2.speed_x * self.DT)
                        )
                        ** 2
                        + (
                            (mol1.y + mol1.speed_y * self.DT)
                            - (mol2.y + mol2.speed_y * self.DT)
                        )
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
