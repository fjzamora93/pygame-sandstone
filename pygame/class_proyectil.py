import pygame, random, sys, os,glob
import soundtrack

ancho=900
alto=554


    
class Proyectil(pygame.sprite.Sprite):
    def __init__(self,player_x,player_y,direction):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models','skill','sweep_1.png')).convert_alpha()
        self.objeto = None      
        self.vector= "melee"
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.pos_origen = self.rect.x
        self.rect.y = player_y + 10
        self.direction = direction
        self.contador = 0

        #Condiciones de los ataques
        self.skill = 0 
        self.speed = 5
        self.speed_y = 0
        self.limite = 3
        self.cargas_acumuladas = 0

        #Solo para el mob (de ahí que esté en negativo)
        self.target = -10
    
        #Rutas de imágenes
        self.carpeta = 'models/particle/explosion'
        self.proyectil_path_png = self.obtener_ruta()
        

        
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

        elif self.vector == "melee":
            if self.direction == "right":
                self.rect.x += self.speed 
            elif self.direction == "left":
                self.rect.x -= self.speed
            if self.rect.x > self.pos_origen +100 or self.rect.x  < self.pos_origen-120:
                self.kill()
        
        elif self.vector == "static":
            self.rect.x = self.rect.x
            self.rect.y = self.rect.y
            

        if self.rect.x > ancho or self.rect.x < 0 or self.rect.y < -30 or self.rect.y > alto:
            self.kill()
        
        #ACTUALIZACIÓN DE IMAGEN
        self.contador += 1
        if self.contador > 49:
            self.contador = 0
        if self.skill == 3:
            self.image = pygame.image.load(os.path.join(self.proyectil_path_png[self.contador//10])).convert_alpha()

    def skill_set(self,all_sprites_list,proyectil_list):
        if self.skill == 0 or self.cargas_acumuladas <= 0:
            self.image = pygame.image.load(os.path.join('models','skill','sweep_1.png')).convert_alpha()
            soundtrack.sword.play()

        if self.skill == 1 and self.cargas_acumuladas > 0:    
            self.image = pygame.image.load(os.path.join('models','skill','arrow.png')).convert_alpha()
            self.speed_y += 0.5
            self.speed = 10
            soundtrack.arco.play()
            self.vector = "horizontal"
            if self.direction == "left":
                self.image = pygame.image.load(os.path.join('models','skill','arrow_left.png')).convert_alpha()

        if self.skill == 2 and self.cargas_acumuladas > 0:    
            self.image = pygame.image.load(os.path.join('models','skill','snowball.png')).convert_alpha()
            soundtrack.ice.play()
            self.vector = "horizontal"
            self.speed = 10
            self.limite = 5
          
        if self.skill == 3 and self.cargas_acumuladas > 0:         
            self.image = pygame.image.load(os.path.join('models','skill','fireball.png')).convert_alpha()
            soundtrack.atack_fireball_1.play()
            self.vector = "horizontal"
            self.speed = 10
            self.limite = 10

        if self.skill == 4 and self.cargas_acumuladas > 0:    
            self.image = pygame.image.load(os.path.join('models','skill','sonic.png')).convert_alpha()
            soundtrack.efecto_magia_1.play()
            self.vector = "horizontal"
            self.speed = 5
            self.rect.y -= 20
            self.limite = 20

        if self.skill == 5:
            self.image = pygame.image.load(os.path.join('models','skill','rocket.png')).convert_alpha()
            soundtrack.atack_laser.play()

        if self.skill == 6:
            self.image= pygame.image.load(os.path.join('models', 'skill', 'buble.png')).convert_alpha()
            self.vector = "static"
        
            
        all_sprites_list.add(self)
        proyectil_list.add(self)

    def obtener_ruta(self):
        self.patron_png = os.path.join(self.carpeta, '*.png')
        self.proyectil_path_png=[]
        self.proyectil_path_png = glob.glob(self.patron_png)
        return self.proyectil_path_png