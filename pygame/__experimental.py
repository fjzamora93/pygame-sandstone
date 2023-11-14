"""
En este tutorial veremos la pantalla de Game OVER,
del mismo modo que aprenderemos a introducir texto.

os es la librería para tener directorios guapos y no andar cambiando la url de las fotos
Instalar la librería de movie: pip install pygame moviepy
Buscar un tutorial para GIF

Librería de artes gratis: https://opengameart.org/content/lpc-medieval-fantasy-character-sprites
"""


import pygame, random, os
import soundtrack,textos_pantalla,stats

from class_proyectil import Proyectil


pygame.mixer.init()

ancho = 900
alto = 554
black = (0, 0, 0)
white = (255, 255, 255)


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


# TODO Clase de proyectil importada
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 480
        self.speed_x = 0
        self.speed_y = 0
        self.vidas = 10
        self.direction="right"

        # variables del salto
        self.jumping = False
        self.jump_count = 10
        self.jump_height = 0

    def changespeedx(self, x):
        self.speed_x += x
        if x > 0:
            self.image = pygame.image.load(os.path.join('models', 'player_right.png')).convert_alpha()
            self.direction = "right"
        elif x < 0:
            self.image = pygame.image.load(os.path.join('models', 'player_left.png')).convert_alpha()
            self.direction = "left"

    def update(self):  # Establecer la posición de origen, que se modifica con la velocidad
        self.rect.x += self.speed_x
        self.rect.y = 480 + self.speed_y


class Game(object):
    def __init__(self):
        # Creamos una instancia de game over FALSE
        self.game_over = False
        self.score = 0

        # Creamos todas las listas donde estamos acumulando cosas
        self.proyectil_list = pygame.sprite.Group()
        self.corazon_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.vidas_list =pygame.sprite.Group()
        

        for i in range(20):
            self.corazon = Corazon()
            
            self.all_sprites_list.add(self.corazon)  # Necesario hacerlo aquí para que salgan todos los corazones
            self.corazon_list.add(self.corazon)

        # Vamos a empezar a crear las entidades del juego. Solo las que aparecen al principio
        self.player = Player()
        self.all_sprites_list.add(self.player)
       
        

    def process_events(self):
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            # LÓGICA DE LOS CONTROLES
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.changespeedx(5)
                if event.key == pygame.K_a:
                    self.player.changespeedx(-5)

                # El control de salto sigue una lógica muy concreto, revisa abajo en la parte lógica lo que está haciendo
                if event.key == pygame.K_w and not self.player.jumping:
                    self.player.jumping = True

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
            #!BUENA SUERTE.... JEJEJE, PORQUE ESTÁ JODIDA LA COSA. Aunque no sale a cuenta trabajar con esta clase
            if self.score > 10:
                self.mob_1 = Corazon()
                self.mob_1.image=pygame.image.load(os.path.join('models', 'bad_omen.png')).convert_alpha()
                self.mob_1.rect.x= 500
                self.mob_1.rect.y= 300
                self.all_sprites_list.add(self.mob_1)
                

            player_hit_list = pygame.sprite.spritecollide(self.player, self.corazon_list, True)
            for corazon in player_hit_list:
                self.player.vidas -= 1
                soundtrack.daño_recibido.play()


            #El primer True elimina instancias del Grupo 2, El segundo True elimina instancias del Grupo 1
            success_shot_list = pygame.sprite.groupcollide(self.proyectil_list, self.corazon_list, False,True)
            for shot in success_shot_list:
                self.score += 1
                soundtrack.coins.play()
                print(self.score)

        #Aquí tenemos la lógica del salto
            if self.player.jumping:
                    #Calcula la altura del salto en el momento actual. Utiliza una fórmula simple de parábola para calcular la altura en función del tiempo de salto (self.player.jump_count). A medida que jump_count disminuye, la altura del salto disminuye.
                    self.player.jump_height = self.player.jump_count ** 2 * 0.5
                    #Recalcula la posición del jugador al saltar
                    self.player.rect.y -= self.player.jump_height
                    #Este contador es el que disminuye la altura:
                    self.player.jump_count -= 1
                    #Reestablece todos los valores a 0
                    if self.player.jump_count < 0:
                        self.player.jumping = False
                        self.player.jump_count = 20
                        self.player.jump_height = 0

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