import networkx as nx
import random
import py5
import time

# Función para generar un laberinto aleatorio (grafo)
def generar_laberinto(n):
    G = nx.grid_2d_graph(n, n)
    edges = list(G.edges())
    random.shuffle(edges)
    maze = nx.Graph()
    maze.add_edges_from(edges[:n * n - 1])
    return maze

n = 5
jugador_pos = (0, 0)
jugador_dest = jugador_pos
laberinto = generar_laberinto(n)
inicio = (0, 0)
salida = (n - 1, n - 1)
tiempo_inicio = time.time()
tiempo_limite = 30
juego_terminado = False
ganaste = False

def setup():
    py5.size(400, 400)
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text_size(20)

def draw():
    global juego_terminado, ganaste
    
    if not juego_terminado:
        py5.background(255)
        dibujar_laberinto(laberinto)
        dibujar_jugador(jugador_pos)
        marcar_salida(salida)
        
        tiempo_actual = time.time()
        tiempo_restante = max(0, tiempo_limite - int(tiempo_actual - tiempo_inicio))
        
        py5.fill(0)
        py5.text(f"Tiempo restante: {tiempo_restante} s", 200, 30)
        
        if jugador_dest == salida:
            juego_terminado = True
            ganaste = True
        
        if tiempo_restante == 0 and not ganaste:
            juego_terminado = True
    
    if juego_terminado:
        py5.background(255)
        py5.fill(0)
        if ganaste:
            py5.text("Ganaste", 200, 200)
        else:
            py5.text("Perdiste", 200, 200)

def dibujar_laberinto(grafo):
    py5.stroke(0)
    py5.stroke_weight(3)
    for (nodo1, nodo2) in grafo.edges():
        x1, y1 = nodo1
        x2, y2 = nodo2
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

def dibujar_jugador(pos):
    global jugador_pos
    x_actual, y_actual = jugador_pos
    x_dest, y_dest = jugador_dest
    jugador_pos = (
        x_actual + (x_dest - x_actual) * 0.2,
        y_actual + (y_dest - y_actual) * 0.2
    )
    
    x, y = jugador_pos
    py5.fill(0, 0, 255)
    py5.no_stroke()
    py5.ellipse(x * 80 + 40, y * 80 + 40, 20, 20)

def marcar_salida(pos):
    x, y = pos
    py5.fill(255, 0, 0)  
    py5.rect(x * 80 + 30, y * 80 + 30, 20, 20)

def mostrar_solucion():
    py5.stroke(255, 0, 0)
    camino = nx.shortest_path(laberinto, source=inicio, target=salida, method='bfs')
    for i in range(len(camino) - 1):
        x1, y1 = camino[i]
        x2, y2 = camino[i + 1]
        py5.line(x1 * 80 + 40, y1 * 80 + 40, x2 * 80 + 40, y2 * 80 + 40)

def key_pressed():
    global jugador_dest
    x, y = jugador_dest
    if py5.key == py5.CODED:
        if py5.key_code == py5.UP and (x, y - 1) in laberinto.neighbors((x, y)):
            jugador_dest = (x, y - 1)
        elif py5.key_code == py5.DOWN and (x, y + 1) in laberinto.neighbors((x, y)):
            jugador_dest = (x, y + 1)
        elif py5.key_code == py5.LEFT and (x - 1, y) in laberinto.neighbors((x, y)):
            jugador_dest = (x - 1, y)
        elif py5.key_code == py5.RIGHT and (x + 1, y) in laberinto.neighbors((x, y)):
            jugador_dest = (x + 1, y)

py5.run_sketch()
