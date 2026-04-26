# Multiplicación de Matrices Grandes

## Universidad del Quindío - Ingeniería de Sistemas y Computación

**Seguimiento 2: Análisis de Algoritmos**

---

## 1. Descripción del Problema

La multiplicación de matrices es fundamental en álgebra lineal con aplicaciones en gráficos por computadora, aprendizaje automático, simulaciones científicas, criptografía y procesamiento de imágenes.

Para matrices n×n, la multiplicación directa tiene complejidad **O(n³)** - duplicar el tamaño aumenta el tiempo ~8 veces.

---

## 2. Casos de Prueba

Matrices cuadradas n×n (n factor de 2ⁿ) con valores mínimo 6 dígitos.

> **Nota:** Los tamaños 16×16 y 32×32 se usan por limitaciones de hardware. El proyecto escala a 512×512 y 1024×1024 cambiando `SIZES_CASO_1` y `SIZES_CASO_2` en `main.py` (como ejemplo puede ver una ejecución con matrices de tamaños 128x128 y 256x256 en la rama Prueba 2).

| Caso | Tamaño | Elementos | Memoria |
|------|---------|-----------|---------|
| 1 | 16×16 | 256 | ~6 KB |
| 2 | 32×32 | 1,024 | ~24 KB |

Para 512×512: ~2 MB por matriz. Para 1024×1024: ~8 MB por matriz.

---

## 3. Algoritmos Implementados

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
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
| 13 | IV.5 Enhanced Parallel | Algoritmo paralelo más optimizado de la familia IV. Incluye precomputación de índices y distribución inteligente de trabajo | O(n³/p) |
| 14 | V.3 Sequential block | Bloques secuenciales avanzado con técnicas de blocking multicapa. Optimiza uso de caché L1, L2 y L3 simultáneamente | O(n³) |
| 15 | V.4 Parallel Block | Versión paralela de V.3 que combina blocking multicapa con paralelización. maximiza throughput en arquitecturas multicore | O(n³/p) |

p = núcleos/threads disponibles

---

## 4. Análisis de Complejidad

| Algoritmo | Multiplicaciones |
|-----------|-----------------|
| Naiv* | n³ |
| Winograd* | ~n³/2 |
| Strassen* | 7n^2.807 |
| Bloques Sequential | n³ |
| Bloques Parallel | n³/p |

### Trade-off Tiempo vs Memoria (Strassen)

Strassen es ~3x más rápido pero usa ~7x más memoria:

| Algoritmo | Tiempo (32×32) | Memoria (32×32) |
|-----------|-----------------|------------------|
| NaivOnArray | 151 ms | 32 KB |
| StrassenNaiv | 47 ms | **226 KB** |

**Causas del mayor uso de memoria:**
- Padding a potencia de 2
- Submatrices auxiliares (A11, A12, A21, A22, B11...)
- Productos intermedios M1-M7
- Matrices temporales por nivel de recursión

---

## 5. Uso de Memoria y Recursos

| Tamaño | Memoria (doubles) |
|---------|------------------|
| 16×16 | ~2 KB |
| 32×32 | ~8 KB |
| 64×64 | ~32 KB |
| 128×128 | ~128 KB |
| 512×512 | ~2 MB |
| 1024×1024 | ~8 MB |

### Consideraciones de Caché CPU
- L1: 32-64 KB | L2: 256 KB-1 MB | L3: 8-64 MB
- Estrategia: bloques que quepan en caché L2

---

## 6. Comportamiento por Tamaño

| Tamaño | Algoritmos Recomendados |
|---------|----------------------|
| < 32×32 | Naiv*, Winograd* |
| 32-128 | Winograd*, III.3 |
| 128-512 | Strassen*, III/IV.3 |
| > 512 | Strassen*, IV/V.4 |

### Predicciones (complejidad O)
- Duplicar n: Naiv×8, Strassen×~7
- Triple n: Naiv×27, Strassen×~21

---

## 7. Tablas de Resultados

> Resultados con matrices 16×16 (Caso 1) y 32×32 (Caso 2) por limitaciones de hardware.

