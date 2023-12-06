import pygame, random, sys, os,glob
import class_soundtrack

ancho=900
alto=554

carpeta = 'models/items'
patron_png= os.path.join(carpeta,'*.png')
list_path = []
list_path=glob.glob(patron_png)

for archivo in list_path:
    print(archivo)

class Items(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.list_path= list_path
        self.list_path_random=self.list_path[random.randint(0,5)]
        self.image = pygame.image.load(os.path.join(self.list_path_random))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(350, 450)
        self.bonificacion = None
        self.autodestruccion = False

    def update(self):
        pass
        
    def spawn(self):    
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(350, 450)
        self.image = pygame.image.load(os.path.join(self.list_path_random))

    