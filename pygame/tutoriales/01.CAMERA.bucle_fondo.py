import pygame
import random
import os

pygame.mixer.init()
ANCHO = 900
ALTO = 554
SCREEN = pygame.display.set_mode([ANCHO, ALTO])
clock = pygame.time.Clock()
done = False
background = pygame.image.load(os.path.join('background', 'mountain', 'mountain_1.png')).convert_alpha()

x = 0
all_sprite_list = pygame.sprite.Group()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'player', 'player.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.speed_x = 0
        self.speed_y = 0
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
       

pygame.init()

player = Player()
all_sprite_list.add(player)
# ...

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.speed_y = -3
            if event.key == pygame.K_s:
                player.speed_y = 3
            if event.key == pygame.K_a:
                player.speed_x = -3
            if event.key == pygame.K_d:
                player.speed_x = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.speed_y = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player.speed_x = 0

    

    # Imprime las coordenadas del jugador
    print(player.rect.x, player.rect.y)



    #!PANTALLA EN BUCLE DE DESPLAZAMIENTO

    SCREEN.blit(background, [0, 0])

    x_relativa = x % background.get_rect().width
    SCREEN.blit(background, [x_relativa - background.get_rect().width, 0])
    if x_relativa < ANCHO:
        SCREEN.blit(background, (x_relativa, 0))

    x += 1
    all_sprite_list.draw(SCREEN)
    all_sprite_list.update()


      #! FIN PANTALLA EN BUCLE DE DESPLAZAMIENTO


    pygame.display.flip()
    clock.tick(50)

pygame.quit()
