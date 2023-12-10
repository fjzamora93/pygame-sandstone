import pygame


#!NO UTILIZAR. Screen no es una clase, es un módulo con un conjunto de métodos
class Screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ancho = 900
        self.alto = 554
        pygame.display.set_mode([self.ancho, self.alto])
    
