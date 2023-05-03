
import pygame
import sys
import IA1
import IA2

# Constantes
ancho = 800
alto = 600
posicion_inicial_paleta1 = (50, alto // 2)
posicion_inicial_paleta2 = (ancho - 50, alto // 2)
posicion_inicial_pelota = (ancho // 2, alto // 2)

class Paleta:
    def __init__(self, posicion):
        self.x, self.y = posicion
        self.width = 20
        self.height = 100
        self.color = (255, 255, 255)
        self.speed = 5

    def mover(self, accion):
        if accion == 0:  # Mover hacia arriba
            self.y -= self.speed
        elif accion == 1:  # Mover hacia abajo
            self.y += self.speed

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.width, self.height))

class Pelota:
    def __init__(self, posicion):
        self.x, self.y = posicion
        self.width = 20
        self.height = 20
        self.color = (255, 255, 255)
        self.speed_x = 5
        self.speed_y = 5

    def actualizar(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.width, self.height))

def detectar_colisiones(paleta1, paleta2, pelota):
    if pelota.y <= 0 or pelota.y + pelota.height >= alto:
        pelota.speed_y = -pelota.speed_y

    if (paleta1.x <= pelota.x <= paleta1.x + paleta1.width and
            paleta1.y <= pelota.y <= paleta1.y + paleta1.height) or (
            paleta2.x <= pelota.x + pelota.width <= paleta2.x + paleta2.width and
            paleta2.y <= pelota.y <= paleta2.y + paleta2.height):
        pelota.speed_x = -pelota.speed_x

def dibujar(pantalla, paleta1, paleta2, pelota):
    pantalla.fill((0, 0, 0))
    paleta1.dibujar(pantalla)
    paleta2.dibujar(pantalla)
    pelota.dibujar(pantalla)


# Inicializar pygame y crear ventana de juego
pygame.init()
pantalla = pygame.display.set_mode((ancho, alto))

# Crear objetos para las paletas y la pelota
paleta1 = Paleta(posicion_inicial_paleta1)
paleta2 = Paleta(posicion_inicial_paleta2)
pelota = Pelota(posicion_inicial_pelota)

# Inicializar actores y críticos globales para A3C
actor_global = IA2.inicializar_actor()
critic_global = IA2.inicializar_critic()

# Instanciar las dos inteligencias artificiales (DDPG y A3C)
jugador1 = IA1.Jugador(paleta1)  # DDPG
jugador2 = IA2.Trabajador(paleta2, actor_global, critic_global)  # A3C

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar las posiciones de las paletas y la pelota usando DDPG y A3C
    jugador1.actualizar(paleta1, pelota)  # DDPG
    jugador2.actualizar(paleta2, pelota)  # A3C
    pelota.actualizar()

    # Detectar colisiones y actualizar las puntuaciones
    detectar_colisiones(paleta1, paleta2, pelota)

    # Dibujar en la ventana
    dibujar(pantalla, paleta1, paleta2, pelota)

    # Actualizar la ventana
    pygame.display.flip()