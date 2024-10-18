import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("song.mpeg")

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Esquiva los bloques")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
mejor_puntuacion = 0
fuente = pygame.font.Font(None, 36)
fuente_t = pygame.font.Font(None, 60)
tamano_jugador = 50
posicion_jugador = [ANCHO // 2, ALTO - 2 * tamano_jugador]
tamano_bloque = 50
lista_bloques = []
velocidad = 10
dificultad = 'Media'
nivel = 1
puntuacion = 0
juego_terminado = False


archivo_puntuacion = "mejor_puntuacion.txt"
def cargar_mejor_puntuacion():
    global mejor_puntuacion
    if os.path.exists(archivo_puntuacion):
        with open(archivo_puntuacion, 'r') as archivo:
            mejor_puntuacion = int(archivo.read())
    else:
        mejor_puntuacion = 0 

def guardar_mejor_puntuacion():
    with open(archivo_puntuacion, 'w') as archivo:
        archivo.write(str(mejor_puntuacion))
# Tipos de bloques
class Bloque:
    def __init__(self, x, y, tipo_bloque):
        self.x = x
        self.y = y
        self.tipo = tipo_bloque
        self.ancho = tamano_bloque
        self.alto = tamano_bloque
        self.movible = (self.tipo == 'movible')
        if nivel == 3:
            self.ancho = tamano_bloque * 1.5 
            self.alto = tamano_bloque * 1.5   
        self.direccion = random.choice([-1, 1]) if self.movible else 0  
        self.velocidad = 6 if nivel == 3 else 2  
    def mover(self):
        if self.movible:
            self.x += self.direccion * self.velocidad
            if self.x <= 0 or self.x >= ANCHO - self.ancho:
                self.direccion *= -1  

    def dibujar(self):
        if self.movible:
            pygame.draw.rect(pantalla, AMARILLO, (self.x, self.y, self.ancho, self.alto))
        else:
            pygame.draw.rect(pantalla, ROJO, (self.x, self.y, self.ancho, self.alto))

def dibujar_texto(texto, fuente, color, superficie, x, y):
    objeto_texto = fuente.render(texto, True, color)
    rectangulo_texto = objeto_texto.get_rect()
    rectangulo_texto.center = (x, y)
    superficie.blit(objeto_texto, rectangulo_texto)

def menu_principal():
    global dificultad
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto('Esquiva el Bloque', fuente_t, BLANCO, pantalla, ANCHO // 2, ALTO // 4)
        dibujar_texto('Presiona espacio para Jugar', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 2-100)
        dibujar_texto('Presiona D para cambiar la dificultad', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 1.75)
        dibujar_texto(f'Dificultad: {dificultad}', fuente, VERDE, pantalla, ANCHO // 2, ALTO // 1.5)
        dibujar_texto('Presiona I para Instrucciones', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 1.25)
        dibujar_texto('Presiona Q para Salir', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 1.1)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bucle_juego()  # Iniciar el juego
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_i:
                    mostrar_instrucciones()
                elif evento.key == pygame.K_d:
                    cambiar_dificultad()

        pygame.display.update()

def mostrar_instrucciones():
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto('Instrucciones:', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 4)
        dibujar_texto('1. Esquiva los bloques que caen ', fuente, ROJO, pantalla, ANCHO // 2, ALTO // 2)
        dibujar_texto('2. Usa las flechas para moverte', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 1.75)
        dibujar_texto('Presiona B para volver', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 1.25)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_b:
                    return  

        pygame.display.update()

def cambiar_dificultad():
    global dificultad
    if dificultad == 'Facil':
        dificultad = 'Media'
    elif dificultad == 'Media':
        dificultad = 'Dificil'
    else:  # Dificil
        dificultad = 'Facil'

def soltar_bloques(lista_bloques, nivel):
    if len(lista_bloques) < 10:
        if nivel == 1:
            if random.random() < 0.2: 
                tipo_bloque = 'normal'
                x_posicion = random.randint(0, ANCHO - tamano_bloque)
                lista_bloques.append(Bloque(x_posicion, 0, tipo_bloque))
        elif nivel == 2:
            if random.random() < 0.2: 
                tipo_bloque = random.choice(['normal', 'movible'])
                x_posicion = random.randint(0, ANCHO - tamano_bloque)
                lista_bloques.append(Bloque(x_posicion, 0, tipo_bloque))
            
        elif nivel == 3:
               if random.random() < 0.2: 
                tipo_bloque = random.choice(['normal', 'movible'])
                x_posicion = random.randint(0, ANCHO - tamano_bloque)
                lista_bloques.append(Bloque(x_posicion, 0, tipo_bloque))

def actualizar_posicion_bloques(lista_bloques, puntuacion, velocidad):
    for idx, bloque in enumerate(lista_bloques):
        if bloque.y >= 0 and bloque.y < ALTO:
            bloque.y += velocidad
            bloque.mover() 
        else:
            lista_bloques.pop(idx)
            puntuacion += 1
    return puntuacion

def detectar_colision(lista_bloques, posicion_jugador):
    for bloque in lista_bloques:
        if checar_colision((posicion_jugador[0], posicion_jugador[1]), (bloque.x, bloque.y)):
            return True
    return False

def checar_colision(posicion_jugador, posicion_bloque):
    j_x = posicion_jugador[0]
    j_y = posicion_jugador[1]
    b_x = posicion_bloque[0]
    b_y = posicion_bloque[1]

    if (b_x >= j_x and b_x < (j_x + tamano_jugador)) or (j_x >= b_x and j_x < (b_x + tamano_bloque)):
        if (b_y >= j_y and b_y < (j_y + tamano_jugador)) or (j_y >= b_y and j_y < (b_y + tamano_bloque)):
            return True
    return False
def actualizar_tiempo(tiempo_transcurrido):
    tiempo_transcurrido+=1;

def bucle_juego():
    global lista_bloques, puntuacion, posicion_jugador, velocidad, juego_terminado, dificultad, nivel,mejor_puntuacion

    lista_bloques = []
    puntuacion = 0
    posicion_jugador = [ANCHO // 2, ALTO - 2 * tamano_jugador]
    juego_terminado = False
    nivel = 1

    if dificultad == 'Facil':
        velocidad = 5
    elif dificultad == 'Media':
        velocidad = 10
    else:  # Dificil
        velocidad = 15

    pygame.mixer.music.play(-1)
    reloj = pygame.time.Clock()

    while not juego_terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and posicion_jugador[0] > 0:
            posicion_jugador[0] -= 10
        if teclas[pygame.K_RIGHT] and posicion_jugador[0] < ANCHO - tamano_jugador:
            posicion_jugador[0] += 10

        pantalla.fill(NEGRO)

        pygame.draw.rect(pantalla, AZUL, (posicion_jugador[0], posicion_jugador[1], tamano_jugador, tamano_jugador))

        soltar_bloques(lista_bloques, nivel)

        puntuacion = actualizar_posicion_bloques(lista_bloques, puntuacion, velocidad)


        for bloque in lista_bloques:
            bloque.dibujar()


        if detectar_colision(lista_bloques, posicion_jugador):
            juego_terminado = True
            pygame.mixer.music.stop()
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion 
                guardar_mejor_puntuacion()
            mostrar_juego_terminado()   
  

        dibujar_texto(f'Puntuación: {puntuacion}', fuente, BLANCO, pantalla, 100, 30)
        dibujar_texto(f'Mejor Puntuación: {mejor_puntuacion}', fuente, BLANCO, pantalla, ANCHO-180, 30)  # Muestra mejor puntuación
        if puntuacion >= 50 and nivel == 1:
            nivel += 1
        elif puntuacion >= 80 and nivel == 2:
            nivel += 1
        elif puntuacion >= 180 and nivel == 3:
            nivel += 1
        if nivel > 3:
            nivel = 1

        pygame.display.update()
        reloj.tick(30)
def mostrar_juego_terminado():
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto('Juego Terminado', fuente, ROJO, pantalla, ANCHO // 2, ALTO // 4)
        dibujar_texto(f'Tu puntuación: {puntuacion}', fuente, BLANCO, pantalla, ANCHO // 2, ALTO // 2)
        dibujar_texto('Presiona Espacio para reiniciar', fuente, VERDE, pantalla, ANCHO // 2, ALTO // 2+40)
        dibujar_texto('Presiona M para volver al menú', fuente, AZUL, pantalla, ANCHO // 2, ALTO // 2+80)
        dibujar_texto('Presiona Q para salir', fuente, ROJO, pantalla, ANCHO // 2, ALTO // 2+120)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                     bucle_juego()
                elif evento.key == pygame.K_m:
                    return 'menu'  
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
cargar_mejor_puntuacion()
menu_principal()
