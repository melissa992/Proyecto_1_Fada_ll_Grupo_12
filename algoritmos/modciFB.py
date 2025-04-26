import time
from math import ceil
from copy import deepcopy
from itertools import product

# ---------------- FUNCIONES PARA PROCESAR LOS DATOS ---------------- #

def inicializar_grupo(numAgentes, opinion1, opinion2, rigidez):
    return {'numAgentes': numAgentes, 'opinion1': opinion1, 'opinion2': opinion2, 'rigidez': rigidez}

def conflictoInterno(grupos):
    n = len(grupos)
    return sum((grupo['numAgentes'] * (grupo['opinion1'] - grupo['opinion2']) ** 2) / n for grupo in grupos)

def esfuerzo(grupos, tratamiento):
    return sum(ceil(abs(grupo['opinion1'] - grupo['opinion2']) * grupo['rigidez'] * t) for grupo, t in zip(grupos, tratamiento))

# ---------------- ALGORITMOS ---------------- #
def modciFB(grupos, valorDisponible):
    n = len(grupos)
    conflicto_inicial = conflictoInterno(grupos)
    mejor_conflicto = conflicto_inicial
    mejor_estrategia = [0] * n
    mejor_esfuerzo = 0

    posibles_tratamientos = [range(0, grupo['numAgentes'] + 1) for grupo in grupos]

    for tratamiento in product(*posibles_tratamientos):  
        esfuerzo_actual = esfuerzo(grupos, tratamiento)
        if esfuerzo_actual <= valorDisponible:
            conflicto_actual = conflicto_inicial - sum(
                ((grupo['opinion1'] - grupo['opinion2']) ** 2 * k) / n for grupo, k in zip(grupos, tratamiento)
            )
            if conflicto_actual < mejor_conflicto:
                mejor_conflicto = conflicto_actual
                mejor_estrategia = tratamiento
                mejor_esfuerzo = esfuerzo_actual

    return mejor_estrategia, mejor_conflicto, mejor_esfuerzo

def cargar_archivo_entrada(ruta_archivo):
    grupos = []
    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()

        num_grupos = int(lineas[0].strip())
        valor_disponible = int(lineas[-1].strip())

        for i in range(1, 1 + num_grupos):
            datos = lineas[i].strip().split(',')
            grupo = inicializar_grupo(int(datos[0]), int(datos[1]), int(datos[2]), float(datos[3]))
            grupos.append(grupo)

        return grupos, valor_disponible
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return [], 0

# ---------------- EJECUCIÓN ---------------- #
if __name__ == "__main__":
    archivo_entrada = input("Ingrese la ruta del archivo de entrada: ")

    # Cargar los datos del archivo
    grupos, valor_disponible = cargar_archivo_entrada(archivo_entrada)
    if not grupos:
        print("No se pudieron cargar los datos del archivo.")
        exit()

    print(f"Datos cargados correctamente:\nGrupos: {grupos}\nValor disponible: {valor_disponible}")

    # Ejecutar el algoritmo
    tiempo_inicial = time.time()
    estrategia, conflicto, esfuerzo = modciFB(grupos, valor_disponible)
    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial

    # Mostrar resultados
    print(f"""
    ➤ Algoritmo: Fuerza Bruta
       Estrategia: {estrategia}
       Conflicto: {conflicto}
       Esfuerzo: {esfuerzo}
       Tiempo total: {tiempo_total:.4f} segundos
    """)