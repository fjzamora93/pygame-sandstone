"""

Instalar la librería de movie: pip install pygame moviepy
Buscar un tutorial para GIF

Librería de artes gratis: https://opengameart.org/content/lpc-medieval-fantasy-character-sprites
"""


import pygame, random, os
import soundtrack,textos_pantalla,stats
pygame.mixer.init() #Para reproducir sonidos, guapi


ancho = 900
alto = 554
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5


#todo ANTES DE CLASS GAME, PODRÍAN IR TODAS LAS CLASES IMPORTADAS
from class_generic import Proyectil
from class_generic import Minion
from class_generic import Mob
from class_player import Player
from class_blocks import Block
from class_blocks import obtener_ruta
from background import obtener_background_path
from class_items import Items


class Game(object):
    def __init__(self):
        # Creamos una instancia de game over FALSE
        soundtrack.ambiente_sunset.play()
        self.game_over = False
        self.score = 0
        self.n = 0
        self.contador_1 = 0
        self.nivel_dificultad = 1
        
        self.condicion= False
        self.proyectil_case = 0
        self.cargas_acumuladas = 0
        

        # Creamos todas las listas donde estamos acumulando cosas
        self.proyectil_list = pygame.sprite.Group()
        self.minion_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.mob_list =pygame.sprite.Group()
        self.mob_atack_list = pygame.sprite.Group()
        self.fuegos_cruzados = pygame.sprite.Group()
        self.blocks_list =pygame.sprite.Group()
        self.items_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()

        
        for i in range(5):
            self.minion = Minion()
            self.all_sprites_list.add(self.minion)  
            self.minion_list.add(self.minion)
   

        for i in range(10):
            self.block = Block()
            self.all_sprites_list.add(self.block)
            self.blocks_list.add(self.block)

        for i in range(10):
            self.platform_2 = Block()
            self.platform_2.rect.y = 300
            self.all_sprites_list.add(self.platform_2)
            self.platform_list.add(self.platform_2)


        #!INICIALIZACIÓN DE ENTIDADES
        self.item = Items()
        self.mob = Mob()
        self.player = Player()
        self.proyectil = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)
        self.block = Block()
        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.block)
        self.all_sprites_list.add(self.item)
        self.blocks_list.add(self.block)
        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            if event.type == pygame.KEYDOWN:
                #Lógica de movimientos y salto
                if event.key == pygame.K_d:
                    self.player.changespeed_x(5)
                if event.key == pygame.K_a:
                    self.player.changespeed_x(-5)
                if event.key == pygame.K_s:
                    self.player.esquivar()
                if not self.player.jumping:
                    if event.key == pygame.K_w:
                        self.player.jumping = True

                #Lógica de ataques
                if event.key == pygame.K_SPACE:
                    self.proyectil = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)
                    self.proyectil.cargas_acumuladas = self.cargas_acumuladas
                    self.cargas_acumuladas -= 1
                    if self.cargas_acumuladas < 0:
                        self.cargas_acumuladas = 0
                    
                    self.proyectil.skill = self.proyectil_case
                    self.player.atack(self.proyectil_case)
                    self.proyectil.skill_set(self.all_sprites_list,self.proyectil_list)
                
                if event.key == pygame.K_q:
                    self.proyectil = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)
                    self.proyectil.vector = "vertical"
                    self.proyectil.skill = 5
                    self.proyectil.skill_set(self.all_sprites_list,self.proyectil_list)
             
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.player.speed_x = 0
                if event.key == pygame.K_a:
                    self.player.speed_x = 0
            
           

             #CREAMOS UNA NUEVA LÓGICA PARA REINICIAR EL JUEGO
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    if self.game_over:
                        self.__init__()

            
        # Obtén las coordenadas del ratón
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print(f"X: {mouse_x}, Y: {mouse_y}")

        # Se me olvidó qué es esto
        return False

    def run_logic(self):
        if not self.game_over:
            self.all_sprites_list.update()

            
            self.player.deteccion_colision(self.blocks_list,self.block.rect,self.block.rect.y,self.block.rect.top,self.block.rect.left,self.block.rect.right)
            self.player.deteccion_colision(self.platform_list,self.platform_2.rect,self.platform_2.rect.y,self.platform_2.rect.top,self.platform_2.rect.left,self.platform_2.rect.right)

     
      
            #!BOSS Y MOBS PRINCIPALES
            if self.score % 10 == 0 :
                self.mob.spawn(self.player.rect.x, self.player.rect.y)
                self.mob.accion_aleatoria(self.all_sprites_list, self.mob_atack_list,self.player.rect.x)
                self.mob_list.add(self.mob)
            if pygame.Rect.colliderect(self.player.rect, self.mob.rect) and self.mob.vida > 0:
                if self.mob.temporizador == 10: #ralentiza ticks para que el mob haga menos daño por colision
                    self.player.vidas -=1
            #Daño al mob        
            fuegos_cruzados = pygame.sprite.groupcollide(self.proyectil_list,self.mob_atack_list, False, True)
            mob_hit_list = pygame.sprite.spritecollide(self.mob,self.proyectil_list, True)
            for _ in mob_hit_list:
                self.mob.vida -= 1 
                self.mob.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_damage.png')).convert_alpha()
            
            #!MINIONS Y MOBS SECUNDARIOS            
            if len(self.minion_list) == 0:
                for i in range(self.nivel_dificultad):
                    self.nivel_dificultad += 1
                    self.minion_1 = Minion()
                    self.minion_1.speed += self.nivel_dificultad
                    self.minion_1.image = pygame.image.load(os.path.join('models','skill','pointed_dripstone.png'))
                    self.minion_list.add(self.minion_1)
                    self.all_sprites_list.add(self.minion_1)

            #Daño y pérdida de vida
            player_hit_list = pygame.sprite.spritecollide(self.player, self.minion_list, True)
            player_hit_list += pygame.sprite.spritecollide(self.player, self.mob_atack_list, True)
            for _ in player_hit_list:
                self.player.vidas -= 1
                soundtrack.daño_recibido.play()

            #Puntuación y score    
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.minion_list, False,True)    
            for shot in success_shot_list:
                self.score += 1
                self.cargas_acumuladas += 2
                soundtrack.coins.play()
            
            
            #! BONIFICACIONES Y CONTROL DE ATAQUE
            if len(self.proyectil_list) > self.proyectil.limite:
                sprite_a_eliminar = self.proyectil_list.sprites()[self.proyectil.limite]
                sprite_a_eliminar.kill()

            if pygame.sprite.spritecollide(self.player,self.items_list, True):
                self.cargas_acumuladas += 10
                if self.item.list_path_random == "models/items\gema.png":
                    self.player.vidas += 1
                if self.item.list_path_random == "models/items\manzana.png":
                    self.player.vidas += 0
                if self.item.list_path_random == "models/items\pearl.png":
                    self.proyectil_case = 1
                if self.item.list_path_random == "models/items\libro.png":
                    self.proyectil_case = 2
                if self.item.list_path_random == "models/items\diamond.png":
                    self.proyectil_case = 3
                if self.item.list_path_random == "models/items\emerald.png":
                    self.proyectil_case = 4
                self.item = Items()
                
                self.all_sprites_list.add(self.item)
            
            
            if random.randint(0,1000) == 10:
                self.item = Items()
            self.items_list.add(self.item)
                


            #!Condición de GAME OVER
            if self.player.vidas == 0:
                self.game_over = True
            
    def display_frame(self,screen):
        #TODO Este es el contador que ralentizará las animaciones
        self.contador_1 += 1
        if self.contador_1 == 9:
            self.contador_1 = 0
        if self.contador_1 == 0:
            if self.n<5:
                self.n += 1
            else:
                self.n = 0
        self.background = obtener_background_path()
        background= pygame.image.load(self.background[self.n]).convert()
        background_resized=pygame.transform.scale(background, (ancho, alto))
        screen.blit(background_resized, [0,0])
       
       #TODO Animaciones en movimiento propias del jugador
        if self.player.speed_x > 0:
            self.player.image=pygame.image.load(self.player.lista_caminar[self.n]).convert_alpha()


        #TODO Bloques en pantalla
      

        #! PANTALLA DE FIN DEL JUEGO
        if self.game_over and len(self.minion_list) == 0:
            textos_pantalla.texto_game_over_1(black,ancho,alto,screen)
        elif self.game_over and self.player.vidas == 0:
            textos_pantalla.texto_game_over_2(black,ancho,alto,screen)
        

        #! PANTALLA SI NO ES FIN DEL JUEGO
        if not self.game_over:
            textos_pantalla.texto_puntuacion(screen, self.score)
            stats.hearts(screen, self.player.vidas)
            textos_pantalla.texto_cargas(screen, self.cargas_acumuladas)

            #!Este de aquí es obligatorio para actualizar lo que se ve en pantalla
            self.all_sprites_list.draw(screen) 
            
        pygame.display.flip()

def main():
    pygame.init()
    screen= pygame.display.set_mode([ancho,alto])
    pygame.display.set_caption("Coordenadas del Ratón")
    done= False
    clock = pygame.time.Clock()
    game = Game()
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(50)
    pygame.quit()

if __name__ == "__main__":
    main()