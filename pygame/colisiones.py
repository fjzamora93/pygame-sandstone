#Archivo con varias funciones útiles en cualquier caso:
import os,glob,pygame
import class_soundtrack
from temporizador import Temporizador



class Detectar_Colision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.temporizador = Temporizador(20)
     
    def update(self):
        ...
    
    #Función aplicada a los mobs
    def detect(self, unidad, grupo, booleano, player): #solo para mobs
        if unidad.vida > 0:
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
    

def generador_bloques(sprites, group_list, clase, x, y):
    ruta_imagen = 'models/blocks'
    clase.carpeta = ruta_imagen
    clase.rect.x = x
    clase.rect.y = y
    sprites.add(clase)
    group_list.add(clase)