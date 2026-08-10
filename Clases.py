
from settings import VERDE_PISTA
import pygame as pg
import Funciones as fn
import random as rm
import math
from settings import *
import sys 
import os
#posiciones en x de los carriles
list_x1 = [316, 366, 416, 465]      
list_x2 = [750, 800, 850, 899]      
list_x = [440, 545, 650, 755]

class Bici(pg.sprite.Sprite):
    def __init__(self, x, y, player, lista_carriles, competencia=False):
        pg.sprite.Sprite.__init__(self)
        self.lista_carriles = lista_carriles
        
        # 1. Cargamos las imágenes originales
        self.image_der = fn.carga("bici(der)")
        self.image_izq = fn.carga("bici(izq)")
        
        # 2. Si estamos en competencia, las encogemos
        if competencia:
            self.image_der = pg.transform.scale(self.image_der, (90, 100))
            self.image_izq = pg.transform.scale(self.image_izq, (90, 100))
            
        # 3. Asignamos la imagen principal que usará Pygame (ya encogida si aplica)
        self.image = self.image_der

        # 4. AHORA SÍ, sacamos el rectángulo de la imagen
        self.rect = self.image.get_rect()
        
        # 5. Calculamos la hitbox según el tamaño
        if competencia:
            self.hitbox = self.rect.inflate(-60, -65) 
        else: 
            self.hitbox = self.rect.inflate(-100, -100)
            
        # 6. Posicionamos
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.anim = 0
        self.img_cayendo = fn.carga("cayendo") 
        self.choque = False
        self.competencia = competencia
        self.vel = 0


    def pedalear(self):

        if not self.choque:
            if  self.anim <= 30:
                self.image = self.image_der
            elif  self.anim <= 60:
                self.image = self.image_izq
            if self.anim > 60:
                self.anim= 0
        self.anim += 1

    def move(self,event):
        if not self.choque:
           
         if self.player == 1:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if self.lista_carriles.index(self.rect.x) - 1 == -1 :
                       print("estas en el limite") 
                    else:
                        self.rect.x = self.lista_carriles[self.lista_carriles.index(self.rect.x)-1]
                elif event.key == pg.K_RIGHT:
                    if self.lista_carriles.index(self.rect.x) + 1 == 4:
                        print("estas en el limite")
                    else:
                        self.rect.x = self.lista_carriles[self.lista_carriles.index(self.rect.x)+1]
         else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    if self.lista_carriles.index(self.rect.x) - 1 == -1:
                        print("estas en el limite")
                    else:
                        self.rect.x = self.lista_carriles[self.lista_carriles.index(self.rect.x)-1]
                elif event.key == pg.K_d:
                    if self.lista_carriles.index(self.rect.x) + 1 == 4:
                        print("estas en el limite")
                    else:
                        self.rect.x = self.lista_carriles[self.lista_carriles.index(self.rect.x)+1]

        self.hitbox.center = self.rect.center 
        if self.competencia:
            self.hitbox.y -= 25  # Empuja la caja roja hacia arriba en Competencia
        else:
            self.hitbox.y -= 40  #
    def acelerar(self):
        if self.competencia:
            t_acelerar = pg.key.get_pressed()
            if t_acelerar[pg.K_UP] and self.vel < 18 and self.player == 1:
                self.vel += 0.5
            elif t_acelerar[pg.K_w] and self.vel < 18 and self.player == 2:
                self.vel += 0.5
            elif t_acelerar[pg.K_DOWN] and self.player == 1:
                self.vel -= 0.5
            elif t_acelerar[pg.K_s] and self.player == 2:
                self.vel -= 0.5
            if self.vel < 0:
                self.vel = 0

            if self.vel > 0:
                self.vel -= 0.05
    
             

    def colision(self,obs_hitbox):
      if not self.choque: 
        if self.hitbox.colliderect(obs_hitbox):
            self.choque = True
            self.image = self.img_cayendo
            return True
        return False

    def caerse(self):
        if self.rect.y > 250:
            self.rect.y -= 10
            ancho_actual = self.image.get_width()
            alto_actual = self.image.get_height()
            
            if self.rect.y > 385:
                nuevo_ancho = ancho_actual + 5
                nuevo_alto = alto_actual + 5
            else:
                nuevo_ancho = ancho_actual - 5
                nuevo_alto = alto_actual - 5
                
            if self.competencia == False:
                if nuevo_ancho < 120:
                    nuevo_ancho, nuevo_alto = 120, 120
            else:
                if nuevo_ancho < 90:
                    nuevo_ancho,nuevo_alto = 90,90

            self.image = pg.transform.scale(self.img_cayendo, (nuevo_ancho, nuevo_alto))
            centro_viejo = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = centro_viejo
        
                
        

