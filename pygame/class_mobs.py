import pygame, random, sys, os, class_soundtrack, mis_sprites, temporizador, stats
from class_proyectil import Proyectil
from colisiones import Detectar_Colision
ancho=900
alto=554
screen= pygame.display.set_mode([ancho,alto])


class Mob(pygame.sprite.Sprite):
    def __init__(self, subcarpeta, nivel, player_x):
        super().__init__()
        self.n = 0
        self.nivel = nivel
        self.image = mis_sprites.cargar_sprite(f'models/entity/{subcarpeta}/{nivel}', self.n)
        self.rect = self.image.get_rect()
        self.rect.x = 400 #EN ALGÚN MOMENTO LO TENDRÁS QUE METER ESTO COMO PARÁMETRO
        self.rect.y = 0
        self.speed = 1
        self.speed_y = 1
        self.direction = "right"
        self.vida = self.nivel 
        self.stats = None
       
        #Gestión de acciones
        self.posicion_origen = self.rect.x, self.rect.y
        self.posicion_jugador = player_x
        self.aparicion= False
        self.count = temporizador.Temporizador(20 - self.nivel) #creamos una clase de temporizador
        self.jumping = False
        self.jump_count = 10
        self.listado_acciones= ["atacar","desplazarse", "misil", "pausa", "salto"]
        self.eleccion = None


        #Gestión de frames y colisiones
        self.colision = Detectar_Colision()
        self.subtipo = subcarpeta
        
        
    def update(self):
        if self.subtipo == "minion":
            self.movimiento_minion()
        if self.subtipo == "mob":
            self.movimiento_bucle()
           

        if self.subtipo != "minion":
            if self.count.temporizar(20):
                self.image_update()
            self.rect.x += self.speed
            if self.rect.x < 0: 
                self.rect.x = 0
            if self.rect.x > 700:
                self.rect.x = 700
            if self.jumping:
                if self.jump_count >= -10:
                    self.rect.y -= int((self.jump_count * abs(self.jump_count)) * 0.4)
                    self.jump_count -= 1
                else:
                    self.jump_count = 10
                    self.jumping = False
            if self.vida <= 0:
                self.speed = 0

    def accion_aleatoria(self, sprites_list, mob_atack_list,player_position):
        if self.vida > 0:
            self.eleccion= random.choice(self.listado_acciones)
            if self.count.contador == 0:
                match self.eleccion:
                    case "atacar":
                        self.atacar(sprites_list, mob_atack_list,player_position)
                    case "desplazarse":
                        self.desplazarse()
                    case "pausa":
                        self.speed = 0
                        self.count.contador = 0
                    case "salto":
                        self.jumping = True   
                    case "misil":
                        self.misil(sprites_list, mob_atack_list, player_position)   
            
            
        
    def atacar(self,all_sprites_list, mob_atack_list, player_position):
        self.attacking = True
        self.mob_atack = Proyectil(self.rect.x,self.rect.y,self.direction,3)
        self.mob_atack.skill = -5 #PON EN NEGATIVO LA SKILL DEL MOB, EN POSITIVO LAS DEL PLAYER
        self.mob_atack.vector = "horizontal"
        self.mob_atack.speed = 3
        self.mob_atack.subtipo = "smoke"
        if player_position > self.rect.x:
            self.direction = "right"
        elif player_position < self.rect.x:
            self.direction = "left"
        all_sprites_list.add(self.mob_atack)
        mob_atack_list.add(self.mob_atack)

    def desplazarse(self):
        if self.rect.x < 100:
            self.speed += 3
        elif self.rect.x > 700:
            self.speed -= 3
        else:
            self.speed += random.randint(-5,5)
    
    def movimiento_bucle(self):
        if self.rect.x < self.posicion_origen[0] - 100:
            self.speed = 3
        if self.rect.x > self.posicion_origen[0] + 100:
            self.speed = -3
       

    def misil(self,all_sprites_list, mob_atack_list, player_position):
        self.mob_atack = Proyectil(self.rect.x,self.rect.y,self.direction,3)
        self.mob_atack.skill = -3
        self.mob_atack.vector = "vertical"
        self.mob_atack.target = player_position
        self.mob_atack.subtipo = "rocket"
        all_sprites_list.add(self.mob_atack)
        mob_atack_list.add(self.mob_atack)

    
    def image_update(self):
        if self.speed == 0:
            self.n = 0
        elif self.speed > 0:
            self.n = 1
            self.direction = "right"
        elif self.speed < 0:
            self.n = 2
            self.direction = "left"
        if self.jumping:
            self.n = 3
        elif self.eleccion == "atacar":
            self.n = 4
        elif self.eleccion == "pausa":
            self.n = 6
        if self.vida <= 0 :
           self.n = 5 #Los sprites los detecta fatal... El 5 es el 4???
        self.image = mis_sprites.cargar_sprite(f'models/entity/{self.subtipo}/{self.nivel}', self.n)
        if self.direction == "left":
            self.image = pygame.transform.flip(mis_sprites.cargar_sprite(f'models/entity/{self.subtipo}/{self.nivel}', self.n), True, False)
        
 
    def spawn(self, player_x, sprites_list, mob_list):
        if self.vida > 0:
            sprites_list.add(self)
            if self.aparicion == False:
                mob_list.append (self)
                self.rect.y = 480
                self.aparicion=True
                if player_x < ancho // 2:
                    self.rect.x = player_x + 300
                elif player_x > ancho // 2:
                    self.rect.x = player_x - 300
                    
                #ACTUALIZACIÓN DE STATS
                if self.subtipo == "boss":
                    self.vida = 10
                self.stats = stats.Stats(f'models/stats/{self.subtipo}',self.rect.x, self.rect.y, self.vida)
                sprites_list.add(self.stats)
            self.stats.actualizar( self.rect.x, self.rect.y -30, self.vida, self.subtipo)
        else:
            sprites_list.remove(self.stats)
            #del instancia, es la otra forma de acabar con una instancia
       
        



    def generar_minion(self, sprites, minion_list):
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(alto)
        self.speed_y = 1
        sprites.add(self)  
        minion_list.add(self)

    def movimiento_minion(self):
        self.rect.y += self.speed
        if self.rect.y > alto:
            self.rect.y = -10
            self.rect.x = random.randrange(ancho)

    
        
    

 