def leer_controles(archivo_ruta):
    """
    Recibe un archivo con la configuración de los controles, y devuelve una tupla con el tipo
    de acción y las teclas que la inician.
    """
    try:
        with open(archivo_ruta, 'r') as archivo:
            linea = archivo.readlines()
            TECLAS = tuple(map(lambda x: tuple(x.rstrip().split('=')), linea))
    except Exception:
        raise Exception(f"El archivo {archivo_ruta} no existe. El juego no puede comenzar") from None

    if not TECLAS:
        raise Exception(f"El archivo {archivo_ruta} se encuentra vacio, no hay controles disponibles.")

    return TECLAS