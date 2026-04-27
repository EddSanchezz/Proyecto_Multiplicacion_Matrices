# Multiplicación de Matrices Grandes

## Universidad del Quindío \- Ingeniería de Sistemas y Computación

**Seguimiento 2: Análisis de Algoritmos**

---

## 1\. Descripción del Problema

La multiplicación de matrices es fundamental en álgebra lineal con aplicaciones en gráficos por computadora, aprendizaje automático, simulaciones científicas, criptografía y procesamiento de imágenes.

Para matrices n×n, la multiplicación directa tiene complejidad **O(n³)** \- duplicar el tamaño aumenta el tiempo \~8 veces.

---

## 2\. Algoritmos Implementados

| \# | Algoritmo | Descripción | Complejidad |
| :---- | :---- | :---- | :---- |
| 1 | NaivOnArray | Triple bucle `for` ingenuo sobre arrays numpy. Itera filas de A y columnas de B, acumulando productos escalares | O(n³) |
| 2 | NaivLoopUnrollingTwo | Optimización del algoritmo naive que procesa 2 elementos por iteración reduciendo overhead de control de flujo | O(n³) |
| 3 | NaivLoopUnrollingFour | Desenrollado de bucle ×4 para mayor throughput. Procesa 4 elementos simultáneamente minimizando iteraciones | O(n³) |
| 4 | WinogradOriginal | Algoritmo de Winograd original con fórmulas de reducción de multiplicaciones. Divide matrices y usa precomputación de términos | O(n³) |
| 5 | WinogradScaled | Variante de Winograd con escalado de datos para evitar overflow y mejorar estabilidad numérica en matrices grandes | O(n³) |
| 6 | StrassenNaiv | Algoritmo divide y vencerás de Strassen. Divide matrices en 4 submatrices y calcula 7 productos en lugar de 8 | O(n^2.807) |
| 7 | StrassenWinograd | Combinación de Strassen con fórmulas optimizadas de Winograd. Minimiza productos matriciales a 7 multiplicaciones | O(n^2.807) |
| 8 | III.3 Sequential block | Multiplicación por bloques secuencial. Divide matrices en bloques que caben en caché L2 para optimizar acceso a memoria | O(n³) |
| 9 | III.4 Parallel Block | Versión paralela de III.3 usando `ThreadPoolExecutor`. Distribuye bloques entre múltiples hilos de ejecución | O(n³/p) |
| 10 | III.5 Enhanced Parallel | Optimización de III.4 con mejor granularidad de bloques y balanceo de carga dinámico entre threads | O(n³/p) |
| 11 | IV.3 Sequential block | Bloques secuenciales con tamaño de bloque optimizado para caché. Versión mejorada de III.3 con patron de acceso optimizado | O(n³) |
| 12 | IV.4 Parallel Block | Paralelización de IV.3 con pool de hilos. Usa estrategias de particionamiento para minimizar espera entre threads | O(n³/p) |
| 13 | IV.5 Enhanced Parallel | Algoritmo paralelo más optimizado de la familia IV. Incluye pre computación de índices y distribución inteligente de trabajo | O(n³/p) |
| 14 | V.3 Sequential block | Bloques secuenciales avanzados con técnicas de blocking multicapa. Optimiza uso de caché L1, L2 y L3 simultáneamente | O(n³) |
| 15 | V.4 Parallel Block | Versión paralela de V.3 que combina blocking multicapa con paralelización. maximiza throughput en arquitecturas multicore | O(n³/p) |

p \= núcleos/hilos disponibles

---

## 3\. Casos de Prueba

Matrices cuadradas n×n (n factor de 2ⁿ) con valores mínimo 6 dígitos.

