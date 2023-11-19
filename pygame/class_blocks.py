import pygame
import os
import glob
import random

ancho = 900
alto = 554

def obtener_ruta(carpeta_final):
    # Ruta de la carpeta que contiene los archivos PNG
    carpeta = os.path.join('models/blocks', carpeta_final)

    # Patrón de búsqueda para archivos PNG
    patron_png = os.path.join(carpeta, '*.png')

    # Lista para almacenar los nombres de archivos PNG
    block_path_png = []

    # Utiliza glob para obtener la lista de archivos que coinciden con el patrón
    block_path_png = glob.glob(patron_png)

    # Imprime la lista de archivos PNG. Eso nos enseñará cuál es la ruta
    print("Archivos PNG en la carpeta:")
    for archivo in block_path_png:
        print(archivo)

    return block_path_png  # Devuelve la lista de archivos PNG

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.carpeta_final = "interruptor"
        self.path_definitivo = random.choice(obtener_ruta(self.carpeta_final))
        self.image = pygame.image.load(self.path_definitivo).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = 400
    
    def update(self):
        
        # Puedes cambiar estos valores para controlar el movimiento del bloque
        self.rect.x += 0
        self.rect.y += 0