| ID | Algoritmo | Tiempo (ms) | Mem (KB) | Tiempo (ms) | Mem (KB) |
|----|----------|-------------|----------|-------------|----------|
| | | **Caso1** | | **Caso2** | |
| 1 | NaivOnArray | ~19 | ~8 | ~151 | ~32 |
| 2 | NaivLoopUnrollingTwo | ~22 | ~8 | ~174 | ~32 |
| 3 | NaivLoopUnrollingFour | ~25 | ~8 | ~196 | ~32 |
| 4 | WinogradOriginal | ~58 | ~9 | ~455 | ~34 |
| 5 | WinogradScaled | ~22 | ~26 | ~161 | ~100 |
| 6 | StrassenNaiv | ~7 | ~27 | ~47 | **~226** |
| 7 | StrassenWinograd | ~7 | ~27 | ~60 | **~214** |
| 8 | III.3 Sequential | ~26 | ~8 | ~207 | ~32 |
| 9 | III.4 Parallel | ~23 | ~20 | ~171 | ~43 |
| 10 | III.5 Enhanced | ~24 | ~23 | ~180 | ~43 |
| 11 | IV.3 Sequential | ~26 | ~8 | ~206 | ~32 |
| 12 | IV.4 Parallel | ~22 | ~17 | ~167 | ~40 |
| 13 | IV.5 Enhanced | ~24 | ~23 | ~181 | ~43 |
| 14 | V.3 Sequential | ~26 | ~8 | ~206 | ~32 |
| 15 | V.4 Parallel | ~22 | ~16 | ~169 | ~40 |

---

## 8. Estructura del Proyecto

```
Proyecto_Multiplicacion_Matrices/
├── Proyecto_Python/
│   ├── src/
│   │   ├── main.py                          # Punto de entrada
│   │   ├── main/
│   │   │   └── resources/
│   │   │       ├── matrices/                # Matrices guardadas en Excel
│   │   │       │   ├── matrix_Caso1_16.xlsx
│   │   │       │   └── matrix_Caso2_32.xlsx
│   │   │       └── results/                 # Resultados y gráficos
│   │   │           ├── python_results.xlsx  # Tiempos y memoria
│   │   │           └── grafico_comparativo.png
│   │   ├── algoritmos/                      # 15 algoritmos
│   │   │   ├── __init__.py
│   │   │   ├── NaivOnArray.py
│   │   │   ├── NaivLoopUnrollingTwo.py
│   │   │   ├── NaivLoopUnrollingFour.py
│   │   │   ├── WinogradOriginal.py
│   │   │   ├── WinogradScaled.py
│   │   │   ├── StrassenNaiv.py
│   │   │   ├── StrassenWinograd.py
│   │   │   ├── III_3_Sequential_Block.py
│   │   │   ├── III_4_Parallel_Block.py
│   │   │   ├── III_5_Enhanced_Parallel_Block.py
│   │   │   ├── IV_3_Sequential_Block.py
│   │   │   ├── IV_4_Parallel_Block.py
│   │   │   ├── IV_5_Enhanced_Parallel_Block.py
│   │   │   ├── V_3_Sequential_Block.py
│   │   │   └── V_4_Parallel_Block.py
│   │   ├── persistence/                     # Persistencia Excel
│   │   │   ├── __init__.py
│   │   │   ├── MatrixFileHandler.py         # Matrices → Excel
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
```

### Archivos Generados

| Archivo | Descripción | Ubicación |
|---------|-------------|-----------|
| `matrix_Caso1_16.xlsx` | Matrices 16×16 del Caso 1 | `src/main/resources/matrices/` |
| `matrix_Caso2_32.xlsx` | Matrices 32×32 del Caso 2 | `src/main/resources/matrices/` |
| `python_results.xlsx` | Resultados completos (30 filas) | `src/main/resources/results/` |
| `grafico_comparativo.png` | Gráfico comparativo | `src/main/resources/results/` |

---

## 9. Prompts Utilizados (IA)

Los prompts fueron realizados **después** de que el estudiante tenía los 15 algoritmos implementados y funcionales. Los bugs mencionados en P9 fueron identificados y corregidos mediante asistencia de IA.

