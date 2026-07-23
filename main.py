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
qucat_title_img = pygame.image.load("img/QuCatTitulo.png").convert_alpha()
victoria_title_img = pygame.image.load("img/titulo_victoria.png").convert_alpha()
defeat_title_img = pygame.image.load("img/titulo_derrota.png").convert_alpha()


def remove_green_background(surface):
    result = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            r, g, b, a = surface.get_at((x, y))
            if a == 0:
                result.set_at((x, y), (0, 0, 0, 0))
                continue

            is_green_background = (
                g > 100 and
                g > r + 20 and
                g > b + 20 and
                abs(g - r) > 25 and
                abs(g - b) > 25
            )

            if is_green_background:
                result.set_at((x, y), (0, 0, 0, 0))
            else:
                result.set_at((x, y), (r, g, b, a))
    return result


qucat_title_img = remove_green_background(qucat_title_img)
victoria_title_img = remove_green_background(victoria_title_img)
defeat_title_img = remove_green_background(defeat_title_img)

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

medidor = pygame.Rect(W - 160, H - 315, 60, 60)
medidor_font = pygame.font.SysFont(None, 28)
text_medidor = medidor_font.render("MEDIDOR", True, WHITE)
text_medidor_shadow = medidor_font.render("MEDIDOR", True, BLUE)
medidor_img = pygame.transform.smoothscale(pygame.image.load("img/medidor.jpeg"), (60, 60))

block = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
compuertas = ["H", "X", "Y", "Z", "S", "T"]
compuerta_H_img = pygame.image.load("img/compuerta_H.png").convert_alpha()
compuerta_X_img = pygame.image.load("img/compuerta_X.png").convert_alpha()
compuerta_Y_img = pygame.image.load("img/compuerta_Y.png").convert_alpha()
compuerta_Z_img = pygame.image.load("img/compuerta_Z.png").convert_alpha()
compuerta_S_img = pygame.image.load("img/compuerta_S.jpeg").convert()
compuerta_T_img = pygame.image.load("img/compuerta_T.jpeg").convert()
compuerta_actual = "H"
b_speed = 2
base_b_speed = 2
compuertas_recolectadas = []

text_surface = font.render("H", True, BLACK)
text_rect = text_surface.get_rect()
text_rect.center = block.center
text_qubit = font.render("Estado actual: ", True, BLACK)
text_puntos = font.render("Puntos: 0", True, BLACK)
text_colapso = font.render(" ", True, WHITE)

sonido_compuerta = pygame.mixer.Sound("sfx/get_gate.mp3.mpeg")
sonido_salto = pygame.mixer.Sound("sfx/pixel_jump_sound.mp3.mpeg")
sonido_medicion = pygame.mixer.Sound("sfx/medicion.mp3.mpeg")
sonido_victoria = pygame.mixer.Sound("sfx/victoria.mp3.mpeg")
sonido_game_over = pygame.mixer.Sound("sfx/game_over.mp3.mpeg")

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
STATE_DEFEAT = "defeat"
state = STATE_MENU
play_button = pygame.Rect(450, 300, 300, 70)
exit_button = pygame.Rect(450, 400, 300, 70)
victory_start_time = 0
defeat_start_time = 0
objetivo_colapso = 0


