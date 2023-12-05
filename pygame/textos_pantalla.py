import random,sys,pygame,os
from class_proyectil import Proyectil
#TEXTOS AL ACBAR LA PARTIDA
ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)



"""
la variable texto se remplaza con el string a insertar (entre comillas).
Este texto está pensado para que vaya siempre centrado en la pantalla, sin más.
"""
def texto_1(color,ancho,alto,screen,texto):
    font= pygame.font.SysFont("consolas", 30)
    text = font.render(texto, True, color) #La variable texto es el textoq ue va a aparecer en pantalla.
    center_x = (ancho//2 ) - (text.get_width()//2)
    center_y= (alto//2) - (text.get_height()//2)
    screen.blit(text, [center_x, center_y])


#El texto en pantalla depende de una variable interna
def texto_variable(screen, score, x, y):
    font= pygame.font.SysFont("consolas", 30)
    puntuacion = font.render(f"Score: {score}", True, white)
    screen.blit(puntuacion,[x,y])


def texto_cargas(screen, cargas_acumuladas):
    font= pygame.font.SysFont("consolas",40)
    proyectil_actual = pygame.image.load(os.path.join('models','skill','charges.png'))
    screen.blit(proyectil_actual,[20,100])
    cargas_acumuladas = font.render(f"    x {cargas_acumuladas}", True, white)
    screen.blit(cargas_acumuladas, [10, 100])

