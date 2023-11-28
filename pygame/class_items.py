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

    #! FUNCIÓN OBSOLETA, BORRAR
    def bonus(self):
        match self.list_path_random:
            case "models/items\gema.png":
                self.bonificacion = "gema"
                print ("amatista")
            case "models/items\manzana.png":
                self.bonificacion= "manzana"
                print ("apple")
            case "models/items\pearl.png":
                self.bonificacion= "pearl"
                print ("perla")
            case "models/items\libro.png":
                self.bonificacion= "fireball"
                print ("book")
            case "models/items\diamond.png":
                self.bonificacion= "diamond"
                print ("diamante")
            case "models/items\emerald.png":
                self.bonificacion= "emerald"
                print ("esmeralda")
        return self.bonificacion

#item= Items()    
#print (item.bonus())

