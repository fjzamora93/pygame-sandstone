import pygame,glob,random, mis_funciones
from mis_funciones import Detectar_Colision
import os, mis_sprites
from class_proyectil import Proyectil
from class_items import Items
ancho = 900
alto = 554


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites_player = mis_funciones.obtener_ruta('models/player') 
        
        self.image = mis_sprites.cargar_sprite('models/player', 0)
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
        self.pisando = False

        #Variables habilidades
        self.n = 0 #mi contador de sprites
        self.animacion = False
        self.subcarpeta = None
        
        self.amount_charge = 0
        self.proyectil_case=0
        self.guardia_activa = True
        self.limite_proyectil = 1
        self.destruccion_proyectil = False
        self.colision = Detectar_Colision()
        

       

    def update(self):  
        if self.speed_x != 0:
            self.subcarpeta = 'caminar'
            self.animacion = True
            if self.speed_x > 0:
                self.direction = "right"
            elif self.speed_x < 0:
                self.direction = "left"
                
            
            
        if self.is_falling and not self.jumping and self.rect.y < 480:
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #LÍMITES DEL CAMARA
        if self.rect.y > 480:
            self.rect.y = 480
        if self.rect.x < 10:
            self.rect.x = 10
        if self.rect.x > 850:
            self.rect.x = 850

        # Lógica salto
        if self.jumping:
            self.is_falling = True
            if self.jump_count >= -8:
                self.rect.y -= int((self.jump_count * abs(self.jump_count)) * 0.4)
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.jumping = False

        #CONDICIONES ESPECIALES      
        if self.speed_x != 0:
            self.guardia_activa = False

        if self.animacion:
            self.n += 1
            if self.direction == "right":
                self.image = mis_sprites.cargar_sprite(f'models/player/{self.subcarpeta}', self.n // 4)
            elif self.direction == "left":
                 self.image = pygame.transform.flip(mis_sprites.cargar_sprite(f'models/player/{self.subcarpeta}', self.n//4), True, False) #invierte la imagen
            if self.n == 32:
                self.n = 0
                self.animacion = False
            
             
                
 
    def atack(self,skill):
        self.n = 0
        self.animacion = True
        match skill:
            case 0:
                self.subcarpeta = 'sword'
            case 1:
                self.subcarpeta='arco'
            case 2:
                self.subcarpeta='concentrate'
            case 3:
                self.subcarpeta='concentrate'
            case 5:
                self.subcarpeta='cast'
            case 6:
                self.subcarpeta='protection'

    def proteccion(self):
        self.guardia_activa = True
        self.subcarpeta = 'protection'
        
    

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
            self.is_falling = True

    def controles_1(self,event,all_sprites_list,proyectil_list):
        if event.type == pygame.KEYDOWN:
            #Lógica de movimientos y salto
            if event.key == pygame.K_d:
                self.speed_x = 5
            if event.key == pygame.K_a:
                self.speed_x = -5
            if event.key == pygame.K_s:
                self.proteccion()
            
            if not self.jumping:
                if event.key == pygame.K_w:
                    self.jumping = True
            
            #Lógica de ataques
            if event.key == pygame.K_SPACE:
                self.proyectil = Proyectil(self.rect.x, self.rect.y, self.direction, self.limite_proyectil)
                self.proyectil.cargas_acumuladas = self.amount_charge
                self.proyectil.skill = self.proyectil_case

                self.atack(self.proyectil_case)
                if self.proyectil.skill != 0:
                    self.amount_charge -= 1
                if self.amount_charge <= 0:
                    self.amount_charge = 0
                    self.proyectil.skill = 0
                    self.atack(0)
                    self.proyectil_case = 0

                self.proyectil.skill_set(all_sprites_list,proyectil_list)
            
            if event.key == pygame.K_q:
                self.proyectil = Proyectil(self.rect.x, self.rect.y, self.direction, 3)
                self.destruccion_proyectil = True
                self.proyectil.vector = "vertical"
                self.proyectil.skill = 5
                self.proyectil.skill_set(all_sprites_list,proyectil_list)
             
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.speed_x = 0
            if event.key == pygame.K_a:
                self.speed_x = 0


    def clasificar_proyectil(self,all_sprites_list,item):      
        self.amount_charge += 5
        self.destruccion_proyectil = True
        if item.list_path_random == "models/items\manzana.png":
            self.vidas += 1
            self.limite_proyectil = 2
        if item.list_path_random == "models/items\manzana_dorada.png":
            self.vidas += 2
            self.limite_proyectil = 3
        if item.list_path_random == "models/items\larco.png":
            self.proyectil_case = 1
            self.limite_proyectil = 2
        if item.list_path_random == "models/items\diamond.png":
            self.proyectil_case = 2
            self.limite_proyectil = 3
        if item.list_path_random == "models/items\lantern.png":
            self.proyectil_case = 3
            self.limite_proyectil = 2
        if item.list_path_random == "models/items\libro.png":
            self.proyectil_case = 4
            self.limite_proyectil = 1
            self.destruccion_proyectil = False
        
        
                
        

