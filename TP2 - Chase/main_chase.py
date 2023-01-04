import gamelib
import chase_logic
import chase_archivos

ANCHO_VENTANA, ALTO_VENTANA = 1200, 640

PIEZA_VENTANA_X, PIEZA_VENTANA_Y = ANCHO_VENTANA//chase_logic.ANCHO_JUEGO, (ALTO_VENTANA-40)//chase_logic.ALTO_JUEGO

X, Y = chase_logic.X, chase_logic.Y

CONTROLES = chase_archivos.leer_controles('controles.txt')

ARRIBA, DIAGONA_SUP_IZQ, IZQUIERDA, DIAGONA_INF_IQZ, ABAJO, DIAGONAL_INF_DER, DERECHA, DIAGONAL_SUP_DER, TP, REINCIO = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9

#Funciones para graficar la posición del juegador, los obstaculos y los escombros escombros generados durante el juego.

def graficar_jugador(posicion):
    gamelib.draw_image("./jugador.gif", PIEZA_VENTANA_X*posicion[X], PIEZA_VENTANA_Y*posicion[Y]+40)

def graficar_robots_comunes(robots):
    for robot in robots:
        gamelib.draw_image("./comun.gif", PIEZA_VENTANA_X*robot[X], PIEZA_VENTANA_Y*robot[Y]+40)

def graficar_robots_rapidos(robots):
    for robot in robots:
        gamelib.draw_image("./rapido.gif", PIEZA_VENTANA_X*robot[X], PIEZA_VENTANA_Y*robot[Y]+40)

def graficar_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        gamelib.draw_image("./obstaculo.gif", PIEZA_VENTANA_X*obstaculo[X], PIEZA_VENTANA_Y*obstaculo[Y]+40)

def graficar_escombros(escombros):
    for escombro in escombros:
        gamelib.draw_image("./escombro.gif", PIEZA_VENTANA_X*escombro[X], PIEZA_VENTANA_Y*escombro[Y]+40)

def graficar_linea():
    gamelib.draw_line(0, 40, ANCHO_VENTANA, 40, fill="White")

def mostrar_estado_juego(juego):
    """
    Muestra en la parte superior de la ventana el nivel, TPs restantes y usos del arma.
    """

    if not chase_logic.juego_terminado(juego):
        gamelib.draw_text(f'Nivel: {juego.NIVEL}    TPs disponibles: {juego.TELETRANSPORTACION}', ANCHO_VENTANA//2, 20, fill='white')
    else:
        gamelib.draw_text(f'¡JUEGO TERMINADO!    Nivel alcanzado: {juego.NIVEL}', ANCHO_VENTANA//2, 20, fill='white')

    return graficar_jugador(juego.POSICION), graficar_obstaculos(juego.OBSTACULOS), graficar_robots_comunes(juego.ROBOTS["comunes"]), graficar_robots_rapidos(juego.ROBOTS["rapidos"]), graficar_escombros(juego.ESCOMBROS), graficar_linea()


def manejar_movimientos(evento, juego):
    """
    Función para manejar eventos según controles asignados previemente en
    un archivo llamado 'controles.txt'.
    """
    
    if evento in CONTROLES[ARRIBA][1]:
        return juego.mover(0, -1)
    elif evento in CONTROLES[DIAGONAL_SUP_DER][1]:
        return juego.mover(1, -1)
    elif evento in CONTROLES[DERECHA][1]:
        return juego.mover(1, 0)
    elif evento in CONTROLES[DIAGONAL_INF_DER][1]:
        return juego.mover(1, 1)
    elif evento in CONTROLES[ABAJO][1]:
        return juego.mover(0, 1)
    elif evento in CONTROLES[DIAGONA_INF_IQZ][1]:
        return juego.mover(-1, 1)
    elif evento in CONTROLES[IZQUIERDA][1]:
        return juego.mover(-1, 0)
    elif evento in CONTROLES[DIAGONA_SUP_IZQ][1]:
        return juego.mover(-1, -1)
    elif evento in CONTROLES[TP][1]:
        return juego.teletransportarse()


def main():
    """
    Función principal, incial el juego, maneja el mismo y le da interfaz gráfica.
    """
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    gamelib.title('Chase: No dejes que te atrapen')
    juego = chase_logic.crear_partida()

    while gamelib.loop(fps=60):

        gamelib.draw_begin()
        mostrar_estado_juego(juego)
        gamelib.draw_end()
        
        for event in gamelib.get_events():

            if event.type == gamelib.EventType.KeyPress:
                manejar_movimientos(event.key, juego) #Maneja todos los eventos (menos el reinicio del juego).

                if event.key in CONTROLES[REINCIO][1]:
                    juego = chase_logic.crear_partida()
        
        if not juego.ROBOTS["comunes"]:
            juego.subir_nivel()

#Se incia el juego
gamelib.init(main)