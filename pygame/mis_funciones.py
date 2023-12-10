#Archivo con varias funciones útiles en cualquier caso:
import os,glob,pygame
import class_soundtrack
from temporizador import Temporizador

def obtener_ruta(carpeta_destino):
    patron_png = os.path.join(carpeta_destino,"*.png")
    path_list = []
    path_list = glob.glob(patron_png)
    return path_list

#os.path.join() busca en la carpeta de destino todos los archivos con esa terminación.
#path_list es la lista donde vamos a guardar cosas.
#glob.glob() nos devuelve los archivos del patron_png y nos lo mete en la lista.
#return nos indica lo que devuelve la función, para almacenarlo en una variable (por lo general tendrá el mismo nombre)


#!El contador no puede funcionar, ya que los parámetros no salen fuera de la función. ¿Una clase de contador?
def contador (n):
    n += 1
    if n > 20:
        n = 0
        return True
    print (n)
    

#Crea un contador universal. 
#n debería ser self.n para que cada clase tenga su contador.
#Los n deberían inialiarse en 0.
#m es el máximo de iteraciones posibles antes de volver a 0

def generador_bloques(sprites, group_list, clase, x, y):
    ruta_imagen = 'models/blocks'
    clase.carpeta = ruta_imagen
    clase.rect.x = x
    clase.rect.y = y
    sprites.add(clase)
    group_list.add(clase)



class Detectar_Colision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.temporizador = Temporizador(20)
     
    def update(self):
        ...
        
    def detect(self, unidad, grupo, booleano, player): #solo para mobs
        
        self.unidad = unidad
        self.grupo = grupo
        self.booleano = booleano
        self.hit_list = pygame.sprite.spritecollide(self.unidad, self.grupo, self.booleano)
        for _ in self.hit_list:
            if unidad.vida > 0:
                self.unidad.vida -= 1
                player.score += 1
                print (player.score)
            if unidad.vida <= 0:
                self.unidad.aparicion = False
   
    
    #Esta función debería tomar dos caminos dependiendo de si es una lista o no.
    def recibir_impacto(self, unidad, grupo, booleano):
        self.unidad = unidad
        self.grupo = grupo
        self.booleano = booleano
       
        #print(type(unidad)) #conocer de qué tipo es una instancia

        #LA PRIMERA CONDICIÓN ES PARA CUANDO COLISIONA CON GRUPOS
        if isinstance(unidad, pygame.sprite.Group):
            self.hit_list = pygame.sprite.groupcollide(self.unidad, self.grupo, self.booleano, True)
            
       
        elif isinstance (grupo, list):
            for mob in grupo:
                if self.unidad.rect.colliderect(mob.rect):
                    if not unidad.guardia_activa and self.temporizador.temporizar(20) and mob.vida:
                        self.unidad.vidas -= 1
                        print("¡Colisión detectada!")
                        class_soundtrack.daño_recibido.play()
                    unidad.guardia_activa = False

        #!EN EL MOMENTO EN EL QUE UN MOB MUERE, EL OTRO DEJA DE HACER DAÑO... NECESITAN LISTAS INDEPENDIENTES
        else:
            self.hit_list = pygame.sprite.spritecollide(self.unidad, self.grupo, self.booleano)
            for _ in self.hit_list:
                if self.booleano and not unidad.guardia_activa:
                    self.unidad.vidas -=1
                    class_soundtrack.daño_recibido.play()
                if not unidad.guardia_activa and self.temporizador.temporizar(20):    
                    self.unidad.vidas -=1
                    class_soundtrack.daño_recibido.play()
                unidad.guardia_activa = False
    