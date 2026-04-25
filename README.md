# Documento de diseño: Multiplicación de Matrices Grandes

---

## Propósito del Proyecto

Implementar y analizar algoritmos que permitan la multiplicación de matrices grandes mediante **algoritmos iterativos** y **algoritmos divide y vencerás** para el Seguimiento 2 de Análisis de Algoritmos.

---

## 1. Descripción del Problema

La multiplicación de matrices es una operación fundamental en álgebra lineal con aplicaciones en:
- Gráficos por computadora
- Aprendizaje automático (redes neuronales)
- Simulaciones científicas
- Criptografía
- Procesamiento de imágenes

Para matrices cuadradas de tamaño n×n, la multiplicación directa tiene complejidad **O(n³)**, lo que significa que al duplicar el tamaño de la matriz, el tiempo de ejecución aumenta aproximadamente **8 veces**.

---

## 2. Casos de Prueba

Matrices cuadradas n×n donde n es potencia de 2, con valores aleatorios de mínimo 6 dígitos.

### Tamaños configurados en esta rama

| Caso | Dimensión | Descripción | Elementos | Memoria Aprox. |
|------|----------|-------------|-----------|----------------|
| 1 | **128×128 (2⁷)** | Caso base de comparación | 16,384 | ~128 KB |
| 2 | **256×256 (2⁸)** | Caso ampliado de comparación | 65,536 | ~512 KB |

### Justificación

La rama `Prueba-2` quedó ajustada para ejecutar pruebas intermedias que siguen siendo suficientemente exigentes, pero todavía viables en el hardware disponible.

| Factor | Impacto |
|--------|---------|
| **CPU** | Los algoritmos O(n³) en Python puro ya superan el minuto por algoritmo en 256×256 |
| **Memoria RAM** | Los algoritmos de Strassen elevan el consumo temporal de memoria al crear submatrices auxiliares |
| **Tiempo de ejecución** | La corrida completa de los 15 algoritmos sobre ambos casos toma varios minutos |

### Configuración actual en `main.py`

```python
SIZES_CASO_1 = [128]
SIZES_CASO_2 = [256]
```

### Cálculo de memoria

Para matrices `float64` (8 bytes por elemento):
- **128×128**: 128 × 128 × 8 = **131,072 bytes** (~128 KB por matriz)
- **256×256**: 256 × 256 × 8 = **524,288 bytes** (~512 KB por matriz)

Con dos matrices de entrada y una de resultado:
- Caso 1: ~384 KB totales
- Caso 2: ~1.5 MB totales

---

## 3. Algoritmos Implementados

### 3.1 Algoritmos Básicos (Iterativos)

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 1 | **NaivOnArray** | Triple bucle ingenuo | O(n³) |
| 2 | **NaivLoopUnrollingTwo** | Desenrollado de lazos ×2 | O(n³) |
| 3 | **NaivLoopUnrollingFour** | Desenrollado de lazos ×4 | O(n³) |
| 4 | **WinogradOriginal** | Optimización de Winograd | O(n³) |
| 5 | **WinogradScaled** | Winograd con escalado | O(n³) |

### 3.2 Algoritmos Divide y Vencerás

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 6 | **StrassenNaiv** | Algoritmo de Strassen base | O(n^log₂7) ≈ O(n^2.807) |
| 7 | **StrassenWinograd** | Strassen con optimizaciones | O(n^log₂7) ≈ O(n^2.807) |

### 3.3 Algoritmos por Bloques (Nivel 3)

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 8 | **III.3 Sequential block** | Bloques secuenciales | O(n³) |
| 9 | **III.4 Parallel Block** | Bloques paralelos | O(n³/p) |
| 10 | **III.5 Enhanced Parallel Block** | Bloques paralelos optimizados | O(n³/p) |

### 3.4 Algoritmos por Bloques (Nivel 4)

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 11 | **IV.3 Sequential block** | Bloques secuenciales optimizados | O(n³) |
| 12 | **IV.4 Parallel Block** | Bloques paralelos optimizados | O(n³/p) |
| 13 | **IV.5 Enhanced Parallel Block** | Bloques paralelos mejorados | O(n³/p) |

### 3.5 Algoritmos por Bloques (Nivel 5)

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 14 | **V.3 Sequential block** | Bloques secuenciales avanzados | O(n³) |
| 15 | **V.4 Parallel Block** | Bloques paralelos avanzados | O(n³/p) |

Donde **p** = número de núcleos/threads disponibles.

---

## 4. Análisis de Complejidad Algorítmica

### Tabla Resumen de Complejidad

