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

from class_mobs import Minion
from class_mobs import Mob
from class_proyectil import Proyectil
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
        self.autodestruccion= True
        self.camera = 0
    

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

        
        for i in range(10):
            self.minion = Minion()
            self.all_sprites_list.add(self.minion)  
            self.minion_list.add(self.minion)
   

        for i in range(8):
            self.block = Block() 
            self.block.rect.y = 300
            self.all_sprites_list.add(self.block)
            self.blocks_list.add(self.block)
       
        for i in range(2):
            self.platform_2 = Block()
            self.platform_2.carpeta = 'models/blocks/big-block'
            self.platform_2.obtener_ruta()
            self.platform_2.rect.y = 400
            self.all_sprites_list.add(self.platform_2)
            self.platform_list.add(self.platform_2)
       

        #!INICIALIZACIÓN DE ENTIDADES
        self.item = Items()
        self.mob = Mob()
        self.vidas_mob = self.mob.vida

        self.player = Player()
        self.x = self.player.rect.x

        self.proyectil = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)

        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.item)
    
        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            self.player.controles_1(event,self.all_sprites_list,self.proyectil_list)
           

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
            if self.score % 20 == 0:
                if self.mob.vida <= 1:
                    self.mob.kill()
                    self.mob = Mob()      
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
                self.score += 1 
                self.mob.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_damage.png')).convert_alpha()
            
            #!MINIONS Y MOBS SECUNDARIOS            
            if len(self.minion_list) == 0:
                for i in range(self.nivel_dificultad):
                    self.nivel_dificultad = 10
                    self.minion_1 = Minion()
                    self.minion_1.speed += 0
                    self.minion_1.image = pygame.image.load(os.path.join('models','skill','pointed_dripstone.png'))
                    self.minion_list.add(self.minion_1)
                    self.all_sprites_list.add(self.minion_1)

            #Daño y pérdida de vida
            
            player_hit_list = pygame.sprite.spritecollide(self.player, self.minion_list, True)
            player_hit_list += pygame.sprite.spritecollide(self.player, self.mob_atack_list, True)
            
            if not self.player.guardia_activa:
                for _ in player_hit_list:
                    self.player.vidas -= 1
                    soundtrack.daño_recibido.play()
            if player_hit_list:
                self.player.guardia_activa = False
                self.player.image = pygame.image.load(os.path.join('models','player','player_meditate.png')).convert_alpha()
            
            #Puntuación y score    
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.minion_list, self.autodestruccion,True)    
            for shot in success_shot_list:
                
                self.score += 1
                self.player.amount_charge += 1
                soundtrack.coins.play()
            
            
            #! BONIFICACIONES Y CONTROL DE ATAQUE
            if len(self.proyectil_list) > self.proyectil.limite:
                sprite_a_eliminar = self.proyectil_list.sprites()[self.proyectil.limite]
                sprite_a_eliminar.kill()

            if pygame.sprite.spritecollide(self.player,self.items_list, True):
                self.player.clasificar_proyectil(self.all_sprites_list, self.item)

            if random.randint(0,500) == 500:
                self.item = Items()
                self.all_sprites_list.add(self.item)
            self.items_list.add(self.item)
            if pygame.sprite.spritecollide(self.player,self.items_list, True):
                self.item.kill()
                    

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
        background= pygame.image.load(self.background[8]).convert()

        
        self.camera += (self.player.rect.x - self.camera - ancho //2)/100
        screen.blit(background, [-900-self.camera, 0])
        self.x += self.player.speed_x // 10




       #TODO Animaciones en movimiento propias del jugador
        if self.player.speed_x > 0:
            self.player.image=pygame.image.load(self.player.lista_caminar[self.n]).convert_alpha()


        #TODO Bloques en pantalla
        
    

        #! PANTALLA DE FIN DEL JUEGO
        if self.game_over and len(self.minion_list) == 0:
            textos_pantalla.texto_game_over_1(black,ancho,alto,screen)
        elif self.game_over and self.player.vidas == 0:
            textos_pantalla.texto_game_over_2(black,ancho,alto,screen)
        

        #! STATS Y PUNTUACIONES
        if not self.game_over:
            textos_pantalla.texto_puntuacion(screen, self.score)
            stats.hearts(screen, self.player.vidas)
            stats.hearts_mob(screen,self.mob.vida)
            textos_pantalla.texto_cargas(screen, self.player.amount_charge)
            

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