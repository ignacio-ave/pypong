import pygame
import sys

# Parámetros del juego
ancho = 800
alto = 600
posicion_inicial_paleta1 = (50, 250)
posicion_inicial_paleta2 = (750, 250)
posicion_inicial_pelota = (400, 300)

class Paleta:
    def __init__(self, posicion_inicial):
        self.rect = pygame.Rect(posicion_inicial[0], posicion_inicial[1], 10, 100)

    def mover(self, dy):
        if 0 <= self.rect.y + dy <= alto - self.rect.height:
            self.rect.y += dy

class Pelota:
    def __init__(self, posicion_inicial):
        self.rect = pygame.Rect(posicion_inicial[0], posicion_inicial[1], 10, 10)
        self.dx, self.dy = 1, 1

    def actualizar(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= alto:
            self.dy *= -1

def detectar_colisiones(paleta1, paleta2, pelota, marcador):
    if pelota.rect.colliderect(paleta1.rect) or pelota.rect.colliderect(paleta2.rect):
        pelota.dx *= -1

    if pelota.rect.left <= 0:
        marcador["jugador2"] += 1
        pelota.rect.x = ancho // 2
        pelota.rect.y = alto // 2

    if pelota.rect.right >= ancho:
        marcador["jugador1"] += 1
        pelota.rect.x = ancho // 2
        pelota.rect.y = alto // 2

    return marcador

def dibujar(pantalla, paleta1, paleta2, pelota, marcador):
    pantalla.fill((0, 0, 0))
    pygame.draw.rect(pantalla, (255, 255, 255), paleta1.rect)
    pygame.draw.rect(pantalla, (255, 255, 255), paleta2.rect)
    pygame.draw.ellipse(pantalla, (255, 255, 255), pelota.rect)
    pygame.draw.aaline(pantalla, (255, 255, 255), (ancho // 2, 0), (ancho // 2, alto))

    fuente = pygame.font.Font(None, 36)
    texto_jugador1 = fuente.render(str(marcador["jugador1"]), True, (255, 255, 255))
    texto_jugador2 = fuente.render(str(marcador["jugador2"]), True, (255, 255, 255))
    pantalla.blit(texto_jugador1, (ancho // 2 - 100, 10))
    pantalla.blit(texto_jugador2, (ancho // 2 + 100, 10))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ancho, alto))

    paleta1 = Paleta(posicion_inicial_paleta1)
    paleta2 = Paleta(posicion_inicial_paleta2)
    pelota = Pelota(posicion_inicial_pelota)
    marcador = {"jugador1": 0, "jugador2": 0}



    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paleta1.mover(-5)
        if keys[pygame.K_s]:
            paleta1.mover(5)
        if keys[pygame.K_UP]:
            paleta2.mover(-5)
        if keys[pygame.K_DOWN]:
            paleta2.mover(5)

        marcador = detectar_colisiones(paleta1, paleta2, pelota, marcador)
        pelota.actualizar()
        #detectar_colisiones(paleta1, paleta2, pelota)
        
        dibujar(pantalla, paleta1, paleta2, pelota, marcador)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
