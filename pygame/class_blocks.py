import pygame
import os
import glob
import random

ancho = 900
alto = 554

def obtener_ruta(carpeta_final):
     # Patrón de búsqueda para archivos PNG
    carpeta_final = 'interruptor', '*.png'
    
    # Ruta de la carpeta que contiene los archivos PNG
    patron_png = os.path.join('models/blocks', carpeta_final,'*.png')

   
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
        self.carpeta = 'models/blocks/interruptor'
        self.block_path_png = self.obtener_ruta()
        self.image = pygame.image.load(self.block_path_png[1]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = 400
        self.n= 0

        
    
    def update(self):
        # Puedes cambiar estos valores para controlar el movimiento del bloque
        self.rect.x += 0
        self.rect.y += 0
        self.image = pygame.image.load(self.block_path_png[self.n]).convert_alpha()
    
    def obtener_ruta(self):
        

        # Patrón de búsqueda para archivos PNG
        self.patron_png = os.path.join(self.carpeta, '*.png')

        # Lista para almacenar los nombres de archivos PNG
        self.block_path_png = []

        # Utiliza glob para obtener la lista de archivos que coinciden con el patrón
        self.block_path_png = glob.glob(self.patron_png)

        # Imprime la lista de archivos PNG. Eso nos enseñará cuál es la ruta
        print("Archivos PNG en la carpeta:")
        for archivo in self.block_path_png:
            print(archivo)

        return self.block_path_png