def reset_game():
    global player, block, compuerta_actual, compuertas_recolectadas, qubit, medido, puntos, score, isjump, v, player_direction, player_frame, objetivo_colapso
    player = pygame.Rect(W // 2 - 60, H - 100 - player_height, player_height, player_height)
    block = pygame.Rect(random.randint(0, W - 50), 0, 50, 50)
    compuerta_actual = random.choice(compuertas)
    compuertas_recolectadas = []
    medido = False
    puntos = 0
    score = 0
    isjump = False
    v = v_0
    player_direction = 1
    player_frame = 0
    objetivo_colapso = random.choice([0, 1])
    qubit = Statevector.from_label('1' if objetivo_colapso == 0 else '0')


reset_game()


def draw_menu_button(text, rect, border_color=WHITE):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    pygame.draw.rect(panel, border_color, panel.get_rect(), 2)

    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(rect.width // 2, rect.height // 2))
    panel.blit(text_surface, text_rect)
    screen.blit(panel, rect.topleft)


def draw_menu():
    screen.blit(bg, (0, 0))
    title = pygame.transform.scale(qucat_title_img, (600, 300))
    title_rect = title.get_rect(center=(W // 2, 150))
    screen.blit(title, title_rect)

    draw_menu_button("Jugar", play_button)
    draw_menu_button("Salir", exit_button)


def draw_victory():
    screen.blit(bg, (0, 0))
    victory_title = pygame.transform.scale(victoria_title_img, (600, 350))
    victory_rect = victory_title.get_rect(center=(W // 2, H // 2 - 20))
    screen.blit(victory_title, victory_rect)


def draw_defeat():
    screen.blit(bg, (0, 0))
    defeat_title = pygame.transform.scale(defeat_title_img, (600, 350))
    defeat_rect = defeat_title.get_rect(center=(W // 2, H // 2 - 20))
    screen.blit(defeat_title, defeat_rect)


def format_component(value):
    if abs(value) < 1e-9:
        return "0.000"
    rounded = round(value, 3)
    if abs(rounded) < 1e-9:
        return "0.000"
    return f"{rounded:.3f}"


def format_state_amplitude(value):
    real = value.real
    imag = value.imag

    if abs(real) < 1e-9 and abs(imag) < 1e-9:
        return "0.000"

    if abs(imag) < 1e-9:
        return format_component(real)

    if abs(real) < 1e-9:
        imag_text = format_component(abs(imag))
        if imag >= 0:
            return f"{imag_text}i"
        return f"-{imag_text}i"

    real_text = format_component(real)
    imag_text = format_component(abs(imag))
    if imag >= 0:
        return f"({real_text} + {imag_text}i)"
    return f"({real_text} - {imag_text}i)"


def format_state_display(amplitude0, amplitude1):
    term0 = format_state_amplitude(amplitude0)
    term1 = format_state_amplitude(amplitude1)

    sign1 = "+" if amplitude1.real >= 0 and amplitude1.imag >= 0 else "-"
    abs_term1 = term1.lstrip("-")

    if sign1 == "+":
        return f"{term0} |0> + {abs_term1} |1>"
    return f"{term0} |0> - {abs_term1} |1>"


def draw_hud_panel(text_surface, rect, border_color=WHITE):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    pygame.draw.rect(panel, border_color, panel.get_rect(), 2)

    text_rect = text_surface.get_rect(center=(rect.width // 2, rect.height // 2))
    panel.blit(text_surface, text_rect)
    screen.blit(panel, rect.topleft)


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

        b_speed = base_b_speed + (puntos * 0.15) - (max(0, -puntos) * 0.10)
        if b_speed < 1.0:
            b_speed = 1.0
        if b_speed > 5.5:
            b_speed = 5.5

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
            sonido_medicion.play()
            resultado = superposition.colapsar_qubit(qubit)
            qubit = Statevector.from_label('0')
            resultado_collapse = int(resultado[0])

            if resultado_collapse == objetivo_colapso:
                puntos += 1
                text_colapso = font.render(
                                        f"Último colapso: {resultado_collapse} (Correcto: +1 punto)",
                                        True,
                                        WHITE,
                                    )
            else:
                puntos -= 1
                text_colapso = font.render(
                                        f"Último colapso: {resultado_collapse} (Incorrecto: -1 punto)",
                                        True,
                                        WHITE,
                                    )

            objetivo_colapso = random.choice([0, 1])
            qubit = Statevector.from_label('1' if objetivo_colapso == 0 else '0')
            medido = True

        if block.y >= suelo.top:
            compuerta_actual = random.choice(compuertas)
            block.y = 0
            block.x = random.randint(0, W - 50)

        if not isjump and keys[pygame.K_SPACE]:
            sonido_salto.play()
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

        if puntos >= 5:
            sonido_victoria.play()
            state = STATE_VICTORY
            victory_start_time = pygame.time.get_ticks()

        if puntos <= -5:
            sonido_game_over.play()
            state = STATE_DEFEAT
            defeat_start_time = pygame.time.get_ticks()

    elif state == STATE_VICTORY:
        if pygame.time.get_ticks() - victory_start_time >= 5000:
            state = STATE_MENU

    elif state == STATE_DEFEAT:
        if pygame.time.get_ticks() - defeat_start_time >= 5000:
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
            "S": pygame.transform.scale(compuerta_S_img, block.size),
            "T": pygame.transform.scale(compuerta_T_img, block.size),
        }[compuerta_actual]
        screen.blit(gate_image, block)

        prob_0 = abs(qubit.data[0]) ** 2
        prob_1 = abs(qubit.data[1]) ** 2

        text_qubit = font.render(
            "Estado: " + format_state_display(qubit.data[0], qubit.data[1]),
            True,
            WHITE,
        )
        text_probabilidades = font.render(
            f"P(0)={prob_0:.2%}   P(1)={prob_1:.2%}",
            True,
            WHITE,
        )
        text_puntos = font.render("Puntos: " + str(puntos), True, WHITE)
        text_objetivo = font.render(f"Objetivo: Colapsar a {objetivo_colapso}", True, WHITE)

        pygame.draw.rect(screen, BLACK, suelo)
        pygame.draw.rect(screen, WHITE, medidor)

        draw_hud_panel(text_qubit, pygame.Rect(10, 15, 560, 52))
        draw_hud_panel(text_probabilidades, pygame.Rect(585, 15, 340, 52))
        draw_hud_panel(text_puntos, pygame.Rect(W - 240, 15, 220, 52))

        screen.blit(medidor_img, medidor)
        screen.blit(text_medidor_shadow, (W - 173, H - 248))
        screen.blit(text_medidor, (W - 175, H - 250))
        screen.blit(suelo_final, suelo)

        draw_hud_panel(text_colapso, pygame.Rect(20, H - 65, 520, 52))
        draw_hud_panel(text_objetivo, pygame.Rect(W - 300, H - 65, 280, 52))

    elif state == STATE_VICTORY:
        draw_victory()
    elif state == STATE_DEFEAT:
        draw_defeat()

    pygame.display.flip()
    clock.tick(60)