| Algoritmo | O(n³) | O(n^2.807) | O(n³/p) | Multiplicaciones |
|----------|-------|-------------|---------|-----------------|
| NaivOnArray | ✓ | | | n³ |
| NaivLoopUnrollingTwo | ✓ | | | n³ |
| NaivLoopUnrollingFour | ✓ | | | n³ |
| WinogradOriginal | ✓ | | | ~n³/2 |
| WinogradScaled | ✓ | | | | ~n³/2 |
| StrassenNaiv | | ✓ | | 7n^2.807 |
| StrassenWinograd | | ✓ | | 7n^2.807 |
| III.3 Sequential block | ✓ | | | n³ |
| III.4 Parallel Block | | | ✓ | n³/p |
| III.5 Enhanced Parallel | | | ✓ | | n³/p |
| IV.3 Sequential block | ✓ | | | n³ |
| IV.4 Parallel Block | | | ✓ | n³/p |
| IV.5 Enhanced Parallel | | | ✓ | n³/p |
| V.3 Sequential block | ✓ | | | n³ |
| V.4 Parallel Block | | | ✓ | n³/p |

### Análisis Teórico de Rendimiento

#### Algoritmos Iterativos (Naiv*, Winograd*)
- **Ventaja**: Simplicidad, bajo overhead
- **Desventaja**: n³ multiplicaciones exactas
- **Rendimiento constante** independientemente del tamaño

#### Algoritmos Divide y Vencerás (Strassen*)
- **Ventaja**: Menos multiplicaciones asintóticamente (n^2.807 vs n³)
- **Desventaja**: Overhead significativo por recursión y asignación de memoria
- **Rendimiento mejorado** para matrices grandes (>128×128)

#### Algoritmos por Bloques (III/IV/V*)
- **Ventaja**: Mejor uso de caché CPU, paralelización
- **Desventaja**: Overhead de sincronización en versiones paralelas
- **Rendimiento depende** del tamaño de bloque y número de hilos

---

## 5. Uso de Memoria y Recursos del Sistema

### 5.1 Análisis de Memoria

| Tamaño | Elementos | Memoria (doubles) | Memoria (float32) |
|--------|----------|------------------|------------------|
| 8×8 | 64 | 512 bytes | 256 bytes |
| 16×16 | 256 | 2 KB | 1 KB |
| 32×32 | 1,024 | 8 KB | 4 KB |
| 64×64 | 4,096 | 32 KB | 16 KB |
| 128×128 | 16,384 | 128 KB | 64 KB |
| 256×256 | 65,536 | 512 KB | 256 KB |
| 512×512 | 262,144 | 2 MB | 1 MB |
| 1024×1024 | 1,048,576 | 8 MB | 4 MB |

### 5.2 Consideraciones de Caché CPU

Los procesadores modernos tienen múltiples niveles de caché:
- **L1**: 32-64 KB (por núcleo)
- **L2**: 256 KB - 1 MB (por núcleo)
- **L3**: 8-64 MB (compartido)

**Estrategia de optimización**: Dividir matrices en bloques que quepan en caché L2.

### 5.3 Paging y Swap

Para matrices grandes que no caben en RAM:
- **Linux**: `vm.swappiness`, `/proc/sys/vm`
- **Windows**: Configuración de paging en Sistema > Opciones avanzadas

**Señales de paging**:
- Tiempo de ejecución altamente variable
- Disco duro en actividad constante

### 5.4 Trade-off: Tiempo vs Memoria (Strassen)

Los algoritmos de Strassen presentan una característica importante: **intercambian tiempo por espacio**.

#### Resultados observados (256×256)

| Algoritmo | Tiempo (ms) | Memoria (KB) | Observación |
|-----------|-------------|-------------|-------------|
| NaivOnArray | 78982.85 | 2090.0 KB | Base |
| StrassenNaiv | 22750.54 | **13209.6 KB** | **~3.5x más rápido, pero con mucho más uso de memoria** |
| StrassenWinograd | 23502.41 | **12492.8 KB** | **~3.4x más rápido, con alto overhead de memoria** |

#### Análisis del Trade-off

**Strassen es ~3.5x más rápido** pero usa **~6x más memoria** que los algoritmos naïve en 256×256.

| Aspecto | Naiv* | Strassen* |
|---------|-------|-----------|
| Tiempo | Alto | Bajo (para matrices grandes) |
| Memoria | Bajo | Alto |
| Multiplicaciones | n³ | 7n^2.807 |
| Overhead | Mínimo | Padding, recursion, auxiliares |

#### ¿Por qué Strassen usa más memoria?

1. **Padding a potencia de 2**: El algoritmo garantiza dimensiones convenientes para la recursión
2. **Submatrices auxiliares**: A11, A12, A21, A22, B11, B12, B21, B22
3. **Productos intermedios**: M1, M2, M3, M4, M5, M6, M7
4. **Matrices resultado temporales**: Para cada nivel de recursión

