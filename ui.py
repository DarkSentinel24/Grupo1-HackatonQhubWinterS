import pygame
from configuracion import BLANCO, NEGRO, FUENTE_BOTON, FUENTE_MENU


def dibujar_panel(texto_superficie, rectangulo, color_borde=BLANCO):
    panel = pygame.Surface((rectangulo.width, rectangulo.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    pygame.draw.rect(panel, color_borde, panel.get_rect(), 2)

    rect_texto = texto_superficie.get_rect(center=(rectangulo.width // 2, rectangulo.height // 2))
    panel.blit(texto_superficie, rect_texto)
    return panel, rectangulo.topleft


def dibujar_boton_menu(texto, rectangulo, color_borde=BLANCO):
    panel = pygame.Surface((rectangulo.width, rectangulo.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    pygame.draw.rect(panel, color_borde, panel.get_rect(), 2)

    superficie_texto = FUENTE_BOTON.render(texto, True, BLANCO)
    rect_texto = superficie_texto.get_rect(center=(rectangulo.width // 2, rectangulo.height // 2))
    panel.blit(superficie_texto, rect_texto)
    return panel, rectangulo.topleft


def dibujar_menu(screen, fondo, titulo, boton_jugar, boton_salir):
    screen.blit(fondo, (0, 0))
    titulo_escala = pygame.transform.scale(titulo, (600, 280))
    rect_titulo = titulo_escala.get_rect(center=(screen.get_width() // 2, 150))
    screen.blit(titulo_escala, rect_titulo)

    panel_jugar, pos_jugar = dibujar_boton_menu("Jugar", boton_jugar)
    panel_salir, pos_salir = dibujar_boton_menu("Salir", boton_salir)
    screen.blit(panel_jugar, pos_jugar)
    screen.blit(panel_salir, pos_salir)


def dibujar_titulo_final(screen, fondo, titulo_final):
    screen.blit(fondo, (0, 0))
    titulo_escala = pygame.transform.scale(titulo_final, (600, 300))
    rect_titulo = titulo_escala.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
    screen.blit(titulo_escala, rect_titulo)
