from vpython import *
from itertools import combinations
import random

# Criar uma cena
scene = canvas()

# Definir o tamanho do espaço restrito
box_size = vector(10, 10, 10)

# Criar um espaço restrito (caixa)
restriction_box = box(
    pos=vector(0, 0, 0), size=box_size, opacity=0.1, color=color.white
)

moleculas_quantidade = 20
moleculas_lista = []


for _ in range(moleculas_quantidade):
    # Criar uma esfera dentro do espaço restrito
    mol = sphere(
        pos=vector.random() * 4,
        radius=0.5,
        color=color.red,
        velocity=vector.random() * 2,
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
        if (
            mol.pos.z + mol.radius > box_size.z / 2
            or mol.pos.z - mol.radius < -box_size.z / 2
        ):
            mol.velocity.z *= -1


def colisões_mol(moleculas_lista):
    for mol1, mol2 in combinations(moleculas_lista, 2):
        distancia = sqrt(
            (mol1.pos.x - mol2.pos.x) ** 2
            + (mol1.pos.y - mol2.pos.y) ** 2
            + (mol1.pos.z - mol2.pos.z) ** 2
        )
        if distancia <= (mol1.radius + mol2.radius):
            mol1.velocity *= -1
            mol2.velocity *= -1


while True:
    rate(300)
    atualizar_posição(box_size, moleculas_lista, dt)
    colisões_mol(moleculas_lista)
