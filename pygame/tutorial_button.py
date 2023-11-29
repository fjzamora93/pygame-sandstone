"""En este tutorial aprendemos a mover el juego con el mouse

También aprendemos a crear las primeras clases
"""


import pygame,random,os, sys

pygame.init()

ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
clock = pygame.time.Clock()
done=False
pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("cambria",50)
#Creamos un marcador
score=0

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)

image = pygame.image.load(os.path.join("models", "menu","map.png"))

#quitar el botón si no funciona
""""""
class Button():
    def __init__(self,image, pos_x, pos_y , text_input):
        self.image = image
        self.x_pos = pos_x
        self.y_pos = pos_y
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.base_color, self.hovering_color = black, white
        self.text_input = text_input
        self.text = main_font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        """SOLO EN EL JUEGO
        if self.image is None:
            self.image = self.text
        
        self.rect = self.image.get_rect (center=(self.x_pos,self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))
        """

    def update(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.text, self.text_rect)


    def checkForInput(self,position):
        if position [0] in range (self.rect.left, self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            return True
            print ("Botón presionado!!")
        return False
    
    def changeColor(self,position):
        if position [0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = main_font.render(self.text_input,True,self.base_color)

button_surface= pygame.image.load(os.path.join("models", "menu","map.png"))
button = Button(button_surface,400,300, "click me!")
                                                                                        

all_sprite_list = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'player', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect()
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        player.rect.x= mouse_pos[0]
        player.rect.y= mouse_pos[1]
player= Player()
all_sprite_list.add(player)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(black)



    all_sprite_list.update()
    button.update()
    button.changeColor(pygame.mouse.get_pos())

    all_sprite_list.draw(screen) 
    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()