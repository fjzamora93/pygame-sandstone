import pygame,os

pygame.mixer.init()


    #AMBIENTE
ambiente_sunset = pygame.mixer.Sound(os.path.join('sounds','ambiente_sunset.mp3'))

#! TODA LA MÚSICA TIENE QUE QUEDAR GUARDADA EN VARIABLES SIGUIENDO ESTE FORMATO
fondo = os.path.join('sounds','ambiente_sunset.mp3')
magia = os.path.join('sounds','efecto_magia_2.mp3')



#! ESTE OTRO FORMATO ES UNA REPRODUCCIÓN AUTOMÁTICA DEL SONIDO.
    #INTERACCIONES
dialogue_1 = pygame.mixer.Sound(os.path.join('sounds','dialogue_1.mp3'))
coins = pygame.mixer.Sound(os.path.join('sounds','coins.mp3'))
sombra= pygame.mixer.Sound(os.path.join('sounds','shade14.wav'))

    #EFECTOS 5-10 SEGUNDOS
efecto_magia_1 = pygame.mixer.Sound(os.path.join('sounds','efecto_magia_1.mp3'))
efecto_magia_2 = pygame.mixer.Sound(os.path.join('sounds','efecto_magia_2.mp3'))

    #CRÉDITOS
game_over_1 = pygame.mixer.Sound(os.path.join('sounds','game_over_1.mp3'))
game_over_2 = pygame.mixer.Sound(os.path.join('sounds','game_over_2.mp3'))

    #IMPACTOS
atack_laser = pygame.mixer.Sound(os.path.join('sounds','atack_laser.ogg'))
atack_fireball_1 = pygame.mixer.Sound(os.path.join('sounds','atack_fireball_1.mp3'))
daño_recibido = pygame.mixer.Sound(os.path.join('sounds','daño_recibido.mp3'))
ice = pygame.mixer.Sound(os.path.join('sounds','ice.mp3'))
sword= pygame.mixer.Sound(os.path.join('sounds','sword.wav'))
arco = pygame.mixer.Sound(os.path.join('sounds','arco.wav'))


#IMÁGENES DE CONTROL DE AUDIO

audio_on = pygame.image.load(os.path.join('models','menu','audio_on.png'))
audio_off = pygame.image.load(os.path.join('models','menu','audio_off.png'))


#Intenta meter el control de audio dentro del menú, no lo dejes por ahí suelto
class Soundtrack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('models','menu','audio_on.png'))
        self.rect = self.image.get_rect()
        self.rect.x = 860
        self.rect.y = 20
        self.volume= "on"
        self.play_music(fondo)
        
    def update(self):
        if self.volume == "on":
            self.image = pygame.image.load(os.path.join('models','menu','audio_on.png'))
        if self.volume == "off":
            self.image = pygame.image.load(os.path.join('models','menu','audio_off.png'))

    def play_music(self, fondo):
        pygame.mixer.music.load(fondo)
        pygame.mixer.music.play(-1) #El argumento es el número de reproducciones. -1 = bucle infinito.
        pygame.mixer.music.set_volume(1.0)

    #CONTROL DE AUDIO DESDE EL TECLADO
    def control_audio(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_9]and pygame.mixer.music.get_volume() <= 0.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 1.0)
            self.volume = "on"
            print ("sonido activado o desactivado")

        if keys[pygame.K_8] and pygame.mixer.music.get_volume() >= 1.0:
            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 1.0)
            self.volume = "off"
            print ("sonido activado o desactivado")


