import pygame, sys, os
from tkinter import *
from pygame import *
from class_button import Button
from class_soundtrack import Soundtrack


font= pygame.font.SysFont("arial",40)
ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5


class Menu(pygame.sprite.Sprite):
    def __init__(self, nivel):
        super().__init__()
        self.nivel = nivel
        self.open_menu= False
        self.game_over = False
        self.soundtrack = Soundtrack()

    def update (self):
        if self.open_menu:
            self.main_menu()
            
            
    def main_menu(self):
        if not self.game_over:
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.play_button = Button(ancho//2,150, "Reanudar", 'models/menu', 0)
            self.restart_button = Button(ancho//2,200, "Reiniciar",'models/menu',0 )
            self.save_button = Button(ancho//2,250, "Guardar", 'models/menu', 0)
            self.load_button = Button(ancho//2,300, "Cargar", 'models/menu', 0)
            self.level_button = Button(ancho//2,300, "Cambiar de nivel", 'models/menu', 0)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                    mouse_position = pygame.mouse.get_pos()
                    if self.play_button.checkForInput(mouse_position):
                        self.open_menu = False
                        print ("botón presionado")
                        
                    if self.restart_button.checkForInput(mouse_position):    
                        self.game_over = True
                        print ("botón presionado")
                       
                    if self.save_button.checkForInput (mouse_position):
                        ...
                    if self.load_button.checkForInput(mouse_position):
                        ...
                    if self.level_button.checkForInput(mouse_position):
                        if self.nivel == 1:
                            self.nivel = 2
                        elif self.nivel == 2:
                            self.nivel = 1
                            print("segundo control activado")

            for button in [self.play_button, self.restart_button, self.save_button, self.load_button, self.level_button]:
                button.changeColor(MOUSE_POSITION)
                button.update()

            #AUDIO DEL MENÚ    
            self.soundtrack.control_audio()

