import pygame
import random
import sys
import superposicion
from qiskit.quantum_info import Statevector

from configuracion import *
from assets import cargar_activos, cargar_sprite_gato
from ui import dibujar_panel, dibujar_menu, dibujar_instrucciones, dibujar_titulo_final
from formato_qubit import formatear_estado

pygame.init()

screen = PANTALLA
clock = RELOJ

activos = cargar_activos()
bg = activos["fondo"]
qucat_title_img = activos["titulo_qucat"]
victoria_title_img = activos["titulo_victoria"]
defeat_title_img = activos["titulo_derrota"]
medidor_img = activos["medidor"]
suelo_final = activos["suelo"]

fuente = FUENTE
fuente_menu = FUENTE_MENU
fuente_boton = FUENTE_BOTON
altura_jugador = ALTURA_JUGADOR
jugador = pygame.Rect(ANCHO // 2 - 60, ALTO - 100 - altura_jugador, altura_jugador, altura_jugador)
direccion_jugador = 1

sprite_gato = cargar_sprite_gato("img/cat.png", jugador.size)
cuadro_jugador = 0
tiempo_animacion_jugador = 0

suelo = pygame.Rect(0, ALTO - 100, ANCHO, ALTO // 5)

medidor = pygame.Rect(ANCHO - 160, ALTO - 315, 60, 60)
fuente_medidor = FUENTE_MEDIDOR
texto_medidor = fuente_medidor.render("MEDIDOR", True, BLANCO)
texto_medidor_sombra = fuente_medidor.render("MEDIDOR", True, AZUL)

bloque = pygame.Rect(random.randint(0, ANCHO - 50), 0, 50, 50)
compuertas = ["H", "X", "Y", "Z", "S", "T"]
compuerta_H_img = pygame.image.load("img/compuerta_H.png").convert_alpha()
compuerta_X_img = pygame.image.load("img/compuerta_X.png").convert_alpha()
compuerta_Y_img = pygame.image.load("img/compuerta_Y.png").convert_alpha()
compuerta_Z_img = pygame.image.load("img/compuerta_Z.png").convert_alpha()
compuerta_S_img = pygame.image.load("img/compuerta_S.jpeg").convert()
compuerta_T_img = pygame.image.load("img/compuerta_T.jpeg").convert()
compuerta_actual = "H"
velocidad_bloque = VELOCIDAD_BASE_CAIDA
velocidad_base_bloque = VELOCIDAD_BASE_CAIDA
compuertas_recolectadas = []

texto_colapso = fuente.render(" ", True, BLANCO)

sonido_compuerta = pygame.mixer.Sound("sfx/get_gate.mp3.mpeg")
sonido_salto = pygame.mixer.Sound("sfx/pixel_jump_sound.mp3.mpeg")
sonido_medicion = pygame.mixer.Sound("sfx/medicion.mp3.mpeg")
sonido_victoria = pygame.mixer.Sound("sfx/victoria.mp3.mpeg")
sonido_game_over = pygame.mixer.Sound("sfx/game_over.mp3.mpeg")

suelo_y = suelo.top

velocidad_salto_inicial = VELOCIDAD_SALTO
gravedad = GRAVEDAD
salto_activo = False
velocidad_vertical = velocidad_salto_inicial
qubit = Statevector.from_label('0')
medido = False
puntos = 0
puntuacion = 0

ESTADO_MENU = "menu"
ESTADO_JUGANDO = "playing"
ESTADO_VICTORIA = "victory"
ESTADO_DERROTA = "defeat"
ESTADO_INSTRUCCIONES = "instructions"
estado = ESTADO_MENU
boton_jugar = pygame.Rect(450, 300, 300, 70)
boton_instrucciones = pygame.Rect(450, 390, 300, 70)
boton_salir = pygame.Rect(450, 480, 300, 70)
boton_regresar = pygame.Rect(450, 470, 300, 70)
tiempo_inicio_victoria = 0
tiempo_inicio_derrota = 0
objetivo_colapso = 0
INSTRUCCIONES = (
    """Tu objetivo es colapsar al estado objetivo.\nModifica la superposición de tu qubit
    recolectando las compuertas H, X, Y, Z, S y T que caen.\nColapsa la medida de tu qubit
    con el medidor de la parte derecha.\nEn la parte superior podrás visualizar el estado actual
    de tu qubit, las probabilidades de colapsar a 0 y a 1, y tu puntaje actual.\nSi consigues 5 
    puntos, ganas.\nSi llegas a -5 puntos, pierdes."""
)


def reiniciar_juego():
    global jugador, bloque, compuerta_actual, compuertas_recolectadas, qubit, medido, puntos, puntuacion, salto_activo, velocidad_vertical, direccion_jugador, cuadro_jugador, objetivo_colapso
    jugador = pygame.Rect(ANCHO // 2 - 60, ALTO - 100 - altura_jugador, altura_jugador, altura_jugador)
    bloque = pygame.Rect(random.randint(0, ANCHO - 50), 0, 50, 50)
    compuerta_actual = random.choice(compuertas)
    compuertas_recolectadas = []
    medido = False
    puntos = 0
    puntuacion = 0
    salto_activo = False
    velocidad_vertical = velocidad_salto_inicial
    direccion_jugador = 1
    cuadro_jugador = 0
    objetivo_colapso = random.choice([0, 1])
    qubit = Statevector.from_label('1' if objetivo_colapso == 0 else '0')


reiniciar_juego()


run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if estado == ESTADO_MENU:
                if boton_jugar.collidepoint(e.pos):
                    reiniciar_juego()
                    estado = ESTADO_JUGANDO
                elif boton_instrucciones.collidepoint(e.pos):
                    estado = ESTADO_INSTRUCCIONES
                elif boton_salir.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()
            elif estado == ESTADO_INSTRUCCIONES and boton_regresar.collidepoint(e.pos):
                estado = ESTADO_MENU

    teclas = pygame.key.get_pressed()

    if estado == ESTADO_JUGANDO:
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and jugador.left > 0:
            jugador.move_ip(-8, 0)
            direccion_jugador = -1
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and jugador.right < ANCHO:
            jugador.move_ip(8, 0)
            direccion_jugador = 1

        velocidad_bloque = velocidad_base_bloque + (puntos * 0.15) - (max(0, -puntos) * 0.10)
        if velocidad_bloque < 1.0:
            velocidad_bloque = 1.0
        if velocidad_bloque > 5.5:
            velocidad_bloque = 5.5

        bloque.y += velocidad_bloque

        if bloque.colliderect(jugador):
            sonido_compuerta.play()
            bloque.y = 0
            bloque.x = random.randint(0, ANCHO - 50)
            puntuacion += 1
            compuertas_recolectadas.append(compuerta_actual)
            qubit = superposicion.qubit_actual(qubit, compuerta_actual)
            compuerta_actual = random.choice(compuertas)

        if medidor.colliderect(jugador) and not medido:
            sonido_medicion.play()
            resultado = superposicion.colapsar_qubit(qubit)
            qubit = Statevector.from_label('0')
            resultado_colapso = int(resultado[0])

            if resultado_colapso == objetivo_colapso:
                puntos += 1
                texto_colapso = fuente.render(
                    f"Último colapso: {resultado_colapso} (Correcto: +1 punto)",
                    True,
                    BLANCO,
                )
            else:
                puntos -= 1
                texto_colapso = fuente.render(
                    f"Último colapso: {resultado_colapso} (Incorrecto: -1 punto)",
                    True,
                    BLANCO,
                )

            objetivo_colapso = random.choice([0, 1])
            qubit = Statevector.from_label('1' if objetivo_colapso == 0 else '0')
            medido = True

        if bloque.y >= suelo.top:
            compuerta_actual = random.choice(compuertas)
            bloque.y = 0
            bloque.x = random.randint(0, ANCHO - 50)

        if not salto_activo and teclas[pygame.K_SPACE]:
            sonido_salto.play()
            salto_activo = True
            velocidad_vertical = velocidad_salto_inicial

        if salto_activo:
            jugador.y -= velocidad_vertical
            velocidad_vertical -= gravedad / 10
            if velocidad_vertical <= -20:
                salto_activo = False
                velocidad_vertical = 5
                jugador.y = ALTO - 100 - altura_jugador
                medido = False

        if puntos >= 5:
            sonido_victoria.play()
            estado = ESTADO_VICTORIA
            tiempo_inicio_victoria = pygame.time.get_ticks()

        if puntos <= -5:
            sonido_game_over.play()
            estado = ESTADO_DERROTA
            tiempo_inicio_derrota = pygame.time.get_ticks()

    elif estado == ESTADO_VICTORIA:
        if pygame.time.get_ticks() - tiempo_inicio_victoria >= 5000:
            estado = ESTADO_MENU

    elif estado == ESTADO_DERROTA:
        if pygame.time.get_ticks() - tiempo_inicio_derrota >= 5000:
            estado = ESTADO_MENU

    screen.fill(NEGRO)

    if estado == ESTADO_MENU:
        dibujar_menu(screen, bg, qucat_title_img, boton_jugar, boton_salir, boton_instrucciones)
    elif estado == ESTADO_INSTRUCCIONES:
        dibujar_instrucciones(screen, bg, INSTRUCCIONES, boton_regresar)
    elif estado == ESTADO_JUGANDO:
        screen.blit(bg, (0, 0))

        sprite_jugador = sprite_gato.copy()
        if direccion_jugador == -1:
            sprite_jugador = pygame.transform.flip(sprite_jugador, True, False)

        screen.blit(sprite_jugador, jugador)

        imagen_compuerta = {
            "H": pygame.transform.scale(compuerta_H_img, bloque.size),
            "X": pygame.transform.scale(compuerta_X_img, bloque.size),
            "Y": pygame.transform.scale(compuerta_Y_img, bloque.size),
            "Z": pygame.transform.scale(compuerta_Z_img, bloque.size),
            "S": pygame.transform.scale(compuerta_S_img, bloque.size),
            "T": pygame.transform.scale(compuerta_T_img, bloque.size),
        }[compuerta_actual]
        screen.blit(imagen_compuerta, bloque)

        prob_0 = abs(qubit.data[0]) ** 2
        prob_1 = abs(qubit.data[1]) ** 2

        texto_qubit = fuente.render(
            "Estado: " + formatear_estado(qubit.data[0], qubit.data[1]),
            True,
            BLANCO,
        )
        texto_probabilidades = fuente.render(
            f"P(0)={prob_0:.2%}   P(1)={prob_1:.2%}",
            True,
            BLANCO,
        )
        texto_puntos = fuente.render("Puntos: " + str(puntos), True, BLANCO)
        texto_objetivo = fuente.render(f"Objetivo: Colapsar a {objetivo_colapso}", True, BLANCO)

        pygame.draw.rect(screen, NEGRO, suelo)
        pygame.draw.rect(screen, BLANCO, medidor)

        panel_qubit, ubicacion_qubit = dibujar_panel(texto_qubit, pygame.Rect(10, 15, 560, 52))
        panel_probabilidades, ubicacion_probabilidades = dibujar_panel(texto_probabilidades, pygame.Rect(585, 15, 340, 52))
        panel_puntos, ubicacion_puntos = dibujar_panel(texto_puntos, pygame.Rect(ANCHO - 240, 15, 220, 52))
        screen.blit(panel_qubit, ubicacion_qubit)
        screen.blit(panel_probabilidades, ubicacion_probabilidades)
        screen.blit(panel_puntos, ubicacion_puntos)

        screen.blit(medidor_img, medidor)
        screen.blit(texto_medidor_sombra, (ANCHO - 173, ALTO - 248))
        screen.blit(texto_medidor, (ANCHO - 175, ALTO - 250))
        screen.blit(suelo_final, suelo)

        panel_colapso, ubicacion_colapso = dibujar_panel(texto_colapso, pygame.Rect(20, ALTO - 65, 520, 52))
        panel_objetivo, ubicacion_objetivo = dibujar_panel(texto_objetivo, pygame.Rect(ANCHO - 300, ALTO - 65, 280, 52))
        screen.blit(panel_colapso, ubicacion_colapso)
        screen.blit(panel_objetivo, ubicacion_objetivo)

    elif estado == ESTADO_VICTORIA:
        dibujar_titulo_final(screen, bg, victoria_title_img)
    elif estado == ESTADO_DERROTA:
        dibujar_titulo_final(screen, bg, defeat_title_img)

    pygame.display.flip()
    clock.tick(60)