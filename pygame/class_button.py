import pygame
import sys,os

#YOUTUBE: baraltech HOW TO MAKE A MENU SCREEN IN PYGAME!
#Youtube: baraltech WAY to Make BUTTONS for Python / PyGame Projects

pygame.init()
ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
pygame.display.set_caption("Button!")
main_font = pygame.font.SysFont("consolas",50)
black = (0, 0, 0)
white = (255, 255, 255)


class Button():
    def __init__(self, pos_x, pos_y , text_input):
        self.image = pygame.image.load(os.path.join("models", "menu","menu_bar.png"))
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
            
            #print(pygame.font.get_fonts()) Imprime todas las fonts de pygame
            return True
            
        return False
    
    def changeColor(self,position):
        if position [0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            self.text = main_font.render(self.text_input, True, self.hovering_color)
            self.image = pygame.image.load(os.path.join("models", "menu","menu_bar_pressed.png"))
        else:
            self.text = main_font.render(self.text_input,True,self.base_color)
            self.image = pygame.image.load(os.path.join("models", "menu","menu_bar.png"))




"""
class Button():
    def __init__(self,image,pos,text_input,font,base_color,hovering_color):
        self.image = image
        self.x_pos = pos [0]
        self.y_pos = pos [1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text
        
        self.rect = self.image.get_rect (center=(self.x_pos,self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos,self.y_pos))

    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image,self.rect)
        screen.blit(self.text,self.text_rect)

    def checkForInput(self,position):
        if position [0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self,position):
        if position [0] in range (self.rect.left,self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input,True,self.base_color)
                                                                                        
        
"""