#### Conclusión

Para sistemas con **memoria limitada**, los algoritmos naïve o por bloques pueden ser preferibles. Para sistemas con ** CPUs potentes y memoria suficiente**, Strassen ofrece mejor rendimiento en matrices grandes.

---

## 6. Comportamiento por Tamaño de Entrada

### 6.1 Análisis Teórico

| Tamaño | Algoritmos Recomendados | Razón |
|--------|------------------------|-------|
| < 32×32 | Naiv*, Winograd* | Overhead bajo, simples |
| 32-128 | Winograd*, III.3 | Mejor balance |
| 128-512 | Strassen*, III/IV.3 | Beneficio de divide y vencerás |
| > 512 | Strassen*, IV/V.4 | Optimización de caché |

### 6.2 Predicciones de Rendimiento

Basado en complejidad O(n³):
- Duplicar n multiplica tiempo por **8**
- Triple n multiplica tiempo por **27**

Basado en O(n^2.807) (Strassen):
- Duplicar n multiplica tiempo por **~7**
- Triple n multiplica tiempo por **~21**

### 6.3 Puntos de Cruce

| Comparación | Punto de Cruce Aprox. |
|------------|----------------------|
| NaivOnArray vs StrassenNaiv | ~64×64 |
| NaivOnArray vs WinogradOriginal | ~8×8 |
| Sequential vs Parallel | Depende de hilos |

---

## 7. Tablas de Resultados

> **Nota:** Los siguientes resultados corresponden a la ejecución real de esta rama con matrices **128×128 (Caso 1)** y **256×256 (Caso 2)**.

### Tabla 1: Tiempos de Ejecución y Memoria

| ID | Algoritmo | Caso 1 Tiempo (ms) | Caso 1 Memoria | Caso 2 Tiempo (ms) | Caso 2 Memoria |
|----|----------|--------------------|----------------|--------------------|----------------|
| 1 | NaivOnArray | 9669.754 | 517.9 KB | 78982.851 | 2.04 MB |
| 2 | NaivLoopUnrollingTwo | 9502.785 | 517.9 KB | 75822.770 | 2.04 MB |
| 3 | NaivLoopUnrollingFour | 9541.205 | 517.9 KB | 77576.543 | 2.04 MB |
| 4 | WinogradOriginal | 11233.782 | 526.0 KB | 85616.510 | 2.05 MB |
| 5 | WinogradScaled | 4022.539 | 1.53 MB | 31030.600 | 6.11 MB |
| 6 | StrassenNaiv | 3214.351 | 3.32 MB | 22750.538 | 12.90 MB |
| 7 | StrassenWinograd | 3301.112 | 3.12 MB | 23502.408 | 12.20 MB |
| 8 | III.3 Sequential block | 10110.369 | 516.6 KB | 81788.459 | 2.04 MB |
| 9 | III.4 Parallel Block | 10258.631 | 543.7 KB | 80397.801 | 2.04 MB |
| 10 | III.5 Enhanced Parallel Block | 10067.390 | 529.0 KB | 81636.835 | 2.04 MB |
| 11 | IV.3 Sequential block | 10031.176 | 517.2 KB | 80388.906 | 2.04 MB |
| 12 | IV.4 Parallel Block | 10000.218 | 524.0 KB | 82182.180 | 2.04 MB |
| 13 | IV.5 Enhanced Parallel Block | 10238.998 | 529.0 KB | 81385.720 | 2.04 MB |
| 14 | V.3 Sequential block | 9935.476 | 517.2 KB | 83677.251 | 2.04 MB |
| 15 | V.4 Parallel Block | 9886.084 | 523.8 KB | 79055.443 | 2.04 MB |

### Hallazgos principales

- `StrassenNaiv` fue el algoritmo más rápido en ambos casos.
- `StrassenWinograd` quedó muy cerca en tiempo, pero mantuvo un consumo alto de memoria.
- Los algoritmos naïve y por bloques se agruparon cerca de los 9.5-11.2 s para 128×128 y 75-86 s para 256×256.
- `WinogradScaled` fue el mejor compromiso entre tiempo y complejidad de implementación fuera de la familia Strassen.

---

## 8. Estructura del Proyecto

