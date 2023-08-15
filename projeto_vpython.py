from vpython import *
from itertools import combinations
import random

####constantes


moleculas_quantidade = 100


# Criar uma cena
scene = canvas()

# Definir o tamanho do espaço restrito
box_size = vector(30, 30)

# Criar um espaço restrito (caixa)
restriction_box = box(pos=vector(0, 0), size=box_size, opacity=0.1, color=color.white)

moleculas_lista = []


for _ in range(moleculas_quantidade):
    # Criar uma esfera dentro do espaço restrito
    mol = sphere(
        pos=vector.random() * 10,
        radius=0.5,
        color=color.red,
        velocity=vector.random() * 5,
    )

    moleculas_lista.append(mol)


# Loop de animação
dt = 0.01


def atualizar_posição(box_size, moleculas_lista, dt):
    for mol in moleculas_lista:
        # Atualizar a posição da esfera
        mol.pos = mol.pos + mol.velocity * dt

        # Verificar colisão com as paredes do espaço restrito
        if (
            mol.pos.x + mol.radius > box_size.x / 2
            or mol.pos.x - mol.radius < -box_size.x / 2
        ):
            mol.velocity.x *= -1
        if (
            mol.pos.y + mol.radius > box_size.y / 2
            or mol.pos.y - mol.radius < -box_size.y / 2
        ):
            mol.velocity.y *= -1
        # if (
        #     mol.pos.z + mol.radius > box_size.z / 2
        #     or mol.pos.z - mol.radius < -box_size.z / 2
        # ):
        #     mol.velocity.z *= -1


def colisões_mol(moleculas_lista):
    for mol1, mol2 in combinations(moleculas_lista, 2):
        distancia = sqrt(
            (mol1.pos.x - mol2.pos.x) ** 2 + (mol1.pos.y - mol2.pos.y) ** 2
        )
        if distancia <= (mol1.radius + mol2.radius):
            if abs(mol1.pos.x - mol2.pos.x) <= (mol1.radius + mol2.radius):
                mol1.velocity.x *= -1
                mol2.velocity.x *= -1
                # print("x")

            if abs(mol1.pos.y - mol2.pos.y) <= (mol1.radius + mol2.radius):
                mol1.velocity.y *= -1
                mol2.velocity.y *= -1
                # print("y")

            # if abs(mol1.pos.z - mol2.pos.z) <= (mol1.radius + mol2.radius):
            #     mol1.velocity.z *= -1
            #     mol2.velocity.z *= -1
            #     # print("z")


while True:
    rate(300)
    atualizar_posição(box_size, moleculas_lista, dt)
    colisões_mol(moleculas_lista)