class Obst(Bici):
    
    def __init__(self,x,y,imgref,lista_carril_obs, competencia=False):
        super().__init__(x,y, 0,lista_carril_obs,competencia)
        self.image = fn.carga(imgref)
        self.competencia = competencia # Guardamos si es competencia
        if competencia == True:
            if imgref == "Obs":
                self.image = pg.transform.scale(self.image,(45,45)) # Tamaño reducido para que quepa en el carril (antes 80x80)
            else:
                self.image = pg.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.imgref = imgref
        self.lista_carril_obs = lista_carril_obs
        if imgref == "Obs":
            self.hitbox = self.rect.inflate(-10, -10) # Hitbox ajustada al nuevo tamaño
        else:
            self.hitbox = self.rect.inflate(-10, -10)
        self.hitbox.y = 50
        self.y_float = float(y)
        
    def aparicion(self,n):
        x_obs = rm.randint(0,3)
        
        while n == x_obs: 
            x_obs = rm.randint(0,3)
            
        # Centrar el obstáculo en el carril
        if self.competencia:
            # En competencia, el ancho de la bici es 90, su centro está a +45
            self.rect.centerx = self.lista_carril_obs[x_obs] + 45
        else:
            # En libre, el centro es +60 aproximadamente
            self.rect.centerx = self.lista_carril_obs[x_obs] + 60
            
        if self.imgref == "cauch":
            self.rect.centery += 50

        return x_obs
    
    def pos(self,v):
        self.y_float += v
        self.rect.y = int(self.y_float)
        self.hitbox.center = self.rect.center



class Boton:
    # Botones clásicos (para los modos de juego)
    def __init__(self, x, y, ancho, alto, texto, accion):
        self.rect = pg.Rect(x, y, ancho, alto)
        self.texto = texto
        self.accion = accion
        self.fuente = pg.font.SysFont("Arial", 36, bold=True)

    def draw(self, pantalla):
        pos_raton = pg.mouse.get_pos()
        color = AZUL_HOVER if self.rect.collidepoint(pos_raton) else AZUL_BOTON
        pg.draw.rect(pantalla, color, self.rect, border_radius=25) # Bordes más redondeados
        pg.draw.rect(pantalla, BLANCO, self.rect, 3, border_radius=25) 
        texto_superficie = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_superficie.get_rect(center=self.rect.center)
        pantalla.blit(texto_superficie, texto_rect)

    def check_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.accion
        return None

class BotonCircular:
    
    def __init__(self, x, y, radio, texto, accion):
        self.x = x
        self.y = y
        self.radio = radio
        self.texto = texto
        self.accion = accion
        self.fuente = pg.font.SysFont("Arial", int(radio * 1.2), bold=True)

    def draw(self, pantalla):
        pos_raton = pg.mouse.get_pos()
        # Calcular si el ratón está dentro del círculo usando el teorema de Pitágoras
        distancia = math.hypot(pos_raton[0] - self.x, pos_raton[1] - self.y)
        color = AZUL_HOVER if distancia <= self.radio else (20, 50, 100)
        
        # Dibujar círculo y borde
        pg.draw.circle(pantalla, color, (self.x, self.y), self.radio)
        pg.draw.circle(pantalla, BLANCO, (self.x, self.y), self.radio, 3)

        # Renderizar texto o símbolo adentro
        texto_superficie = self.fuente.render(self.texto, True, BLANCO)
        texto_rect = texto_superficie.get_rect(center=(self.x, self.y))
        pantalla.blit(texto_superficie, texto_rect)

    def check_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            distancia = math.hypot(event.pos[0] - self.x, event.pos[1] - self.y)
            if distancia <= self.radio:
                return self.accion
        return None

