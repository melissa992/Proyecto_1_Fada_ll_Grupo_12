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

# ---------------- ALGORITMO VORAZ ---------------- #
def modciV(grupos, valorDisponible):  # Renombrada para evitar conflictos
    esfuerzo_disponible = valorDisponible
    estrategia = [0] * len(grupos)

    grupos_ordenados = sorted(grupos, key=lambda g: abs(g['opinion1'] - g['opinion2']) * g['rigidez'], reverse=True)

    for grupo in grupos_ordenados:
        for k in range(1, grupo['numAgentes'] + 1):
            costo = ceil(abs(grupo['opinion1'] - grupo['opinion2']) * grupo['rigidez'] * k)
            if esfuerzo_disponible >= costo:
                esfuerzo_disponible -= costo
                estrategia[grupos.index(grupo)] += k
            else:
                break

    conflicto_final = conflictoInterno(grupos)
    return estrategia, conflicto_final, valorDisponible - esfuerzo_disponible

# ---------------- FUNCIONES PARA CARGAR DATOS ---------------- #

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
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
    return grupos, valor_disponible

# ---------------- EJECUCIÓN ---------------- #

if __name__ == "__main__":
    archivo_entrada = "entrada.txt"  # Cambia por tu archivo de entrada
    grupos, valor_disponible = cargar_archivo_entrada(archivo_entrada)

    tiempo_inicial = time.time()
    estrategia_greedy, conflicto_greedy, esfuerzo_greedy = modciV(grupos, valor_disponible)
    tiempo_final = time.time()

    tiempo_total = tiempo_final - tiempo_inicial

    # Mostrar resultados
    print(f"""
       Programación Voraz
       Estrategia: {estrategia_greedy}
       Conflicto: {conflicto_greedy}
       Esfuerzo: {esfuerzo_greedy}

    ⏱️ Tiempo total: {tiempo_total:.4f} segundos
    """)