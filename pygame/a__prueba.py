import pygame
import imageio
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("GIF en Pygame")

# Cargar el archivo GIF con imageio
gif_path = "background.gif"
gif = imageio.get_reader(gif_path)

# Obtener el tamaño del primer cuadro del GIF
try:
    first_frame = gif.get_data(0)
    gif_width, gif_height = first_frame.shape[1], first_frame.shape[0]
except Exception as e:
    print(f"Error: No se pudo obtener el tamaño del primer cuadro del GIF. {e}")
    sys.exit()

# Configurar el bucle principal
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener el siguiente cuadro del GIF
    try:
        img = pygame.image.fromstring(gif.get_next_data(), (gif_width, gif_height), 'RGB')
    except StopIteration:
        gif.close()
        gif = imageio.get_reader(gif_path)

    # Limpiar la pantalla
    screen.fill((255, 255, 255))

    # Dibujar el cuadro actual del GIF en la pantalla
    screen.blit(img, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(30)