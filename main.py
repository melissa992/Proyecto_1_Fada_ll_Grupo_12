import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algoritmos.modciFB import modciFB
from algoritmos.modciV import modciV
from algoritmos.modciPD import modciPD

# ---------------- FUNCIONES PARA PROCESAR DATOS ---------------- #

def cargar_archivo_entrada(ruta_archivo):
    grupos = []
    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()
        num_grupos = int(lineas[0].strip())
        valor_disponible = int(lineas[-1].strip())

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

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        entrada_var.set(archivo)
        try:
            mostrar_grafica_entrada()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {str(e)}")

def calcular_resultados():
    archivo_entrada = entrada_var.get()
    algoritmo = algoritmo_var.get()
    if not archivo_entrada:
        messagebox.showerror("Error", "Debe seleccionar un archivo de entrada.")
        return
    if not algoritmo:
        messagebox.showerror("Error", "Debe seleccionar un algoritmo.")
        return

    resultado_texto.set("Ejecutando el algoritmo, por favor espere...")
    root.update_idletasks()

    try:
        grupos, valor_disponible = cargar_archivo_entrada(archivo_entrada)
        tiempo_inicial = time.time()

        if algoritmo == "Programación Dinámica":
            estrategia, conflicto, esfuerzo = modciPD(grupos, valor_disponible)
        elif algoritmo == "Voraz":
            estrategia, conflicto, esfuerzo = modciV(grupos, valor_disponible)
        elif algoritmo == "Fuerza Bruta":
            estrategia, conflicto, esfuerzo = modciFB(grupos, valor_disponible)
        else:
            raise ValueError("Algoritmo no reconocido.")

        tiempo_final = time.time()
        tiempo_total = tiempo_final - tiempo_inicial

        resultados = f"=== Algoritmo Utilizado: {algoritmo} ===\n\n"
        resultados += f"CI: {conflicto}\nEsfuerzo: {esfuerzo}\n"
        for i, estrategia_mod in enumerate(estrategia):
            resultados += f"mod{i}: {estrategia_mod}\n"
        resultados += f"Tiempo total de ejecucion: {tiempo_total:.4f} segundos\n"

        text_resultados.delete('1.0', tk.END)
        text_resultados.insert(tk.END, resultados)

        # Guardar automáticamente
        carpeta_salida = "resultados"
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida) 

        nombre_archivo_entrada = os.path.basename(archivo_entrada)
        nombre_salida = os.path.splitext(nombre_archivo_entrada)[0] + f"_{algoritmo.replace(' ', '_')}_resultados.txt"
        ruta_archivo_salida = os.path.join(carpeta_salida, nombre_salida)

        with open(ruta_archivo_salida, 'w') as f:
            f.write(resultados)

        messagebox.showinfo("Información", f"Resultados guardados automáticamente en: {ruta_archivo_salida}")

        # Mostrar gráfica de resultados
        mostrar_grafica_resultados(estrategia, conflicto, esfuerzo, tiempo_total)   

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo calcular los resultados: {str(e)}")

