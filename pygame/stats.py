import random,sys,pygame,os, mis_sprites
#TEXTOS AL ACBAR LA PARTIDA
ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)



class Stats(pygame.sprite.Sprite):
    def __init__(self, ruta, x, y, n):
        super().__init__()
        self.n = n
        self.ruta = ruta
        self.image = mis_sprites.cargar_sprite(ruta, self.n)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.image = mis_sprites.cargar_sprite(self.ruta, self.n)
       
        
    def actualizar(self, x, y, n, subtipo):
        self.n= n
        if subtipo == "mob":
            self.rect.x = x
            self.rect.y = y 
        if subtipo == "boss":
            self.rect.x = 830 
            self.rect.y = 100
     
    
    
    
    

        


def generar_stat(screen, stat, ruta, x, y, z, proyectil_list):
    coordenadas = []
    for i in range(stat-proyectil_list):
        x = z + i*20 #z es la separacion
        y = y
        coordenadas.append([x,y])
    for coordenada in coordenadas:
        sprite = pygame.image.load(ruta).convert_alpha()
        screen.blit (sprite,coordenada)


def hearts(screen,vidas):
    coordenadas=[]
    for i in range(vidas):
        x=10+i*20
        y=20
        coordenadas.append([x, y])
    for coordenada in coordenadas:
        hearts= pygame.image.load(os.path.join('models', 'stats', 'hearts.png')).convert_alpha()
        screen.blit(hearts,coordenada)



def hearts_mob(screen,vidas_mob):
    coordenadas=[]
    for i in range(vidas_mob):
        x=830
        y=100 + i*20
        coordenadas.append([x, y])
    for coordenada in coordenadas:
        hearts= pygame.image.load(os.path.join('models', 'stats', 'mob_hearts.png')).convert_alpha()
        screen.blit(hearts,coordenada)

def mob_stats(screen,vidas_mob, x, y):
    coordenadas=[]
    for i in range(vidas_mob):
        x=830
        y=100 + i
        i += 20
        coordenadas.append([x, y])
    for coordenada in coordenadas:
        hearts= pygame.image.load(os.path.join('models', 'stats', 'mob_hearts.png')).convert_alpha()
        screen.blit(hearts,coordenada)