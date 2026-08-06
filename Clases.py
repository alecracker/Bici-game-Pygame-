
from os import SEEK_CUR
import pygame as pg
import Funciones as fn
import random as rm

list_x = [355,500,650,800]

class Bici(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = fn.carga("bici(der)")
        self.image_der = self.image
        self.image_izq = fn.carga("bici(izq)")
        self.rect = self.image_izq.get_rect()
        self.hitbox = self.rect.inflate(-140,-130)
        self.rect.x = x #posicion
        self.rect.y = y #Posicion
        self.anim = 0
        

    def pedalear(self):
        if  self.anim <= 30:
            self.image = self.image_der
        elif  self.anim <= 60:
            self.image = self.image_izq
        if self.anim > 60:
            self.anim= 0
        self.anim += 1

    def move(self,event):
        
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                if list_x.index(self.rect.x) - 1 == -1 :
                   print("estas en el limite") 
                else:
                    self.rect.x = list_x[list_x.index(self.rect.x)-1]
            elif event.key == pg.K_RIGHT:
                if list_x.index(self.rect.x) + 1 == 4:
                    print("estas en el limite")
                else:
                    self.rect.x = list_x[list_x.index(self.rect.x)+1]
        self.hitbox.center = self.rect.center 
        self.hitbox.y -= 50
    def colision(self,obs_hitbox):
        if self.hitbox.colliderect(obs_hitbox):
            print("colisiono")
        
                
        

class Obst(Bici):
    
    def __init__(self,x,y,imgref):
        super().__init__(x,y,imgref)
        self.image = fn.carga(imgref)
        self.rect = self.image.get_rect()
        if imgref == "Obs":
            self.hitbox = self.rect.inflate(-110, -110)
        elif imgref == "cauch":
            self.hitbox = self.rect.inflate(-20, -20)
        self.hitbox.y = 50
        self.y_float = float(y)
        
    def aparicion(self,n):
        x_obs = rm.randint(0,3)
        while n == x_obs: 
            x_obs = rm.randint(0,3)
            self.rect.x = list_x[x_obs]
        if self.imgref == "cauch":
            self.rect.centerx = list_x[x_obs] + 100
        else:
            self.rect.x = list_x[x_obs]

        return x_obs
    
    def pos(self,v):
        self.y_float += v
        self.rect.y = int(self.y_float)
        self.hitbox.center = self.rect.center