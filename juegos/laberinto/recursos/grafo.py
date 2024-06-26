import random
import pygame
from juegos.laberinto.recursos.constantes import *

class Grafo:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.grafo = {}
        self.salida = None
        self.generar_lab()

    def agregar_aristas(self, vertice):
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            x, y = vertice
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and (nx, ny) not in self.grafo:
                self.grafo[vertice].append((nx, ny))
                self.grafo[(nx, ny)] = [(x, y)]
                self.agregar_aristas((nx, ny))

    def generar_lab(self):
        inicio = (0, 0)
        self.grafo[inicio] = []
        self.agregar_aristas(inicio)

        self.salida = (self.filas - 1, self.columnas - 1)

    def obtener_mov_validos(self, posicion):
        return self.grafo.get(posicion, [])

    def mostrar_lab(self, pantalla, jugador, margen_x, margen_y, jugador_img):
        # Dibujar fondo VERDE_P del laberinto
        pygame.draw.rect(pantalla, VERDE_P, (margen_x, margen_y, self.columnas * TAMANIO_CELDA, self.filas * TAMANIO_CELDA))

        for fila in range(self.filas):
            for columna in range(self.columnas):
                x = margen_x + columna * TAMANIO_CELDA
                y = margen_y + fila * TAMANIO_CELDA

                # Dibujar jugador como imagen
                if (fila, columna) == jugador:
                    pantalla.blit(jugador_img, (x, y))

                # Dibujar salida
                elif (fila, columna) == self.salida:
                    pygame.draw.rect(pantalla, VERDE, (x, y, TAMANIO_CELDA, TAMANIO_CELDA))

                # Dibujar muros
                if (fila, columna) in self.grafo:
                    if (fila, columna + 1) not in self.grafo[(fila, columna)]:
                        pygame.draw.line(pantalla, VERDE_O, (x + TAMANIO_CELDA, y), (x + TAMANIO_CELDA, y + TAMANIO_CELDA), 5)  # Muro derecha
                    if (fila, columna - 1) not in self.grafo[(fila, columna)]:
                        pygame.draw.line(pantalla, VERDE_O, (x, y), (x, y + TAMANIO_CELDA), 5)  # Muro izquierda
                    if (fila + 1, columna) not in self.grafo[(fila, columna)]:
                        pygame.draw.line(pantalla, VERDE_O, (x, y + TAMANIO_CELDA), (x + TAMANIO_CELDA, y + TAMANIO_CELDA), 5)  # Muro abajo
                    if (fila - 1, columna) not in self.grafo[(fila, columna)]:
                        pygame.draw.line(pantalla, VERDE_O, (x, y), (x + TAMANIO_CELDA, y), 5)  # Muro arriba


