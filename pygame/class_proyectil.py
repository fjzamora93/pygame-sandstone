import pygame, random, sys, os,glob
import class_soundtrack
import colisiones
import mis_sprites

ancho=900
alto=554


    
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, direction, n):
        super().__init__()
        self.image = mis_sprites.cargar_sprite('models/particle/sword', 0)
        self.image_list = []
        self.objeto = None      
        self.vector= "melee"
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.pos_origen = self.rect.x
        self.rect.y = player_y + 10
        self.direction = direction
        self.contador = 0
   

        #Condiciones de los ataques
        self.subtipo = "sword"
        self.skill = 0  
        self.speed = 5
        self.speed_y = 0
        self.limite = n
        self.cargas_acumuladas = 0
        self.autodestruccion = True
       
        #Solo para el mob (de ahí que esté en negativo)
        self.target = -10
    

        
    def update(self):
        if self.vector == "vertical": 
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.vector = "caida"
                
        if self.vector == "caida":
            self.rect.x = self.target
            self.rect.y += 10
           
        elif self.vector== "horizontal":
            self.rect.y += self.speed_y
            if self.direction == "right":
                self.rect.x += self.speed
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.skill == 3:
                if self.rect.x > self.pos_origen +350 or self.rect.x  < self.pos_origen-350:
                    self.kill()

        elif self.vector == "melee":
            if self.direction == "right":
                self.rect.x += self.speed 
            elif self.direction == "left":
                self.rect.x -= self.speed
            if self.rect.x > self.pos_origen +80 or self.rect.x  < self.pos_origen-100:
                self.kill()
        
        #PARA EL ESCUDO
        if self.vector == "static":
            self.speed = 0
        if self.rect.x > ancho or self.rect.x < 0 or self.rect.y < -30 or self.rect.y > alto:
            self.kill()
        
        #!ACTUALIZACIONES DE IMAGEN
        self.contador += 1
        if self.contador >= 20:
            self.contador = 0
        self.image = mis_sprites.cargar_sprite(f'models/particle/{self.subtipo}', self.contador//3).convert_alpha()
            
          

    def skill_set(self, all_sprites_list, proyectil_list):
        if self.skill == 0 or self.cargas_acumuladas <= 0:
            class_soundtrack.sword.play()
            self.subtipo = "sword"

        if self.skill == 1 and self.cargas_acumuladas > 0:    
            self.speed_y += 0.5
            self.speed = 10
            self.subtipo = "arrow"
            class_soundtrack.arco.play()
            self.vector = "horizontal"
            
        if self.skill == 2 and self.cargas_acumuladas > 0:    
            class_soundtrack.ice.play()
            self.vector = "horizontal"
            self.speed = 15
            self.subtipo = "ice"
        
        if self.skill == 3 and self.cargas_acumuladas > 0:         
            class_soundtrack.atack_fireball_1.play()
            self.vector = "horizontal"
            self.speed = 15
            self.subtipo = "explosion"

        if self.skill == 4 and self.cargas_acumuladas > 0:    
            class_soundtrack.efecto_magia_1.play()
            self.vector = "horizontal"
            self.speed = 10
            self.rect.y -= 20
            self.subtipo = "sonic"

        if self.skill == 5:
            class_soundtrack.atack_laser.play()
            self.subtipo = "rocket"

        if self.skill == 6:
            self.vector = "static"
            self.subtipo = "shield"
            
        all_sprites_list.add(self)
        proyectil_list.add(self)

    