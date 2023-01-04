import random

ANCHO_JUEGO, ALTO_JUEGO = 50, 25

X, Y = 0, 1

def posiciones_random(juego, cantidad=None):
    """
    Función auxiliar para crear posiciones aleatorias en el tablero teniendo en cuenta
    si se trata de un juego nuevo o si hay obstaculos presentes en el mismo.
    """

    posiciones = []
    if not cantidad:
        cantidad = juego.NIVEL * 5

    while len(posiciones) < cantidad:
        coordenadas = [random.randint(0, ANCHO_JUEGO-1), random.randint(0, ALTO_JUEGO-1)]
        if juego:
            posiciones_ocupadas = juego.OBSTACULOS + juego.ESCOMBROS + juego.POSICION
            if not coordenadas in posiciones_ocupadas: 
                posiciones.append(coordenadas)
        else:
            posiciones.append(coordenadas)

    return posiciones

def crear_partida(cantidad_robots=5, cantidad_obstaculos=10):
    """
    Crea una nueva partida, generando un tablero, el jugador (en el medio del tablero), los
    obstaculos (10 por defecto o según dificultad elegida) y los respectivos robots (5 por defecto o según difultad elegida).
    """

    posicion_jugador_inicial = [ANCHO_JUEGO//2, ALTO_JUEGO//2]

    posiciones_robots_inicial = {
        "comunes": posiciones_random(None, cantidad_robots),
        "rapidos": []
    }

    obstaculos = posiciones_random(None, cantidad_obstaculos)

    escombros = [] #Robots colisionados, comienza vacia

    teletransportacion = 1

    nivel = 1

    juego = chase(ANCHO_JUEGO, ALTO_JUEGO, posicion_jugador_inicial, posiciones_robots_inicial, obstaculos, escombros,
        teletransportacion, nivel)

    return juego

#print(crear_partida())

def encontrar_duplicados(lista):
    """
    Auxiliar de mover_robots.
    Dada una lista devuelve dos listas con los elementos duplicados y los únicos respectivamente.
    """
    no_duplicados = []
    duplicados = []
    for i in lista:
        if not i in no_duplicados:
            no_duplicados.append(i)
        else:
            duplicados.append(i)

    for i in duplicados:
        no_duplicados.remove(i)

    return duplicados, no_duplicados

def posicion_ocupada(punto, juego):
    """
    Función auxiliar de "mover" para conocer si un punto está ocupado tanto como por un escombro como por un obstaculo.
    //True == Ocupada, False == libre
    También devuelve el tipo de objeto que habita el lugar seleccionado.
    """

    if punto in juego.OBSTACULOS:
        return "OBSTACULO"
    elif punto in juego.ESCOMBROS:
        return "ESCOMBRO"

    return "LIBRE"

def sumar_coordenadas(punto, x, y):
    """
    Función auxiliar de "mover", solo suma coordenadas en un punto.
    """
    punto[X] += x
    punto[Y] += y
    return punto


def acercar_al_punto(p1, p2, obstaculos, tipo):
    """
    Función auxiliar de "mover_robots", Esencialmente mueve un punto p1 hacia otro p2.
    Si la coordenada X o Y son iguales, puede que al ser aleatorio (0,1 dependiendo dirección) el robot común no se mueva.
    Los robots no saltan en los obtaculos.
    False si el robot no se debe convertir en chatarra.
    """
    PUNTO_ORIGINAL_X, PUNTO_ORIGINAL_Y = p1[X], p1[Y]

    if tipo == "rapidos": #Robots rapidos se pueden mover en diagonal (Tanto X como Y).
        if p1[X] < p2[X]:
            p1[X] += 1
        elif p1[X] > p2[X]:
            p1[X] -= 1
        if p1[Y] < p2[Y]:
            p1[Y] += 1
        elif p1[Y] > p2[Y]:
            p1[Y] -= 1

    else:
        movimiento = random.randint(0,1) #Con esta variable no hay movimientos diagonales (comunes solo se mueven un casillero en dirección X o Y).

        if movimiento == X: 
            if p1[X] < p2[X]:
                p1[X] += 1
            elif p1[X] > p2[X]:
                p1[X] -= 1
        else:
            if p1[Y] < p2[Y]:
                p1[Y] += 1
            elif p1[Y] > p2[Y]:
                p1[Y] -= 1

    if p1 in obstaculos:
        return [PUNTO_ORIGINAL_X, PUNTO_ORIGINAL_Y], p1

    return p1, False

def juego_terminado(juego):
    """
    Avisa si el juego se terminó (True)
    Si bien el jugador no puede "tirarse" sobre un escombro, al usar TP puede terminar
    en el mismo, una vez allí el juego se considera perdido.
    """

    posiciones_para_perder = juego.ROBOTS["comunes"] + juego.ROBOTS["rapidos"] + juego.ESCOMBROS

    if juego.POSICION in posiciones_para_perder:
        return True

    return False

#Auxiliares para la clase del juego.

def validar_arreglo(dato):
    """Verifica que la variable dada se trate un arreglo."""

    if not isinstance(dato, list):
        raise TypeError("{!r} no es una lista.".format(dato))

    return dato

def validar_int(dato):
    """Verifica que la variable dada se trate de un número entero."""

    if not isinstance(dato, int):
        raise TypeError("{!r} no es un entero.".format(dato))

    return dato

def validar_diccionario(dato):
    """Verifica que la varaible dada se trate de un diccionario."""

    if not isinstance(dato, dict):
        raise TypeError("{!r} no es un diccionario.".format(dato))

    return dato

class chase():
    def __init__(self, ANCHO_JUEGO=50 , ALTO_JUEGO=25, POSICION=[], ROBOTS={}, OBSTACULOS=[], ESCOMBROS=[], TELETRANSPORTACION=1, NIVEL=1):
        self.ANCHO_JUEGO = validar_int(ANCHO_JUEGO)
        self.ALTO_JUEGO = validar_int(ALTO_JUEGO)
        self.POSICION = validar_arreglo(POSICION)
        self.ROBOTS = validar_diccionario(ROBOTS)
        self.OBSTACULOS = validar_arreglo(OBSTACULOS)
        self.ESCOMBROS = validar_arreglo(ESCOMBROS)
        self.TELETRANSPORTACION = TELETRANSPORTACION
        self.NIVEL = validar_int(NIVEL)
        
    def mover_robots(self, juego, tipo):
        """
        Mueve los robots presentes en el juego hacia la posicion actual del jugador y
        genera escombros entre los robots que choquen entre si.
        Si un robot colisiona contra la chatarra, este se convierte en una.
        """

        if tipo == "todos":
            self.mover_robots(self, "comunes")
            tipo = "rapidos"

        colisionados = []

        for i in self.ROBOTS[tipo]:
            i, colisionado = acercar_al_punto(i, self.POSICION, self.OBSTACULOS, tipo)
            if colisionado:
                colisionados.append([i, colisionado])
            if i in self.ESCOMBROS:
                self.ROBOTS[tipo].remove(i)

        nuevos_escombros, self.ROBOTS[tipo] = encontrar_duplicados(self.ROBOTS[tipo]) #Veo si robots del mismo tipo se chocan.

        mas_escombros = encontrar_duplicados(self.ROBOTS["comunes"]+self.ROBOTS["rapidos"])[0] #Veo si robots de distinto tipo se chocan.
        
        for i in nuevos_escombros:
            self.ESCOMBROS.append(i)

        for i in colisionados:
            self.ROBOTS[tipo].remove(i[1]) #No uso X e Y, porque no son vectores, sino posiciones en un array de longitud 1.
            self.ESCOMBROS.append(i[0])

        for i in mas_escombros:
            self.ESCOMBROS.append(i)
            self.ROBOTS["comunes"].remove(i)
            self.ROBOTS["rapidos"].remove(i)


        return self
    
    def subir_nivel(self):
        """
        Cuando todos los robots son eliminados, se agregan mas robots,
        se agregan una oportunidad más para usar teletransportación (son acumulables) y
        se suma un nivel más.
        """

        self.TELETRANSPORTACION += 1
        self.NIVEL += 1

        self.ROBOTS["comunes"] = posiciones_random(self)

        if self.NIVEL % 3 == 0:
            self.ROBOTS["rapidos"] += posiciones_random(self, self.NIVEL//3)

        return True
    
    def mover(self, x, y): #Ver si es necesario pasar todo el juego o solo los tipos de obstaculos
        """
        Mueve el jugador según las coordenadas dadas.
        Si hay un escombro presente en el camino del jugador y el mismo no está pegado a
        la un borde del campo se producira un efecto sokoban permitiendo al jugador desplazarse moviendo
        solidariamente el escombro.
        El valor booleano determina si llamo a la funcion "mover robots"
        """

        if juego_terminado(self):
            return self.POSICION, self.ESCOMBROS

        posicion = sumar_coordenadas(self.POSICION, x, y)

        if not 0 <= posicion[X] < ANCHO_JUEGO or not 0 <= posicion[Y] < ALTO_JUEGO:
            posicion_original = sumar_coordenadas(posicion, -x, -y)
            return [posicion_original, self.ESCOMBROS] #No hacer nada

        futura_posicion = posicion_ocupada([posicion[X], posicion[Y]], self)

        if futura_posicion == "OBSTACULO":
            posicion_original = sumar_coordenadas(posicion, -x, -y)
            return [posicion_original, self.ESCOMBROS] #No muevo nada, un obstaculo no se mueve

        elif futura_posicion == "ESCOMBRO":
            escombro_por_mover = self.ESCOMBROS[self.ESCOMBROS.index(posicion)]
            escombro_movido = sumar_coordenadas(escombro_por_mover, x, y)
            duplicados, unicos = encontrar_duplicados(self.ESCOMBROS)
            if not 0 <= escombro_movido[X] < ANCHO_JUEGO or not 0 <= escombro_movido[Y] < ALTO_JUEGO or duplicados or escombro_movido in self.OBSTACULOS:
                sumar_coordenadas(escombro_movido, -x, -y) #Revierto la operación
                posicion_original = sumar_coordenadas(posicion, -x, -y)
                return [posicion_original, self.ESCOMBROS]
            self.mover_robots(self, "todos")
            return [posicion, self.ESCOMBROS]

        self.mover_robots(self, "todos")
        return [posicion, self.ESCOMBROS, True]

    def teletransportarse(self):
        """
        Teletransporta al jugado a una posicion random.
        Si el juego terminó, no se puede usar tp.
        """
        if not self.TELETRANSPORTACION or juego_terminado(self):
            return self.POSICION

        posiciones_ocupadas = self.POSICION + self.OBSTACULOS

        self.TELETRANSPORTACION -= 1
        self.POSICION = [random.randint(0,ANCHO_JUEGO-1), random.randint(0,ALTO_JUEGO-1)]
        self.mover_robots(self, "todos")

        while self.POSICION in posiciones_ocupadas:
            self.POSICION = [random.randint(0,ANCHO_JUEGO-1), random.randint(0,ALTO_JUEGO-1)]
        
        return self.POSICION