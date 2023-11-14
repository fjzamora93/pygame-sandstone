import random,sys,pygame,os
#TEXTOS AL ACBAR LA PARTIDA
ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)


def hearts(screen,vidas,):
    coordenadas=[]
    for i in range(vidas):
        x=10+i*20
        y=20
        coordenadas.append([x, y])
    for coordenada in coordenadas:
        hearts= pygame.image.load(os.path.join('models', 'vidas.png')).convert_alpha()
        screen.blit(hearts,coordenada)