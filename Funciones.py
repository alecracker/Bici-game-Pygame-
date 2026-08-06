import pygame as pg
import os

pg.init()

def carga(img):    

    if img == "calle":
        calle = pg.image.load(os.path.join('assets','calle.png'))
        calle_opt = pg.transform.scale(calle,(600,800))
        return calle_opt
    elif img == "grama":
        grama = pg.image.load(os.path.join('assets','jardin.png'))
        grama_opt = pg.transform.scale(grama,(1280,720))
        return grama_opt
    elif img == "bici(der)":
        bici = pg.image.load(os.path.join('assets','bici(der).png'))
        bici_opt = pg.transform.scale(bici,(200,200))
        return bici_opt
    elif img == "bici(izq)":
        bici = pg.image.load(os.path.join('assets','bici(izq).png'))
        bici_opt = pg.transform.scale(bici,(200,200))
        return bici_opt
    elif img == "Obs":
        Obs = pg.image.load(os.path.join('assets','Obs.png'))
        Obs_opt = pg.transform.scale(Obs,(200,200))
        return Obs_opt
    elif img == "cauch":
        Caucho = pg.image.load(os.path.join('assets','cauch.png'))
        Caucho_opt = pg.transform.scale(Caucho,(120,120))
        return Caucho_opt