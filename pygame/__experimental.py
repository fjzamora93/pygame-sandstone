"""

Instalar la librería de movie: pip install pygame moviepy
Buscar un tutorial para GIF

Librería de artes gratis: https://opengameart.org/content/lpc-medieval-fantasy-character-sprites
"""


import pygame, random, os
import soundtrack,textos_pantalla,stats



pygame.mixer.init()

ancho = 900
alto = 554
black = (0, 0, 0)
white = (255, 255, 255)


#todo ANTES DE CLASS GAME, PODRÍAN IR TODAS LAS CLASES IMPORTADAS
from class_generic import Proyectil
from class_generic import Corazon
from class_generic import Wall
from class_player import Player



class Game(object):
    def __init__(self):
        # Creamos una instancia de game over FALSE
        self.game_over = False
        self.score = 0

        # Creamos todas las listas donde estamos acumulando cosas
        self.proyectil_list = pygame.sprite.Group()
        self.corazon_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.mob_list =pygame.sprite.Group()
        self.mob_atack_list = pygame.sprite.Group()
        self.fuegos_cruzados = pygame.sprite.Group()
        

        for i in range(20):
            self.corazon = Corazon()
            
            self.all_sprites_list.add(self.corazon)  # Necesario hacerlo aquí para que salgan todos los corazones
            self.corazon_list.add(self.corazon)

        # Vamos a empezar a crear las entidades del juego. Solo las que aparecen al principio
        
        self.mob = Wall()
        self.player = Player()
        
        
        self.all_sprites_list.add(self.player)
        
        
       
        

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            
            # LÓGICA DE LOS CONTROLES
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.changespeed_x(5)
                if event.key == pygame.K_a:
                    self.player.changespeed_x(-5)

                # El control de salto sigue una lógica muy concreto, revisa abajo en la parte lógica lo que está haciendo
                if not self.player.jumping:
                    if event.key == pygame.K_w:
                        self.player.proceso_salto()
                

                if event.key == pygame.K_SPACE:
                    self.proyectil_2 = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)
                    self.proyectil_2.vector = "horizontal"
                    self.player.image = pygame.image.load(os.path.join('models', 'player_concentrate.png')).convert_alpha()
                    self.all_sprites_list.add(self.proyectil_2)
                    self.proyectil_list.add(self.proyectil_2)
                
                if event.key == pygame.K_q:
                    self.proyectil = Proyectil(self.player.rect.x,self.player.rect.y,self.player.direction)
                    self.proyectil.vector = "vertical"
                    self.all_sprites_list.add(self.proyectil)
                    self.proyectil_list.add(self.proyectil)

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
        print(f"X: {mouse_x}, Y: {mouse_y}")

        # Se me olvidó qué es esto
        return False

    def run_logic(self):
        # Introducimos una condición de cuando NO es Game over
        if not self.game_over:
            self.all_sprites_list.update()

        #!Sigue provocando daño aunque no esté en pantalla!!!!
            if self.score > 1 and self.mob.vida != 0:
                self.mob.spawn(self.player.rect.x, self.player.rect.y)
                self.mob.accion_aleatoria(self.all_sprites_list, self.mob_atack_list,self.player.rect.x)
                if self.mob.vida > 0:
                    self.mob_list.add(self.mob)
                    self.all_sprites_list.add(self.mob)
                if self.mob.vida < 0:
                    self.mob.kill()
                
            
            player_hit_list = pygame.sprite.spritecollide(self.player, self.corazon_list, True)
            player_hit_list = pygame.sprite.spritecollide(self.player, self.mob_atack_list, True)
            for _ in player_hit_list:
                self.player.vidas -= 1
                soundtrack.daño_recibido.play()

            #! He tenido que meter la segunda condición...pero hay que limpiar ese código
            if pygame.Rect.colliderect(self.player.rect, self.mob.rect) and self.mob.vida > 0:
                #El temporizador del mob nos asegura que no se vaya de madre...
                if self.mob.temporizador == 10:
                    self.player.vidas -=1


            #El primer True elimina instancias del Grupo 2, El segundo True elimina instancias del Grupo 1
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.corazon_list, False,True)
            fuegos_cruzados = pygame.sprite.groupcollide(self.proyectil_list,self.mob_atack_list, False, True)

            mob_hit_list = pygame.sprite.spritecollide(self.mob,self.proyectil_list, True)
            for _ in mob_hit_list:
                self.mob.vida -= 10
                
            for shot in success_shot_list:
                self.score += 1
                soundtrack.coins.play()

        #Pero al mismo tiempo, dentro de la lógica, debemos revisar qué sucede cuando Game Over es True
            if len(self.corazon_list)==0 or self.player.vidas ==0:
                self.game_over = True
            

    def display_frame(self,screen):
        background= pygame.image.load("background.jpg").convert()
        #? Puedes activar la linea de abajo para pasar la pantalla a blanco o el fondo
        screen.fill(white)
        screen.blit(background, [0,0])
       

        #CREAR LAS CONDICIONES DE LO QUE SE MUESTRA EN PANTALLA
        #Y así aprendemos a meter texto en pantalla (Video Implementando Game Over)
        if self.game_over and len(self.corazon_list) == 0:
            textos_pantalla.texto_game_over_1(black,ancho,alto,screen)
        elif self.game_over and self.player.vidas == 0:
            textos_pantalla.texto_game_over_2(black,ancho,alto,screen)
        

         #A partir de aquí metemos otras cosas que se muestran en pantalla:
        if not self.game_over:
            textos_pantalla.texto_puntuacion(screen, self.score)
            stats.hearts(screen, self.player.vidas)

            #!MOBS
        


            #CON ESTE CÓDIGO SE ELIMINA EL ÍNDICE i DE LA LISTA. Por defecto, el número 2 par ano duplicar proyectiles
            if len(self.proyectil_list) > 3:
                # Elimina el primer sprite del grupo
                sprite_a_eliminar = self.proyectil_list.sprites()[3]
                sprite_a_eliminar.kill()
              
     
            


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
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()