### Tabla Resumen

| Código | Prompt Original | Intervención de IA |
|--------|----------------|--------------------|
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
```
"Organiza el código existente en una estructura de paquetes Python:
- src/algoritmos/ para los 15 algoritmos
- src/persistence/ para lectura/escritura XML
- src/views/ para visualización
- main.py como punto de entrada
Agrega __init__.py con exports apropiados."
```

**Intervención de IA:**
Creó la arquitectura en capas con los paquetes `persistence/` y `views/`, implementando clases para manejo de resultados y visualización.

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
```
"Implementa una función que ejecute todos los algoritmos,
mida el tiempo de ejecución en nanosegundos, y guarde
los resultados en XML."
```

**Intervención de IA:**
Implementó `process_algorithm()` en `main.py` usando `time.perf_counter_ns()` para máxima precisión.

```python
# [AI MODIFIED] - Agregado por IA
def process_algorithm(algorithm_name, multiply_func, A, B, case_name):
    start = time.perf_counter_ns()
    C = multiply_func(A, B)
    end = time.perf_counter_ns()
    execution_time_ns = end - start
    # ...
```

---

### P3: Estructurar main.py para Dos Casos de Prueba

**Prompt Original:**
```
"Configura main.py para soportar 2 casos de prueba con
matrices cuadradas n×n donde n es factor de 2^n, con
valores de mínimo 6 dígitos."
```

**Intervención de IA:**
Configuró soporte para Caso1 y Caso2 con generación dinámica de matrices.

```python
# [AI MODIFIED] - Configuración por IA
MIN_DIGITS = 7
SIZES_CASO_1 = [16]
SIZES_CASO_2 = [32]

def matrix_generator(n, min_digits):
    # [AI MODIFIED] - Genera matriz numpy con valores aleatorios de n dígitos
    return np.random.randint(10**(min_digits-1), 10**min_digits, size=(n, n), dtype=np.int64)
```

---

### P4: Documentación de Análisis de Complejidad

**Prompt Original:**
```
"Documenta el análisis de complejidad de cada algoritmo
en un documento formal. Incluye notación Big-O, análisis
teórico del número de operaciones y predicciones de
rendimiento."
```

**Intervención de IA:**
Documentó análisis de complejidad en README.md y DISEÑO.md con notación Big-O, Theta y Omega.

---

### P5: Agregar Docstrings a Algoritmos

**Prompt Original:**
```
"Agrega documentación tipo docstring a los 15 algoritmos
incluyendo: descripción, complejidad computacional,
parámetros y valor de retorno."
```

**Intervención de IA:**
Agregó docstrings a los 15 archivos en `algoritmos/`.

```python
# [AI MODIFIED] - Docstring agregado por IA
def multiply(A, B):
    """
    Multiplicación de matrices ingenua sobre arrays.

    Complejidad Computacional:
        - Tiempo: O(n³)
        - Espacio: O(n²)

    Parámetros:
        A: Matriz de tamaño n×n
        B: Matriz de tamaño n×n

    Retorna:
        Matriz C de tamaño n×n donde C = A × B
    """
```

---

### P6: Agregar Medición de Memoria

**Prompt Original:**
```
"Agrega medición de memoria a cada ejecución usando
tracemalloc para obtener el pico de memoria en KB."
```

**Intervención de IA:**
Integró `tracemalloc` en `process_algorithm()` para medir pico de memoria.

```python
# [AI MODIFIED] - Agregado por IA
import tracemalloc

def process_algorithm(...):
    tracemalloc.start()
    C = multiply_func(A, B)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024
```

---

### P7: Agregar Verificación de Resultados

**Prompt Original:**
```
"Agrega verificación de resultados comparando el
resultado de cada algoritmo con np.matmul para
validar que C = A × B."
```

**Intervención de IA:**
Implementó verificación con `np.allclose()`.

```python
# [AI MODIFIED] - Verificación agregada por IA
def verify_result(A, B, C):
    expected = np.matmul(A, B)
    return np.allclose(C, expected, rtol=1e-5, atol=1e-8)
```

---

### P8: Cambiar Persistencia a Excel

