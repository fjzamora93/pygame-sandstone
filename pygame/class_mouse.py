import pygame,os


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'menu', 'mouse.png')).convert_alpha()
        self.rect = self.image.get_rect()
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x= mouse_pos[0]
        self.rect.y= mouse_pos[1]