```
Proyecto_Multiplicacion_Matrices/
├── Proyecto_Python/
│   ├── src/
│   │   ├── main.py                      # Punto de entrada
│   │   ├── algoritmos/                   # 15 algoritmos
│   │   │   ├── __init__.py               # Exports
│   │   │   ├── NaivOnArray.py             # Algoritmo 1
│   │   │   ├── NaivLoopUnrollingTwo.py   # Algoritmo 2
│   │   │   ├── NaivLoopUnrollingFour.py   # Algoritmo 3
│   │   │   ├── WinogradOriginal.py        # Algoritmo 4
│   │   │   ├── WinogradScaled.py          # Algoritmo 5
│   │   │   ├── StrassenNaiv.py           # Algoritmo 6
│   │   │   ├── StrassenWinograd.py       # Algoritmo 7
│   │   │   ├── III_3_Sequential_Block.py # Algoritmo 8
│   │   │   ├── III_4_Parallel_Block.py   # Algoritmo 9
│   │   │   ├── III_5_Enhanced_Parallel_Block.py # Algoritmo 10
│   │   │   ├── IV_3_Sequential_Block.py  # Algoritmo 11
│   │   │   ├── IV_4_Parallel_Block.py   # Algoritmo 12
│   │   │   ├── IV_5_Enhanced_Parallel_Block.py # Algoritmo 13
│   │   │   ├── V_3_Sequential_Block.py   # Algoritmo 14
│   │   │   └── V_4_Parallel_Block.py     # Algoritmo 15
│   │   ├── persistence/                  # Persistencia Excel
│   │   │   ├── ResultData.py
│   │   │   ├── ResultFileHandler.py
│   │   │   ├── Results.py
│   │   │   ├── ResultsManager.py
│   │   │   ├── MatrixFileHandler.py
│   │   │   └── MatrixWrapper.py
│   │   └── views/                       # Visualización
│   │       └── ResultsViewer.py
│   ├── .gitignore
│   └── requirements.txt
├── .gitignore
├── README.md
└── DISEÑO.md
```

---

## 9. Prompts Utilizados en el Desarrollo

Documentación técnica de las iteraciones con IA que modificaron el proyecto. **Nota:** Los prompts documentados aquí fueron realizados **después** de que el estudiante ya tenía los 15 algoritmos implementados y funcionales.

### 9.1 Tabla Resumen de Prompts

| Código | Descripción Breve | Decisión Algorítmica Principal |
|--------|-------------------|-------------------------------|
| **P1** | Organizar código en paquetes modulares | Arquitectura en capas: algoritmos, persistence, views |
| **P2** | Implementar medición de tiempos | Uso de time.perf_counter_ns() y persistencia Excel |
| **P3** | Estructurar main.py para 2 casos | Soporte para Caso1 (128×128) y Caso2 (256×256) |
| **P4** | Documentar análisis de complejidad | Análisis teórico y documentación formal |
| **P5** | Agregar docstrings a algoritmos | Documentación tipo docstring a los 15 algoritmos |
| **P6** | Agregar medición de memoria | Uso de tracemalloc para medir pico de memoria |
| **P7** | Agregar verificación de resultados | Validación C = A × B usando NumPy como referencia |
| **P8** | Cambiar persistencia a Excel | Reemplazo de XML por Excel con openpyxl |
| **P9** | Corregir bugs de algoritmos | Identificó y corrigió bugs en III.5, IV.5, StrassenWinograd |

*En esta rama, los tamaños de trabajo quedaron fijados en 128×128 y 256×256 para permitir ejecuciones completas con tiempos manejables.

### 9.2 Detalle de Prompts

---

#### P1: Organizar Código en Paquetes Modulares

**Prompt Original:**
```
"Organiza el código existente en una estructura de paquetes Python:
- src/algoritmos/ para los 15 algoritmos
- src/persistence/ para lectura/escritura XML
- src/views/ para visualización
- main.py como punto de entrada
Agrega __init__.py con exports apropiados."
```

**Decisión Algorítmica:**
- Arquitectura en capas separada:
  - **Capa de algoritmos**: Lógica pura de multiplicación (ya existente)
  - **Capa de persistencia**: Excel (lectura/escritura de matrices y resultados con openpyxl)
  - **Capa de views**: Visualización con tkinter/matplotlib
- Se implementó el patrón DataManager para resultados:
  - `Results`: Contenedor de lista de resultados
  - `ResultData`: Dataclass con size, algorithm, language, executionTime, case, rows, cols, memory_kb, verified
- Se creó `ResultsManager` para combinar resultados de múltiples archivos Excel

**Archivos Creados por IA:**
- `algoritmos/__init__.py`
- `persistence/__init__.py`
- `views/__init__.py`
- `persistence/ResultData.py`
- `persistence/Results.py`
- `persistence/ResultFileHandler.py`
- `persistence/ResultsManager.py`
- `persistence/MatrixFileHandler.py`
- `persistence/MatrixWrapper.py`
- `views/ResultsViewer.py`

---

#### P2: Implementar Medición de Tiempos

**Prompt Original:**
```
"Implementa una función que ejecute todos los algoritmos,
mida el tiempo de ejecución en nanosegundos, y guarde
los resultados en XML."
```

