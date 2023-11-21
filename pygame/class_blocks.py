import pygame
import os
import glob
import random

ancho = 900
alto = 554

def obtener_ruta(carpeta_final):
     # Patrón de búsqueda para archivos PNG
    carpeta_final = 'interruptor', '*.png'
    


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.carpeta= 'models/blocks/interruptor'
        self.n = 0
        self.block_path_png = self.obtener_ruta()
        self.image = pygame.image.load(os.path.join(self.block_path_png[self.n])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = 400
       
        #Actualmente sin usar 
        #imagen del bloque
        
        
    def update(self):
        # Puedes cambiar estos valores para controlar el movimiento del bloque
        self.rect.x += 0
        self.rect.y += 0
        self.image = pygame.image.load(os.path.join(self.block_path_png[self.n//5])).convert_alpha()
        self.n += 1
        if self.n > 39:
            self.n= 0
      
    def obtener_ruta(self):
        self.patron_png = os.path.join(self.carpeta, '*.png')
        self.block_path_png=[]
        self.block_path_png = glob.glob(self.patron_png)
        return self.block_path_png