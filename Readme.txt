Integrantes Grupo 12:

Angie Melissa Ocoro Hurtado - 2310176
Juan Camilo López Quintana - 2310177
Juan Manuel Perea Coronado - 1926462
Yenny Margot Rivas Tello - 2182527
README - Moderando el conflicto interno de opiniones en una red social
Descripción del Proyecto
Este proyecto es parte del curso de "Análisis y Diseño de Algoritmos II" de la Escuela de Ingeniería de Sistemas y Computación. El objetivo es aplicar técnicas de diseño de algoritmos (fuerza bruta, voraz y programación dinámica) para moderar el extremismo de opiniones en una red social, reduciendo la polarización de opiniones de los usuarios.

Objetivos del Proyecto
Este proyecto abarca un problema que se plantea en el contexto de las redes sociales, donde se busca minimizar el conflicto interno que surge cuando agentes (personas) expresan opiniones incoherentes sobre afirmaciones similares. Para esto, se busca obtener la estrategia con la cuál se pueda disminuir el conflicto con un máximo de esfuerzo que no supere un valor disponible en la red social.
Con el propósito de explorar la eficiencia y viabilidad de diferentes enfoques algorítmicos aplicados a este problema, este informe pretende presentar el diseño, análisis y comparación de tres estrategias: fuerza bruta, programación voraz y programación dinámica. 
Cada enfoque ofrece una perspectiva distinta frente al problema, la fuerza bruta, por ejemplo, intenta encontrar la solución óptima explorando exhaustivamente todas las posibilidades. El método voraz propone decisiones locales inmediatas con la intención de aproximarse a una solución. Por su parte, la programación dinámica se apoya en la descomposición del problema en subestructuras que se resuelven mediante el almacenamiento de sus resultados.
Cada estrategia se desarrolla en función de varios criterios, como son la caracterización del problema abordado, el diseño del algoritmo, el análisis de complejidad computacional, y la presentación de casos de prueba en escenarios de diversa escala. 
Finalmente, el informe busca proporcionar una comprensión profunda del problema y las implicaciones de seleccionar una estrategia de resolución sobre otra, comparándolas, e identificando las condiciones bajo las cuales cada método resulta más conveniente.
El proyecto está dividido en las siguientes secciones:

Algoritmo de Fuerza Bruta (modciFB)

Genera todas las posibles soluciones y selecciona la mejor.
Complejidad: Exponencial.
Sección de corrección: Demuestra que siempre da la respuesta correcta.
Algoritmo Voraz (modciV)

Estrategia basada en la selección de agentes según criterios específicos para moderar.
Complejidad: Lineal/Polinómica.
Sección de corrección: Analiza los casos en los que el algoritmo es correcto y cuando no lo es.
Programación Dinámica (modciPD)

Solución utilizando subestructuras óptimas y soluciones recursivas.
Complejidad: Polinómica.
Sección de corrección: Comprobación de la estructura y cálculo de soluciones óptimas.
Archivos Incluidos
Código fuente:

modciFB.py: Implementación del algoritmo de fuerza bruta.
modciV.py: Implementación del algoritmo voraz.
modciPD.py: Implementación del algoritmo de programación dinámica.
Interfaz de Usuario:
main.py

Una interfaz gráfica que permite leer las entradas y mostrar las salidas de cada algoritmo.
Archivos de Entrada y Salida:

Formato de Entrada: Archivo de texto que describe el número de agentes, sus opiniones, niveles de receptividad, y el máximo esfuerzo permitido.
Formato de Salida: Archivo de texto que muestra la estrategia óptima, el esfuerzo total y el extremismo resultante.
Informe del Proyecto (Proyecto_1_ADA_ll_Grupo_12_Informe.pdf):

Documento que contiene el análisis detallado de cada estrategia, la complejidad de los algoritmos, los resultados de los experimentos y una comparación entre las diferentes técnicas de resolución.
Instrucciones de Ejecución


Cargue un archivo de entrada desde la interfaz.
Seleccione el algoritmo deseado para ejecutar.
Visualice los resultados generados.

