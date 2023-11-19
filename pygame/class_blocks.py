import pygame
import os,glob,random

ancho = 900
alto = 554

def obtener_ruta():
    # Ruta de la carpeta que contiene los archivos PNG
    carpeta = 'models/blocks'

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

    return block_path_png


class Block(pygame.sprite.Sprite):
    def __init__(self,block_path_png):
        super().__init__()
        self.image=pygame.image.load(block_path_png).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(400,401)
    
    def update(self):
        self.rect.x += 0
        self.rect.y += 0
    
    
    
if __name__== "__main__":
    obtener_ruta()

   