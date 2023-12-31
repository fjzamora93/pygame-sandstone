"""
Instalar la librería de movie: pip install pygame moviepy
Librería de artes gratis: https://opengameart.org/content/lpc-medieval-fantasy-character-sprites
"""


import pygame, random, os
import class_soundtrack,textos_pantalla,stats

pygame.mixer.init() #Para reproducir sonidos, guapi


ancho = 900
alto = 554
screen= pygame.display.set_mode([ancho,alto])
black = (0, 0, 0)
white = (255, 255, 255)
temporizador = 10
numero_frames = 5



#todo ANTES DE CLASS GAME, PODRÍAN IR TODAS LAS CLASES IMPORTADAS

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
import _lvl_2

class Game(object):
    def __init__(self):
        pygame.display.set_caption("Tales of Sandstone") 
        self.nivel = 1
        self.game_over = False
        self.score = 0
        self.n = 0
        self.contador_1 = 0
        self.nivel_dificultad = 1
        self.autodestruccion= True
        self.camera = 0
        self.open_menu= False
    

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
        
        for i in range(5):
            self.platform_2 = Block(0)
            self.platform_2.bloque_dinamico = False #CAMBIAR A TRUE PARA ANIMAR BLOQUE
            self.platform_2.carpeta = 'models/blocks/interruptor'
            self.platform_2.obtener_ruta()
            mis_funciones.generador_bloques(self.sprites,self.blocks_list,self.platform_2,self.platform_2.rect.x,400)
        for i in range (5):
            self.block = Block(1)
            mis_funciones.generador_bloques(self.sprites,self.blocks_list,self.block,self.block.rect.x,400)
       
        self.item = Items()
        self.mob = Mob()
        self.menu = Menu(self.nivel)
        self.button = Button(ancho//2,50, "Menu", 'models/menu', 0)
        self.inventario = Button (800, 50, "Inventario", 'models/menu', 3)
        
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
        self.sprites.add(self.soundtrack)
       
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
                    print("primer control de botón presionado!")
                    self.menu.open_menu = True
 
            #soundtrack.control_audio(event,screen,soundtrack)
            self.player.controles_1(event,self.sprites,self.proyectil_list)
            self.soundtrack.control_audio(event,screen)
 
            #CREAMOS UNA NUEVA LÓGICA PARA REINICIAR EL JUEGO
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    if self.game_over:
                        self.__init__()

        # Esto retornará false y está almacenado en la variable "done"
        return False

                

    def run_logic(self):
        if not self.game_over:
            self.sprites.update()

            self.player.deteccion_colision(self.blocks_list,self.block.rect,self.block.rect.y,self.block.rect.top,self.block.rect.left,self.block.rect.right)
            self.player.deteccion_colision(self.platform_list,self.platform_2.rect,self.platform_2.rect.y,self.platform_2.rect.top,self.platform_2.rect.left,self.platform_2.rect.right)

            #!BOSS Y MOBS PRINCIPALES
            if self.score > 10:
                if self.mob.vida <= 1:
                    self.mob.kill()
                    self.mob = Mob()
                    self.mob.aparicion = False
                    self.nivel = 2
            if self.score > 5:
                self.mob.spawn(self.player.rect.x, self.player.rect.y)
                self.mob.accion_aleatoria(self.sprites, self.mob_atack_list,self.player.rect.x)
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
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.minion_list, self.autodestruccion,True)    
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

            if random.randint(0,500) == 500:
                self.item = Items()
                self.sprites.add(self.item)
            self.items_list.add(self.item)

            #!Condición de GAME OVER
            if self.player.vidas == 0 or self.menu.game_over == True:
                self.game_over = True
            if self.menu.nivel == 2:
                self.nivel = 2
            
            
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
        background= pygame.image.load(self.background[9]).convert_alpha()
        suelo = pygame.image.load(os.path.join('background','mountain','suelo_2.png')).convert_alpha()


        #En la siguiente linea: la posición del jugador se le resta la cámara (0) y el ancho (si dividimos ancho//2 me quedo sin pantalla!!!)
        self.camera += (self.player.rect.x/2 - self.camera - ancho)
        screen.blit(background, [-900-self.camera, 0])
        screen.blit(suelo, [0,520])



        #! PANTALLA DE FIN DEL JUEGO
        if self.game_over:
            textos_pantalla.texto_1(white,ancho,alto,screen, "Haz click en pantalla para reiniciar")
            pygame.mouse.set_visible(True)
        

        #!MENU PRINCIPAL DEL JUEGO
        if self.menu.open_menu:
            self.menu.main_menu()
            self.sprites.add(self.soundtrack)
            
        if not self.menu.open_menu:
            self.soundtrack.kill()

        self.button.update()
        self.button.changeColor(pygame.mouse.get_pos())

        #! STATS Y PUNTUACIONES
        if not self.game_over and not self.menu.open_menu:
            textos_pantalla.texto_variable(screen, self.score, 710,10)
            stats.hearts(screen, self.player.vidas)
            ruta = os.path.join('models', 'particle', 'mana.png')
            stats.generar_stat(screen, self.player.limite_proyectil, ruta, 10, 50, 10, len(self.proyectil_list))
            if self.mob.aparicion == True:
                stats.hearts_mob(screen,self.mob.vida)
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
    game = Game()
    while not done:
        if game.nivel == 1:
            done = game.process_events(screen)
            game.run_logic()
            game.display_frame(screen)
            
        if game.nivel == 2:
            _lvl_2.main()

    pygame.quit()


if __name__ == "__main__":
    main()