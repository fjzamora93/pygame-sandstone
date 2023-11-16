import pygame, random, sys, os
import soundtrack

ancho=900
alto=554
black = (0,0,0)
white = (255,255,255)

class Corazon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # convert alpha es lo que va a quitar el color de fondo
        self.image = pygame.image.load("corazon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(alto)

    def update(self):
        self.rect.y += 1
        if self.rect.y > alto:
            self.rect.y = -10
            self.rect.x = random.randrange(ancho)


class Proyectil(pygame.sprite.Sprite):
    def __init__(self,player_x,player_y,direction):
        super().__init__()
        
        #IMAGEN Y POSICIÓN
        self.image = pygame.image.load(os.path.join('models','proyectil','fireball.png')).convert_alpha()
        self.objeto = None      
        self.vector= None
        self.sonidos= True #Esto activa el sonido una vez. Si está en false, se repetirá en bucle
        self.rect = self.image.get_rect()
        self.rect.x = player_x +10
        self.rect.y = player_y +10
        self.direction = direction
        self.speed = 5
        
    def update(self):
        if self.vector== "vertical":
            self.rect.y -= self.speed
            self.image = pygame.image.load("firework_rocket.png").convert_alpha()
            if self.sonidos == True:
                soundtrack.atack_laser.play()
                self.sonidos = False
        elif self.vector== "horizontal":
            if self.direction == "right":
                self.rect.x += self.speed
            if self.direction == "left":
                self.rect.x -= self.speed
            if self.sonidos == True:
                soundtrack.atack_fireball_1.play()
                self.sonidos = False
        if self.rect.x > ancho or self.rect.x < 0 or self.rect.y<0:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_up.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.temporizador = 10
        self.rect.x = 0
        self.rect.y = 0
        self.speed_x = 0
        self.aparicion= False
        self.vida = 10
        self.direction = "right"
        
        
    
    def accion_aleatoria(self, all_sprites_list, mob_atack_list,player_direction):
        self.listado_acciones= ["atacar", "desplazarse", "pausa", "salto"]
        eleccion= random.choice(self.listado_acciones)
        self.temporizador -= 1
        if self.temporizador == 0:
            self.temporizador = 10
            if eleccion == "atacar":
                self.atacar(all_sprites_list, mob_atack_list,player_direction)
            elif eleccion == "desplazarse":
                if self.rect.x < 100:
                    self.speed_x += 5
                    self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_right.png')).convert_alpha()
                elif self.rect.x > 700:
                    self.speed_x -= 5
                    self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_left.png')).convert_alpha()
                else:
                    self.speed_x += random.randint(-5,5)
            elif eleccion == "pausa":
                self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_pause.png')).convert_alpha()
                self.speed_x = 0
        
    def atacar(self, all_sprites_list, mob_atack_list, player_position):
        self.mob_atack = Proyectil(self.rect.x,self.rect.y,self.direction)
        self.mob_atack.vector = "horizontal"
        self.mob_atack.speed = 3
        self.mob_atack.image = pygame.image.load(os.path.join('models','proyectil','bad_omen.png')).convert_alpha()
        if player_position > self.rect.x:
            self.direction = "right"
            self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_atack.png')).convert_alpha()
        if player_position < self.rect.x:
            self.direction = "left"
            self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_atack.png')).convert_alpha()
        
        #!NO FUNCIONA
        if self.vida > 0:
            all_sprites_list.add(self.mob_atack)
            mob_atack_list.add(self.mob_atack)
        elif self.vida< 0:
            self.kill()
    

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x < 0: 
            self.rect.x = 0
        if self.rect.x > 700:
            self.rect.x = 700
         

    def spawn(self,player_x,player_y):
        if self.aparicion == False:
            self.rect.y = player_y
            self.aparicion=True
            if player_x < ancho // 2:
                self.rect.x = player_x + 300
            elif player_x > ancho // 2:
                self.rect.x = player_x - 300
        
            
            


