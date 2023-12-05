import pygame, sys, os
from tkinter import *
from pygame import *



font= pygame.font.SysFont("arial",40)
ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def main_menu(self):
        if not self.game_over:
            MOUSE_POSITION = pygame.mouse.get_pos()

            play_button = Button(ancho//2,150, "Reanudar")
            restart_button = Button(ancho//2,200, "Reiniciar")
            save_button = Button(ancho//2,250, "Guardar")
            load_button = Button(ancho//2,300, "Cargar")
            level_button = Button(ancho//2,300, "Cambiar de nivel")

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                    mouse_position = pygame.mouse.get_pos()
                    if play_button.checkForInput(mouse_position):
                        self.open_menu = False
                    if restart_button.checkForInput(mouse_position):    
                        self.game_over = True
                    if save_button.checkForInput (mouse_position):
                        ...
                    if load_button.checkForInput(mouse_position):
                        ...
                    if level_button.checkForInput(mouse_position):
                        if self.nivel == 1:
                            self.nivel = 2
                        elif self.nivel == 2:
                            self.nivel = 1

            for button in [play_button, restart_button, save_button, load_button, level_button]:
                button.changeColor(MOUSE_POSITION)
                button.update()

