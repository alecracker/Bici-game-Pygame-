import pygame as pg
from Funciones import carga
import Clases as cs

pg.init()

x = 1280
y = 720
ventana = pg.display.set_mode((x,y))
frames = pg.time.Clock()
run = True
grama = carga("grama")
grama2 = carga("grama")
calle = carga("calle")
calle2= carga("calle")
sprites = pg.sprite.Group()
v = 0
aux = 0 #auxiliar de posicion de los obs
obscont = v
vel = 0.5 
bici = cs.Bici(500,520)
obs=cs.Obst(1000,v-100,"cauch")
obs1=cs.Obst(1000,v-200,"cauch")
obs2=cs.Obst(1000,v-300,"Obs")
obs3=cs.Obst(1000,v-400,"Obs")
sprites.add(bici)
sprites.add(obs)
sprites.add(obs1)
sprites.add(obs2)
sprites.add(obs3)
np= obs.aparicion(v-100)
n1p= obs1.aparicion(v-200)
n2p = obs2.aparicion(v-300)
n3p = obs3.aparicion(v-400)

while run:

    ventana.fill((0,0,0))
    for event in pg.event.get(): 
        bici.move(event)
        bici.colision(obs.hitbox)
        bici.colision(obs1.hitbox)
        bici.colision(obs2.hitbox)
        bici.colision(obs3.hitbox) 
        if event.type == pg.QUIT:
            run = False

    vel+=0.01
    v+=vel
    ventana.blit(grama2,(0,v-720))
    ventana.blit(calle2,(380,v-720))
    ventana.blit(grama,(0,v))
    ventana.blit(calle,(380,v))
    bici.pedalear() 
    obs.pos(vel)   
    obs1.pos(vel)  
    obs2.pos(vel)  
    obs3.pos(vel)
    sprites.draw(ventana)
    pg.draw.rect(ventana,(255,0,0),obs.hitbox,2)
    pg.draw.rect(ventana,(0,255,0),bici.hitbox,2)
    pg.draw.rect(ventana,(255,0,0),obs1.hitbox,2)
    pg.draw.rect(ventana,(255,0,0),obs2.hitbox,2)
    pg.draw.rect(ventana,(255,0,0),obs3.hitbox,2)
    if obs.y_float>=720:
        n=obs.aparicion(np)
        obs.y_float=-100
    if obs1.y_float>=720:     
        n1=obs1.aparicion(n1p)
        obs1.y_float=-100
    if obs2.y_float>=720:
        n2=obs2.aparicion(n2p)
        obs2.y_float=-100
    if obs3.y_float>=720:
        n3=obs3.aparicion(n3p)
        obs3.y_float=-100
    if v >= 720: 
        v = 0

    pg.display.flip()
    frames.tick(60)

pg.quit()
