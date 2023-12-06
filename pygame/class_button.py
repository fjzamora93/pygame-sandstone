import pygame
import sys,os, mis_sprites

#YOUTUBE: baraltech HOW TO MAKE A MENU SCREEN IN PYGAME!
#Youtube: baraltech WAY to Make BUTTONS for Python / PyGame Projects

pygame.init()
ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("consolas",30)
black = (0, 0, 0)
white = (255, 255, 255)


class Button():
    def __init__(self, pos_x, pos_y , text_input, ruta, n):
        self.ruta = ruta
        self.n = n
        self.image = mis_sprites.cargar_sprite(ruta, n)
        
        self.text_input = text_input
        self.base_color, self.hovering_color = black, white
        self.text = main_font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.x_pos = pos_x
        self.y_pos = pos_y
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
       
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        
        
      
    def update(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.text, self.text_rect)


    def checkForInput(self,position):
        if position [0] in range (self.rect.left, self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            
            #print(pygame.font.get_fonts()) Imprime todas las fonts de pygame
            return True
            
        return False
    
    def changeColor(self,position):
        if position [0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, self.hovering_color)
            self.image = mis_sprites.cargar_sprite(self.ruta, self.n + 1)
        else:
            self.text = main_font.render(self.text_input,True,self.base_color)
            self.image = mis_sprites.cargar_sprite(self.ruta, self.n)


