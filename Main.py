import pygame as pg
from Fuciones import carga

pg.init()

x = 1280
y = 720
ventana = pg.display.set_mode((x,y))
frames = pg.time.Clock()
run = True
grama = carga("grama")
calle = carga("calle")
v = 0
velocidad = 0.5 
while run:
    ventana.fill((0,0,0))
    for event in pg.event.get():
         
        if event.type == pg.QUIT:
            run = False

    velocidad+=0.01    
    v += velocidad
    ventana.blit(grama,(0,v))
    ventana.blit(calle,(450,v))
    
       
    print(v)
    pg.display.flip()

    frames.tick(60)

pg.quit()
