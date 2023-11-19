import random,sys,pygame
#TEXTOS AL ACBAR LA PARTIDA
ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)

def texto_game_over_1(black,ancho,alto,screen):
    font= pygame.font.SysFont("arial", 40)
    text = font.render("¡Victoria!", True, black) 
    center_x = (ancho//2 ) - (text.get_width()//2)
    center_y= (alto//2) - (text.get_height()//2)
    screen.blit(text, [center_x, center_y])

def texto_game_over_2(black,ancho,alto,screen):
    font= pygame.font.SysFont("arial", 40)
    text = font.render("¡Has sido derrotado!", True, black) 
    center_x = (ancho//2 ) - (text.get_width()//2)
    center_y= (alto//2) - (text.get_height()//2)
    screen.blit(text, [center_x, center_y])

def texto_puntuacion(screen, score):
    font= pygame.font.SysFont("arial", 50)
    puntuacion = font.render(f"Score: {score}", True, white)
    screen.blit(puntuacion,[710,10])

def texto_cargas(screen, cargas_acumuladas):
    font= pygame.font.SysFont("arial",50)
    cargas_acumuladas = font.render(f"Cargas: {cargas_acumuladas}", True, white)
    screen.blit(cargas_acumuladas, [10, 50])
