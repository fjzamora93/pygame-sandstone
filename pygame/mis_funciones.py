#Archivo con varias funciones útiles en cualquier caso:
import os,glob



def obtener_ruta(carpeta_destino):
    patron_png = os.path.join(carpeta_destino,"*.png")
    path_list = []
    path_list = glob.glob(patron_png)
    return path_list

#os.path.join() busca en la carpeta de destino todos los archivos con esa terminación.
#path_list es la lista donde vamos a guardar cosas.
#glob.glob() nos devuelve los archivos del patron_png y nos lo mete en la lista.
#return nos indica lo que devuelve la función, para almacenarlo en una variable (por lo general tendrá el mismo nombre)


def contador (n,m):
    n += 1
    if n > m:
        n = 0
    return n

#Crea un contador universal. 
#n debería ser self.n para que cada clase tenga su contador.
#Los n deberían inialiarse en 0.
#m es el máximo de iteraciones posibles antes de volver a 0