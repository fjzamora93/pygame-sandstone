import pygame
import os
import glob
import sys

ancho = 900
alto = 554

# Ruta de la carpeta que contiene los archivos PNG
carpeta = 'models/blocks'

# Patrón de búsqueda para archivos PNG
patron_png = os.path.join(carpeta, '*.png')

# Lista para almacenar los nombres de archivos PNG
archivos_png = glob.glob(patron_png)

# Verificar si hay al menos una imagen en la carpeta
if not archivos_png:
    print("No se encontraron archivos PNG en la carpeta:", carpeta)
    sys.exit()

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Seleccionar Bloque')

# Clase Block
class Block(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, image_path):
        self.image = pygame.image.load(image_path)

# Crear instancia de Block
bloque = Block(archivos_png[0])

# Grupo de sprites
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(bloque)

# Bucle principal
ejecutando = True
indice_imagen_actual = 0

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                indice_imagen_actual = (indice_imagen_actual + 1) % len(archivos_png)
                bloque.update(archivos_png[indice_imagen_actual])

    pantalla.fill((255, 255, 255))
    todos_los_sprites.draw(pantalla)
    pygame.display.flip()

# Salir de Pygame
pygame.quit()