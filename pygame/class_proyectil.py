import pygame, random, sys, os,glob
import class_soundtrack
import mis_funciones
import mis_sprites

ancho=900
alto=554


    
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, direction, n):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models','skill','sweep_1.png')).convert_alpha()
        self.image_list = []
        self.objeto = None      
        self.vector= "melee"
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.pos_origen = self.rect.x
        self.rect.y = player_y + 10
        self.direction = direction
        self.contador = 0
        self.n = 24

        #Condiciones de los ataques
        self.skill = 0  #El mob tiene la skill en neativo -1,-2,-3
        self.speed = 5
        self.speed_y = 0
        self.limite = n
        self.cargas_acumuladas = 0
        self.autodestruccion = True

        #Solo para el mob (de ahí que esté en negativo)
        self.target = -10
    
        #Rutas de imágenes
        self.explosion = 'models/particle/explosion'
        self.sonic = 'models/particle/sonic'
        self.proyectil_path_png = self.obtener_ruta(self.explosion)
        

        
    def update(self):
        if self.vector == "vertical": 
            self.rect.y -= self.speed
            if self.rect.y < 0:
                self.vector = "caida"
                print ("Condición 1")
        if self.vector == "caida":
            self.rect.x = self.target
            self.rect.y += 10
            print ("Condición 2")
        
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
        elif self.vector == "static":
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y
        if self.rect.x > ancho or self.rect.x < 0 or self.rect.y < -30 or self.rect.y > alto:
            self.kill()
        
        #!ACTUALIZACIONES DE IMAGEN
        self.contador += 1
        if self.contador >= self.n:
            self.contador = 0
        
        if self.skill == 4 or self.skill == 2 or self.skill == 0 or self.skill == 3:
            self.image = pygame.image.load(os.path.join(self.image_list [self.contador//3])).convert_alpha()
          


    def skill_set(self, all_sprites_list, proyectil_list):
        if self.skill == 0 or self.cargas_acumuladas <= 0:
            self.image_list = mis_funciones.obtener_ruta(mis_sprites.sword)
            class_soundtrack.sword.play()

        if self.skill == 1 and self.cargas_acumuladas > 0:    
            self.image = pygame.image.load(os.path.join('models','skill','arrow.png')).convert_alpha()
            self.speed_y += 0.5
            self.speed = 10
           
            class_soundtrack.arco.play()
            self.vector = "horizontal"
            if self.direction == "left":
                self.image = pygame.image.load(os.path.join('models','skill','arrow_left.png')).convert_alpha()

        if self.skill == 2 and self.cargas_acumuladas > 0:    
            self.image_list = mis_funciones.obtener_ruta(mis_sprites.ice)
            class_soundtrack.ice.play()
            self.vector = "horizontal"
            self.speed = 15

        

        if self.skill == 3 and self.cargas_acumuladas > 0:         
            self.image_list = mis_funciones.obtener_ruta(mis_sprites.explosion)
            class_soundtrack.atack_fireball_1.play()
            self.vector = "horizontal"
            self.speed = 15

        #! FORMA 2 DE OBTENER UN PATH DE IMAGEN, CREO QUE QUEDA MÁS LIMPIO
        if self.skill == 4 and self.cargas_acumuladas > 0:    
            self.image_list = mis_funciones.obtener_ruta(mis_sprites.sonic)
            class_soundtrack.efecto_magia_1.play()
            self.vector = "horizontal"
            self.n = 47
            self.speed = 10
            self.rect.y -= 20

        if self.skill == 5:
            self.image = pygame.image.load(os.path.join('models','skill','rocket.png')).convert_alpha()
            class_soundtrack.atack_laser.play()
            print ("LIMITE A 5!!")

        if self.skill == 6:
            self.image= pygame.image.load(os.path.join('models', 'skill', 'buble.png')).convert_alpha()
            self.vector = "static"
            
        
            
        all_sprites_list.add(self)
        proyectil_list.add(self)

    def obtener_ruta(self,ruta):
        self.patron_png = os.path.join(ruta, '*.png')
        self.proyectil_path_png=[]
        self.proyectil_path_png = glob.glob(self.patron_png)
        return self.proyectil_path_png