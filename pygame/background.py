import os,glob

def obtener_background_path():
    carpeta= 'background/mountain'
    patron_png = os.path.join(carpeta,'*.png')
    background_path_png=[]
    background_path_png=glob.glob(patron_png)

    print("Archivos png de la carpeta: ")
    for background in background_path_png:
        print (background)

    return background_path_png
