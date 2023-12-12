

import pygame, random, os
import textos_pantalla,stats, mis_funciones, mis_sprites
from tkinter import *
pygame.mixer.init() #Para reproducir sonidos, guapi

nivel = 2
ancho = 900
alto = 554
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5




#todo ANTES DE CLASS GAME, PODRÍAN IR TODAS LAS CLASES IMPORTADAS
import __lvl_0__


from class_mobs import Mob
from class_proyectil import Proyectil
from class_player import Player
from class_blocks import Block
from class_blocks import obtener_ruta
from background import obtener_background_path
from class_items import Items
from class_button import Button
from class_mouse import Mouse
from class_menu import Menu

class Game_2(object):
    def __init__(self):
        pygame.display.set_caption("Tales of Sandstone")
        self.screen = pygame.display.set_mode([ancho,alto])
        self.nivel = 2
        self.game_over = False
        self.n = 0
        self.contador_1 = 0
        self.sprites_nivel = f'background/{self.nivel}'
        self.camera = 0
      
        # TODOS LAS LISTAS QUE VAMOS A UTILIZAR
        self.mob_list = [] # En esta lista estarán todas los mobs que no mueren por colision

        self.proyectil_list = pygame.sprite.Group()
        self.minion_list = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.minion_list = pygame.sprite.Group()
        self.fuegos_cruzados = pygame.sprite.Group()
        self.blocks_list =pygame.sprite.Group()
        self.items_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        
        #TODOS LOS ENTIDADES QUE VAMOS A INICIALIZAR
        self.menu = Menu(self.nivel)
        self.item = Items()
        self.player = Player()
        self.boss = Mob('boss', self.nivel, self.player.rect.x)
        self.mob = Mob('mob', self.nivel, self.player.rect.x)
        
        self.button = Button(ancho//2,50, "Menu", 'models/menu', 0)
        self.inventario = Button (800, 50, "", 'models/menu', 2)
        self.mouse = Mouse()
        
        #TODO LISTA DE SPRITES
        self.sprites.add(self.mouse)
        self.sprites.add(self.player)
        self.sprites.add(self.item)

        #Ocultamos cursor
        pygame.mouse.set_visible(False)
 
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            #CONTROL DEL RATÓN Y BOTÓN DE MENÚ
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 representa el botón izquierdo del ratón
                MOUSE_POSITION = pygame.mouse.get_pos()
                if self.button.checkForInput(MOUSE_POSITION):
                    self.menu.open_menu= True
 
            self.player.controles_1(event,self.sprites,self.proyectil_list)
    
          
            #CREAMOS UNA NUEVA LÓGICA PARA REINICIAR EL JUEGO
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        # Esto retornará false y está almacenado en la variable "done"
        return False

    def run_logic(self):
        if not self.game_over:
            self.sprites.update()

            #TODOS SPAWN DE MOBS
            if self.player.score >= 0:
                self.mob.spawn(self.player.rect.x, self.sprites, self.mob_list)    
            if self.player.score >= 2:
                self.boss.spawn(self.player.rect.x, self.sprites, self.mob_list)
                self.boss.accion_aleatoria(self.sprites, self.minion_list, self.player.rect.x)
            if len(self.minion_list) == 0:
                for i in range(self.nivel*5):
                    self.minion = Mob('minion', self.nivel, self.player.rect.x)
                    self.minion.generar_minion(self.sprites, self.minion_list)

            #TODO COLISIONES CON LOS MOBS
            self.mob.colision.detect(self.mob, self.proyectil_list, True, self.player)
            self.boss.colision.detect(self.boss, self.proyectil_list, True, self.player)

            #TODO COLISIONES PLAYER
            self.player.colision.recibir_impacto(self.player, self.minion_list, True) 
            self.player.colision.recibir_impacto(self.proyectil_list, self.minion_list, self.player.destruccion_proyectil)
            self.player.colision.recibir_impacto(self.player, self.mob_list, False)
            

            #! BONIFICACIONES Y CONTROL DE ATAQUE
            if len(self.proyectil_list) > self.player.limite_proyectil:
                sprite_a_eliminar = self.proyectil_list.sprites()[self.player.limite_proyectil]
                sprite_a_eliminar.kill()

            if pygame.sprite.spritecollide(self.player, self.items_list, True):
                if self.item.autodestruccion == False:
                    self.player.clasificar_proyectil(self.sprites, self.item)
                    self.item.autodestruccion = True
                    self.item.kill()

            if random.randint(0,1) == 1 and self.player.score%5 == 0 and self.player.score != 0:
                self.player.score +=1 
                self.item = Items()
                self.sprites.add(self.item)
            self.items_list.add(self.item)

            #!Condición de GAME OVER
            if self.player.vidas == 0 or self.menu.game_over == True:
                self.game_over = True
            if self.menu.nivel == 1:
                self.nivel = 1
          

            
    def display_frame(self):
       
        background= mis_sprites.cargar_sprite(self.sprites_nivel, 0)
        suelo = pygame.image.load(os.path.join('background','mountain','suelo_2.png')).convert_alpha()
        
        #En la siguiente linea: la posición del jugador se le resta la cámara (0) y el ancho (si dividimos ancho//2 me quedo sin pantalla!!!)
        self.camera += (self.player.rect.x/2 - self.camera - ancho)
        self.screen.blit(background, [-900-self.camera, 0])
        self.screen.blit(suelo, [0,520])


    

        #! PANTALLA DE FIN DEL JUEGO
        if self.game_over:
            textos_pantalla.texto_1(white,ancho,alto,self.screen, "Haz click en pantalla para reiniciar")
            pygame.mouse.set_visible(True)
        
        self.button.update()
        self.inventario.update()
        self.button.changeColor(pygame.mouse.get_pos())
        self.inventario.changeColor(pygame.mouse.get_pos())
        

        #!MENU PRINCIPAL DEL JUEGO
        if self.menu.open_menu:
            pygame.mouse.set_visible(True)
            self.menu.main_menu()


        #! STATS Y PUNTUACIONES
        if not self.game_over and not self.menu.open_menu:
            pygame.mouse.set_visible(False)
            textos_pantalla.texto_variable(self.screen, self.player.score, 710,10)
            stats.generar_stat(self.screen, self.player.limite_proyectil, 'models/stats/mana.png', 10, 50, 10, len(self.proyectil_list))
            stats.generar_stat(self.screen, self.player.vidas, 'models/stats/hearts.png', 10, 20, 10, 0)
            textos_pantalla.texto_cargas(self.screen, self.player.amount_charge)
            

            #!Este de aquí es obligatorio para actualizar lo que se ve en pantalla
            self.sprites.draw(self.screen) 
        pygame.display.flip()

def main():
    pygame.init()
   
    pygame.display.set_caption("Coordenadas del Ratón")
    done= False
    clock = pygame.time.Clock()
    game_2 = Game_2()
    
    while not done:
        if game_2.nivel == 2:
            done = game_2.process_events()
            game_2.run_logic()
            game_2.display_frame()
            clock.tick(60)

        elif game_2.nivel == 1:
            print ("ahora debería ejecutarse el nivel 0")
            __lvl_0__.main()
        

    pygame.quit()


if __name__ == "__main__":
    main()