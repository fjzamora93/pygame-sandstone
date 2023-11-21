import pygame, random, sys, os
import soundtrack

ancho=900
alto=554



class Minion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models', 'particle', 'biter.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho)
        self.rect.y = random.randrange(alto)
        self.speed = 1


    def update(self):
        self.rect.y += self.speed
        if self.rect.y > alto:
            self.rect.y = -10
            self.rect.x = random.randrange(ancho)
    
    
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

        #Condiciones de los ataques
        self.skill = 0 
        self.speed = 5
        self.speed_y = 0
        self.limite = 3
        self.cargas_acumuladas = 0

        #Solo para el mob (de ahí que esté en negativo)
        self.target = -10
        

        
    def update(self):
        
        if self.vector == "vertical": #SUBIDA DEL MISIL
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

    def skill_set(self,all_sprites_list,proyectil_list):
        print (f"Depuración Nº3: {self.cargas_acumuladas}")
      
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




class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_up.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.temporizador = 10
        self.rect.x = 0
        self.rect.y = 0
        self.jumping = False
        self.speed_x = 0
        self.speed_y = 1
        self.aparicion= False
        self.vida = 10
        self.direction = "right"
        self.jumping = False
        self.jump_count = 10
        self.listado_acciones= ["atacar","desplazarse", "misil", "pausa", "salto"]

    def accion_aleatoria(self, all_sprites_list, mob_atack_list,player_position):
        if self.vida > 0:
            all_sprites_list.add(self)
            eleccion= random.choice(self.listado_acciones)
            self.temporizador -= 1
            if self.temporizador == 0:
                self.temporizador = 20
                if eleccion == "atacar":
                    self.atacar(all_sprites_list, mob_atack_list,player_position)
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
                elif eleccion == "salto":
                    self.jumping = True   
                elif eleccion == "misil":
                    self.misil(all_sprites_list, mob_atack_list, player_position)      
        else:
            self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_death.png')).convert_alpha()
            self.rect.y = 500
            
            
        
    def atacar(self,all_sprites_list, mob_atack_list, player_position):
        self.mob_atack = Proyectil(self.rect.x,self.rect.y,self.direction)
        self.mob_atack.vector = "horizontal"
        self.mob_atack.speed = 3
        self.mob_atack.image = pygame.image.load(os.path.join('models','skill','bad_omen.png')).convert_alpha()
        if player_position > self.rect.x:
            self.direction = "right"
            self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_atack.png')).convert_alpha()
        elif player_position < self.rect.x:
            self.direction = "left"
            self.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_atack.png')).convert_alpha()
        all_sprites_list.add(self.mob_atack)
        mob_atack_list.add(self.mob_atack)

    def misil(self,all_sprites_list, mob_atack_list, player_position):
        self.mob_atack = Proyectil(self.rect.x,self.rect.y,self.direction)
        self.mob_atack.vector = "vertical"
        self.mob_atack.target = player_position
        
        self.mob_atack.image = pygame.image.load(os.path.join('models','skill','conduit.png')).convert_alpha()
        
        all_sprites_list.add(self.mob_atack)
        mob_atack_list.add(self.mob_atack)
    
        

    def update(self):
        self.rect.x += self.speed_x
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
    
    
         
    def spawn(self,player_x,player_y):
        if self.aparicion == False:
            self.rect.y = player_y
            self.aparicion=True
            if player_x < ancho // 2:
                self.rect.x = player_x + 300
            elif player_x > ancho // 2:
                self.rect.x = player_x - 300
        
            
            


