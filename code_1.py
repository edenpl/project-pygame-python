import pygame
import random
import math

pygame.init()

ANCHO = 800
ALTO = 600


pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Espacio Nave")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)


class Jugador:
    def __init__(self):
        self.ancho = 40
        self.alto = 40
        self.x = ANCHO // 2
        self.y = ALTO - 60
        self.velocidad = 5
        self.vida = 100
        self.puntuacion = 0
        
    def dibujar(self, superficie):
        pygame.draw.polygon(superficie, BLANCO, [
            (self.x, self.y - self.alto//2),
            (self.x - self.ancho//2, self.y + self.alto//2),
            (self.x + self.ancho//2, self.y + self.alto//2)
        ])
        
    def mover(self, direccion):
        if direccion == "izquierda" and self.x > self.ancho//2:
            self.x -= self.velocidad
        if direccion == "derecha" and self.x < ANCHO - self.ancho//2:
            self.x += self.velocidad

class Enemigo:
    def __init__(self):
        self.ancho = 30
        self.alto = 30
        self.x = random.randint(self.ancho, ANCHO - self.ancho)
        self.y = -self.alto
        self.velocidad = random.randint(2, 4)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, ROJO, (self.x - self.ancho//2, self.y - self.alto//2, self.ancho, self.alto))
        
    def mover(self):
        self.y += self.velocidad
        return self.y > ALTO + self.alto


class Disparo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 7
        self.radio = 3
        
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, VERDE, (self.x, self.y), self.radio)
        
    def mover(self):
        self.y -= self.velocidad
        return self.y < -self.radio

def mostrar_controles():
    mostrando_controles = True
    while mostrando_controles:
        pantalla.fill(NEGRO)
        
        dibujar_texto("CONTROLES", 64, ANCHO//2, 50)
        
        y_pos = 150
        dibujar_texto("Movimiento:", 40, ANCHO//2, y_pos)
        y_pos += 60
        dibujar_texto("← Flecha Izquierda: Mover a la izquierda", 32, ANCHO//2, y_pos)
        y_pos += 40
        dibujar_texto("→ Flecha Derecha: Mover a la derecha", 32, ANCHO//2, y_pos)
        y_pos += 60
        dibujar_texto("Disparo:", 40, ANCHO//2, y_pos)
        y_pos += 40
        dibujar_texto("BARRA ESPACIADORA", 32, ANCHO//2, y_pos) 
        y_pos += 60
        dibujar_texto("Otros:", 40, ANCHO//2, y_pos)
        


        y_pos += 40
        dibujar_texto("ESC: Salir al menú", 32, ANCHO//2, y_pos)
        y_pos += 80
        dibujar_texto("Presiona ESPACIO para volver al menú", 32, ANCHO//2, y_pos)
        
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return True
def mostrar_menu():
    menu = True
    while menu:
        pantalla.fill(NEGRO)
        dibujar_texto("Espacio Nave", 64, ANCHO//2, ALTO//4)
        
        y_pos = ALTO//2
        dibujar_texto("Presiona ESPACIO para jugar", 32, ANCHO//2, y_pos)
        
        y_pos += 50
        dibujar_texto("Presiona C para ver los controles", 32, ANCHO//2, y_pos)
        
        y_pos += 50
        dibujar_texto("Presiona ESC para salir", 32, ANCHO//2, y_pos)
        
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_c:
                    if not mostrar_controles():
                        return False
                if evento.key == pygame.K_ESCAPE:
                    return False
    
def dibujar_texto(texto, tamaño, x, y):
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, BLANCO)
    rect = superficie.get_rect()
    rect.midtop = (x, y)
    pantalla.blit(superficie, rect)



def detectar_colision(obj1_x, obj1_y, obj1_w, obj1_h, obj2_x, obj2_y, obj2_w, obj2_h):
    return (abs(obj1_x - obj2_x) < (obj1_w + obj2_w)//2 and 
            abs(obj1_y - obj2_y) < (obj1_h + obj2_h)//2)

def juego_principal():
    reloj = pygame.time.Clock()
    jugador = Jugador()
    enemigos = []
    disparos = []
    tiempo_ultimo_enemigo = 0
    intervalo_enemigo = 1000  
    jugando = True
    while jugando:
        tiempo_actual = pygame.time.get_ticks()
    
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return True
                if evento.key == pygame.K_SPACE:
                    disparos.append(Disparo(jugador.x, jugador.y - jugador.alto//2))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador.mover("izquierda")
        if teclas[pygame.K_RIGHT]:
            jugador.mover("derecha")
        

        if tiempo_actual - tiempo_ultimo_enemigo > intervalo_enemigo:
            enemigos.append(Enemigo())
            tiempo_ultimo_enemigo = tiempo_actual
        
        enemigos = [enemigo for enemigo in enemigos if not enemigo.mover()]
        disparos = [disparo for disparo in disparos if not disparo.mover()]
        for enemigo in enemigos[:]:
            if detectar_colision(jugador.x, jugador.y, jugador.ancho, jugador.alto,
                               enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto):
                jugador.vida -= 10
                enemigos.remove(enemigo)
                if jugador.vida <= 0:
                    mostrar_game_over(jugador.puntuacion)
                    return True
            for disparo in disparos[:]:
                if detectar_colision(disparo.x, disparo.y, disparo.radio*2, disparo.radio*2,
                                   enemigo.x, enemigo.y, enemigo.ancho, enemigo.alto):
                    if disparo in disparos:
                        disparos.remove(disparo)
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                        jugador.puntuacion += 100
        
        pantalla.fill(NEGRO)
        jugador.dibujar(pantalla)
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)
        for disparo in disparos:
            disparo.dibujar(pantalla)
            
        dibujar_texto(f"Puntuación: {jugador.puntuacion}", 32, 100, 10)
        dibujar_texto(f"Vida: {jugador.vida}", 32, ANCHO - 100, 10)
        
        pygame.display.flip()
        reloj.tick(60)

def mostrar_game_over(puntuacion):
    esperando = True
    while esperando:
        pantalla.fill(NEGRO)
        dibujar_texto("¡GAME OVER!", 64, ANCHO//2, ALTO//4)
        dibujar_texto(f"Puntuación final: {puntuacion}", 32, ANCHO//2, ALTO//2)
        dibujar_texto("Presiona ESPACIO para volver al menú", 32, ANCHO//2, ALTO*3//4)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

def main():
    jugando = True
    while jugando:
        jugando = mostrar_menu()
        if jugando:
            jugando = juego_principal()
    
    pygame.quit()

if __name__ == "__main__":
    main()




