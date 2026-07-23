import pygame
import random
import sys
import random
import superposition
from qiskit.quantum_info import Statevector

pygame.init() # Init pygame
W, H = 1200, 600 # Screen setup

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("QuCat")

screen_size = screen.get_size()

clock = pygame.time.Clock()

# create a surface object, image is drawn on it.
imp = pygame.image.load("img/fondo.jpeg").convert()
bg = pygame.transform.scale(imp, screen_size)

# Using blit to copy content from one surface to other
screen.blit(bg, (0, 0))

# paint screen one time
pygame.display.flip()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 24)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Paddle and block
player = pygame.Rect(W // 2 - 60, H - 150, 50, 50)
suelo = pygame.Rect(0, H - 100, W, H//5)

# Compuertas
block = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
compuertas = ["H", "X", "Y", "Z"]
compuerta_actual = "H"
b_speed = 2
compuertas_recolectadas = []

medidor = pygame.Rect(W - 150, H - 250, 46, 46)
text_medidor = font.render("Medidor", True, RED)
medidor_img = pygame.image.load("img/boton_medidor.jpg")

# Texto
text_surface = font.render("H", True, BLACK)
text_rect = text_surface.get_rect()
text_rect.center = block.center

text_qubit = font.render("Estado actual: ", True, BLACK)

puntos = 0
text_puntos = font.render("Puntos: " + str(puntos), True, BLACK)

FLOOR_Y = suelo.top

# --- PHYSICS VARIABLES ---
v_0 = 20
g = 9.81
isjump = False
v = v_0

score = 0 # Score

qubit = Statevector.from_label('0')
medido = False

# Game loop
run = True
while run:
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
        player.move_ip(-8, 0)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < W:
        player.move_ip(8, 0)

    # Move block
    block.y += b_speed

    # Block caught
    if block.colliderect(player):
        block.y = 0
        block.x = random.randint(0, W - 50)
        score += 1
        compuertas_recolectadas.append(compuerta_actual)
        qubit = superposition.qubit_actual(qubit, compuerta_actual)
        compuerta_actual = random.choice(compuertas)

    if medidor.colliderect(player) and not medido:
        resultado = superposition.colapsar_qubit(qubit)
        qubit = Statevector.from_label('0')
        print(resultado[0])
        if resultado[0] == '0':
            puntos -= 1
        else:
            puntos += 1
        medido = True

    if block.y >= suelo.top:
        compuerta_actual = random.choice(compuertas)
        block.y = 0
        block.x = random.randint(0, W - 50)

    if isjump == False:
        if keys[pygame.K_SPACE]:
            isjump = True
            v = v_0

             
    if isjump :
        player.y -= v
        v -= g/10
        if v <= -20:
            isjump = False
            v = 5
            m = 5
            player.y = H-150
            medido = False

    screen.fill((0, 0, 0))

    screen.blit(bg, (0, 0))

    pygame.draw.rect(screen, WHITE, player)

    if compuerta_actual == "H":
        text_surface = font.render("H", True, BLACK)
        pygame.draw.rect(screen, RED, block)
    elif compuerta_actual == "X":
        text_surface = font.render("X", True, BLACK)
        pygame.draw.rect(screen, BLUE, block)
    elif compuerta_actual == "Y":
        text_surface = font.render("Y", True, BLACK)
        pygame.draw.rect(screen, PINK, block)
    else:
        text_surface = font.render("Z", True, BLACK)
        pygame.draw.rect(screen, GREEN, block)

    text_qubit = font.render("Estado actual: " + str(qubit.data[0]) + " |0> " + str(qubit.data[1]) + " |1>", True, WHITE)
    text_puntos = font.render("Puntos: " + str(puntos), True, WHITE)

    pygame.draw.rect(screen, BLACK, suelo)

    text_rect = text_surface.get_rect()
    text_rect.center = block.center

    screen.blit(text_surface, text_rect)
    pygame.draw.rect(screen, WHITE, medidor)
    screen.blit(text_puntos, (W-200, 20))
    screen.blit(text_qubit, (10, 20))

    screen.blit(text_medidor, (W - 175, H - 200))
    screen.blit(medidor_img, medidor)

    pygame.display.flip()

    clock.tick(60)