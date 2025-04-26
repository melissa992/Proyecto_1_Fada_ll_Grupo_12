import time
from math import ceil
from copy import deepcopy

# ---------------- FUNCIONES PARA PROCESAR LOS DATOS ---------------- #

def inicializar_grupo(numAgentes, opinion1, opinion2, rigidez):
    return {'numAgentes': numAgentes, 'opinion1': opinion1, 'opinion2': opinion2, 'rigidez': rigidez}

def conflictoInterno(grupos):
    n = len(grupos)
    return sum((grupo['numAgentes'] * (grupo['opinion1'] - grupo['opinion2']) ** 2) / n for grupo in grupos)

def esfuerzo(grupos, tratamiento):
    return sum(ceil(abs(grupo['opinion1'] - grupo['opinion2']) * grupo['rigidez'] * t) for grupo, t in zip(grupos, tratamiento))

# ---------------- ALGORITMO ---------------- #
def modciPD(grupos, valorDisponible):
    n = len(grupos)
    E_max = valorDisponible
    dp = [float('inf')] * (E_max + 1)
    path = [None] * (E_max + 1)

    # Estado base: Esfuerzo 0 → Conflicto inicial
    conflicto_inicial = conflictoInterno(grupos)
    dp[0] = conflicto_inicial
    path[0] = [0] * n

    # Uso de programación dinámica
    for i, grupo in enumerate(grupos):
        for e in range(E_max, -1, -1):
            if dp[e] != float('inf'):
                for k in range(1, grupo['numAgentes'] + 1):
                    costo = ceil(abs(grupo['opinion1'] - grupo['opinion2']) * grupo['rigidez'] * k)
                    nuevo_e = e + costo
                    if nuevo_e <= E_max:
                        reduccion = ((grupo['opinion1'] - grupo['opinion2']) ** 2 * k) / n
                        nuevo_conflicto = dp[e] - reduccion
                        if nuevo_conflicto < dp[nuevo_e]:
                            dp[nuevo_e] = nuevo_conflicto
                            nueva_path = deepcopy(path[e])
                            nueva_path[i] += k
                            path[nuevo_e] = nueva_path

    mejor_e = min(range(E_max + 1), key=lambda e: dp[e] if path[e] is not None else float('inf'))
    mejor_estrategia = path[mejor_e] if path[mejor_e] is not None else [0] * n
    mejor_conflicto = dp[mejor_e]

    return mejor_estrategia, mejor_conflicto, mejor_e

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
    estrategia, conflicto, esfuerzo = modciPD(grupos, valor_disponible)
    tiempo_final = time.time()
    tiempo_total = tiempo_final - tiempo_inicial

    # Mostrar resultados
    print(f"""
    ➤ Algoritmo: Programación Dinámica
       Estrategia: {estrategia}
       Conflicto: {conflicto}
       Esfuerzo: {esfuerzo}
       Tiempo total: {tiempo_total:.4f} segundos
    """)