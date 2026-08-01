import pygame as pg
import os

pg.init()

def carga(obj):    

    if obj == "calle":
        calle = pg.image.load(os.path.join('Recursos','calle.png'))
        calle_opt = pg.transform.scale(calle,(400,800))
        return calle_opt
    elif obj == "grama":
        grama = pg.image.load(os.path.join('Recursos','jardin.png'))
        grama_opt = pg.transform.scale(grama,(1280,720))
        
        return grama_opt