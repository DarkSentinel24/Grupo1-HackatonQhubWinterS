import pygame
import random
import sys
import superposition
from qiskit.quantum_info import Statevector

pygame.init()
W, H = 1200, 600

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("QuCat")

screen_size = screen.get_size()
clock = pygame.time.Clock()

fondo = pygame.image.load("img/fondo.jpeg").convert()
bg = pygame.transform.scale(fondo, screen_size)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
menu_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)
player_height = 120

player = pygame.Rect(W // 2 - 60, H - 100 - player_height, player_height, player_height)
player_direction = 1


def load_cat_sprite(path, size):
    sprite = pygame.image.load(path).convert_alpha()
    transparent_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
    bg_color = (79, 133, 81)

    for y in range(sprite.get_height()):
        for x in range(sprite.get_width()):
            r, g, b, a = sprite.get_at((x, y))
            if a == 0:
                transparent_surface.set_at((x, y), (0, 0, 0, 0))
                continue

            distance = abs(r - bg_color[0]) + abs(g - bg_color[1]) + abs(b - bg_color[2])
            if distance < 70:
                transparent_surface.set_at((x, y), (0, 0, 0, 0))
            else:
                transparent_surface.set_at((x, y), (r, g, b, a))

    return pygame.transform.smoothscale(transparent_surface, size)


cat_sprite = load_cat_sprite("img/cat.png", player.size)
player_frame = 0
player_animation_time = 0

suelo = pygame.Rect(0, H - 100, W, H // 5)
tam_suelo = suelo.size
suelo_img = pygame.image.load("img/suelo.jpeg")
suelo_final = pygame.transform.scale(suelo_img, tam_suelo)

medidor = pygame.Rect(W - 150, H - 300, 46, 46)
text_medidor = font.render("Medidor", True, RED)
medidor_img = pygame.image.load("img/boton_medidor.jpg")

block = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
compuertas = ["H", "X", "Y", "Z"]
compuerta_H_img = pygame.image.load("img/compuerta_H.png").convert_alpha()
compuerta_X_img = pygame.image.load("img/compuerta_X.png").convert_alpha()
compuerta_Y_img = pygame.image.load("img/compuerta_Y.png").convert_alpha()
compuerta_Z_img = pygame.image.load("img/compuerta_Z.png").convert_alpha()
compuerta_actual = "H"
b_speed = 2
compuertas_recolectadas = []

text_surface = font.render("H", True, BLACK)
text_rect = text_surface.get_rect()
text_rect.center = block.center
text_qubit = font.render("Estado actual: ", True, BLACK)
text_puntos = font.render("Puntos: 0", True, BLACK)
text_colapso = font.render(" ", True, WHITE)

sonido_compuerta = pygame.mixer.Sound("sfx/get_gate.mp3.mpeg")

FLOOR_Y = suelo.top

v_0 = 20
g = 9.81
isjump = False
v = v_0
qubit = Statevector.from_label('0')
medido = False
puntos = 0
score = 0

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_VICTORY = "victory"
state = STATE_MENU
play_button = pygame.Rect(450, 220, 300, 70)
exit_button = pygame.Rect(450, 320, 300, 70)
victory_start_time = 0


def reset_game():
    global player, block, compuerta_actual, compuertas_recolectadas, qubit, medido, puntos, score, isjump, v, player_direction, player_frame
    player = pygame.Rect(W // 2 - 60, H - 100 - player_height, player_height, player_height)
    block = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
    compuerta_actual = random.choice(compuertas)
    compuertas_recolectadas = []
    qubit = Statevector.from_label('0')
    medido = False
    puntos = 0
    score = 0
    isjump = False
    v = v_0
    player_direction = 1
    player_frame = 0


reset_game()


def draw_menu():
    screen.blit(bg, (0, 0))
    title = menu_font.render("QuCat", True, WHITE)
    title_rect = title.get_rect(center=(W // 2, 100))
    screen.blit(title, title_rect)

    pygame.draw.rect(screen, WHITE, play_button)
    pygame.draw.rect(screen, WHITE, exit_button)

    play_text = button_font.render("Jugar", True, BLACK)
    exit_text = button_font.render("Salir", True, BLACK)
    screen.blit(play_text, play_text.get_rect(center=play_button.center))
    screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))


def draw_victory():
    screen.blit(bg, (0, 0))
    victory_text = menu_font.render("¡Victoria!", True, WHITE)
    victory_rect = victory_text.get_rect(center=(W // 2, H // 2))
    screen.blit(victory_text, victory_rect)


run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if state == STATE_MENU:
                if play_button.collidepoint(e.pos):
                    reset_game()
                    state = STATE_PLAYING
                elif exit_button.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

    keys = pygame.key.get_pressed()
    player_moving = False

    if state == STATE_PLAYING:
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left > 0:
            player.move_ip(-8, 0)
            player_direction = -1
            player_moving = True
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right < W:
            player.move_ip(8, 0)
            player_direction = 1
            player_moving = True

        block.y += b_speed

        if block.colliderect(player):
            sonido_compuerta.play()
            block.y = 0
            block.x = random.randint(0, W - 50)
            score += 1
            compuertas_recolectadas.append(compuerta_actual)
            qubit = superposition.qubit_actual(qubit, compuerta_actual)
            compuerta_actual = random.choice(compuertas)

        if medidor.colliderect(player) and not medido:
            resultado = superposition.colapsar_qubit(qubit)
            qubit = Statevector.from_label('0')
            if resultado[0] == '0':
                puntos -= 1
                text_colapso = font.render(
                                        "Último colapso: 0 (Perdiste 1 punto)",
                                        True,
                                        WHITE,
                                    )
            else:
                puntos += 1
                text_colapso = font.render(
                                        "Último colapso: 1 (Ganaste 1 punto)",
                                        True,
                                        WHITE,
                                    )
            medido = True

        if block.y >= suelo.top:
            compuerta_actual = random.choice(compuertas)
            block.y = 0
            block.x = random.randint(0, W - 50)

        if not isjump and keys[pygame.K_SPACE]:
            isjump = True
            v = v_0

        if isjump:
            player.y -= v
            v -= g / 10
            if v <= -20:
                isjump = False
                v = 5
                player.y = H - 100 - player_height
                medido = False

        if puntos >= 10:
            state = STATE_VICTORY
            victory_start_time = pygame.time.get_ticks()

    elif state == STATE_VICTORY:
        if pygame.time.get_ticks() - victory_start_time >= 5000:
            state = STATE_MENU

    screen.fill(BLACK)

    if state == STATE_MENU:
        draw_menu()
    elif state == STATE_PLAYING:
        screen.blit(bg, (0, 0))

        player_sprite = cat_sprite.copy()

        if player_direction == -1:
            player_sprite = pygame.transform.flip(player_sprite, True, False)

        screen.blit(player_sprite, player)

        gate_image = {
            "H": pygame.transform.scale(compuerta_H_img, block.size),
            "X": pygame.transform.scale(compuerta_X_img, block.size),
            "Y": pygame.transform.scale(compuerta_Y_img, block.size),
            "Z": pygame.transform.scale(compuerta_Z_img, block.size),
        }[compuerta_actual]
        screen.blit(gate_image, block)

        text_qubit = font.render(
            "Estado actual: " + str(qubit.data[0]) + " |0> + " + str(qubit.data[1]) + " |1>",
            True,
            WHITE,
        )
        text_puntos = font.render("Puntos: " + str(puntos), True, WHITE)

        pygame.draw.rect(screen, BLACK, suelo)
        pygame.draw.rect(screen, WHITE, medidor)
        screen.blit(text_puntos, (W - 200, 20))
        screen.blit(text_qubit, (10, 20))
        screen.blit(text_medidor, (W - 175, H - 250))
        screen.blit(medidor_img, medidor)
        screen.blit(suelo_final, suelo)
        screen.blit(text_colapso, (20, H - 40))
    elif state == STATE_VICTORY:
        draw_victory()

    pygame.display.flip()
    clock.tick(60)