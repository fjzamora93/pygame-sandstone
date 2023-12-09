import pygame
import random

class Temporizador(pygame.sprite.Sprite):
    def __init__(self,  limite):
        self.contador = 0
        self.limite = limite

    def temporizar(self, limite):
        self.contador += 1
        if self.contador > limite:
            self.contador = 0
            return True

