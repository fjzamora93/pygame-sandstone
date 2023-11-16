import pygame, random, sys, os
import soundtrack

ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 480
        self.speed_x = 0
        self.speed_y = 0
        self.vidas = 10
        self.direction="right"
        
        # variables del salto
        self.jumping = False
        self.jump_count = 5
        self.parabola = True

    def changespeed_x(self, x):
        self.speed_x += x
        if x > 0:
            self.image = pygame.image.load(os.path.join('models', 'player_right.png')).convert_alpha()
            self.direction = "right"
        elif x < 0:
            self.image = pygame.image.load(os.path.join('models', 'player_left.png')).convert_alpha()
            self.direction = "left"

    def changespeed_y(self,y):
        self.speed_y += y
    
    def proceso_salto(self):
        if not self.jumping:
            self.jumping = True

    def update(self):  # Establecer la posición de origen, que se modifica con la velocidad
        self.rect.x += self.speed_x
        self.rect.y = 480 + self.speed_y

        #Logica salto
        if self.jumping:
            if self.jump_count <= 10 and not self.parabola: #Parabola de subida del salto
                self.rect.y -= (self.jump_count * self.jump_count * 0.8)
                self.jump_count += 0.2 #Velocidad de subida y bajada
            elif self.jump_count >= 0: #Parabola de bajada del dalto
                self.rect.y -= (self.jump_count * self.jump_count * 0.8)
                self.jump_count -= 0.2
                self.parabola= True
            if self.jump_count < 5: #Restablecimiento del salto
                self.jump_count=10
                self.jumping = False
                self.parabola= False

