import pygame, os, random, glob, mis_sprites

class Inventario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mis_sprites.cargar_sprite('models/menu', 0)
        self.rect = self.image.get_rect()

    def update(self):
        pass