**Nota:** Los tamaños 16×16 y 32×32 se usan por limitaciones de hardware. El proyecto se puede adaptar a 128x128 y 256x256 entre otros tamaños cambiando `SIZES_CASO_1` y `SIZES_CASO_2` en [`main.py`](http://main.py) (de igual forma la rama “Prueba-2” del GitHub anexado ya lo tiene implementado).

| Caso | Tamaño de matriz | Elementos |
| :---- | :---- | :---- |
| 1 | 16×16 | 256 |
| 2 | 32×32 | 1,024 |

Al ejecutar el código de python con los parámetros anteriores, obtendremos la siguiente tabla comparativa:  
![][image1]  
---

## 4\. Análisis de Complejidad

| Algoritmo | Multiplicaciones |
| :---- | :---- |
| Naiv\* | n³ |
| Winograd\* | \~n³/2 |
| Strassen\* | 7n^2.807 |
| Bloques Sequential | n³ |
| Bloques Parallel | n³/p |

### Trade-off Tiempo y Memoria (Strassen)

Strassen es hasta tres veces más rápido pero usa muchísima más memoria:

| Algoritmo | Tiempo (32×32) | Memoria (32×32) |
| :---- | :---- | :---- |
| NaivOnArray | 151 ms | 32 KB |
| StrassenNaiv | 47 ms | **226 KB** |

Algunas causas por las que los algoritmos que usan Strassen utilizan tanta memoria se debe a:

- Padding a potencia de 2  
- Submatrices auxiliares (A11, A12, A21, A22, B11...)  
- Productos intermedios M1-M7  
- Matrices temporales por nivel de recursión

En pocas palabras, debido a que el código es más complejo en cada iteración, este tarda menos a costa de utilizar más memoria con tal de utilizar menos ciclos.  
---

## 5\. Uso de Memoria y Recursos

| Tamaño | Memoria (doubles) |
| :---- | :---- |
| 16×16 | \~2 KB |
| 32×32 | \~8 KB |
| 64×64 | \~32 KB |
| 128×128 | \~128 KB |
| 512×512 | \~2 MB |
| 1024×1024 | \~8 MB |

### Consideraciones de Caché CPU

- L1: 32-64 KB | L2: 256 KB-1 MB | L3: 8-64 MB  
- Estrategia: bloques que quepan en caché L2

---

## 6\. Comportamiento por Tamaño

Gracias a los comportamientos de los algoritmos, podemos utilizar un algoritmo en especifico según el tamaño de las matrices a multiplicar:

| Tamaño | Algoritmos Recomendados |
| :---- | :---- |
| \< 32×32 | Naiv\*, Winograd\* |
| 32-128 | Winograd\*, III.3 |
| 128-512 | Strassen\*, III/IV.3 |
| \> 512 | Strassen\*, IV/V.4 |

### Predicciones (complejidad O)

- Duplicar n: Naiv×8, Strassen×\~7  
- Triple n: Naiv×27, Strassen×\~21

---

## 7\. Tablas de Resultados

Resultados con matrices 16×16 (Caso 1\) y 32×32 (Caso 2):

| Resultados \- Caso 1 |  |  |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Algoritmo** | **Tamaño** | **Tiempo (ns)** | **Tiempo (ms)** | **Memoria** | **Verificado** | **Caso** |
| NaivOnArray | 16 | 18896800 | 18,897 | 8.33 KB | SI | Caso1 |
| NaivLoopUnrollingTwo | 16 | 21912200 | 21,912 | 8.32 KB | SI | Caso1 |
| NaivLoopUnrollingFour | 16 | 24783600 | 24,784 | 8.32 KB | SI | Caso1 |
| WinogradOriginal | 16 | 58111200 | 58,111 | 9.32 KB | SI | Caso1 |
| WinogradScaled | 16 | 22746200 | 22,746 | 25.59 KB | SI | Caso1 |
| StrassenNaiv | 16 | 6730800 | 6,731 | 26.58 KB | SI | Caso1 |
| StrassenWinograd | 16 | 7297500 | 7,298 | 26.58 KB | SI | Caso1 |
| III\_3\_Sequential\_Block | 16 | 25503600 | 25,504 | 8.39 KB | SI | Caso1 |
| III\_4\_Parallel\_Block | 16 | 24706800 | 24,707 | 20.50 KB | SI | Caso1 |
| III\_5\_Enhanced\_Parallel\_Block | 16 | 24784900 | 24,785 | 24.01 KB | SI | Caso1 |
| IV\_3\_Sequential\_Block | 16 | 25703300 | 25,703 | 8.30 KB | SI | Caso1 |
| IV\_4\_Parallel\_Block | 16 | 21768800 | 21,769 | 16.46 KB | SI | Caso1 |
| IV\_5\_Enhanced\_Parallel\_Block | 16 | 23314600 | 23,315 | 22.44 KB | SI | Caso1 |
| V\_3\_Sequential\_Block | 16 | 26122400 | 26,122 | 8.30 KB | SI | Caso1 |
| V\_4\_Parallel\_Block | 16 | 21667100 | 21,667 | 16.06 KB | SI | Caso1 |

| Resultados \- Caso 2 |  |  |  |  |  |  |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Algoritmo** | **Tamaño** | **Tiempo (ns)** | **Tiempo (ms)** | **Memoria** | **Verificado** | **Caso** |
| NaivOnArray | 32 | 150679300 | 150,679 | 32.42 KB | SI | Caso2 |
| NaivLoopUnrollingTwo | 32 | 172782100 | 172,782 | 32.45 KB | SI | Caso2 |
| NaivLoopUnrollingFour | 32 | 196038000 | 196,038 | 32.45 KB | SI | Caso2 |
| WinogradOriginal | 32 | 450939000 | 450,939 | 34.45 KB | SI | Caso2 |
| WinogradScaled | 32 | 160303900 | 160,304 | 100.17 KB | SI | Caso2 |
| StrassenNaiv | 32 | 47196100 | 47,196 | 226.10 KB | SI | Caso2 |
| StrassenWinograd | 32 | 59414200 | 59,414 | 213.88 KB | SI | Caso2 |
| III\_3\_Sequential\_Block | 32 | 205890500 | 205,891 | 32.42 KB | SI | Caso2 |
| III\_4\_Parallel\_Block | 32 | 170369300 | 170,369 | 42.82 KB | SI | Caso2 |
| III\_5\_Enhanced\_Parallel\_Block | 32 | 180036300 | 180,036 | 43.07 KB | SI | Caso2 |
| IV\_3\_Sequential\_Block | 32 | 203795400 | 203,795 | 32.42 KB | SI | Caso2 |
| IV\_4\_Parallel\_Block | 32 | 167231200 | 167,231 | 40.07 KB | SI | Caso2 |
| IV\_5\_Enhanced\_Parallel\_Block | 32 | 182540100 | 182,54 | 42.75 KB | SI | Caso2 |
| V\_3\_Sequential\_Block | 32 | 206868500 | 206,869 | 32.42 KB | SI | Caso2 |
| V\_4\_Parallel\_Block | 32 | 167297700 | 167,298 | 39.91 KB | SI | Caso2 |

---

## 8\. Estructura del Proyecto

Proyecto\_Multiplicacion\_Matrices/

├── Proyecto\_Python/

│   ├── src/

│   │   ├── main.py                          \# Punto de entrada

│   │   ├── main/

│   │   │   └── resources/

│   │   │       ├── matrices/                \# Matrices guardadas en Excel

│   │   │       │   ├── matrix\_Caso1\_16.xlsx

│   │   │       │   └── matrix\_Caso2\_32.xlsx

│   │   │       └── results/                 \# Resultados y gráficos

│   │   │           ├── python\_results.xlsx  \# Tiempos y memoria

│   │   │           └── grafico\_comparativo.png

│   │   ├── algoritmos/                      \# 15 algoritmos

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── NaivOnArray.py

│   │   │   ├── NaivLoopUnrollingTwo.py

│   │   │   ├── NaivLoopUnrollingFour.py

│   │   │   ├── WinogradOriginal.py

│   │   │   ├── WinogradScaled.py

│   │   │   ├── StrassenNaiv.py

│   │   │   ├── StrassenWinograd.py

│   │   │   ├── III\_3\_Sequential\_Block.py

│   │   │   ├── III\_4\_Parallel\_Block.py

│   │   │   ├── III\_5\_Enhanced\_Parallel\_Block.py

│   │   │   ├── IV\_3\_Sequential\_Block.py

│   │   │   ├── IV\_4\_Parallel\_Block.py

│   │   │   ├── IV\_5\_Enhanced\_Parallel\_Block.py

│   │   │   ├── V\_3\_Sequential\_Block.py

│   │   │   └── V\_4\_Parallel\_Block.py

│   │   ├── persistence/                     \# Persistencia Excel

│   │   │   ├── \_\_init\_\_.py

│   │   │   ├── MatrixFileHandler.py         \# Matrices → Excel

│   │   │   ├── ResultData.py

│   │   │   ├── ResultFileHandler.py

│   │   │   ├── Results.py

│   │   │   ├── ResultsManager.py

│   │   │   ├── MatrixWrapper.py

│   │   │   └── ResultsViewer.py

│   │   └── views/

│   └── requirements.txt

├── README.md

└── DISEÑO.md

### Archivos Generados

Los siguientes archivos se agregan a sus respectivas carpetas al ejecutar el proyecto:

| Archivo | Descripción | Ubicación |
| :---- | :---- | :---- |
| `matrix_Caso1_16.xlsx` | Matrices 16×16 del Caso 1 | `src/main/resources/matrices/` |
| `matrix_Caso2_32.xlsx` | Matrices 32×32 del Caso 2 | `src/main/resources/matrices/` |
| `python_results.xlsx` | Resultados completos (30 filas) | `src/main/resources/results/` |
| `grafico_comparativo.png` | Gráfico comparativo | `src/main/resources/results/` |

---

## 9\. Prompts Utilizados (IA)

Los prompts fueron realizados **después** de que el estudiante tenía los 15 algoritmos implementados y funcionales. Los bugs mencionados en P9 fueron identificados y corregidos mediante asistencia de IA.

### Tabla Resumen

| Código | Prompt Original | Intervención de IA |
| :---- | :---- | :---- |
| P1 | Organizar código en paquetes modulares | Creó `persistence/` y `views/` |
| P2 | Implementar medición de tiempos | `time.perf_counter_ns()` en `main.py` |
| P3 | Estructurar main.py para 2 casos | `run_case()` con `matrix_generator()` |
| P4 | Documentar análisis de complejidad | Análisis teórico formal |
| P5 | Agregar docstrings a algoritmos | 15 archivos documentados |
| P6 | Agregar medición de memoria | `tracemalloc` en `process_algorithm()` |
| P7 | Agregar verificación de resultados | `np.allclose()` en verificación |
| P8 | Cambiar persistencia a Excel | Reemplazó XML por Excel con openpyxl |
| P9 | Corregir bugs de algoritmos | Bugs en III.5, IV.5, StrassenWinograd |

---

### P1: Organizar Código en Paquetes Modulares

**Prompt Original:**

"Organiza el código existente en una estructura de paquetes Python:

\- src/algoritmos/ para los 15 algoritmos

\- src/persistence/ para lectura/escritura XML

\- src/views/ para visualización

\- main.py como punto de entrada

Agrega \_\_init\_\_.py con exports apropiados."

**Intervención de IA:** Creó la arquitectura en capas con los paquetes `persistence/` y `views/`, implementando clases para manejo de resultados y visualización.

**Archivos creados/modificados:**

- `algoritmos/__init__.py`  
- `persistence/__init__.py`  
- `persistence/ResultData.py`  
- `persistence/Results.py`  
- `persistence/ResultFileHandler.py`  
- `persistence/ResultsManager.py`  
- `persistence/MatrixFileHandler.py`  
- `persistence/MatrixWrapper.py`  
- `views/__init__.py`  
- `views/ResultsViewer.py`

---

### P2: Implementar Medición de Tiempos

**Prompt Original:**

"Implementa una función que ejecute todos los algoritmos,

mida el tiempo de ejecución en nanosegundos, y guarde

los resultados en XML."

**Intervención de IA:** Implementó `process_algorithm()` en `main.py` usando `time.perf_counter_ns()` para máxima precisión.

\# \[AI MODIFIED\] \- Agregado por IA

def process\_algorithm(algorithm\_name, multiply\_func, A, B, case\_name):

    start \= time.perf\_counter\_ns()

    C \= multiply\_func(A, B)

    end \= time.perf\_counter\_ns()

    execution\_time\_ns \= end \- start

    \# ...

---

### P3: Estructurar main.py para Dos Casos de Prueba

**Prompt Original:**

"Configura main.py para soportar 2 casos de prueba con

matrices cuadradas n×n donde n es factor de 2^n, con

valores de mínimo 6 dígitos."

**Intervención de IA:** Configuró soporte para Caso1 y Caso2 con generación dinámica de matrices.

\# \[AI MODIFIED\] \- Configuración por IA

MIN\_DIGITS \= 7

SIZES\_CASO\_1 \= \[16\]

SIZES\_CASO\_2 \= \[32\]

def matrix\_generator(n, min\_digits):

    \# \[AI MODIFIED\] \- Genera matriz numpy con valores aleatorios de n dígitos

    return np.random.randint(10\*\*(min\_digits-1), 10\*\*min\_digits, size=(n, n), dtype=np.int64)

---

### P4: Documentación de Análisis de Complejidad

**Prompt Original:**

"Documenta el análisis de complejidad de cada algoritmo

en un documento formal. Incluye notación Big-O, análisis

teórico del número de operaciones y predicciones de

rendimiento."

**Intervención de IA:** Documentó análisis de complejidad en README.md y DISEÑO.md con notación Big-O, Theta y Omega.

---

### P5: Agregar Docstrings a Algoritmos

**Prompt Original:**

"Agrega documentación tipo docstring a los 15 algoritmos

incluyendo: descripción, complejidad computacional,

parámetros y valor de retorno."

**Intervención de IA:** Agregó docstrings a los 15 archivos en `algoritmos/`.

\# \[AI MODIFIED\] \- Docstring agregado por IA

def multiply(A, B):

    """

    Multiplicación de matrices ingenua sobre arrays.

    Complejidad Computacional:

        \- Tiempo: O(n³)

        \- Espacio: O(n²)

    Parámetros:

        A: Matriz de tamaño n×n

        B: Matriz de tamaño n×n

    Retorna:

        Matriz C de tamaño n×n donde C \= A × B

    """

---

### P6: Agregar Medición de Memoria

**Prompt Original:**

"Agrega medición de memoria a cada ejecución usando

tracemalloc para obtener el pico de memoria en KB."

**Intervención de IA:** Integró `tracemalloc` en `process_algorithm()` para medir pico de memoria.

\# \[AI MODIFIED\] \- Agregado por IA

import tracemalloc

def process\_algorithm(...):

    tracemalloc.start()

    C \= multiply\_func(A, B)

    current, peak \= tracemalloc.get\_traced\_memory()

    tracemalloc.stop()

    peak\_kb \= peak / 1024

---

### P7: Agregar Verificación de Resultados

**Prompt Original:**

"Agrega verificación de resultados comparando el

resultado de cada algoritmo con np.matmul para

validar que C \= A × B."

**Intervención de IA:** Implementó verificación con `np.allclose()`.

\# \[AI MODIFIED\] \- Verificación agregada por IA

def verify\_result(A, B, C):

    expected \= np.matmul(A, B)

    return np.allclose(C, expected, rtol=1e-5, atol=1e-8)

---

### P8: Cambiar Persistencia a Excel

**Prompt Original:**

"Cambia la persistencia de XML a Excel usando openpyxl.

Genera gráficos comparativos del rendimiento."

**Intervención de IA:** Reemplazó XML por Excel con openpyxl, agregando generación de gráficos con matplotlib.

**Archivos modificados:**

- `persistence/MatrixFileHandler.py` \- Cambio a Excel  
- `persistence/ResultsExcelHandler.py` \- Resultados en Excel  
- `main.py` \- Integración de persistencia

---

### P9: Corrección de Bugs de Algoritmos

**Prompt Original:**

"Revisa los algoritmos y corrige los bugs que encuentres.

Los algoritmos que fallan la verificación son:

\- III.5 Enhanced Parallel Block

\- IV.5 Enhanced Parallel Block

\- StrassenWinograd"

**Intervención de IA:** Identificó y corrigió los siguientes bugs:

#### Bug 1: Parámetros incorrectos en ThreadPoolExecutor (III.5, IV.5)

**Problema:** La segunda llamada a `executor.submit()` usaba `N, N, P, M` en lugar de `N, P, M`.

\# \[AI MODIFIED\] \- Bug corregido por IA

\# INCORRECTO (original):

executor.submit(block\_multiply\_section, matrizA, matrizB, matrizRes, mid\_point, N, N, P, M, block\_size)

\# CORRECTO:

executor.submit(block\_multiply\_section, matrizA, matrizB, matrizRes, mid\_point, N, P, M, block\_size)

#### Bug 2: Indexación incorrecta en IV.5 Enhanced Parallel

**Problema:** Usaba `C[i][k]` en lugar de `C[i][j]` en el bucle interno.

\# \[AI MODIFIED\] \- Bug corregido por IA

\# INCORRECTO (original):

C\[i\]\[k\] \+= temp1 \+ temp2

\# CORRECTO:

C\[i\]\[j\] \+= temp1 \+ temp2

#### Bug 3: Padding incorrecto en Strassen (Naiv y Winograd)

**Problema:** newSize \= 17 para input 16×16, debía ser potencia de 2\.

\# \[AI MODIFIED\] \- Bug corregido por IA

\# INCORRECTO (original):

newSize \= n \+ 1 if n % 2 \== 1 else n

\# CORRECTO:

newSize \= 1

while newSize \< n:

    newSize \*= 2

#### Bug 4: Overflow de entero en StrassenWinograd

**Problema:** Matriz resultado inicializada como `[[0]]` (int) causaba overflow.

\# \[AI MODIFIED\] \- Bug corregido por IA

\# INCORRECTO (original):

result \= \[\[0\] \* size\] \* size

\# CORRECTO:

result \= \[\[0.0\] \* size\] \* size

#### Bug 5: Fórmulas incorrectas en StrassenWinograd

**Problema:** El algoritmo implementaba fórmulas de Winograd incorrectas, causando resultados erróneos para tamaños ≥32×32.

**Solución:** Reescritura completa del algoritmo usando la fórmula estándar de Strassen-Winograd con variables temporales separadas para cada producto M1-M7.

---

## 10\. Cómo Ejecutar

cd Proyecto\_Python

pip install \-r requirements.txt

python src/main.py

**Archivos generados:**

- `src/main/resources/matrices/matrix_Caso{1,2}_{size}.xlsx`  
- `src/main/resources/results/python_results.xlsx`  
- `src/main/resources/results/grafico_comparativo.png`

**Cambiar tamaños de prueba:**

\# En main.py

SIZES\_CASO\_1 \= \[512\]  \# o \[16\], \[32\], etc.

SIZES\_CASO\_2 \= \[1024\]

---

## 11\. Conclusiones

1. **Matrices pequeñas (\<64×64)**: Naiv\* y Winograd\* son más eficientes por bajo overhead  
2. **Matrices grandes (\>512×512)**: Strassen\* y paralelos muestran mejor rendimiento  
3. **Strassen**: Trade-off tiempo/memoria \- usa \~7x más memoria para ser \~3x más rápido  
4. **Paralelización**: Speedup lineal con núcleos, límite práctico \~8-16 hilos

---

## 12\. Aclaración Importante

Los 15 algoritmos son implementaciones conocidas de la literatura académica obtenidas de un repositorio GitHub público. La IA ayudó únicamente en tareas técnicas de organización, medición, documentación y corrección de bugs, no en el diseño de algoritmos, estos algoritmos se encuentran en el fork original del repositorio.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAnAAAAIhCAYAAADOwYfxAACAAElEQVR4XuydB9gVxfXGIygqFuxo7EZj19hRo9ixJKixxRZLFBvGXrBhCWqsUbEQxRJ7iSVRUYO9RdBoomLDgoKKgvhXQZGy/7yDZ517vt177+y3s7N7v/f3PPPs3p3duXPPmZ157+zszE8iQgghhBBSKX6iDxBCCCGEkHJDAUcIIYQQUjEo4AghhBBCKgYFHOnwLLnkklH//v1rjv3kJ9luDVyn03Ih6/f6Yp999ol69uypDzcNfk97rk8DNta2wufRo0fXHMuLpDLiyuOPP94mz0WA77zuuuv04dxI+01pxwWJh20bnduIpDT052bJw9dZyZpn0jFhaSFe+NOf/mQqo969e0dnnnlmh6mYmhVw559/vgk4X/bLiIuAs39LWX9PMwwbNsz8FrvMtrdR/+abb2o+I+3333+/5pgvmhVwyI/9uydMmGD2G/lfzm/2e4Sy1gkuvrbtNXXq1DblRhNKxJPWhCWJeCGtIpt33nnjuAsvvNAcw/58880XH5911lnNdrnllovjN9tsszj+22+/jV599dX4s3yPVI4SLrvssjbnTJ8+vc0xu8Lu1KlTHIf0APZXW221mmtsTjzxxJo0Ja2ZZ545PvbJJ5/UXvQDOj37s86nHBP7bLLJJjXx0isl4fDDDzfHN9544zZpde7cuc0xGzm+/vrrxw34AgssEB/v1q1b7QVR298ix5Kuf+qpp8yx7bbbLj4GwSAiAuA6CEgw11xzxecdccQR8W8FI0aMiOPkGISEfWzvvfc2x5sBZfSkk06q+T12GZE0f/3rX9eco/Mgx8TWduNtn6vL7W233ZaYjgT7vtHnCb/97W9r4kVY2ce0qNQCbumll67xv05HkH2dH9lqX+BPnR1v955dc8018XkXX3xxfJ6drj728ssv16Rh38NSTvEbmr2Hu3fv3vQ9jOMzzTRTtMsuu5j7bJtttonTP+aYY+Jru3TpEp9v5wHbjTbaqOazoM+VMinXgK5du7Y5j3Qc6HHiBVQm6623nj7cpoKSLSpK2cc/WR0vDb5UVOPGjaupuPr06dPm3+1LL71Uc84tt9wS79voxlmwv3+DDTZoEy/oa5DWQgstVPPdSdcBfVw+r7vuujXXnnDCCTXxiyyySE3+brjhhhpRY5+L7QMPPBDvP/jgg2YLIQgxAFFrIw0P2HTTTWsacDto7Dj7Guzvuuuuba6XfNikCTh9nv1bsRUxgv2JEyfGokGO6eull3DIkCE1xz/++OP43D322MP4ESSVkQ8++CDeRyN+3HHHxfHHH398zblACzjpgbOPDxo0qOYcANstuOCCZh9CwY7ffvvtje819vdiH/ZAHsUWEmzE9pMmTYp++tOfmn34wEXASbx93PbFfvvtV3M+sMWXzpMck4B7WAS7TVoaso/f0OgelvpqlllmaSPWJWjs70RAeZVjjzzySM21zz33XJs6Cvt33XVXzWcAn+NPi4AyrfOCsost/iCce+65cb1JOg5tSyQhOSCVjEZXXrJFBVwvXgs46dVApbXOOuuYijOpcrTTsHsCbJIaZ3sf2zQhoY9h3xZwjR4p6vTkMwTcyiuv3EZoSLxusPDbXAQcuPfee+MeUZt6Aq7e79HpyDFbwNnXJwm4UaNGxccgWtLs3l4BJ8ckfWHFFVeM4+zrksqIDwGn8w3SBBw4+eSTzefHHnssPgbsc7Bvl/00H9riGdsePXq0EXCXX355vC/Y1+Qt4B566KE26WcVcGllSY6lCbg0e0k8wH20+OKL1wg4bO3eUvg5qY6SciCfgRZwKN86L6+99pqJw30kgpt0LOhx4g151CcBzDPPPPHnCy64wBzDfiMBZz9qQw8B/nHK57XWWitRwG299dY134/KP+sj1HqVPxpuO01Jy378knQd0Mftz/a1UsnbeZZ9bG0BJ+HQQw818UmPUO3P+M0aiVtzzTXjBtx+BCrp2Nhx9vfUu37bbbeNP+MRqp3OCiusENs96yNUO71mwHlbbLFFzWegBRyC/bjMPq6PCXb5XGONNeJzGwk42Zdg3zcSvvzyy/hcIEJPgggr+5jcc4It4ARbwEkP3vzzz98mb+Coo46K07aPy2+SgHvZjrfLcqNHqEm/o9lHqM3ewyinzd7D+pgt4FZdddWaa+36RM7BNknAyb59br9+/docsz/b15KOAT1OSo+u5EgytqgpC8jPTjvtpA+3BDLGktTHFqWEkPzgXUVKDwVcc5RNwKH34ze/+Y0+XHl22GEHM3gcPbxTpkzR0URBAUeIH3hXkQ6DHqxPCCGEVJUgAk4/t2dgYGBgYGBgYKgfarRUzaeC+L//+z99iBCvYD4rGURMCCGEVA0KONJhwJtlr7zySjR58mTzecyYMeoMQgghpBpQwJEOwY477mi2mLxTpl0ghBBSXjCRNqaJwmo7DDMCpkkSKOBIy/PRRx+ZSUgvvfTS6N133zUTrhJCCCk3tlghMxBBCyjgSMtz++23m1nVb7zxxujNN9/U0YQQQkqILeCwFGKzoQi23HJLfcgbiy66aLwvPXGAAo60PC+88IKZrZ/ThhBCSHUQAQdRtu6eg5sKK29zmkplxqoiWGNWlhtzAcuW9erVSx+Owcof++67r9nHyhuffPJJ9MUXX5jPWFLt9ddfN/tY0k+TdK1w5ZVXxtfef//98XEKOEIIIYSUGlvAbXH0M00FiDiNFjoCloHDEmfC8ssvb7ZzzjlnfAzIsmuCLPMnHHLIIWZ76623Rvfcc49Zjxv7SyyxRLT77rvH52HpSFnOTdDXYj1v7ENw2tcKFHCEEEIIKTV5CTis22uDdbnfeuutWAChtwtjpKU3TAsjLeBkJgNw/vnnR8OHD7diZ6zz/Nhjj0VPP/10zXGs4bzgggvGn5Ouveqqq8y1aVDAkZan6+yztZnwsFHANYQQQspBXo9QwZJLLhmPJbvooovMY1HU+3379jWCbty4cdETTzwRdenSpc2SeNJG2Hz55Zdt4rbaaivzPZ9++qn5fMwxx0RbbLGF2U/SOUnXCgsttFB87dlnnx0fp4AjLQ8K9vhT13AK+mYghBASjjK/xIAeu6JAr5xAAUdaHgo4QgipNpxGpC0UcKTloYAjhJBqQwHXFgo40vJQwBFCSLWhgGsLBRxpeSjgCCGk2tgvMTx2wPJNhat2WLI2kah988ANGDAgGjlyZNSpUycdZcDcbTJ/28UXXxy3I0OGDIkefvhh8zICGDt2bHyNUO9arBok1w4cODC+hgKOtDwUcIQQUm1sAafr67QAEafR04hALD366KNmDrbtttsu+u9//xs9+eSTUdeuXaM33ngj6t+/f835YMMNN4z3x48fH+8vssgi0R577BF/1u3IySefHO9DCNpzu7lcK1DAkZaHAo4QQqqNLwHnOg/cHHPMUfP57bffrvlsY187ZsyYaNq0afHnhRdeOFpuueXizxr7WpxnXytQwJGWhwKOEEKqTV4CDo8j8QhV0kNd/9e//tVssczie++9F+26666JPXCYVNd+1KnB41mZrw3nIE0skTV69Oho8803j6+75JJLzBaTAGO1hbRr0buHaxHk2scff9xsAQUcaXko4AghpNqUeR44CMCiuO222+J9CjjS8lDAEUJIteFbqG2hgCMtDwUcIYRUGwq4tkycOJECjrQ2FHCEEFJtMF4MIo7hx/DBBx/E9tFtVpAWjAKO5A0FHCGEkFZGt1lBWjAKOJI3FHCEEEJaGd1mBWnBKOBI3lDAEUIIaWV0mxWkBaOAI3lDAUcIIaSV0W1WkBaMAo7kDQUcIYSQVka3WUFaMAo4kjcUcIQQQloZ3Wa1uwUbNmxYtNpqq5n9xRdfPOrRo4fZX2WVVczyEv369bNPN1DAkbyhgCOEENLK6Dar3S0YJpjr2bNndPPNN8fHjj/++GirrbYy+/YXQrghYO2vKVOmmIVbsQXyGWuGYV/C9OnTa7b2vlxnX5+Upp1eWpoS6l0veZO4pOt13nCNpJGUdlqa9X6vbaOkNCUuLW07JKUdKr/6+qT8Jl2P0KVLl+jz09aOPjttHSPOsB136ppmO2Nfjs3Y4hxcY/9enad6vzcpv66/t17a2gZ22mlp+s6vvj4p7aTr9bGkvKWlWe/3SnxamjptOafR79VpJqWdlmbI/Orr6+XXvj4pTTu9tDQl1Ls+6+/VadppZ01T4nTaeeY3Ke20NOv5p9n86uuT8pt0vRxLy1tSmnbektKU6+qlqdO205S4rGlnyW89/9ghKU2JS0s76fqk/CZdn3QM21wF3D333BN17tzZJDp06NBowoQJ5vhFF10Urb766mafAi7czZ2Wth2S0g6VX319Un6TrkeggPOfX319UtpJ1+tjSXlLS7Pe75X4tDR12nJOo9+r00xKOy3NkPnV19fLr319Upp2emlpSqh3fdbfq9O0086apsTptPPMb1LaaWnW80+z+dXXJ+U36Xo5lpa3pDTtvCWlKdfVS1OnbacpcVnTzpLfev6xQ1KaEpeWdtL1SflNuj7pGLa5CjgBPXDg0EMPjXbccUezj9mDZ5999jgTNnyESvKGj1AJIYS0MrrNCtKCUcCRvKGAI4QQ0sroNitIC0YBR/KGAo4QQkgro9usIC0YBRzJGwo4QgghrYxus4K0YBRwJG8o4AghhLQyus0K0oJRwJG8oYAjhBDSyug2K0gLRgFH8oYCjhBCSCuj26wgLRgFHMkbCjhCCCGtjG6zgrRgFHAkbyjgCCGEtDK6zQrSglHAkbyhgCOEENLK6DYrSAtGAUfyhgKOEEJIK6PbrCAtGAUcyRsKOEIIIa2MbrOCtGAUcCRvKOAIIYS0MrrNCtKCUcCRvKGAI4QQ0sroNitIC0YBR/KGAo4QQkgro9usIC0YBRzJGwo4QgghrYxus4K0YBRwJG8o4AghhLQyus0K0oJRwJG8oYAjhBDSyug2K0gLRgFH8oYCjhBCSCuj26wgLRgFHMkbCjhCCCGtjG6zUluwCRMmRD179oxWXnnl6KabbtLR7YICjuQNBRwhhJBWRrdZiS3YTDPNFPXt2zf+fN9990WLLbaYdUb7oIAjeUMBRwghpJXRbVaQFowCjuQNBRwhhJBWRrdZdVuw7bbbLjr//PNNj9w555yjozNDAUfyhgKOEEJIK6PbrLot2IMPPhh17do1Gjx4cDTHHHPo6MxQwJG8oYAjhBDSyug2q24L1qlTJxNOO+20aNNNN9XRmaGAI3lDAUcIIaSV0W1W3Rbstddei6ZPnx6NHj06mjRpko7ODAUcyRsKOEIIIa2MbrMSW7DFF188eumll2qOnXLKKTWf2wMFHMkbCjhCCCGtjG6zEluwgw46yLy4II9QsT/bbLPp0zJDAUfyhgKOEEJIK6PbrCAtGAUcyRsKOEIIIa2MbrOCtGAUcCRvKOAIIYS0MrrNCtKCUcCRvKGAI4QQ0sroNqtuCyZj4BA6d+6sozNDAUfyhgKOEEJIK6PbrLot2LzzzmvePj399NNNyAsKOJI3FHCEEEJaGd1m1W3BunXrFr3yyivRqFGjTMgLCjiSNxRwhBBCWhndZtVtwTB9iAQ8Rs0LCjiSNxRwhBBCWhndZjVswT7//HN9KOaKK66I5pprLrNm6rfffhvNN9980aeffmritt1222jBBRdUV8yAAo7kDQUcIYSQVka3WXVbMJnEF9uvvvpKR8dgrNwss8xi9uULRMhNnjw5Pk+ggCN5QwFHCCGkldFtVmILhl41cN9995ntvffeG80+++z2KTEvvvhitMACC0RdunQxn9dZZ52aePTOCfhyhKFDh0bPP/98NHLkSLMF2I4dO9aMucP+sGHDzHbKlCk1WxyfMGFCzXWyRXpJaWLbKE05R86305S4ESNG1MQhH/a1CBMnTqw5B79H0vzoo49q4vA5KU07nbQ0JS4pTYmT8yTOTlOCtiXyI2kk2TItzXr+kd+YlqbEZfUPwsknnxy9dMVR0VPX/8mIM2xHnb1N9My1A8z+Z6etY7ZjzuwZn4NrbP/YaWJbzz928OEf2U+yZVqa9fxjh6Q0Jc6Xf+xjsrXvn7Q06/kHwYd/dJqyTfKPTrOef+zzktKU4OqfVq4z5Zhsk/yTh88lLqt/qlhn2t8jcfXuSTknyT+NfC5xEnz4p2p1pqSZZMu0NJsScML8888fC7QePXro6JhNN920TQ8cvhB899138XkCe+BI3rAHjhBCSCuj26y6Ldhtt90WrbjiitHtt9+uo9oFBRzJGwo4QgghrYxusxJbMJm0lxP5kqpAAUcIIaSV0W1WYgu21FJLxVs75AUFHMkbCjhCCCGtjG6z6rZgxx57rNkec8wx0R133KFis0MBR/KGAo4QQkgro9usui3YkCFD4i3meMsLCjiSNxRwhBBCWhndZtVtwTD2rVevXmYuuMMOO0xHZ4YCjuQNBRwhhJBWRrdZdVuwVVdd1Yg3bPOEAo7kDQUcIYSQVka3WXVbsDPOOKMm5AUFHMkbCjhCCCGtjG6z6rZg9kL2XMyelBkKOEIIIa2MbrOaasEuv/zy6Oc//7k+nBkKOJI3FHCEEEJaGd1m1W3BpAcO4bHHHtPRmaGAI3lDAUcIIaSV0W1WkBaMAo7kDQUcIYSQVka3WXVbsMGDB5vttddey0eopNRQwBFCCGlldJtVtwU7++yzzXbAgAHR3HPPrWKzQwFH8oYCjhBCSCuj26y6LZg9Bm7atGk6OjMUcCRvKOAIIYS0MrrNCtKCUcCRvKGAI4QQ0sroNqtuC4a539D7tt9++0WHHnqojs4MBRzJGwo4QgghrYxus+q2YOeff74RcA899BAXsyelhgKOEEJIK6PbrLotmPTAIbAHjpQZCjhCCCGtjG6z6rZgq6yyChezJ5WAAo4QQkgro9usxBZMFq63F7I/88wz1VnZoYAjeUMBRwghpJXRbVZiC3b99dfHWzugNy4PKOBI3lDAEUIIaWV0m+XUgt177736UCYo4EjeUMARQghpZXSbldiCoaft2WefjbfPPPOMeaEhLyjgSN5QwBFCCGlldJuV2IJRwJGqQQFHCCGkldFtVmILZi+hJYECjpQZCjhSBMOGDdOHCCEe2HzzzaPddttNH+7Q6DYrSAtGAUfyhgKO+Oa1114z23322ac2gpSeAQMG6EOk5Ky33npme9ZZZ6mYjotus4K0YBRwJG8o4IhPRo8ebbYffvhh9OSTT0bff/+9OoOUFbQ3V199dXTEEUdEY8eO1dGkZOy0005mO23aNLOVP06EAo60KBRwxBd4jDN9+vT485gxY6xYUmbQ1kydOtUI7rvuuiv64IMP9CmkZFx77bXR6aefbnx3+eWX6+gOjW6z6rZg2267rRn7ttJKK0Uvvviijs4MBVxrI/+cioQCjvigV69e0csvv2wEXJ6TmRP/XHfddWY7ePDg6NNPP62NJKUDa66D119/Pdp5552jd955R51BdJtVtwU78cQTzQsM999/f7TQQgvp6MxQwLU2vXv3Ng3eH/7wBx3lDQo4kje/+93vot///vdm/4orrlCxpMwce+yx8RiqHj16qFhSNnCvnX322dFNN90UDRo0SEeTH9BtVt0W7NxzzzUC7uijj46WWGIJHZ0ZCrjWxO55w5iTTTbZxIr1CwUcyZMpU6aY7S677BL99re/jV599VV1BikreORN4V0tJk+eHI0cOdLsf/311yqWCLrNqtuCodcNAi7P3jdAAdeaYOwCet/g36JvQgo44oPu3bvrQ6TkYLwbRDfmMCXV4q233tKHiIVus4K0YBRwrQV63vbaa6+4wvzjH/+ozvAPBRzxAQbAk2qB4RsU3qQV0W1WYgumJ/HlRL4kDYg3/OO97777oksvvVRHFwYFHCGEkFZGt1l1W7Bjjjkm3l5//fUqNjsUcK0DXss/8sgjzf4WW2yhYouDAo7kxUsvveQcCKky6LW85JJL4v2i6Dr7bKYedgmjRo3SyXQYdJtVtwVDr9uvfvUrs1155ZV1tHnF/pVXXolfcFh88cXjN35WWWUV8/p9v3797EsMFHCtx4gRI/ShQqGAI3kAMfbYAcu3KSv1As6niPuR4447zoQiJzvOIgRwDfmRBx980GwnTJigYvzhWm939HtNt1l1W7DFFlvMPD7Fth5I9NFHH40df9FFF0Wrr756HKehgCN541oRICSVTdKxoYBrHxhSIW8TypugRcD7Pxvw14EHHhh/3mCDDaxY/7j6raPfa7rMtrsEi7hrRsBBuCGMHz/evKaPwiOv68tnDBrGvgR059pbe1+us69PStNOLy1NCfWul7xJXNL1Om+4RtJISjstzXq/17ZRUpoSl5a2HZLSDpVffX1SfpOuR+jSpUv0+WlrR5+dto650bEdd+qaZjtjX47N2OIcXGP/Xp2ner83Kb+uv7de2toGdtppafrOr74+Ke2k6/WxpLylpVnv90p8Wpo6bTmn3u/FhOWP9lm5phz9WJ5mbHU5erTPKuY6SVun6TO/ts/19Un2levs65PStNNLS1OCnH/IIYeYmfPz+L06T3bektLEvSy+0f7BVuoGs3/qWmaLtknSzCu/Ot9p+dVpJ6UpcUlpSpy+Pim/SdcjoIc0LW9Jadp5S0pTrquXpk4bPkjzT+y7Hz4j4N4cPnx4YtpZ8lvPP0n5tdOUuLS0k65Pym/S9UnHsM1VwOGG/eSTT0wAeJS6/vrrm308QsXjVT5C9QsKQZ8+ffRh7+gxQM0En7j+k0PQNwMh7IHLBn4/5n1E7xvWii0a3v/uHHbYYdHAgQPNfqjxy65+6+j3mi6zDUvwnXfeqQ+1Gwq4fNlnn330Ia+UsZFzrQgQ9M1ASBnLdj3wBw7jzZ5//nkdVRgYO/XVV1+ZlQ9CrTXK+9+NhRdeON7ffvvtrZhicfVbyHutDOgyW7cEY/wb1kPFdr/99tPRmaGAaz977rmnWTMOTJw40XSxFkUZGznXigBB3wyElLFspzFp0iSzxZCUvn37qthigGA7/PDDzf5WW22lYoujavf/KaecEu299976cGFA+GPi9dBrxLr6LdS9Bh5++GGzxXJfsF8IdJmtW4KHDBkSbzHGIC8o4NqHFmsQcEVSxkbOtSJA0DcDIWUs20mcfvrp0XvvvVeaBb833nhjfahQqnj/X3zxxdE999yjDxfGRx99pA8VjqvfQtxrSTz11FP6UCHoMlu3BGP6EAT0wD322GM6OjMUcO1n//33N1t546tIytjIuVYECPpmKBItwkk5KGPZ1sjTkA033DDo5Nlloir3/4UXXmjGjgM8du7ouPqt6HsNoLfN/s7PPvvMii0WXWbrlmAodBS2vJU6BVx2TjzxRLM9+uijVUxxlLGRc60IEPTNUCQDBgyIDjjggOi7777TUSQgZSzbSci417zr5qpShfsfPW4AszSEAuXUJfieNNfVb0Xfa/ijLet6FzmvYRq6zNYtwdIDh5Cn6qSAax8Yu/Dxxx/rw4VRxkbOtSJA0DdDkUgPXOhHT6SWMpZtm8suuyx64403zKPTL7/8UkcXhm7omwk+Kfv9j8fdEN1Fz7Nmk6Vs+7aRq9+KvNfAb37zm+ivf/1r9MADD0SjR4/W0YWj/VHXOwsuuGD03//+1ywM3K1bNx2dGQq49hH6X3eWisD3jedaESDom6EI0KN91VVXmf2ixy6SxpSxbGvK8Afuqh2WNL+72YDzfdqozPc/HnlDcB911FFmzNvkyZP1KYWQpWz7tpGr34q81+RNXbxdjZcGy4D2R13vLLvsstE333xjtnjTKS+qLOA4dilbReD7xnOtCBD0zeATjKPAnEt///vfzedbbrlFnUHKQBnLdtkoo43Kfv+DjTbaSB8qlCx+820jV7/5Lkc28qbuZpttpqOCof1R1zvyAoNsEfKgygIOY9DuuOOOQl8jxjgEFFqX4HPsQpaKwPeN51oRIOibwSf2I5RQc2WRxpSxbJeNMtqo7Pc/ePfdd/WhQsniN982cvWb73KkCf20S6P94dc7KVRZwIFHHnlEH/KKayFH0I7OkywVge8br2w2srHnytppp51ULCkTZSzb/APXmDLf/2Uhi99828jVb77LUdnR/qjrHel1k164vKiigPvXv/4Vv/n17bff1kZ6xrWQI2hH50mWisD3jVc2GyXx85//XB8iJYNluzG0UXNkEd4+yeI33zZy9ZvvcgS0T5oJRaH9Udc79913nz6UC1UScDLmDY9NQZ7z4TWLayFH0I7OkywVge8br2w2ItWEZbsxtFFzIH387maD7xc9svitCBvp76wXfJcjpF22F3RstD/qekd63iTkRVUEnL08zW233WbFFItrIUfQjs6TLBWB7xuvbDYi1YRluzG0UXO45sm3jbL4jTZqHHznyUb7o653VlttNfMWxvXXX29CXlRFwAEZu7TJJpuomOJwLeQI2tF5UsZCXjYbgbI9QiGNYdluDG3UHK558m2jLH6jjRoH33my0f6o6x30umEiO8xjI0s35UGVBBwYMWKEPlQoroUcQTs6T8pYyMtmI+CaJ982Io1h2W4MbdQcrnnybaMsfqONGgffebLR/qjrHb7EUA5cCzmCdnSelLGQl81GwDVPvm1EGsOy3RjaqDlc8+TbRln8Rhs1Dr7zZKP9Udc7kyZNMms24lFQnvOeUcC54VrIEbSj86SMhbxsNgKuefJtI9IYlu3G0EbN4Zon3zbK4jfaqHHwnScb7Y+63pEJfA899NBo33331dGZKbuAgzNcg09cCzmCdnSelLGQl81GwDVPvm1EGsOy3RjaqDlc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CCGEkIpBAUcqybRp00woC1hEnjRm6tSp+hAhhJAMdHgBh0XAJ0yYoA8TxYsvvthmwfSQ9OzZs1T5GT58eLThhhuWSlSCpLfAQ7L44ovrQ0Epm79AGfNURu6++259KChlqo/KyogRI6Lvv/9eHw5G1X3WoQWcVJSXXnqpignLiSeeGO211176cBDERjPNNJOKCc+bb75pbsAy9Oosuuii0eeffx5ttNFGOioo33zzjT4UlIsvvjiad955SyFS1lprLbM977zzVEwYYJM+ffqY/b/97W8qNgz333+/2V577bWluM9A//79zfbBBx+sjQjElClTov33379UwuSiiy6q2ZaBWWaZxbRtZeGDDz4w22222UbFVIcOLeAmTZoUHX300fpwUFAZgL/+9a9mIfDQoFGRBg69TGVg/vnnj1ZfffXov//9b7Tsssvq6CB0797dbHv37h0ddNBBKjYM6667bnTddddFTz/9tI4KxieffGJEZdeuXXVUoUhje8kll0THH3989NBDD0VffPGFOqt4/vGPf0Tvvfde4gToofjFL34RXX755dFXX30V/ec//9HRhYN6+1e/+lW0+eabmzJehj8DV199dfTdd9/pw0GZffbZjdj9+uuvo48++khHF8ro0aPNFh0BK6+8crT11lurM8Lws5/9LNpyyy2jrbbaqjR5cqFDCjjc8EsttVS03nrrxcfmmGMO64ww4B8B/ulCVP7yl7/U0YUDkTR+/Pho7Nix0RJLLGGOleVfOAj5z0m63t9+++3o5Zdfjt56663orLPOMgK8DDYqSw+OsP7660e9evWKrrjiimjnnXfW0YXz05/+NN7H43gQ+nHK9ttvH73++uvRI488Ev3xj3/U0UHo0aOH2eIPZRmA2BbBdsQRR6jY4kGZwZ821AHXXHONjg6GtB+wV9nYeOON9aGgiLisIh1OwKFx/fbbb80+/lniXxzYbbfd7NMK5csvv4xuuummaO+99y7NIzg8DgRLL7202aJBCd3AoecN/97AmmuuGfSRhTxS7tevnxG6b7zxhjojDGussUY099xzm96SFVdcUUcHYejQodHkyZOjffbZJxozZoyODgIaXdQF8hgldNkGKEv4A4B5qNATVwbkicDHH3+sYsKwyy67mK08ai4Dt956qynfqI+GDRumowsHnQBl44477jDbU089VcWE59FHHy3F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4JARQkh54FQGhBBSbijgCCE1YCqF/fbbTx8mhJDC+fbbbxmsYEMBRwipAStFYDULQggJCSZNxhRPWsR05CDzRgIKOEKI4ZZbbjFzoV155ZWm0nz77bf1KYQQUhi2WCEzECEHKOAIIQZMSovJfgcPHhx9+OGHOpoQQgrFFnAvvfRS06EIttxyS33IG1gpSKCAI4SkgpnnCSEkNCLgIMqO/FuvpsIe56+vUomibbbZpubzhRdeGC222GLR119/bZbsw1JpDzzwgBk60qVLl5p1noGsqpEGVnAB9nlIA6ueCPZ62rbmSbvWZvLkyfE+BRwhhBBCSk1eAk4LnX/+859mrV4cv/rqq6MNNtjAHN93333NVp+vBRzG5tnMO++8NZ9xPdbNHjRokHmyIWy66abRtddea53Z9tqhQ4eaa4F9rUABRwghhJBSk5eA23rrrWs+zzLLLGZrC6BVV101Wn755c0+1q+10QLOZu6559aHoplmmsnoGvTAYR1gAWOMDzvssPhz0rX33XdfrInsawUKOEKIqRRv+l8F8JJD0BUGIYT4osxj4M4++2x9yBtLLLFEvE8BRwiZUdmhAnAIusIghBBf8C3UtlDAEUIo4AghpYYCri0UcISQSgm4k08+ORo+fLg+TAhpYSjg2kIBRwiphICz12S94IILzCoRhJCOQZnHwB144IH6kDdWX331eJ8CjhBSCQF36KGHRgcddJDZr/cmGCGk9bDfQtUvVKUFvJilef/99808bK+99pqOasiAAQOikSNHRp06ddJRhk8++cQEcPHFF8d15JAhQ6KHH344WmihhcxnTJKuqXftu+++G187cODA+BoKOEJIJQQcJtkcM2ZMzav3hJCOgS3gdF2UFkydpkirt+aff34zfYgg04hgjjgNJvgVXn755Xj/P//5T7T++j9OXaK/y54qBG+TLr744vFnl2sFCjhCSCUEHJgwYYI+RAjpAOQl4DAvm82ss84avfXWW3F9hvWfL7300tSJfOeYY46az/XWibavxZ/PadOmxZ8XXnjhaLnllos/a+xrcZ59rUABRwipjIAjhHRMRMCNGjXK1D3NhiSWXHLJeE3Riy66KOrVq5c5t2/fvkbQjRs3LnEpLQzdSEpXxBXO32233cx+//7943Ovu+66mutGjx4dXyskXYvr9LV9+vSJr6GAI4SUUsB1nW22uOJq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W3tylFErujLgDMMwDMMwjOoxA84wesSKFSv8U4ZhGIaRBDPgipXTvUZ/scUWW/inVHnnO9+ZXexEbgYl99n06dP904ZhGEYEZsD9l4985CPZPOyefPLJYsKECS5FS04cdNBB/il1tt56a/+UGuhr1113dUZcDm1J6vCZz3zGu6IHdTr//POLq666yr+kwmmnneaOX/ziF70revz1r391x6985SveFT2eeOIJ/5Qq3/3ud4vHH3+8OP300/1LalCfnPj3v//t7reTTjrJv6TCtGnTXF0OOOAA/5Iay5cvd8/bnOoUihlwq8jNCzdmzBj/lApiCKy22mreFR244W699dbaiudcVjlvueWW7vi6172uePjhh72r1TJjxgx3nDlzpnclDz73uc8VP/3pT/3TlXPCCSe440UXXeRd0eNtb3ubO2Lk5tAn/eQnP3FHDG/uvRyQwPef/exn9ReUwHhj8JYbc+bMKY4//nj/tBpXXHFFccQRRzi9nXnmmf7lyrnzzjvdceedd/au9A8Da8Ddfffdxdy5c4t//vOfxac+9aniox/9qHqHyc12//33F3vvvXfx8Y9/XL0+gni6cjDi6CwfeOCB4uCDDy7WWmstd077wbLbbrsVixcvLl784hcXm2++uX+5clhFte2227rXf//7353Bqwn6EWPyjW98Y7HXXnupt+3f/e53xYUXXlh84xvfKM455xz/sho33XRT8da3vrU4/PDDndGUA9///veLdddd16WHet7znudfrhT0RhL5Y445pjjllFOK//znP/5HVCDbAv3AySefXHznO9/xL1fOgQce6I702X/84x+L3//+994nqkUMNpL7Y8Rp3//0SWw6gB2AjOgDch3wtmLgDDgUh+sU3vCGN7jYJWAaVYt//OMfxZQpU5zRJiPwHHjooYeKd7/73e61eJg0ee5zn1tLU0MMnOa0hRiz48ePd0bbokWLvE/ogIHEw5aByWte8xr/sgrXXntt8dhjjxX77LNPce+99/qXVSB/JX2BjMK1HyhAW2K6kmn4H//4x/5lFdAbYCjl0Maln8Zgon/KQW8/+MEPnJzojzDAtcnF8C9DijHA8DZ6x8AZcHi4iH0h1uS+++5zo3AQo65qNt5442KbbbZxMQuPPPJI8elPf9r/SOUwbYqhdNhhhxX/+te/3GutOBimA3nQYpgQ84JH6ZWv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>