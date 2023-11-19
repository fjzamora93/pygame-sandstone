import os,glob

def obtener_background_path():
    carpeta= 'background/mountain'
    patron_png = os.path.join(carpeta,'*.png')
    background_path_png=[]
    background_path_png=glob.glob(patron_png)

    

    return background_path_png
