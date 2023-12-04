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
    def __init__(self, n):
        super().__init__()
        self.spawn = True #CONDICIÓN NECESARIA PARA CUANDO QUIERAS QUE LOS BLOQUES APAREZCAN EN UN MOMENTO DADO
        
        self.n = n #LA N VA A DECIR EL NÚMERO DE BLOQUE, 0 POR DEFECTO PARA TODO
        self.carpeta= 'models/blocks'
        self.block_path_png = self.obtener_ruta()
        self.image = pygame.image.load(os.path.join(self.block_path_png[self.n])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = 400
       
        #Poner en True para animar el bloque
        
        self.bloque_dinamico = False
        
        
    def update(self):
        if not self.spawn:
            self.rect = self.image.get_rect()#Mandamos al rectángulo arriba de la pantalla???
        if not self.bloque_dinamico:
            self.image = pygame.image.load(os.path.join(self.block_path_png[self.n])).convert_alpha()
        elif self.bloque_dinamico:
            self.image = pygame.image.load(os.path.join(self.block_path_png[self.n//5])).convert_alpha()
            self.n += 1
            if self.n > 39:
                self.n= 0
        
    def obtener_ruta(self):
        self.patron_png = os.path.join(self.carpeta, '*.png')
        self.block_path_png=[]
        self.block_path_png = glob.glob(self.patron_png)
        return self.block_path_png