
while True:
    x += 1
    
    x_relativa = x % background.get_rect().width
    screen.blit(background, [x_relativa - background.get_rect().width, 0])
    if x_relativa < ancho:
        screen.blit(background,(x_relativa,0))

    