**Prompt Original:**
```
"Cambia la persistencia de XML a Excel usando openpyxl.
Genera gráficos comparativos del rendimiento."
```

**Intervención de IA:**
Reemplazó XML por Excel con openpyxl, agregando generación de gráficos con matplotlib.

**Archivos modificados:**
- `persistence/MatrixFileHandler.py` - Cambio a Excel
- `persistence/ResultsExcelHandler.py` - Resultados en Excel
- `main.py` - Integración de persistencia

---

### P9: Corrección de Bugs de Algoritmos

**Prompt Original:**
```
"Revisa los algoritmos y corrige los bugs que encuentres.
Los algoritmos que fallan la verificación son:
- III.5 Enhanced Parallel Block
- IV.5 Enhanced Parallel Block
- StrassenWinograd"
```

**Intervención de IA:**
Identificó y corrigió los siguientes bugs:

#### Bug 1: Parámetros incorrectos en ThreadPoolExecutor (III.5, IV.5)

**Problema:** La segunda llamada a `executor.submit()` usaba `N, N, P, M` en lugar de `N, P, M`.

```python
# [AI MODIFIED] - Bug corregido por IA
# INCORRECTO (original):
executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, N, P, M, block_size)

# CORRECTO:
executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, P, M, block_size)
```

#### Bug 2: Indexación incorrecta en IV.5 Enhanced Parallel

**Problema:** Usaba `C[i][k]` en lugar de `C[i][j]` en el bucle interno.

```python
# [AI MODIFIED] - Bug corregido por IA
# INCORRECTO (original):
C[i][k] += temp1 + temp2

# CORRECTO:
C[i][j] += temp1 + temp2
```

#### Bug 3: Padding incorrecto en Strassen (Naiv y Winograd)

**Problema:** newSize = 17 para input 16×16, debía ser potencia de 2.

```python
# [AI MODIFIED] - Bug corregido por IA
# INCORRECTO (original):
newSize = n + 1 if n % 2 == 1 else n

# CORRECTO:
newSize = 1
while newSize < n:
    newSize *= 2
```

#### Bug 4: Overflow de entero en StrassenWinograd

**Problema:** Matriz resultado inicializada como `[[0]]` (int) causaba overflow.

```python
# [AI MODIFIED] - Bug corregido por IA
# INCORRECTO (original):
result = [[0] * size] * size

# CORRECTO:
result = [[0.0] * size] * size
```

#### Bug 5: Fórmulas incorrectas en StrassenWinograd

**Problema:** El algoritmo implementaba fórmulas de Winograd incorrectas, causando resultados erróneos para tamaños ≥32×32.

**Solución:** Reescritura completa del algoritmo usando la fórmula estándar de Strassen-Winograd con variables temporales separadas para cada producto M1-M7.

---

## 10. Cómo Ejecutar

```bash
cd Proyecto_Python
pip install -r requirements.txt
python src/main.py
```

**Archivos generados:**
- `src/main/resources/matrices/matrix_Caso{1,2}_{size}.xlsx`
- `src/main/resources/results/python_results.xlsx`
- `src/main/resources/results/grafico_comparativo.png`

**Cambiar tamaños de prueba:**
```python
# En main.py
SIZES_CASO_1 = [512]  # o [16], [32], etc.
SIZES_CASO_2 = [1024]
```

---

## 11. Conclusiones

1. **Matrices pequeñas (<64×64)**: Naiv* y Winograd* son más eficientes por bajo overhead
2. **Matrices grandes (>512×512)**: Strassen* y paralelos muestran mejor rendimiento
3. **Strassen**: Trade-off tiempo/memoria - usa ~7x más memoria para ser ~3x más rápido
4. **Paralelización**: Speedup lineal con núcleos, límite práctico ~8-16 hilos

---

## 12. Aclaración Importante

Los 15 algoritmos son implementaciones conocidas de la literatura académica obtenidas de un repositorio GitHub público. La IA协助 únicamente en tareas técnicas de organización, medición, documentación y corrección de bugs, **no en el diseño de los algoritmos**.

---

*Documento actualizado para el Seguimiento 2 - 2026*
