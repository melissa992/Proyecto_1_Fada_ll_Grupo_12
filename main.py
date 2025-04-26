import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import matplotlib.pyplot as plt
import numpy as np
from algoritmos.modciFB import modciFB
from algoritmos.modciV import modciV
from algoritmos.modciPD import modciPD
# ---------------- FUNCIONES PARA PROCESAR DATOS ---------------- #
def cargar_archivo_entrada(ruta_archivo):
    """Carga el archivo de entrada y organiza los datos en estructuras dinámicas."""
    grupos = []
    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()
        num_grupos = int(lineas[0].strip())  # Número de agentes
        valor_disponible = int(lineas[-1].strip())  # R_max

        # Leer datos de cada agente
        for i in range(1, num_grupos + 1):
            datos = lineas[i].strip().split(',')
            grupo = {
                'numAgentes': int(datos[0]),
                'opinion1': int(datos[1]),
                'opinion2': int(datos[2]),
                'rigidez': float(datos[3])
            }
            grupos.append(grupo)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    return grupos, valor_disponible

def mostrar_datos_estructurados(grupos, valor_disponible):
    """Muestra los datos estructurados en el área de texto."""
    text_archivo.delete('1.0', tk.END)
    text_archivo.insert(tk.END, f"{len(grupos)} = Número de agentes\n\n")

    for i, grupo in enumerate(grupos, start=1):  # Enumerar desde 1
        text_archivo.insert(
            tk.END,
            f"Agente {i}: {grupo['numAgentes']}, "
            f"op0_0: {grupo['opinion1']}, "
            f"op0_1: {grupo['opinion2']}, "
            f"rig{i-1}: {grupo['rigidez']:.3f}\n"
        )
    text_archivo.insert(tk.END, f"\nR_max: {valor_disponible}\n")

def seleccionar_archivo():
    """Abre un cuadro de diálogo para seleccionar un archivo y muestra los datos."""
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        entrada_var.set(archivo)
        try:
            grupos, valor_disponible = cargar_archivo_entrada(archivo)
            mostrar_datos_estructurados(grupos, valor_disponible)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {str(e)}")

# ---------------- ALGORITMOS SIMULADOS ---------------- #
def modciV(grupos, valor_disponible):
    print("Ejecutando algoritmo Voraz...")
    resultado = sum(grupo['numAgentes'] for grupo in grupos)
    messagebox.showinfo("Resultado Voraz", f"Resultado Voraz: {resultado}")

def modciFB(grupos, valor_disponible):
    print("Ejecutando algoritmo Backtracking...")
    resultado = max(grupo['opinion1'] for grupo in grupos)
    messagebox.showinfo("Resultado Backtracking", f"Resultado Backtracking: {resultado}")

def modciPD(grupos, valor_disponible):
    print("Ejecutando algoritmo Programación Dinámica...")
    resultado = min(grupo['rigidez'] for grupo in grupos)
    messagebox.showinfo("Resultado Programación Dinámica", f"Resultado Programación Dinámica: {resultado}")

# ---------------- FUNCION PRINCIPAL DE GRAFICAR ---------------- #
def graficar_datos():
    """Genera un gráfico y ejecuta el algoritmo seleccionado."""
    archivo_entrada = entrada_var.get()
    algoritmo = algoritmo_var.get()

    if not archivo_entrada:
        messagebox.showerror("Error", "Debe seleccionar un archivo de entrada para graficar.")
        return
    if not algoritmo:
        messagebox.showerror("Error", "Debe seleccionar un algoritmo.")
        return

    try:
        grupos, valor_disponible = cargar_archivo_entrada(archivo_entrada)

        # Ejecutar el algoritmo seleccionado
        if algoritmo == "Voraz":
            modciV(grupos, valor_disponible)
        elif algoritmo == "Fuerza Bruta":
            modciFB(grupos, valor_disponible)
        elif algoritmo == "Programación Dinámica":
            modciPD(grupos, valor_disponible)
        else:
            print("Algoritmo no implementado.")

        # --- GRÁFICA ---
        agentes = [f"Agente {i+1}" for i in range(len(grupos))]
        opinion1 = [grupo['opinion1'] for grupo in grupos]
        opinion2 = [grupo['opinion2'] for grupo in grupos]
        rigideces = [grupo['rigidez'] for grupo in grupos]

        x = np.arange(len(agentes))
        width = 0.2

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(x - width, opinion1, width, label="Opinión 1", color="blue")
        ax.bar(x, opinion2, width, label="Opinión 2", color="green")
        ax.bar(x + width, rigideces, width, label="Rigidez", color="orange")

        ax.set_xlabel("Agentes")
        ax.set_ylabel("Valores")
        ax.set_title("Opiniones y Rigidez por Agente")
        ax.set_xticks(x)
        ax.set_xticklabels(agentes)
        ax.legend()

        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")

# ---------------- INTERFAZ GRÁFICA ---------------- #
root = tk.Tk()
root.title("Simulación de Algoritmos")
root.geometry("1000x600")
root.configure(bg="#f5f5f5")

entrada_var = tk.StringVar()
algoritmo_var = tk.StringVar()

# Configuración de los frames
frame_izquierda = tk.Frame(root, bg="#f5f5f5", width=300)
frame_izquierda.pack(side="left", fill="y")

frame_derecha = tk.Frame(root, bg="#ffffff", width=700)
frame_derecha.pack(side="right", fill="both", expand=True)

# Controles en la izquierda
tk.Label(frame_izquierda, text="Cargar Archivo:", font=("Arial", 12), bg="#f5f5f5").pack(pady=10)
tk.Entry(frame_izquierda, textvariable=entrada_var, width=30).pack(pady=5)
tk.Button(frame_izquierda, text="Examinar", command=seleccionar_archivo, bg="#b3d9ff", font=("Arial", 10)).pack(pady=5)

# Selector de algoritmo
tk.Label(frame_izquierda, text="Seleccionar Algoritmo:", font=("Arial", 12), bg="#f5f5f5").pack(pady=10)
combo_algoritmos = ttk.Combobox(frame_izquierda, textvariable=algoritmo_var, font=("Arial", 10))
combo_algoritmos['values'] = ("Voraz", "Backtracking", "Programación Dinámica")
combo_algoritmos.pack(pady=5)

# Botones
tk.Button(frame_izquierda, text="Graficar Datos", command=graficar_datos, bg="#ffd700", font=("Arial", 12)).pack(pady=20)
tk.Button(frame_izquierda, text="Salir", command=root.quit, bg="#ffb3b3", font=("Arial", 12)).pack(pady=20)

# Área de texto para mostrar datos estructurados
tk.Label(frame_derecha, text="Contenido del Archivo:", font=("Arial", 12), bg="#ffffff").pack(pady=10)
frame_archivo = tk.Frame(frame_derecha, bg="#ffffff")
frame_archivo.pack(fill="both", expand=True)

scrollbar_archivo = tk.Scrollbar(frame_archivo)
scrollbar_archivo.pack(side="right", fill="y")

text_archivo = tk.Text(frame_archivo, wrap="none", yscrollcommand=scrollbar_archivo.set, height=10, font=("Courier", 10))
text_archivo.pack(fill="both", expand=True)
scrollbar_archivo.config(command=text_archivo.yview)

# Iniciar la interfaz
root.mainloop()
