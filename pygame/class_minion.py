import os, random, pygame, mis_sprites



class Minion (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'particle', 'biter.png')).convert_alpha()