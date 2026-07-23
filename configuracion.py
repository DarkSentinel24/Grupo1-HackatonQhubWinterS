import pygame

pygame.init()

ANCHO, ALTO = 1200, 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("QuCat")

TAMANO_PANTALLA = PANTALLA.get_size()
RELOJ = pygame.time.Clock()

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROSA = (255, 192, 203)
NEGRO = (0, 0, 0)

FUENTE = pygame.font.SysFont(None, 36)
FUENTE_MENU = pygame.font.SysFont(None, 72)
FUENTE_BOTON = pygame.font.SysFont(None, 48)
FUENTE_MEDIDOR = pygame.font.SysFont(None, 28)

ALTURA_JUGADOR = 120
VELOCIDAD_BASE_CAIDA = 2.0
VELOCIDAD_SALTO = 20
GRAVEDAD = 9.81
