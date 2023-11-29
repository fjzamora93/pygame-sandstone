import pygame, sys, os
from tkinter import *
from pygame import *

#!ESTA CLASE NO FUNCIONA, IGNORAR TODO LO QUE APARECE AQUÍ 

font= pygame.font.SysFont("arial",40)
black = (0,0,0)
white = (255,255,255)


def play(screen):
    pygame.display.set_caption("Play")
    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    screen.fill("black")

    PLAY_TEXT = font.render(f"Texto en pantalla", True, white)
    PLAY_RECT = PLAY_TEXT.get.rect(center=(640,460))

    screen.blit(PLAY_TEXT,PLAY_RECT)

    PLAY_BACK = Button (image=None, pos=(640,460),
                        text_imput="BACK", font= font.render(f"Texto en pantalla", True, white))
    
    PLAY_BACK.changeColor(PLAY_MOUSE_POS)
    PLAY_BACK.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BACK.checkForImput(PLAY_MOUSE_POS):
                main_menu()
    
    pygame.display.update()

    def main_menu(screen):
        pygame.display.set_caption("Menu")

        while True:
            screen.blit(black,(0,0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = pygame.font.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(540,100))

            PLAY_BUTTON = Button(image = pygame.image.load(os.path.join("models", "menu", "map.png"), pos = (640, 250),
                                                            text_imput= "PLAY",font=pygame.font.get_font(75), base_color="#d7fcd4", hovering_color="white"))

            QUIT_BUTTON = Button(image = pygame.image.load(os.path.join("models", "menu", "mission.png"), pos = (640, 250),
                                                            text_imput= "PLAY",font=pygame.font.get_font(75), base_color="#d7fcd4", hovering_color="white"))

        screen.blit(MENU_TEXT, MENU_RECT)

