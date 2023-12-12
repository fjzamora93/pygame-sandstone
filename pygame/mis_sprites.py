
#PATH DE LOS ATAQUES

import mis_funciones,os,pygame,glob

sonic = 'models/particle/sonic'
sword = 'models/particle/sword'
ice = 'models/particle/ice'
explosion = 'models/particle/explosion'

#!Esta función actualiza a la función obtener_ruta de "mis_funciones".
def cargar_sprite(carpeta_destino, n):
    patron_png = os.path.join(carpeta_destino,"*.png")
    path_list = []
    path_list = glob.glob(patron_png)
    sprite_cargado = pygame.image.load(path_list[n]).convert_alpha()
    return sprite_cargado



#iconos_menu = mis_funciones.obtener_ruta('models', 'menu')