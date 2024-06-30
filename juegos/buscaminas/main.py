import pygame
import os
import sys
from common.music_config import cargar_vfx
import config
from common.colores import *
from juegos.buscaminas.recursos.matriz import Matriz
from juegos.buscaminas.recursos import constantes

def main_buscaminas(screen, reloj, estado, dificultad):
    # Ambiente
    pygame.mixer.music.load(os.path.join(config.SOUNDTRACK_DIR, "Buscaminas - Sympathy For The Devil.mp3"))
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)
    # Carga de sonidos
    sonido_click = cargar_vfx("Buscaminas - Grass.mp3", estado)
    sonido_bomba = cargar_vfx("Buscaminas - Bomb.mp3", estado)
    # Fondo
    fondo_img = pygame.image.load(os.path.join(config.FONDOS_DIR, "buscaminasHD.png"))
    # Fuente
    fuente = pygame.font.Font(os.path.join(config.FONTS_DIR, "minecraft.ttf"), 30)
    fuente_minas = pygame.font.Font(os.path.join(config.FONTS_DIR, "minecraft.ttf"), 24)
    # Tablero
    filas = (dificultad[0] + 1)*3
    columnas = (dificultad[0] + 1)*3
    minas = int(((dificultad[0] + 1)*3)**2/4)
    # Crea la matriz con los valores
    matriz = Matriz(filas, columnas, minas)
    tamaño_celda = constantes.TAMANIO_CELDA
    # Calcular margen_x y margen_y para centrar el tablero en la pantalla
    tablero_ancho = columnas * tamaño_celda
    tablero_alto = filas * tamaño_celda
    margen_x = (config.ANCHO_VENTANA - tablero_ancho) // 2
    margen_y = (config.ALTO_VENTANA - tablero_alto) // 2 + 60
    # Bucle principal
    juagar_buscaminas = True
    while juagar_buscaminas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                columna = (pos[0] - margen_x) // tamaño_celda
                fila = (pos[1] - margen_y) // tamaño_celda

                # Verificar que el clic esté dentro de los límites del tablero
                if 0 <= fila < filas and 0 <= columna < columnas:
                    if evento.button == 1:  # Botón izquierdo del ratón
                        if not matriz.revelado[fila][columna]:
                            if not matriz.revelar(fila, columna):
                                sonido_bomba.play()
                                juagar_buscaminas = False
                                matriz.mostrar_bombas(screen, tamaño_celda, margen_x, margen_y)
                                print("perdiste")
                                pygame.time.delay(2000)
                                estado[0] = config.SCREEN_MAPA
                            else:
                                sonido_click.play()
                    elif evento.button == 3:  # Botón derecho del ratón
                        matriz.colocar_bandera(fila, columna)

        screen.blit(fondo_img, (0, 0))  # Dibujar la imagen de fondo
        matriz.mostrar(screen, tamaño_celda, margen_x, margen_y)  # Pasar margen_x y margen_y a la función mostrar

        # Dibujar el cuadro en la parte superior derecha
        cuadro_ancho, cuadro_alto = 200, 100
        cuadro_x, cuadro_y = config.ANCHO_VENTANA - cuadro_ancho - 10, 10
        pygame.draw.rect(screen, MARRON_CLARO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto))
        pygame.draw.rect(screen, NEGRO, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto), 3)

        # Dibujar el texto "Buscaminas"
        texto_buscaminas = fuente.render("Buscaminas", True, GOLD)
        screen.blit(texto_buscaminas, (cuadro_x + 10, cuadro_y + 10))

        # Dibujar el texto de minas restantes
        minas_restantes = matriz.contar_minas_restantes()
        texto_minas = fuente_minas.render(f"Minas: {minas_restantes}", True, NEGRO)
        screen.blit(texto_minas, (cuadro_x + 10, cuadro_y + 60))

        pygame.display.flip()

        # Verificar si se ha ganado
        if matriz.ganaste():
            juagar_buscaminas = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.time.delay(2000)
            print("FELICIDADES")
            estado[0] = config.SCREEN_MAPA
        reloj.tick(config.FPS)

if __name__ == "__main__":
    main_buscaminas()