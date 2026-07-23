import textwrap
import pygame
from configuracion import BLANCO, NEGRO, FUENTE, FUENTE_BOTON, FUENTE_MENU


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


def dibujar_menu(screen, fondo, titulo, boton_jugar, boton_salir, boton_instrucciones):
    screen.blit(fondo, (0, 0))
    titulo_escala = pygame.transform.scale(titulo, (600, 280))
    rect_titulo = titulo_escala.get_rect(center=(screen.get_width() // 2, 150))
    screen.blit(titulo_escala, rect_titulo)

    panel_jugar, pos_jugar = dibujar_boton_menu("Jugar", boton_jugar)
    panel_instrucciones, pos_instrucciones = dibujar_boton_menu("Instrucciones", boton_instrucciones)
    panel_salir, pos_salir = dibujar_boton_menu("Salir", boton_salir)
    screen.blit(panel_jugar, pos_jugar)
    screen.blit(panel_instrucciones, pos_instrucciones)
    screen.blit(panel_salir, pos_salir)


def dibujar_instrucciones(screen, fondo, texto_instrucciones, boton_regresar):
    screen.blit(fondo, (0, 0))

    lineas = []
    for linea_original in texto_instrucciones.splitlines():
        if not linea_original.strip():
            lineas.append("")
            continue
        lineas.extend(
            textwrap.wrap(
                linea_original,
                width=85,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )

    altura_linea = 28
    margen = 25
    altura_panel = max(350, len(lineas) * altura_linea + 70)
    rect_panel = pygame.Rect(80, 90, 1040, altura_panel)

    panel = pygame.Surface((rect_panel.width, rect_panel.height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 160))
    pygame.draw.rect(panel, BLANCO, panel.get_rect(), 2)

    fuente_texto = FUENTE
    y = margen
    for linea in lineas:
        superficie_linea = fuente_texto.render(linea, True, BLANCO)
        panel.blit(superficie_linea, (25, y))
        y += altura_linea

    screen.blit(panel, rect_panel.topleft)

    panel_regresar, pos_regresar = dibujar_boton_menu("Regresar", boton_regresar)
    screen.blit(panel_regresar, pos_regresar)


def dibujar_titulo_final(screen, fondo, titulo_final):
    screen.blit(fondo, (0, 0))
    titulo_escala = pygame.transform.scale(titulo_final, (600, 320))
    rect_titulo = titulo_escala.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
    screen.blit(titulo_escala, rect_titulo)
