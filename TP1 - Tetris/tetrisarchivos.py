import gamelib
import os
import ast
        

def leer_controles(archivo):
    """
    Lee el archivo para establecer los controles del juego.
    PRECONDICIÓN: Las teclas elegidas como controles deben estar escritas como 'tecla = FUNCIÓN'.
    """
    try:
        with open(archivo, 'r') as archivo:
            lineas = archivo.readlines()
            TECLAS = tuple(map(lambda x: tuple(x.rstrip().split(' = ')), lineas))
    except Exception:
        raise Exception(f'El archivo {archivo} no existe, no hay constroles disponibles. El juego no puede comenzar.') from None
    
    if not TECLAS:
        raise Exception('El archivo está vacio.')

    return TECLAS

def leer_piezas(archivo):
    """
    Lee el archivo que contiene las piezas con sus respectivas rotaciones.
    """

    try:
        archivo_de_piezas = open(archivo, 'r')
        lineas = archivo_de_piezas.readlines()
        PIEZA_COMPLETA = tuple(map(lambda x: tuple(map(lambda y: tuple(map(lambda z: (int(z.split(',')[0]),int(z.split(',')[1])) ,[y][0].split(';') )), x.split(' #')[0].split(' ') )), lineas))
        archivo_de_piezas.close()
        return PIEZA_COMPLETA
    except:
        raise Exception(f'No existe el archivo {archivo}, por lo tanto el juego no puede iniciar') from None

def leer_puntajes(ruta, puntaje):
    """
    Lee los puntajes, escribe el record, en un archivo existente o generado (caso contrario) con el nombre 'puntajes',
    devuelve un array con todos los puntajes existentes junto con un booleano que indica si un puntaje debe ser sobreescrito.
    """
    cambio = False
    try:
        archivo = open(ruta, 'r')
    except Exception:
        archivo = open(ruta, 'w+')
   
    lineas = archivo.readlines()
    puntajes_enteros = []

    for linea in lineas:
        if linea:
                puntajes_enteros.append([linea.split(' = ')[0], int(linea.split(' = ')[1])])
    puntajes = list(map(lambda x: x[1], puntajes_enteros))

    if len(puntajes_enteros) < 10:
        jugador = gamelib.input('Nuevo record, indique su apodo: ')
    elif puntaje > min(puntajes) and len(puntajes_enteros) >= 10:
        jugador = gamelib.input('Usted está entre los mejores 10, indique su apodo: ')
        cambio = True
    if 'jugador' in locals():
        while jugador == None:
            jugador = gamelib.input('Debe inidicar un apodo:')
        puntajes_enteros.append([jugador, puntaje])
    archivo.close()

    return puntajes_enteros, cambio


def cargar_puntajes(ruta, puntaje):
    """
    Abre el archivo, lo reescribe teniendo en cuenta el nuevo puntaje en orden ascendente.
    """
    puntajes_enteros, cambio = leer_puntajes(ruta, puntaje)

    if puntajes_enteros:
        puntajes_enteros_ordenados = sorted(puntajes_enteros, key=lambda x: x[1])[::-1]
    puntajes = list(map(lambda x: x[1], puntajes_enteros_ordenados))

    posicion_del_min = puntajes.index(min(puntajes))
    puntaje_a_eliminar = puntajes_enteros_ordenados[posicion_del_min]

    archivo_para_modificar = open(ruta, 'w')
    for i in range(len(puntajes_enteros)):
        if len(puntajes_enteros_ordenados) >= 10 and puntajes_enteros_ordenados[i] != puntaje_a_eliminar and cambio:
            archivo_para_modificar.write(puntajes_enteros_ordenados[i][0]+' = '+str(puntajes_enteros_ordenados[i][1])+'\n')
        elif len(puntajes_enteros_ordenados) < 10 or not cambio:
            archivo_para_modificar.write(puntajes_enteros_ordenados[i][0]+' = '+str(puntajes_enteros_ordenados[i][1])+'\n')

def dibujar_puntajes(ruta, alto, ancho):
    """
    Escribe los primeros 10 puntajes más altos.
    """
    try:
        archivo = open(ruta, 'r')
    except Exception:
        print(f'No hay archivo llamado {ruta}.')

    margen = alto/6
    lineas = archivo.readlines()
    contador = 0
    for linea in lineas:
        contador += 1
        gamelib.draw_text(str(contador) + '. ' + linea.rstrip(),  3*ancho//4, alto//10*contador/2 + margen, fill='black')


def guardar_juego(juego, ruta):
    """
    Sobreescribe el archivo seleccionado (si no hay, la función lo crea) para guardar el estado de juego en el mismo archivo.
    """
    with open(ruta, 'w') as archivo:
        archivo.write(str(juego))

def cargar_juego(ruta):
    """
    Carga el juego guardado en el archivo que previamente se uso para guardar el estado de juego.
    PRECONDICIÓN: Se debe haber guardado una partida antes.
    """
    try:
        archivo = open(ruta, 'r')
    except Exception:
        print('No hay archivo de juego guardado, guarde una partida para poder utilizar la función.')

    juego_entero = archivo.readlines()
    archivo.close()
    return ast.literal_eval(juego_entero[0])