def guardar_resultados():
    archivo_salida = filedialog.asksaveasfilename(title="Guardar resultados", defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    if archivo_salida:
        try:
            with open(archivo_salida, 'w') as f:
                f.write(text_resultados.get('1.0', tk.END))
            messagebox.showinfo("Información", f"Resultados guardados en: {archivo_salida}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

def mostrar_grafica_entrada():
    # Limpiar gráfico anterior si existe
    for widget in frame_grafica_entrada.winfo_children():
        widget.destroy()

    try:
        archivo_entrada = entrada_var.get()
        if not archivo_entrada:
            return
        
        grupos, valor_disponible = cargar_archivo_entrada(archivo_entrada)
        agentes = [f"n {i+1}" for i in range(len(grupos))]
        opiniones1 = [g['opinion1'] for g in grupos]
        opiniones2 = [g['opinion2'] for g in grupos]
        rigidez = [g['rigidez'] for g in grupos]

        fig, ax = plt.subplots(figsize=(6, 4))  # Tamaño ajustado de la gráfica
        ancho = 0.25
        indices = range(len(agentes))

        # Dibujar las barras para las opiniones
        barra_opinion1 = ax.bar(indices, opiniones1, width=0.1, label='Opinión 1', color='skyblue')
        barra_opinion2 = ax.bar([i + ancho for i in indices], opiniones2, width=0.1, label='Opinión 2', color='lightcoral')
    
        # Añadir las barras para la rigidez
        barra_rigidez = ax.bar([i + 2 * ancho for i in indices], rigidez, width=0.1, label='Rigidez', color='green')
 
        # Línea horizontal mostrando el rmax
        ax.axhline(y=valor_disponible, color='red', linestyle='--', label=f'rmax = {valor_disponible}')

        ax.set_xlabel('n')
        ax.set_ylabel('Valores')
        ax.set_title('Opiniones de los Agentes')
        ax.set_xticks([i + ancho for i in indices])
        ax.set_xticklabels(agentes, rotation=0, ha='right')
        ax.legend()

        # Añadir texto a cada barra para mostrar los valores
        for i, (op1, op2, rig) in enumerate(zip(opiniones1, opiniones2, rigidez)):
            ax.text(i, op1 + 0.1, f'{op1}', ha='center', va='bottom', fontsize=9, color='blue')
            ax.text(i + ancho, op2 + 0.1, f'{op2}', ha='center', va='bottom', fontsize=9, color='red')
            ax.text(i + 2 * ancho, rig + 0.1, f'{rig:.3f}', ha='center', va='bottom', fontsize=9, color='green')

        # Crear el canvas para la gráfica de entrada
        canvas = FigureCanvasTkAgg(fig, master=frame_grafica_entrada)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)  # Ajustar para que ocupe todo el espacio disponible

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la gráfica de entrada: {str(e)}")

def mostrar_grafica_resultados(estrategia, conflicto, esfuerzo, tiempo_total):
    # Limpiar gráfico anterior si existe
    for widget in frame_grafica_resultados.winfo_children():
        widget.destroy()

    try:
        # Mostrar la gráfica de resultados (modificación de la estrategia)
        fig, ax = plt.subplots(figsize=(6, 4))  # Tamaño ajustado de la gráfica
        indices = range(len(estrategia))

        # Graficar las estrategias
        ax.bar(indices, estrategia, color='lightgreen', width=0.1)

        # Añadir etiquetas y título
        ax.set_xlabel('Agentes')
        ax.set_ylabel('Valor de la Estrategia')
        ax.set_title('Estrategia de Resultados')
        ax.set_xticks(indices)
        ax.set_xticklabels([f' {i+1}' for i in indices], rotation=0, ha='right')

        # Añadir texto a cada barra para mostrar los valores
        for i, valor in enumerate(estrategia):
            ax.text(i, valor + 0.1, f'{valor:.2f}', ha='center', va='bottom', fontsize=8)

        # Crear un segundo eje para mostrar conflicto, esfuerzo y tiempo
        ax2 = ax.twinx()
        ax2.plot(indices, [conflicto]*len(estrategia), color='red', linestyle='--', label=f'Conflicto = {conflicto}')
        ax2.plot(indices, [esfuerzo]*len(estrategia), color='blue', linestyle='--', label=f'Esfuerzo = {esfuerzo}')
        ax2.plot(indices, [tiempo_total]*len(estrategia), color='green', linestyle='--', label=f'Tiempo Total = {tiempo_total:.2f}')

        # Unir las leyendas de ambos ejes
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        # Crear el canvas para la gráfica de resultados
        canvas = FigureCanvasTkAgg(fig, master=frame_grafica_resultados)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la gráfica de resultados: {str(e)}")

# ---------------- CONFIGURACIÓN DE LA INTERFAZ ---------------- #

root = tk.Tk()
root.title("Interfaz de Cálculos de Algoritmos")

# Crear el marco de la interfaz
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Crear el frame izquierdo para los botones
frame_botones = tk.Frame(main_frame, width=200, padx=10)
frame_botones.pack(side="left", fill="y", padx=10)

# Entrada de archivo y selección de algoritmo
entrada_var = tk.StringVar()
algoritmo_var = tk.StringVar()

tk.Label(frame_botones, text="Cargar archivo:").pack(pady=5)
tk.Entry(frame_botones, textvariable=entrada_var, width=20).pack(pady=5)
tk.Button(frame_botones, text="Seleccionar Archivo", command=seleccionar_archivo, bg="skyblue", fg="black").pack(pady=5)

tk.Label(frame_botones, text="Seleccionar algoritmo:").pack(pady=5)
algoritmo_opciones = ["Programación Dinámica", "Voraz", "Fuerza Bruta"]
algoritmo_menu = ttk.Combobox(frame_botones, textvariable=algoritmo_var, values=algoritmo_opciones, state="readonly")
algoritmo_menu.pack(pady=5)

tk.Button(frame_botones, text="Calcular Resultados", command=calcular_resultados, bg="lightgreen", fg="black").pack(pady=5)
tk.Button(frame_botones, text="Guardar Resultados", command=guardar_resultados, bg="lightcoral", fg="black").pack(pady=5)

# Crear el frame derecho para las gráficas
frame_grafica = tk.Frame(main_frame)
frame_grafica.pack(side="right", fill="both", expand=True)

# Dividir en dos frames para las gráficas
frame_grafica_entrada = tk.Frame(frame_grafica)
frame_grafica_entrada.pack(side="top", fill="both", expand=True)

frame_grafica_resultados = tk.Frame(frame_grafica)
frame_grafica_resultados.pack(side="bottom", fill="both", expand=True)

# Crear un área de resultados
resultado_texto = tk.StringVar()

# Área de texto para resultados
text_resultados = tk.Text(root, height=10, width=50)
text_resultados.pack(pady=10)

root.mainloop()
