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

    def click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            #CONTROL DEL RATÓN Y BOTÓN DE MENÚ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                mouse_position = pygame.mouse.get_pos()