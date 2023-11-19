import pygame,glob,random
import os

ancho = 900
alto = 554


carpeta= 'models/player/caminar'
patron_png = os.path.join(carpeta, '*.png')
player_caminar_list=[]
player_caminar_list = glob.glob(patron_png)





class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.lista_caminar = player_caminar_list #La tengo aquí por tenerla....
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 480
        self.speed_x = 0
        self.speed_y = 0
        self.vidas = 10
        self.direction = "right"
        
        # variables del salto,caida y gravedad
        self.jumping = False
        self.jump_count = 10
        self.is_falling = False
        self.colision_block = False

        #Variables habilidades
        self.skill = None
        self.amount_charge = 0
        
        
    def changespeed_x(self, x):
        self.speed_x += x
        if x > 0:
            self.image = pygame.image.load(os.path.join(player_caminar_list[random.randint(0,5)])).convert_alpha()
            self.direction = "right"
        elif x < 0:
            self.image = pygame.image.load(os.path.join('models', 'player_left.png')).convert_alpha()
            self.direction = "left"
        if not self.jumping and self.rect.y < 480:
            self.speed_y = +5
    def esquivar(self):
        self.image= pygame.image.load(os.path.join('models', 'player', 'player_summoning_2.png')).convert_alpha()
        

    def update(self):  
        #contador interno de animacion
    
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y > 480:
            self.rect.y = 480
        # Lógica salto
        if self.jumping:
            self.is_falling = True
            self.image = pygame.image.load(os.path.join('models','player','player_summoning_1.png')).convert_alpha()
            if self.jump_count >= -8:
                self.rect.y -= int((self.jump_count * abs(self.jump_count)) * 0.4)
                self.jump_count -= 1

            else:
                self.jump_count = 10
                self.jumping = False
                self.image= pygame.image.load(os.path.join('models', 'player', 'player_summoning_2.png')).convert_alpha()
                if not self.colision_block:
                    self.is_falling=False

    def atack(self,skill):
        match skill:
            case 0:
                self.image = pygame.image.load(os.path.join('models','player','player_sword_right.png')).convert_alpha()
                if self.direction == "left":
                    self.image = pygame.image.load(os.path.join('models','player','player_sword_left.png')).convert_alpha()
            case 1:
                self.image = pygame.image.load(os.path.join('models','player','arco', 'player_arco_5.png')).convert_alpha()
                
            case 2:
                self.image = pygame.image.load(os.path.join('models','player','player_summoning_1.png')).convert_alpha()
            
            case 3:
                self.image = pygame.image.load(os.path.join('models', 'player_concentrate.png')).convert_alpha()
                if self.direction == "left":
                    self.image = pygame.image.load(os.path.join('models','player','player_concentrate_left.png')).convert_alpha()
            
            
           
            case 5:
                self.image = pygame.image.load(os.path.join('models','player','player_summoning_1.png')).convert_alpha()
      

    def deteccion_colision(self,blocks_list,block_rect,block_y,block_top,block_left,block_rigth):
        #if self.rect.colliderect(block_rect):
        if pygame.sprite.spritecollide(self, blocks_list, False):
            self.colision_block = True
            if self.rect.y > block_y:
                self.rect.y += 15
                self.is_falling = False
            elif self.is_falling: #PISAR PLATAFORMAS. Es la condición más importante
                self.rect.bottom = block_top
            elif self.speed_x > 0:
                self.rect.x -= 1
                self.speed_x = 0
            elif self.speed_x < 0:
                self.rect.x += 1
                self.speed_x = 0
        elif not self.rect.colliderect(block_rect):
            self.colision_block= False
            self.is_falling = False