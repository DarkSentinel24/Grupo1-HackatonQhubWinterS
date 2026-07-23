import pygame
from configuracion import ANCHO, ALTO


def quitar_fondo_verde(superficie):
    resultado = pygame.Surface(superficie.get_size(), pygame.SRCALPHA)
    for y in range(superficie.get_height()):
        for x in range(superficie.get_width()):
            r, g, b, a = superficie.get_at((x, y))
            if a == 0:
                resultado.set_at((x, y), (0, 0, 0, 0))
                continue

            fondo_verde = (
                g > 100 and
                g > r + 20 and
                g > b + 20 and
                abs(g - r) > 25 and
                abs(g - b) > 25
            )

            if fondo_verde:
                resultado.set_at((x, y), (0, 0, 0, 0))
            else:
                resultado.set_at((x, y), (r, g, b, a))
    return resultado


def cargar_sprite_gato(ruta, tamaño):
    sprite = pygame.image.load(ruta).convert_alpha()
    superficie_transparente = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
    color_fondo = (79, 133, 81)

    for y in range(sprite.get_height()):
        for x in range(sprite.get_width()):
            r, g, b, a = sprite.get_at((x, y))
            if a == 0:
                superficie_transparente.set_at((x, y), (0, 0, 0, 0))
                continue

            distancia = abs(r - color_fondo[0]) + abs(g - color_fondo[1]) + abs(b - color_fondo[2])
            if distancia < 70:
                superficie_transparente.set_at((x, y), (0, 0, 0, 0))
            else:
                superficie_transparente.set_at((x, y), (r, g, b, a))

    return pygame.transform.smoothscale(superficie_transparente, tamaño)


def cargar_activos():
    fondo = pygame.image.load("img/fondo.jpeg").convert()
    fondo_escala = pygame.transform.scale(fondo, (ANCHO, ALTO))

    titulo_qucat = quitar_fondo_verde(pygame.image.load("img/QuCatTitulo.png").convert_alpha())
    titulo_victoria = quitar_fondo_verde(pygame.image.load("img/titulo_victoria.png").convert_alpha())
    titulo_derrota = quitar_fondo_verde(pygame.image.load("img/titulo_derrota.png").convert_alpha())
    medidor_img = pygame.transform.smoothscale(pygame.image.load("img/medidor.jpeg"), (60, 60))
    suelo_img = pygame.image.load("img/suelo.jpeg")

    return {
        "fondo": fondo_escala,
        "titulo_qucat": titulo_qucat,
        "titulo_victoria": titulo_victoria,
        "titulo_derrota": titulo_derrota,
        "medidor": medidor_img,
        "suelo": pygame.transform.scale(suelo_img, (ANCHO, 100)),
    }
