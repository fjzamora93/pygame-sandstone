

import pygame, random, os
import class_soundtrack,textos_pantalla,stats, mis_funciones
from tkinter import *
pygame.mixer.init() #Para reproducir sonidos, guapi

nivel = 2
ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5




#todo ANTES DE CLASS GAME, PODRÍAN IR TODAS LAS CLASES IMPORTADAS
import __lvl_0__

from class_mobs import Minion
from class_mobs import Mob
from class_proyectil import Proyectil
from class_player import Player
from class_blocks import Block
from class_blocks import obtener_ruta
from background import obtener_background_path
from class_items import Items
from class_soundtrack import Soundtrack
from class_button import Button
from class_mouse import Mouse
from class_menu import Menu

class Game_2(object):
    def __init__(self):
        pygame.display.set_caption("Tales of Sandstone") 
        self.nivel = 2
        self.game_over = False
        self.score = 0
        self.n = 0
        self.contador_1 = 0
       
    
        self.camera = 0
      
    

        # TODOS LAS LISTAS QUE VAMOS A UTILIZAR
        self.proyectil_list = pygame.sprite.Group()
        self.minion_list = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.mob_list =pygame.sprite.Group()
        self.mob_atack_list = pygame.sprite.Group()
        self.fuegos_cruzados = pygame.sprite.Group()
        self.blocks_list =pygame.sprite.Group()
        self.items_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        
        #TODOS LOS ENTIDADES QUE VAMOS A INICIALIZAR
        for i in range(10):
            self.minion = Minion()
            self.sprites.add(self.minion)  
            self.minion_list.add(self.minion)
        
        self.menu = Menu(self.nivel)
        self.item = Items()
        self.boss = Mob()
        self.mob = Mob()
        self.button = Button(ancho//2,50, "Menu")
        self.inventario = Button (800, 50, "Inventario")
        self.mouse = Mouse()
        self.player = Player()
        self.x = self.player.rect.x
        self.proyectil = Proyectil(self.player.rect.x, self.player.rect.y, self.player.direction, self.player.proyectil_case+1)

        #Inicializamos la música
        self.soundtrack = Soundtrack()
        self.soundtrack.play_music(class_soundtrack.fondo)

        self.sprites.add(self.mouse)
        self.sprites.add(self.player)
        self.sprites.add(self.item)
        
       
        #Ocultamos cursor
        pygame.mouse.set_visible(False)
 
    def process_events(self,screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            #CONTROL DEL RATÓN Y BOTÓN DE MENÚ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                MOUSE_POSITION = pygame.mouse.get_pos()
                if self.button.checkForInput(MOUSE_POSITION):
                    self.menu.open_menu= True
 
            #soundtrack.control_audio(event,screen,soundtrack)
            self.player.controles_1(event,self.sprites,self.proyectil_list)
            
            if self.menu.open_menu == True:
                self.soundtrack.control_audio(event,screen)
 
            #CREAMOS UNA NUEVA LÓGICA PARA REINICIAR EL JUEGO
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        # Esto retornará false y está almacenado en la variable "done"
        return False



    def run_logic(self):
        if not self.game_over:
            self.sprites.update()

            #!BOSS 
            if self.score % 20 == 0:
                if self.boss.vida <= 1:
                    self.boss.kill()
                    self.boss = Mob()
                    self.boss.aparicion = False      
            if self.score > 10:
                self.boss.spawn(self.player.rect.x, self.player.rect.y)
                self.boss.accion_aleatoria(self.sprites, self.mob_atack_list,self.player.rect.x)
                self.mob_list.add(self.boss)

            if pygame.Rect.colliderect(self.player.rect, self.boss.rect) and self.boss.vida > 0:
                if self.boss.temporizador == 10: #ralentiza ticks para que el mob haga menos daño por colision
                    self.player.vidas -=1
            #Daño al mob        
           
            mob_hit_list = pygame.sprite.spritecollide(self.boss,self.proyectil_list, True)
            for _ in mob_hit_list:
                self.boss.vida -= 1
                self.score += 1 
                self.boss.image = pygame.image.load(os.path.join('models','entity','necromancer','necromancer_damage.png')).convert_alpha()

            fuegos_cruzados = pygame.sprite.groupcollide(self.proyectil_list,self.mob_atack_list, False, True)

            #! MOB 
            if self.score % 10 == 0:
                if self.mob.vida <= 1:
                    self.mob.kill()
                    self.mob = Mob()
                    
                    self.mob.aparicion = False     
                    
            if self.score > 1:
                self.mob.spawn(self.player.rect.x, self.player.rect.y)
                self.mob.image = pygame.image.load(os.path.join('models','entity','armored_skeleton','armored_skeleton_front.png')).convert_alpha()
                self.mob.vida = 5 
                self.mob.accion_aleatoria(self.sprites, self.mob_atack_list,self.player.rect.x)
                self.mob_list.add(self.mob)

            if pygame.Rect.colliderect(self.player.rect, self.mob.rect) and self.mob.vida > 0:
                if self.mob.temporizador == 10: #ralentiza ticks para que el mob haga menos daño por colision
                    self.player.vidas -=1
            #Daño al mob        
           
            mob_hit_list = pygame.sprite.spritecollide(self.mob,self.proyectil_list, True)
            for _ in mob_hit_list:
                self.mob.vida -= 1
                self.score += 1 
                

            fuegos_cruzados = pygame.sprite.groupcollide(self.proyectil_list,self.mob_atack_list, False, True)

            #!MINIONS             
            if len(self.minion_list) == 0:
                for i in range(self.nivel*5):
                    self.minion_1 = Minion()
                    self.minion_1.speed += 0
                    self.minion_1.image = pygame.image.load(os.path.join('models','skill','pointed_dripstone.png'))
                    self.minion_list.add(self.minion_1)
                    self.sprites.add(self.minion_1)

            #Daño y pérdida de vida
            
            player_hit_list = pygame.sprite.spritecollide(self.player, self.minion_list, True)
            player_hit_list += pygame.sprite.spritecollide(self.player, self.mob_atack_list, True)
            
            if not self.player.guardia_activa:
                for _ in player_hit_list:
                    self.player.vidas -= 1
                    class_soundtrack.daño_recibido.play()
            if player_hit_list:
                self.player.guardia_activa = False
                self.player.image = pygame.image.load(os.path.join('models','player','player_meditate.png')).convert_alpha()
            
            #Puntuación y score    
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.minion_list, self.player.destruccion_proyectil, True)    
            for shot in success_shot_list:
                
                self.score += 1
                self.player.amount_charge += 1
                class_soundtrack.coins.play()
            
            
            #! BONIFICACIONES Y CONTROL DE ATAQUE
            if len(self.proyectil_list) > self.player.limite_proyectil:
                sprite_a_eliminar = self.proyectil_list.sprites()[self.player.limite_proyectil]
                sprite_a_eliminar.kill()

            if pygame.sprite.spritecollide(self.player,self.items_list, True):
                if self.item.autodestruccion == False:
                    self.player.clasificar_proyectil(self.sprites, self.item)
                    self.item.autodestruccion = True
                    self.item.kill()

            if random.randint(0,1) == 1 and self.score%5 == 0 and self.score != 0:
                self.score +=1 
                self.item = Items()
                self.sprites.add(self.item)
            self.items_list.add(self.item)

            #!Condición de GAME OVER
            if self.player.vidas == 0 or self.menu.game_over == True:
                self.game_over = True
            if self.menu.nivel == 1:
                self.nivel = 1
                print ("control 2")

            
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
        background= pygame.image.load(self.background[0]).convert_alpha()
        suelo = pygame.image.load(os.path.join('background','mountain','suelo_2.png')).convert_alpha()


        
        #En la siguiente linea: la posición del jugador se le resta la cámara (0) y el ancho (si dividimos ancho//2 me quedo sin pantalla!!!)
        self.camera += (self.player.rect.x/2 - self.camera - ancho)
        screen.blit(background, [-900-self.camera, 0])
        screen.blit(suelo, [0,520])


    

        #! PANTALLA DE FIN DEL JUEGO
        if self.game_over:
            textos_pantalla.texto_1(white,ancho,alto,screen, "Haz click en pantalla para reiniciar")
            pygame.mouse.set_visible(True)
        
        self.button.update()
        self.button.changeColor(pygame.mouse.get_pos())
        

        #!MENU PRINCIPAL DEL JUEGO
        if self.menu.open_menu:
            self.menu.main_menu()
            self.sprites.add(self.soundtrack)
            
        if not self.menu.open_menu:
            self.soundtrack.kill()


        #! STATS Y PUNTUACIONES
        if not self.game_over and not self.menu.open_menu:
            textos_pantalla.texto_variable(screen, self.score, 710,10)
            stats.hearts(screen, self.player.vidas)
            ruta = os.path.join('models', 'particle', 'mana.png')
            stats.generar_stat(screen, self.player.limite_proyectil, ruta, 10, 50, 10, len(self.proyectil_list))
            if self.boss.aparicion == True:
                stats.hearts_mob(screen,self.boss.vida)
            textos_pantalla.texto_cargas(screen, self.player.amount_charge)
            
            #!Este de aquí es obligatorio para actualizar lo que se ve en pantalla
            self.sprites.draw(screen) 


        pygame.display.flip()

def main():
    pygame.init()
    screen= pygame.display.set_mode([ancho,alto])
    pygame.display.set_caption("Coordenadas del Ratón")
    done= False
    clock = pygame.time.Clock()
    game_2 = Game_2()
    
    while not done:
        if game_2.nivel == 2:
            done = game_2.process_events(screen)
            game_2.run_logic()
            game_2.display_frame(screen)
            clock.tick(60)

        elif game_2.nivel == 1:
            print ("ahora debería ejecutarse el nivel 0")
            __lvl_0__.main()
        

    pygame.quit()


if __name__ == "__main__":
    main()