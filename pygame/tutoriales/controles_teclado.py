import pygame

def control_teclado(player, proyectil, Proyectil, all_sprite_list, proyectil_list, sound):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3)
            if event.key == pygame.K_RIGHT:
                player.changespeed(3)
            if event.key == pygame.K_SPACE:
                proyectil = Proyectil()
                proyectil.rect.x = player.rect.x + 45
                proyectil.rect.y = player.rect.y -20
                all_sprite_list.add(proyectil)
                proyectil_list.add(proyectil)
                #METEMOS EL SONIDO EN EL EVENTO
                sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3)