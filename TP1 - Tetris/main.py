import gamelib
import random
import tetrisarchivos
import tetris


ESPERA_DESCENDER = 15

COLORES = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D', '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC', '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399','#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933','#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6']

ARRIBA = 0
IZQUIERDA = 1
DERECHA = 2
ABAJO = 3
GUARDAR = 4
CARGAR = 5
SALIR = 7

ALTO_VENTANA = 500
ANCHO_VENTANA = 500
PIEZA_VENTANA = ANCHO_VENTANA/18
PIEZA_PROXIMA = ANCHO_VENTANA/15

TECLAS = tetrisarchivos.leer_controles('teclas.txt')

def dibujar_grilla():
    gamelib.draw_line(ANCHO_VENTANA/2, 0, ANCHO_VENTANA/2, ALTO_VENTANA, fill='black', width=1)

def dibujar_pieza(pieza, superficie_consolidada, color):
    for i in range(len(pieza)):
            gamelib.draw_rectangle(PIEZA_VENTANA*pieza[i][0], PIEZA_VENTANA*(pieza[i][1]), PIEZA_VENTANA*(pieza[i][0]+1), PIEZA_VENTANA*(pieza[i][1]+1), fill=COLORES[color])

    for i in range(len(superficie_consolidada)):
        gamelib.draw_rectangle(PIEZA_VENTANA*(superficie_consolidada[i][0]), PIEZA_VENTANA*(superficie_consolidada[i][1]), PIEZA_VENTANA*(superficie_consolidada[i][0]+1), PIEZA_VENTANA*(superficie_consolidada[i][1]+1), fill='darkgray')

def dibujar_pieza_proxima(pieza):
    for i in range(len(pieza)):
            gamelib.draw_rectangle(PIEZA_PROXIMA*pieza[i][0]+(3*ANCHO_VENTANA/4.7), PIEZA_PROXIMA*(pieza[i][1])+ALTO_VENTANA/5, PIEZA_PROXIMA*(pieza[i][0]+1)+(3*ANCHO_VENTANA/4.7), PIEZA_PROXIMA*(pieza[i][1]+1)+ALTO_VENTANA/5, fill='gray')

def cambiar_pieza():
    #Solo crea una nueva pieza aleatoria
    return tetris.generar_pieza(pieza=None)




def main():
    # Inicializar el estado del juego

    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    timer_bajar = ESPERA_DESCENDER
    juego = tetris.crear_juego(tetris.generar_pieza(pieza=None))
    proxima = cambiar_pieza()
    color_selecionado = random.randint(0, len(COLORES)-1)

    rotacion = 0 #Sirve para saber en que posicion comienza a caer la primer pieza
    evaluado = False #Veo si ya revisé los puntajes

    while gamelib.loop(fps=30):

        gamelib.draw_begin()
        gamelib.draw_end()
        dibujar_grilla()
        terminado = f'SCORE: {juego[tetris.PUNTAJE]}'
        interrumpir = False
        
        for event in gamelib.get_events():
           
            if not event:
                break

            if event.type == gamelib.EventType.KeyPress:
                tecla = event.key
                
                if tecla == TECLAS[SALIR][0]:
                    interrumpir = True
                elif tecla == TECLAS[DERECHA][0]:
                    tetris.mover(juego, tetris.DERECHA)
                elif tecla == TECLAS[IZQUIERDA][0]:
                    tetris.mover(juego, tetris.IZQUIERDA)
                elif tecla == TECLAS[ABAJO][0]:
                    juego, bool = tetris.avanzar(juego, proxima)
                    if bool:
                        proxima = cambiar_pieza() #Genera otra pieza aleatoria si se toca la superficie consolidada
                elif tecla == TECLAS[ARRIBA][0]:

                    if rotacion + 1 == 4:
                        rotacion = 0
                        juego[1] = tetris.rotar(juego[tetris.PIEZA], juego[tetris.ALTERNATIVAS], rotacion)
                    else:
                        rotacion += 1
                        juego[1] = tetris.rotar(juego[tetris.PIEZA], juego[tetris.ALTERNATIVAS], rotacion)

                elif tecla == TECLAS[GUARDAR][0]:
                    tetrisarchivos.guardar_juego(juego, 'juego_guardado.txt')
                elif tecla == TECLAS[CARGAR][0]:
                    juego = tetrisarchivos.cargar_juego('juego_guardado.txt')

        if interrumpir:
            break
        
        dibujar_pieza(juego[tetris.PIEZA], juego[tetris.SUP_CONSOLIDADA], color_selecionado)
        
        if not evaluado:
            dibujar_pieza_proxima(proxima[0])
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER
            juego, bool = tetris.avanzar(juego, proxima)
            
            if bool:
                proxima = cambiar_pieza()
                color_selecionado = random.randint(0, len(COLORES)-1)
                rotacion = 0

        if tetris.terminado(juego) and not evaluado:
            tetrisarchivos.cargar_puntajes('puntajes.txt', juego[tetris.PUNTAJE])
            evaluado = True

        if tetris.terminado(juego):
            terminado = f'JUEGO TERMINADO!\nPUNTAJE FINAL: {juego[tetris.PUNTAJE]}'
            gamelib.draw_text('LOS MEJORES 10', 3*ANCHO_VENTANA/4, ALTO_VENTANA/10, fill='black')
            tetrisarchivos.dibujar_puntajes('puntajes.txt', ALTO_VENTANA, ANCHO_VENTANA)

        gamelib.draw_text(terminado, 3*ANCHO_VENTANA/4, 4*ALTO_VENTANA/5, fill='black')

gamelib.init(main)