**Decisión Algorítmica:**
- Se implementó `process_algorithm()` en main.py que:
  - Mide tiempo con `time.perf_counter_ns()` (precisión de nanosegundos)
  - Registra resultados en Excel con metadatos completos (size, algorithm, case, rows, cols, memory_kb, verified)
  - Usa el caso de prueba "Caso1" o "Caso2" para diferenciar ejecuciones

**Archivos Editados por IA:**
- `main.py` (función `process_algorithm()`)
- `persistence/ResultFileHandler.py`

---

#### P3: Estructurar main.py para Dos Casos de Prueba

**Prompt Original:**
```
"Configura main.py para soportar 2 casos de prueba con
matrices cuadradas n×n donde n es factor de 2^n, con
valores de mínimo 6 dígitos."
```

**Decisión Algorítmica:**
- Configuración flexible con constantes:
  - `MIN_DIGITS = 7` (valores de 1,000,000 a 9,999,999)
  - `SIZES_CASO_1 = [128]` → 128×128 = 2⁷
  - `SIZES_CASO_2 = [256]` → 256×256 = 2⁸
- **Nota:** La rama `Prueba-2` quedó calibrada para esos dos tamaños y toda la documentación fue actualizada en consecuencia.
- Funciones de generación y persistencia:
  - `matrix_generator(n, min_digits)`: Genera matriz numpy con valores aleatorios de n dígitos
  - `save_matrix()` / `load_matrix()`: Persistencia Excel de matrices
  - `run_case()`: Ejecuta todos los algoritmos para un caso

**Archivos Editados por IA:**
- `main.py` (completamente reescrito)

---

#### P4: Documentación de Análisis de Complejidad

**Prompt Original:**
```
"Crea documentación técnica formal:
- Análisis de complejidad de cada algoritmo
- Uso de memoria y consideraciones de caché
- Comportamiento según tamaño de entrada
- Prompts utilizados durante el desarrollo"
```

**Decisión Algorítmica:**
- Se documentó formalmente:
  - Tablas de complejidad O(n³), O(n^2.807), O(n³/p)
  - Predicciones de rendimiento basadas en análisis teórico
  - Puntos de cruce donde un algoritmo supera a otro
  - Análisis de comportamiento por tamaño de entrada
- Se creó el documento `DISEÑO.md` con especificaciones formales

**Archivos Editados/Creados por IA:**
- `README.md` (completamente reescrito)
- `DISEÑO.md` (creado)

---

#### P5: Agregar Docstrings a Algoritmos

**Prompt Original:**
```
"Agrega docstrings completos a los 15 algoritmos con:
- Complejidad computacional
- Descripción del algoritmo
- Parámetros y retorno
- Referencia bibliográfica"
```

**Decisión Algorítmica:**
- Se agregaron docstrings a cada algoritmo incluyendo:
  - Complejidad temporal y espacial
  - Número de multiplicaciones escalares
  - Descripción de la técnica utilizada
  - Parámetros de entrada y salida
  - Referencia bibliográfica (Strassen 1969, Winograd 1968)

**Archivos Editados por IA:**
- Los 15 archivos en `algoritmos/`

---

#### P6: Agregar Medición de Memoria

**Prompt Original:**
```
Agrega medición de memoria a cada algoritmo usando tracemalloc.
Muestra el pico de memoria en KB en los resultados.
```

**Decisión Algorítmica:**
- Se agregó `tracemalloc.start()` antes de cada ejecución y `tracemalloc.stop()` después
- Se calcula `peak = tracemalloc.get_traced_memory()[1]` para el pico de memoria
- Se incluye columna "Memoria (KB)" en Excel con valores en kilobytes
- Se genera segundo gráfico para сравнениe de memoria

**Archivos Editados por IA:**
- `main.py` (funciones `process_algorithm()`)
- `persistence/ResultsExcelHandler.py`

---

#### P7: Agregar Verificación de Resultados

**Prompt Original:**
```
Agrega verificación de que los resultados de cada algoritmo
son correctos comparando con NumPy.matmul. Muestra [OK] o [FAIL]
en la tabla de resultados.
```

**Decisión Algorítmica:**
- Se implementó `verify_result(matrix_a, matrix_b, result)` usando `np.allclose()`
- Cada algoritmo ejecuta y verifica antes de guardar resultados
- Se incluye columna "Verificado" en Excel con "SI" o "NO"
- Se muestra ✓ [OK] o ✗ [FAIL] en terminal durante ejecución

**Archivos Editados por IA:**
- `main.py` (función `verify_result()`)

---

#### P8: Cambiar Persistencia a Excel