class Menu:
    def __init__(self):
        centro_x = ANCHO // 2 - 150
        self.img_intro = fn.carga("intro")
        self.img_intro = pg.transform.scale(self.img_intro,(ANCHO,ALTO))
        # Botones de Modos de Juego (Centro)
        self.botones_modos = [
            Boton(centro_x, 280, 300, 60, "Modo Libre", "LIBRE"),
            Boton(centro_x, 370, 300, 60, "Competencia", "COMPETENCIA")
        ]
        
        # Botones de Utilidad 
        radio_btn = 30
        self.botones_iconos = [
            BotonCircular(ANCHO - 60, 60, radio_btn, "!", "COMO_JUGAR"),  
            BotonCircular(60, ALTO - 130, radio_btn, "M", "MUSICA"),     
            BotonCircular(60, ALTO - 60, radio_btn, "X", "SALIR")       
        ]
        

        self.titulo_fuente = pg.font.SysFont("Impact", 80)
        
        

    def draw(self, pantalla):

        pantalla.blit(self.img_intro,(0,0))
        
        # Dibujar Título principal
        titulo = self.titulo_fuente.render("RAPIDASH", True, BLANCO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, 100))
        # Sombra del título
        sombra = self.titulo_fuente.render("RAPIDASH", True, NEGRO)
        pantalla.blit(sombra, (titulo_rect.x + 4, titulo_rect.y + 4))
        pantalla.blit(titulo, titulo_rect)

    
        for boton in self.botones_modos + self.botones_iconos:
            boton.draw(pantalla)

    def handle_events(self, event):
        for boton in self.botones_modos + self.botones_iconos:
            accion = boton.check_click(event)
            if accion:
                return accion
        return None
