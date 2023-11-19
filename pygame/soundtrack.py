import pygame,os
pygame.mixer.init()



    #AMBIENTE
ambiente_nubes = pygame.mixer.Sound(os.path.join('sounds','ambiente_nubes.mp3'))
ambiente_sunset = pygame.mixer.Sound(os.path.join('sounds','ambiente_sunset.mp3'))

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