**Prompt Original:**
```
Reemplaza la persistencia XML por Excel usando openpyxl.
Genera archivos .xlsx con formato profesional y gráficos embebidos.
```

**Decisión Algorítmica:**
- Se crearon `MatrixFileHandler.py` y `ResultsExcelHandler.py` para Excel
- Se generó gráfico de barras comparativo con matplotlib
- Se embebió imagen PNG dentro del Excel
- Se usó formato profesional con headers, bordes y colores

**Archivos Creados por IA:**
- `persistence/MatrixFileHandler.py`
- `persistence/ResultsExcelHandler.py`

**Archivos Editados por IA:**
- `main.py`
- `README.md` (sección de estructura actualizada)

---

### 9.3 Decisiones de Diseño (Implementadas por el Estudiante)

Las siguientes decisiones fueron tomadas por el estudiante antes de interactuar con la IA:

| Decisión | Algoritmos Afectados | Justificación |
|----------|---------------------|---------------|
| Interfaz unificada `multiply()` | Todos | Facilita testing y comparación directa |
| block_size = N | III, IV, V | Simplifica implementación, bloque = matriz completa |
| ThreadPoolExecutor | III.4, IV.4, V.4 | Paralelismo por división de filas |
| max_workers=2 | III.5, IV.5, V.5 | Versiones "Enhanced" con workers fijos para estabilidad |

---

## 10. Cómo Ejecutar el Proyecto

### 10.1 Requisitos
- Python 3.8+
- numpy>=1.24.0
- matplotlib>=3.7.0
- openpyxl>=3.1.0
- tkinter (incluido en Python)

### 10.2 Instalación
```bash
cd Proyecto_Python
pip install -r requirements.txt
```

requirements.txt incluye:
- numpy>=1.24.0
- matplotlib>=3.7.0
- openpyxl>=3.1.0

### 10.3 Ejecución

1. **Configurar tamaños** en `src/main.py`:
```python
SIZES_CASO_1 = [128]  # Caso 1: 128×128
SIZES_CASO_2 = [256]  # Caso 2: 256×256
```

2. **Ejecutar**:
```bash
cd Proyecto_Python
python src/main.py
```

**Nota:** El programa ejecuta automáticamente ambos casos y genera los archivos Excel con gráficos.

### 10.4 Ver Resultados

Los resultados se guardan en formato Excel:
- Matrices: `src/main/resources/matrices/matrix_[Caso]_[Tamaño].xlsx`
- Tiempos: `src/main/resources/results/python_results.xlsx`
- Gráfico PNG: `src/main/resources/results/grafico_comparativo.png`

Archivos generados:
| Archivo | Descripción |
|---------|-------------|
| `matrix_Caso1_128x128.xlsx` | Matrices del caso 1 (Hojas: Matriz A, Matriz B, Info) |
| `matrix_Caso2_256x256.xlsx` | Matrices del caso 2 (Hojas: Matriz A, Matriz B, Info) |
| `python_results.xlsx` | Tiempos de ejecución (Hojas: Caso1, Caso2, Comparativa, Gráfico) |
| `grafico_comparativo.png` | Imagen del gráfico comparativo |

El archivo `python_results.xlsx` contiene:
- **Hoja "Caso1"**: Tiempos para matrices 128×128
- **Hoja "Caso2"**: Tiempos para matrices 256×256
- **Hoja "Comparativa"**: Tabla resumen comparando ambos casos
- **Hoja "Gráfico"**: Imagen del gráfico de barras comparativo

---

## 11. Resultados Observados

La ejecución real de esta rama mostró el siguiente comportamiento general:

1. En **128×128**, `StrassenNaiv` y `StrassenWinograd` fueron claramente los más rápidos, con tiempos de ~3.2 s y ~3.3 s respectivamente.
2. En **256×256**, ambos algoritmos de Strassen mantuvieron la ventaja, con ~22.8 s y ~23.5 s, muy por debajo del rango de 75-86 s del resto de implementaciones O(n³).
3. `WinogradScaled` quedó como la mejor alternativa no recursiva, aunque con mayor consumo de memoria que los métodos naïve y por bloques.
4. Todas las ejecuciones terminaron con verificación correcta (`[OK]`) frente a `NumPy.matmul`.

---

## 12. Conclusiones

1. **Para matrices pequeñas (<64×64)**: Los algoritmos iterativos simples (Naiv*, Winograd*) son más eficientes debido al bajo overhead.

2. **Para matrices medianas y grandes (desde 128×128)**: Los algoritmos de Strassen mostraron la mejor relación tiempo/resultado en este entorno.

3. **Uso de memoria**: Los mejores tiempos vinieron acompañados de un costo mayor en memoria, especialmente en `StrassenNaiv` y `StrassenWinograd`.