class Juego:
    def __init__(self):
        self.nivel = 0
        self.puntaje = 0
        self.ventana = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption("Ciclismo Rapidash")
        self.reloj = pg.time.Clock()
        self.grama = fn.carga("grama")
        self.grama2 = fn.carga("grama") 
        self.der = fn.carga("desierto")
        self.mar = fn.carga("mar")
        self.lista_niveles = [self.grama,self.der,self.mar]
        self.fondo_down = self.grama
        self.fondo_up= self.grama2
        self.sprites = pg.sprite.Group()
        self.vel = 0.5
        self.v = 0
        self.estado = "MENU"
        self.menu = Menu()
        self.corriendo = True
        self.musica_activa = True # Variable para controlar la música
        
        pg.mixer.music.load(os.path.join('assets','menu.mp3'))
        pg.mixer.music.set_volume(0.10)
        pg.mixer.music.play(-1)
        self.fuente_puntos = pg.font.SysFont("Impact", 40)
        self.texto = self.fuente_puntos.render(f"Puntaje: {int(self.puntaje)}", True, VERDE_PISTA) 
    
    def procesar_eventos(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.corriendo = False
            if event.type == pg.MOUSEBUTTONDOWN:
                print(f"Clic en X: {event.pos[0]}")
            if self.estado == "MENU":
                accion = self.menu.handle_events(event)
                # --- LÓGICA DE LOS NUEVOS BOTONES ---
                if accion == "SALIR":
                    self.corriendo = False
                elif accion == "MUSICA":
                    self.musica_activa = not self.musica_activa
                    if self.musica_activa == True:
                        pg.mixer.music.unpause()
                    else:
                        pg.mixer.music.pause()
                    pg.mixer.music.set_volume
                elif accion == "COMO_JUGAR":
                    self.estado = "COMO_JUGAR"
                elif accion in ["LIBRE","COMPETENCIA"]:
                    pg.mixer.music.load(os.path.join('assets','ingame.mp3'))
                    pg.mixer.music.set_volume(0.03)
                    pg.mixer.music.play(-1)
                    if self.musica_activa == False:
                        pg.mixer.music.pause()
                    self.estado = accion
                    self.reiniciar()
                    
            elif self.estado == "COMO_JUGAR":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.estado = "MENU"
                        
            elif self.estado == "LIBRE":
                self.bici.move(event)
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.estado = "MENU"
                    pg.mixer.music.load(os.path.join('assets','menu.mp3'))
                    pg.mixer.music.play(-1)
                    if self.musica_activa == False:
                        pg.mixer.music.pause()
                    self.reiniciar()
            elif self.estado == "COMPETENCIA":
                self.bici.move(event)
                self.bici2.move(event)
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.estado = "MENU"
                    pg.mixer.music.load(os.path.join('assets','menu.mp3'))
                    pg.mixer.music.play(-1)
                    if self.musica_activa == False:
                        pg.mixer.music.pause()
                    self.reiniciar()
            elif self.estado == "PERDISTE":
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN: 
                    self.estado = "MENU"
                    pg.mixer.music.load(os.path.join('assets','menu.mp3'))
                    pg.mixer.music.play(-1)
                    if self.musica_activa == False:
                        pg.mixer.music.pause()

    def actualizar(self):
        if self.estado in ["LIBRE", "COMPETENCIA"]:
            # Comprobar si alguien chocó para terminar el juego
            jugando = True
            if self.bici.choque:
                jugando = False
            if self.estado == "COMPETENCIA" and hasattr(self, 'bici2') and self.bici2.choque:
                jugando = False
                
            if jugando:
                self.bici.pedalear()
                self.bici.hitbox.center = self.bici.rect.center
                self.bici.hitbox.y -= 40 if self.estado == "LIBRE" else 25
                
                if self.estado == "COMPETENCIA" and hasattr(self, 'bici2'):
                    self.bici2.pedalear()
                    self.bici2.hitbox.center = self.bici2.rect.center
                    self.bici2.hitbox.y -= 25

                t_acelerar = pg.key.get_pressed()
                acelerando = False
                
                if self.estado == "LIBRE":
                    # Controles Jugador 1
                    if t_acelerar[pg.K_UP] and self.vel < 18:
                        self.vel += 0.05
                        acelerando = True
                    elif t_acelerar[pg.K_DOWN] and self.vel > 0:
                        self.vel -= 0.04
                        
                    # Fricción natural si nadie acelera
                    if not acelerando:
                        self.vel -= 0.01
                        
                    self.vel += 0.01 # Aceleración progresiva global
                    
                elif self.estado == "COMPETENCIA":
                    # Modo automático (estilo Subway Surfers)
                    if self.vel < 12: # Límite máximo de velocidad (antes era 25 y era muy rápido)
                        self.vel += 0.002 # Aumento progresivo mucho más lento para que dure más la partida
                        
                if self.vel < 0:
                    self.vel = 0
                    
                self.puntaje += self.vel
                self.v += self.vel
                
                # Mover todos los obstáculos juntos a la velocidad compartida
                for obs in self.lista_obs:
                    obs.pos(self.vel)
                    if self.bici.colision(obs.hitbox):
                        self.vel = 0
                    if self.estado == "COMPETENCIA" and hasattr(self, 'bici2'):
                        if self.bici2.colision(obs.hitbox):
                            self.vel = 0
                            
                for obs in self.lista_obs:
                    if obs.y_float >= 720:
                        obs.aparicion(-1)
                        obs.y_float = rm.randint(-400,-100)
                        
                if self.v >= 720:
                    self.v = 0
                    self.fondo_down = self.fondo_up
                    if self.estado != "COMPETENCIA":
                        nivel_calculado = int(self.puntaje // 10000)
                        if nivel_calculado > self.nivel:
                            self.nivel = nivel_calculado
                            self.fondo_up = rm.choice(self.lista_niveles)
            else:
                # Alguien chocó
                self.vel = 0
                if self.bici.choque:
                    self.bici.caerse()
                    if self.bici.rect.y <= 250:
                        self.estado = "PERDISTE"
                if self.estado == "COMPETENCIA" and hasattr(self, 'bici2') and self.bici2.choque:
                    self.bici2.caerse()
                    if self.bici2.rect.y <= 250:
                        self.estado = "PERDISTE"
                    
    def dibujar(self):
        if self.estado == "MENU":
            self.menu.draw(self.ventana)
        elif self.estado == "COMO_JUGAR":
            self.ventana.fill(AZUL_BOTON)
            fuente = pg.font.SysFont("Arial", 30)
            fuente_titulo = pg.font.SysFont("Arial", 40, bold=True)
            
            texto1 = fuente_titulo.render("CÓMO JUGAR", True, BLANCO)
            
            t_libre1 = fuente.render("MODO LIBRE:", True, VERDE_PISTA)
            t_libre2 = fuente.render("- Usa las flechas para moverte y acelerar/frenar.", True, BLANCO)
            
            t_comp1 = fuente.render("MODO COMPETICIÓN:", True, VERDE_PISTA)
            t_comp2 = fuente.render("- J1: Flechas | J2: Teclas A/D", True, BLANCO)
            t_comp3 = fuente.render("- ¡La velocidad aumenta sola! Sobrevive.", True, BLANCO)
            
            volver = fuente.render("Presiona ESC para volver al menú", True, NEGRO)
            
            self.ventana.blit(texto1, (ANCHO//2 - texto1.get_width()//2, 80))
            self.ventana.blit(t_libre1, (ANCHO//2 - t_libre1.get_width()//2, 160))
            self.ventana.blit(t_libre2, (ANCHO//2 - t_libre2.get_width()//2, 210))
            
            self.ventana.blit(t_comp1, (ANCHO//2 - t_comp1.get_width()//2, 290))
            self.ventana.blit(t_comp2, (ANCHO//2 - t_comp2.get_width()//2, 340))
            self.ventana.blit(t_comp3, (ANCHO//2 - t_comp3.get_width()//2, 390))
            
            self.ventana.blit(volver, (ANCHO//2 - volver.get_width()//2, ALTO - 100))
        
        elif self.estado == "PERDISTE":
            self.ventana.fill((0, 0, 0)) # Pintamos todo de negro
            fuente_grande = pg.font.SysFont("Arial", 60, bold=True)
            fuente_chica = pg.font.SysFont("Arial", 40)
            
            # --- LÓGICA DE QUIÉN PERDIÓ ---
            if hasattr(self, 'bici2'):
                if self.bici.choque == True:
                    mensaje_fin = "¡PERDIÓ EL JUGADOR 1!"
                elif self.bici2.choque == True:
                    mensaje_fin = "¡PERDIÓ EL JUGADOR 2!"
            else:
                mensaje_fin = "¡JUEGO TERMINADO!" # Mensaje por defecto para el modo Libre

            # Actualizar récord si es necesario
            if self.puntaje > getattr(self, 'record', 0):
                self.record = self.puntaje

            # Renderizamos los textos
            texto1 = fuente_grande.render(mensaje_fin, True, (255, 0, 0))
            texto2 = fuente_chica.render(f"Puntaje Final: {int(self.puntaje)}", True, BLANCO)
            texto_record = fuente_chica.render(f"Récord Máximo: {int(getattr(self, 'record', 0))}", True, VERDE_PISTA)
            texto3 = fuente_chica.render("Presiona ENTER para volver al menú", True, BLANCO)
            
            # Los pegamos centrados en la pantalla
            self.ventana.blit(texto1, (ANCHO//2 - texto1.get_width()//2, 150))
            self.ventana.blit(texto2, (ANCHO//2 - texto2.get_width()//2, 250))
            self.ventana.blit(texto_record, (ANCHO//2 - texto_record.get_width()//2, 320))
            self.ventana.blit(texto3, (ANCHO//2 - texto3.get_width()//2, 450))
                        
        else:
            self.ventana.fill((0,0,0))
            # Fondo Scrolling
            self.ventana.blit(self.fondo_up, (0, self.v - 720))
            self.ventana.blit(self.fondo_down, (0, self.v))

            self.sprites.draw(self.ventana)
            self.puntos = self.fuente_puntos.render(f"Puntaje: {int(self.puntaje)}", True, VERDE_PISTA)
            self.ventana.blit(self.puntos, (20, 20)) 
            
            # Mostrar récord durante el juego también (arriba a la derecha)
            if hasattr(self, 'record') and self.record > 0:
                texto_rec = self.fuente_puntos.render(f"Mejor: {int(self.record)}", True, BLANCO)
                self.ventana.blit(texto_rec, (ANCHO - texto_rec.get_width() - 20, 20))

        pg.display.flip()


    def reiniciar(self):

            self.puntaje = 0
            self.vel = 0.5
            self.v = 0
            self.sprites = pg.sprite.Group()
            
        
            if self.estado == "LIBRE":
                
                self.fondo_down = self.grama
                self.fondo_up = self.grama2
                self.nivel = 0 # También reseteamos el nivel para que empiece de cero
                self.bici = Bici(545, 520, 1,list_x)
                self.obs = Obst(1000, self.v-200, "cauch", list_x)
                self.obs1 = Obst(1000, self.v-450, "cauch", list_x)
                self.obs2 = Obst(1000, self.v-700, "Obs", list_x)
                self.obs3 = Obst(1000, self.v-950, "Obs", list_x)
            
                self.lista_obs = [self.obs, self.obs1, self.obs2, self.obs3]
                for obs in self.lista_obs:
                    obs.aparicion(-1)
                    obs.y_float = rm.randint(-400,-100)
                
                self.sprites.add(self.bici, self.obs, self.obs1, self.obs2, self.obs3)
            
            elif self.estado == "COMPETENCIA":
                
                self.fondo_down = fn.carga("competencia")
                self.fondo_up = fn.carga("competencia")

                # --- MODO COMPETENCIA: Las 2 Bicis ---
                self.bici = Bici(316, 520, 1,list_x1,True)  # Nace en la pista izquierda
                self.bici2 = Bici(750, 520, 2,list_x2,True) # Nace en la pista derecha
                
               

                # 2 obstáculos para el Jugador 1 (en list_x1)
                self.obs = Obst(1000, self.v-200, "cauch", list_x1,True)
                self.obs1 = Obst(1000, self.v-450, "cauch", list_x1,True)
                self.obs6 = Obst(1000,self.v-1200,"Obs",list_x1,True)
                self.obs7 = Obst(1000,self.v-1450,"Obs",list_x1,True)
                # 2 obstáculos para el Jugador 2 (en list_x2)
                self.obs2 = Obst(1000, self.v-700, "Obs", list_x2,True)
                self.obs3 = Obst(1000, self.v-950, "Obs", list_x2,True)
                self.obs4 = Obst(1000,self.v-1200,"cauch",list_x2,True)
                self.obs5 = Obst(1000,self.v-1450,"cauch",list_x2,True)
                
                # Los agrupamos y los preparamos
                self.lista_obs = [self.obs, self.obs1, self.obs2, self.obs3, self.obs4, self.obs5, self.obs6, self.obs7]
                self.lista_obs1 = [self.obs, self.obs1, self.obs6, self.obs7]
                self.lista_obs2 = [self.obs2, self.obs3, self.obs4, self.obs5]
                for obs in self.lista_obs:
                    obs.aparicion(-1)
                    obs.y_float = rm.randint(-400, -100)
                
                # ¡Añadimos TODOS a la pantalla (los metemos al grupo sprites)!
                self.sprites.add(self.bici, self.bici2, self.obs, self.obs1, self.obs2, self.obs3,self.obs4,self.obs5,self.obs6,self.obs7)

    def ejecutar(self):
        while self.corriendo:
            self.procesar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

        pg.quit()
        sys.exit()

        