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
     
    

#ESTE MÉTODO SOLO SE PUEDE USAR EN LA CLASE PRINCIPAL CON SCREEN
def generar_stat(screen, stat, ruta, x, y, z, disminucion_barra):
    coordenadas = []
    for i in range(stat-disminucion_barra):
        x = z + i*20 #z es la separacion
        y = y
        coordenadas.append([x,y])
    for coordenada in coordenadas:
        sprite = pygame.image.load(ruta).convert_alpha()
        screen.blit (sprite,coordenada)