4. **Paralelización**: Los algoritmos paralelos ofrecen speedup lineal con el número de núcleos, hasta un límite práctico de ~8-16 hilos.

5. **Futuras optimizaciones**: Considerar implementación en C/C++ o uso de GPUs para matrices >4096×4096.

---

## 13. Autores

Universidad del Quindío - Ingeniería de Sistemas y Computación

---

## 14. Licencia

Para uso académico - Universidad del Quindío

---

## 15. Declaración de Uso de Inteligencia Artificial

En cumplimiento de las políticas académicas de transparencia, se declara el uso de inteligencia artificial en las siguientes etapas del desarrollo.

### 15.1 Participación del Estudiante (Trabajo Propio)

El estudiante realizó de manera independiente las siguientes tareas:

| # | Actividad | Descripción | Evidencia |
|---|----------|-------------|-----------|
| A1 | Descarga de algoritmos | Se descargaron los algoritmos de multiplicación de matrices de un repositorio GitHub público | Código fuente con implementaciones originales |
| A2 | Adaptación de interfaz | Se adaptaron los algoritmos para cumplir con los requisitos del proyecto: interfaz unificada `multiply(A, B)` y soporte para matrices Python estándar | 15 archivos en `algoritmos/` |
| A3 | Selección de casos de prueba | Se definieron los tamaños 128×128 y 256×256 como casos de prueba de esta rama | Constantes `SIZES_CASO_1`, `SIZES_CASO_2` en main.py |
| A4 | Diseño de pruebas | Se diseñaron los casos de prueba y metodología de verificación | main.py: `run_case()`, `process_algorithm()` |

### 15.2 Interacciones con IA Durante el Desarrollo

La inteligencia artificial fue utilizada para协助 en tareas técnicas después de que el estudiante ya tenía los algoritmos implementados y funcionales.

| Código | Prompt (Resumen) | Intervención de IA | Archivos Modificados |
|--------|-----------------|---------------------|---------------------|
| **P1** | Organizar código en paquetes modulares | Creó la estructura de paquetes `persistence/` y `views/` con susrespectivos módulos | 10 archivos en `persistence/`, `views/` |
| **P2** | Implementar medición de tiempos | Agregó medición de tiempos con `time.perf_counter_ns()` y persistencia Excel | `main.py`, `ResultsExcelHandler.py` |
| **P3** | Estructurar main.py para 2 casos | Configuró soporte para Caso1 (128×128) y Caso2 (256×256) | `main.py` |
| **P4** | Documentar análisis de complejidad | Documentó análisis de complejidad, comportamiento por tamaño, y created DISEÑO.md | `README.md`, `DISEÑO.md` |
| **P5** | Agregar docstrings a algoritmos | Agregó documentación formal tipo docstring a los 15 algoritmos | 15 archivos en `algoritmos/` |
| **P6** | Agregar medición de memoria | Agregó tracemalloc para pico de memoria en KB | `main.py`, `ResultsExcelHandler.py` |
| **P7** | Agregar verificación de resultados | Agregó np.allclose() para validar C = A × B | `main.py` |
| **P8** | Cambiar persistencia a Excel | Reemplazó XML por Excel con gráficos | `MatrixFileHandler.py`, `ResultsExcelHandler.py` |
| **P9** | Corregir bugs de algoritmos | Identificó y corrigió bugs en III.5, IV.5, StrassenWinograd | 3 archivos en `algoritmos/` |

### 15.3 Detalle de Intervenciones de IA

---

**P1 - Modularización del Proyecto:**
Se le pidió a la IA que reorganizara el código existente (ya con los algoritmos adaptados por el estudiante) en una estructura de paquetes profesional. La IA creó los paquetes `persistence/` (manejo de Excel) y `views/` (visualización), implementando clases como `Results`, `ResultData`, `ResultsManager`, `MatrixWrapper`, y `ResultsViewer`. **Archivos creados:** 10 archivos nuevos.

**P2 - Medición de Tiempos:**
Se le pidió a la IA que implementara una función para medir los tiempos de ejecución de cada algoritmo. La IA creó `process_algorithm()` en `main.py` usando `time.perf_counter_ns()` para máxima precisión en nanosegundos. **Archivos editados:** `main.py`, `ResultFileHandler.py`.

**P3 - Soporte para Dos Casos de Prueba:**
Se le pidió a la IA que reconfigurara `main.py` para soportar dos casos de prueba diferenciados (Caso1 y Caso2). La IA implementó `run_case()` con generación dinámica de matrices usando `MIN_DIGITS = 7` para garantizar 6+ dígitos. **Archivos editados:** `main.py`.

