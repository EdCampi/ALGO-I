import tetrisarchivos
import random
import ast

ANCHO_JUEGO, ALTO_JUEGO = 9, 18

IZQUIERDA, DERECHA = -1, 1

CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

GRILLA = 0
PIEZA = 1
SUP_CONSOLIDADA = 2
ALTERNATIVAS = 3
PUNTAJE = 4

X, Y = 0, 1

PIEZA_COMPLETA = tetrisarchivos.leer_piezas('piezas.txt')

def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    pieza_aleatoria = PIEZA_COMPLETA[random.randint(0, 6)]
    pieza_de_inicio = pieza_aleatoria[0]
    return [pieza_de_inicio, pieza_aleatoria]


def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """

    pieza_movida = list(map(lambda x: list(x), pieza))
    pieza_extremo_izquierdo = min(list(map(lambda x: x[0], pieza)))
    pieza_extremo_derecho = max(list(map(lambda x: x[0], pieza)))

    if pieza_extremo_derecho < ANCHO_JUEGO and (pieza_extremo_izquierdo + dx) >= 0:
        for i in range(len(pieza)):
            pieza_movida[i][X] += dx
            pieza_movida[i][Y] += dy

    pieza_reposicionada = (map(lambda x: tuple(x), pieza_movida))

    return tuple(pieza_reposicionada)


def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """

    matriz = []

    for i in range(ANCHO_JUEGO):
        for j in range(ALTO_JUEGO):
            matriz.append((i,j))
    
    pieza = trasladar_pieza(pieza_inicial[0], ANCHO_JUEGO//2, 0)
    alternativas = pieza_inicial[1]

    superficie_consolidada = []
    puntaje = 0

    juego = [tuple(matriz), pieza, superficie_consolidada, alternativas, puntaje]

    return juego


def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """

    dimensiones = (juego[GRILLA][-1][X] + 1,juego[GRILLA][-1][Y] + 1)

    return dimensiones


def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """

    return juego[PIEZA]

def rotar(pieza, alternativas_1, n):
    #Rota la pieza.

    mas_bajos = sorted(pieza)[0]
    pieza_alternativa = alternativas_1[n]
    pieza_final = tuple(map(lambda x: (x[0]+mas_bajos[X], x[1]+mas_bajos[Y]), sorted(pieza_alternativa)))

    if sorted(pieza_final)[-1][X] < ANCHO_JUEGO: 
        return pieza_final
    
    return pieza

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
     
    for i in range(len(juego[SUP_CONSOLIDADA])):
            if x == juego[SUP_CONSOLIDADA][i][X] and y == juego[SUP_CONSOLIDADA][i][Y]:
                return True

    return False


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """

    pieza_hacia_derecha = trasladar_pieza(juego[PIEZA], IZQUIERDA, 0)
    pieza_hacia_izquierda = trasladar_pieza(juego[PIEZA], DERECHA, 0)
    pieza_extremo_derecho = max(list(map(lambda x: x[0], juego[PIEZA])))

    if direccion == DERECHA and pieza_extremo_derecho < ANCHO_JUEGO - 1 and not any(list(map(lambda x: hay_superficie(juego,x[X], x[Y]), pieza_hacia_izquierda))):
        juego[PIEZA] = pieza_hacia_izquierda
    elif direccion == IZQUIERDA and not any(list(map(lambda x: hay_superficie(juego,x[X], x[Y]), pieza_hacia_derecha))):
        juego[PIEZA] = pieza_hacia_derecha

    return juego


def puntajes(filas_eliminadas):
    """
    Calcula los puntos obtenido en funcion de la cantidad de líneas eliminadas.
    """
    if len(filas_eliminadas) == 1:
        puntos = 50
    elif len(filas_eliminadas) == 2:
        puntos = 150
    elif len(filas_eliminadas) == 3:
        puntos = 350
    else:
        puntos = 750
    return puntos

def elimina_lineas(juego):
    """
    Elimina las filas llenas, mueve la parte de arriba de lo que se eliminó uno o más bloques hacia abajo
    y devuelve a su vez el puntaje obtenido.
    """
    puntos_obtenidos = 0

    filas_eliminar = [i for i in range(ALTO_JUEGO)]
    for i in range(ALTO_JUEGO):
        for j in range(ANCHO_JUEGO):
            if not (j, i) in juego:
                filas_eliminar.remove(i)
                break

    cantidad_bajar = len(filas_eliminar)
    superficie_consolidada = list(map(lambda x: x, filter(lambda x: not x[Y] in filas_eliminar, juego)))
        
    if filas_eliminar:
        superior = list(map(lambda x: (x[X], x[Y] + cantidad_bajar), filter(lambda x: x[Y] < min(filas_eliminar), superficie_consolidada)))
        inferior = list(filter(lambda x: x[Y] > max(filas_eliminar), superficie_consolidada))

        superficie_final = inferior + superior
        puntos_obtenidos = puntajes(filas_eliminar)
        return (superficie_final, puntos_obtenidos)

    return (superficie_consolidada, puntos_obtenidos)


def consolidador_de_superficies(superficie, pieza):
    """
    Solamente mete en una lista las posiciones a consolidar.
    """
    for i in range(len(pieza)):
        superficie.append(pieza[i])
    superficie, puntaje = elimina_lineas(superficie)
    
    return superficie, puntaje


def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """

    pieza_avanzada = trasladar_pieza(juego[PIEZA], 0, 1)
    pieza_nueva = trasladar_pieza(siguiente_pieza[0], dimensiones(juego)[X]//2, 0)
    pieza_mas_baja = max(list(map(lambda x: x[1], juego[PIEZA])))

    if terminado(juego):
        return ([juego[GRILLA], juego[PIEZA], juego[SUP_CONSOLIDADA], juego[ALTERNATIVAS], juego[PUNTAJE]], False)
        
    if not juego[SUP_CONSOLIDADA]:
        if pieza_mas_baja < ALTO_JUEGO-1:
            return ([juego[GRILLA], pieza_avanzada, juego[SUP_CONSOLIDADA], juego[ALTERNATIVAS], juego[PUNTAJE]], False)

        superficie_a_consolidar, puntaje_obtenido = consolidador_de_superficies([], juego[PIEZA])
        return ([juego[GRILLA], pieza_nueva, superficie_a_consolidar, siguiente_pieza[1], puntaje_obtenido+juego[PUNTAJE]], True)
        
    pieza_sombra = trasladar_pieza(juego[PIEZA], 0, 1)

    if not pieza_mas_baja < ALTO_JUEGO-1 or any(x in juego[SUP_CONSOLIDADA] for x in pieza_sombra):
        juego[SUP_CONSOLIDADA], puntaje_obtenido = consolidador_de_superficies(juego[SUP_CONSOLIDADA], juego[PIEZA])
        return ([juego[GRILLA], pieza_nueva, juego[SUP_CONSOLIDADA], siguiente_pieza[1], puntaje_obtenido+juego[PUNTAJE]], True)
                
    return ([juego[GRILLA], pieza_avanzada, juego[SUP_CONSOLIDADA], juego[ALTERNATIVAS], juego[PUNTAJE]], False)

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    
    mitad_grilla = dimensiones(juego)[0]//2
    primeros_4_lugares = [(mitad_grilla, 3), (mitad_grilla, 2), (mitad_grilla, 1), (mitad_grilla, 0)]

    if any(x in juego[SUP_CONSOLIDADA] for x in primeros_4_lugares):
        return True
    
    return False

