import pygame, random, sys, os
import soundtrack

ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self,player_x,player_y,direction):
        super().__init__()
        
        #IMAGEN Y POSICIÓN
        self.image = pygame.image.load("proyectil.png").convert_alpha()
        self.vector= None
        self.sonidos= True #Esto activa el sonido una vez. Si está en false, se repetirá en bucle
        self.rect = self.image.get_rect()
        self.rect.x = player_x +10
        self.rect.y = player_y +10
        self.direction = direction
        
        
    def update(self):
        if self.vector== "vertical":
            self.rect.y -= 5
            self.image = pygame.image.load("firework_rocket.png").convert_alpha()
            if self.sonidos == True:
                soundtrack.atack_laser.play()
                self.sonidos = False
            
        elif self.vector== "horizontal":
            if self.direction == "right":
                self.rect.x +=5
            if self.direction == "left":
                self.rect.x -=5
            self.image = pygame.image.load("proyectil.png").convert_alpha()
            if self.sonidos == True:
                soundtrack.atack_fireball_1.play()
                self.sonidos = False

        if self.rect.x > ancho or self.rect.x < 0 or self.rect.y<0:
            self.kill()


