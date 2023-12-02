import pygame,os


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'menu', 'mouse.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.abrir = False
       
        
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x= mouse_pos[0]
        self.rect.y= mouse_pos[1]


    #ESTA FUNCIÓN NO FUNCIONA
    def click(self,boton):
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                    mouse_position = pygame.mouse.get_pos()
                    if boton.checkForInput(mouse_position):
                        print("control de botón de salida presionado!")
                        return False
                else:
                     return True