
#PATH DE LOS ATAQUES

import colisiones,os,pygame,glob



#os.path.join() busca en la carpeta de destino todos los archivos con esa terminación.
#path_list es la lista donde vamos a guardar cosas.
#glob.glob() nos devuelve los archivos del patron_png y nos lo mete en la lista.
#return nos indica lo que devuelve la función, para almacenarlo en una variable (por lo general tendrá el mismo nombre)
def cargar_sprite(carpeta_destino, n):
    patron_png = os.path.join(carpeta_destino,"*.png")
    path_list = []
    path_list = glob.glob(patron_png)
    sprite_cargado = pygame.image.load(path_list[n]).convert_alpha()
    return sprite_cargado



#iconos_menu = mis_funciones.obtener_ruta('models', 'menu')