> **Nota sobre tamaños:** En la rama `Prueba-2` los casos quedaron fijados en 128×128 y 256×256, y la ejecución completa validó los 15 algoritmos con esos tamaños.

**P4 - Documentación Técnica:**
Se le pidió a la IA que reescribiera completamente la documentación. La IA documentó análisis de complejidad, predicciones de rendimiento, puntos de cruce, y creó el documento `DISEÑO.md` con especificaciones formales. **Archivos editados:** `README.md`, `DISEÑO.md`.

**P5 - Documentación de Algoritmos:**
Se le pidió a la IA que agregara docstrings completos a los 15 algoritmos. La IA agregó documentación formal incluyendo complejidad computacional, técnica utilizada, parámetros, retorno y referencias bibliográficas. **Archivos editados:** 15 archivos en `algoritmos/`.

### 15.4 Nivel de Participación Real

| Etapa | Estudiante | IA | Notas |
|------|-----------|-----|-------|
| Diseño de algoritmos | 100% | 0% | Algoritmos de repositorio público |
| Implementación inicial | 100% | 0% | Adaptación de interfaz `multiply()` |
| Estructura del proyecto | 0% | 100% | Paquetes `persistence/`, `views/` |
| Persistencia Excel | 0% | 100% | Clases de lectura/escritura con openpyxl |
| Medición de tiempos | 20% | 80% | Estudiante diseñó metodología, IA implementó |
| Medición de memoria | 10% | 90% | Estudiante solicitó, IA implementó con tracemalloc |
| Verificación de resultados | 10% | 90% | Estudiante solicitó, IA implementó con np.allclose |
| Corrección de bugs algorítmicos | 30% | 70% | IA identificó y corrigió bugs de padding/indexación |
| Documentación | 30% | 70% | Estudiante proporcionó contexto, IA documentó |
| Visualización | 0% | 100% | `ResultsViewer` con matplotlib |

### 15.5 Correcciones de Bugs Identificados

Durante el desarrollo, se identificaron y corrigieron los siguientes bugs en los algoritmos originales:

| Bug | Algoritmo | Descripción | Fix Aplicado |
|-----|-----------|-------------|--------------|
| Indexación incorrecta | IV.5 Enhanced Parallel | `C[i][k]` en lugar de `C[i][j]` | Corregido a `C[i][j]` |
| Padding no potencia de 2 | StrassenNaiv | Cálculo de padding incorrecto para tamaños potencia de 2 | Ajuste al tamaño potencia de 2 correcto |
| Padding no potencia de 2 | StrassenWinograd | Cálculo de padding incorrecto para tamaños potencia de 2 | Ajuste al tamaño potencia de 2 correcto |
| Parámetros incorrectos en ThreadPoolExecutor | III.5 Enhanced Parallel | Segunda llamada `submit(N,N,P,M)` en lugar de `submit(N,P,M)` | Corregido |
| Parámetros incorrectos en ThreadPoolExecutor | IV.5 Enhanced Parallel | Segunda llamada `submit(N,N,P,M)` en lugar de `submit(N,P,M)` | Corregido |
| Tipo de dato entero (overflow) | StrassenWinograd | Matriz resultado inicializada como `[[0]]` (int) | Cambiado a `[[0.0]]` (float) |
| Fórmula incorrecta | StrassenWinograd | Algoritmo con fórmulas de Winograd incorrectas | Reescrito con fórmula estándar de Strassen-Winograd |

### 15.6 Detalle de Correcciones

#### Bug: Parámetros incorrectos en III.5 y IV.5 Enhanced Parallel

**Problema:** La segunda llamada a `executor.submit()` en ambos algoritmos pasaba `N, N, P, M` en lugar de `N, P, M`.

```python
# INCORRECTO:
executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, N, P, M, block_size)

# CORRECTO:
executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, P, M, block_size)
```

#### Bug: StrassenWinograd con overflow y fórmulas incorrectas

**Problema 1:** La matriz resultado se inicializaba como enteros (`[[0] * M]`), causando overflow en matrices grandes.

**Problema 2:** El algoritmo implementaba fórmulas de Winograd de forma incorrecta, causando resultados erróneos al aumentar el tamaño de entrada.

**Solución:** Reescritura completa del algoritmo usando la fórmula estándar de Strassen-Winograd con variables temporales separadas para cada producto M1-M7.

### 15.7 Aclaración importante

Los 15 algoritmos de multiplicación de matrices (Naiv, Winograd, Strassen, Block) son implementaciones conocidas de la literatura académica y fueron obtenidos de un repositorio GitHub público por el estudiante. La IA ayudó únicamente en tareas técnicas de organización, medición, documentación y corrección de bugs, **no en la invención o diseño de los algoritmos**.

---

*Documento actualizado para el Seguimiento 2 - 2026*
