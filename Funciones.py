import pygame as pg
import os

pg.init()

def carga(img):    

    if img == "calle":
        calle = pg.image.load(os.path.join('assets','calle.png'))
        calle_opt = pg.transform.scale(calle,(600,800))
        return calle_opt
    elif img == "grama":
        grama = pg.image.load(os.path.join('assets','bosque.png'))
        grama_opt = pg.transform.scale(grama,(1280,720))
        return grama_opt
    elif img == "bici(der)":
        bici = pg.image.load(os.path.join('assets','bici(der).png'))
        bici_opt = pg.transform.scale(bici,(155,165))
        return bici_opt
    elif img == "bici(izq)":
        bici = pg.image.load(os.path.join('assets','bici(izq).png'))
        bici_opt = pg.transform.scale(bici,(155,165))
        return bici_opt
    elif img == "Obs":
        Obs = pg.image.load(os.path.join('assets','Obs.png'))
        Obs_opt = pg.transform.scale(Obs,(120,120))
        return Obs_opt
    elif img == "cauch":
        Caucho = pg.image.load(os.path.join('assets','cauch.png'))
        Caucho_opt = pg.transform.scale(Caucho,(80,80))
        return Caucho_opt
    elif img == "cayendo":
        Cayendo = pg.image.load(os.path.join('assets','cayendo.png'))
        Cayendo_opt = pg.transform.scale(Cayendo,(80,80))
        return Cayendo_opt
    elif img == "mar":
        mar = pg.image.load(os.path.join('assets','mar.png'))
        mar_opt = pg.transform.scale(mar,(1280,720))
        return mar_opt
    elif img == "desierto":
        des = pg.image.load(os.path.join('assets','desierto.png'))
        des_opt = pg.transform.scale(des,(1280,720))
        return des_opt
    elif img == "competencia":
        comp = pg.image.load(os.path.join('assets','competencia.png'))
        comp_opt = pg.transform.scale(comp,(1280,720))
        return comp_opt
    elif img =="intro":
        intro = pg.image.load(os.path.join('assets','intro.png'))
        intro_opt = pg.transform.scale(intro,(1280,720))
        return intro_opt 