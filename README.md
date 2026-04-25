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

Matrices cuadradas n×n donde n es factor de 2ⁿ, con valores de mínimo 6 dígitos.

| Caso | Dimensión | Descripción | Elementos | Memoria Aprox. |
|------|----------|-------------|-----------|----------------|
| 1 | 512×512 (2⁹) | Matrices cuadradas 2ⁿ | 262,144 | ~2 MB |
| 2 | 1024×1024 (2¹⁰) | Matrices cuadradas 2ⁿ | 1,048,576 | ~8 MB |

### Cálculo de Memoria

Para matrices de doubles (8 bytes por elemento):
- **512×512**: 512 × 512 × 8 = **2,097,152 bytes** (~2 MB por matriz)
- **1024×1024**: 1024 × 1024 × 8 = **8,388,608 bytes** (~8 MB por matriz)

Con dos matrices de entrada + una de resultado:
- Caso 1: ~6 MB total
- Caso 2: ~24 MB total

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

### Tabla 1: Tiempos de Ejecución (nanosegundos)

| ID | Algoritmo | Caso 1 (512×512) | Caso 2 (1024×1024) |
|----|----------|------------------|-------------------|
| 1 | NaivOnArray | TE₁ | TE₂ |
| 2 | NaivLoopUnrollingTwo | TE₁ | TE₂ |
| 3 | NaivLoopUnrollingFour | TE₁ | TE₂ |
| 4 | WinogradOriginal | TE₁ | TE₂ |
| 5 | WinogradScaled | TE₁ | TE₂ |
| 6 | StrassenNaiv | TE₁ | TE₂ |
| 7 | StrassenWinograd | TE₁ | TE₂ |
| 8 | III.3 Sequential block | TE₁ | TE₂ |
| 9 | III.4 Parallel Block | TE₁ | TE₂ |
| 10 | III.5 Enhanced Parallel Block | TE₁ | TE₂ |
| 11 | IV.3 Sequential block | TE₁ | TE₂ |
| 12 | IV.4 Parallel Block | TE₁ | TE₂ |
| 13 | IV.5 Enhanced Parallel Block | TE₁ | TE₂ |
| 14 | V.3 Sequential block | TE₁ | TE₂ |
| 15 | V.4 Parallel Block | TE₁ | TE₂ |

### Tabla 2: Orden de Complejidad

| ID | Algoritmo | Orden de Complejidad |
|----|----------|---------------------|
| 1 | NaivOnArray | O(n³) |
| 2 | NaivLoopUnrollingTwo | O(n³) |
| 3 | NaivLoopUnrollingFour | O(n³) |
| 4 | WinogradOriginal | O(n³) |
| 5 | WinogradScaled | O(n³) |
| 6 | StrassenNaiv | O(n^log₂7) |
| 7 | StrassenWinograd | O(n^log₂7) |
| 8 | III.3 Sequential block | O(n³) |
| 9 | III.4 Parallel Block | O(n³/p) |
| 10 | III.5 Enhanced Parallel Block | O(n³/p) |
| 11 | IV.3 Sequential block | O(n³) |
| 12 | IV.4 Parallel Block | O(n³/p) |
| 13 | IV.5 Enhanced Parallel Block | O(n³/p) |
| 14 | V.3 Sequential block | O(n³) |
| 15 | V.4 Parallel Block | O(n³/p) |

### Tabla 3: Comparativa de Rendimiento (speedup vs NaivOnArray)

| ID | Algoritmo | Speedup Caso 1 | Speedup Caso 2 |
|----|----------|----------------|---------------|
| 1 | NaivOnArray | 1.00× (base) | 1.00× (base) |
| 2 | NaivLoopUnrollingTwo | - | - |
| 3 | NaivLoopUnrollingFour | - | - |
| 4 | WinogradOriginal | - | - |
| 5 | WinogradScaled | - | - |
| 6 | StrassenNaiv | - | - |
| 7 | StrassenWinograd | - | - |
| 8 | III.3 Sequential block | - | - |
| 9 | III.4 Parallel Block | - | - |
| 10 | III.5 Enhanced Parallel Block | - | - |
| 11 | IV.3 Sequential block | - | - |
| 12 | IV.4 Parallel Block | - | - |
| 13 | IV.5 Enhanced Parallel Block | - | - |
| 14 | V.3 Sequential block | - | - |
| 15 | V.4 Parallel Block | - | - |

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
| **P2** | Implementar medición de tiempos | Uso de time.perf_counter_ns() y persistencia XML |
| **P3** | Estructurar main.py para 2 casos | Soporte para Caso1 (512×512) y Caso2 (1024×1024) |
| **P4** | Documentar análisis de complejidad | Análisis teórico y documentación formal |
| **P5** | Agregar docstrings a algoritmos | Documentación tipo docstring a los 15 algoritmos |
| **P6** | Agregar medición de memoria | Uso de tracemalloc para medir pico de memoria |
| **P7** | Agregar verificación de resultados | Validación C = A × B usando NumPy como referencia |
| **P8** | Cambiar persistencia a Excel | Reemplazo de XML por Excel con openpyxl |

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
  - **Capa de persistencia**: XML (lectura/escritura de matrices y resultados)
  - **Capa de views**: Visualización con tkinter/matplotlib
- Se implementó el patrón DataManager para resultados:
  - `Results`: Contenedor de lista de resultados
  - `ResultData`: Dataclass con size, algorithm, language, executionTime, case, rows, cols
- Se creó `ResultsManager` para combinar resultados de múltiples archivos XML

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
  - Registra resultados en XML con metadatos completos (size, algorithm, case, rows, cols)
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
  - `SIZES_CASO_1 = [512]` → 512×512 = 2⁹
  - `SIZES_CASO_2 = [1024]` → 1024×1024 = 2¹⁰
- Funciones de generación y persistencia:
  - `matrix_generator(n, min_digits)`: Genera matriz numpy con valores aleatorios de n dígitos
  - `save_matrix()` / `load_matrix()`: Persistencia XML de matrices
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
SIZES_CASO_1 = [512]  # Caso 1: 512×512
SIZES_CASO_2 = [1024]  # Caso 2: 1024×1024
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
| `matrix_Caso1_512x512.xlsx` | Matrices del caso 1 (Hojas: Matriz A, Matriz B, Info) |
| `matrix_Caso2_1024x1024.xlsx` | Matrices del caso 2 (Hojas: Matriz A, Matriz B, Info) |
| `python_results.xlsx` | Tiempos de ejecución (Hojas: Caso1, Caso2, Comparativa, Gráfico) |
| `grafico_comparativo.png` | Imagen del gráfico comparativo |

El archivo `python_results.xlsx` contiene:
- **Hoja "Caso1"**: Tiempos para matrices 512×512
- **Hoja "Caso2"**: Tiempos para matrices 1024×1024
- **Hoja "Comparativa"**: Tabla resumen comparando ambos casos
- **Hoja "Gráfico"**: Imagen del gráfico de barras comparativo

---

## 11. Análisis de Rendimiento Predicho

Basado en la complejidad algorítmica, esperamos:

### Caso 1 (512×512) - Tiempo Relativo Estimado

| Algoritmo | Factor vs Naiv |
|-----------|----------------|
| NaivOnArray | 1.00× (base) |
| NaivLoopUnrollingTwo | ~0.95× |
| NaivLoopUnrollingFour | ~0.90× |
| WinogradOriginal | ~0.80× |
| WinogradScaled | ~0.85× |
| StrassenNaiv | ~1.20×* |
| StrassenWinograd | ~1.10×* |
| III.3 Sequential block | ~1.00× |
| III.4 Parallel Block | ~0.25×** |
| III.5 Enhanced Parallel Block | ~0.20×** |
| IV.3 Sequential block | ~0.95× |
| IV.4 Parallel Block | ~0.20×** |
| IV.5 Enhanced Parallel Block | ~0.15×** |
| V.3 Sequential block | ~0.90× |
| V.4 Parallel Block | ~0.15×** |

*Strassen tiene overhead para matrices pequeñas
**Paralelo depende del número de núcleos disponibles

### Caso 2 (1024×1024) - Tiempo Relativo Estimado

| Algoritmo | Factor vs Naiv |
|-----------|----------------|
| NaivOnArray | 1.00× (base) |
| StrassenNaiv | ~0.70× |
| StrassenWinograd | ~0.60× |
| IV.4 Parallel Block | ~0.10×** |

---

## 12. Conclusiones

1. **Para matrices pequeñas (<64×64)**: Los algoritmos iterativos simples (Naiv*, Winograd*) son más eficientes debido al bajo overhead.

2. **Para matrices grandes (>512×512)**: Los algoritmos de Strassen y los paralelos muestran mejor rendimiento.

3. **Uso de memoria**: Las matrices 1024×1024 requieren ~24 MB de RAM, manageable en equipos modernos.

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
| A3 | Selección de casos de prueba | Se definieron los tamaños 512×512 y 1024×1024 como casos de prueba | Constantes `SIZES_CASO_1`, `SIZES_CASO_2` en main.py |
| A4 | Diseño de pruebas | Se diseñaron los casos de prueba y metodología de verificación | main.py: `run_case()`, `process_algorithm()` |

### 15.2 Interacciones con IA Durante el Desarrollo

La inteligencia artificial fue utilizada para协助 en tareas técnicas después de que el estudiante ya tenía los algoritmos implementados y funcionales.

| Código | Prompt (Resumen) | Intervención de IA | Archivos Modificados |
|--------|-----------------|---------------------|---------------------|
| **P1** | Organizar código en paquetes modulares | Creó la estructura de paquetes `persistence/` y `views/` con susrespectivos módulos | 10 archivos en `persistence/`, `views/` |
| **P2** | Implementar medición de tiempos | Agregó medición de tiempos con `time.perf_counter_ns()` y persistencia XML | `main.py`, `ResultFileHandler.py` |
| **P3** | Estructurar main.py para 2 casos | Configuró soporte para Caso1 (512×512) y Caso2 (1024×1024) | `main.py` |
| **P4** | Documentar análisis de complejidad | Documentó análisis de complejidad, comportamiento por tamaño, y created DISEÑO.md | `README.md`, `DISEÑO.md` |
| **P5** | Agregar docstrings a algoritmos | Agregó documentación formal tipo docstring a los 15 algoritmos | 15 archivos en `algoritmos/` |
| **P6** | Agregar medición de memoria | Agregó tracemalloc para pico de memoria en KB | `main.py`, `ResultsExcelHandler.py` |
| **P7** | Agregar verificación de resultados | Agregó np.allclose() para validar C = A × B | `main.py` |
| **P8** | Cambiar persistencia a Excel | Reemplazó XML por Excel con gráficos | `MatrixFileHandler.py`, `ResultsExcelHandler.py` |
| **P9** | Corregir bugs de algoritmos | Identificó y corrigió bugs en III.5, IV.5, StrassenWinograd | 3 archivos en `algoritmos/` |

### 15.3 Detalle de Intervenciones de IA

---

**P1 - Modularización del Proyecto:**
Se le pidió a la IA que reorganizara el código existente (ya con los algoritmos adaptados por el estudiante) en una estructura de paquetes profesional. La IA creó los paquetes `persistence/` (manejo de XML) y `views/` (visualización), implementando clases como `Results`, `ResultData`, `ResultsManager`, `MatrixWrapper`, y `ResultsViewer`. **Archivos creados:** 10 archivos nuevos.

**P2 - Medición de Tiempos:**
Se le pidió a la IA que implementara una función para medir los tiempos de ejecución de cada algoritmo. La IA creó `process_algorithm()` en `main.py` usando `time.perf_counter_ns()` para máxima precisión en nanosegundos. **Archivos editados:** `main.py`, `ResultFileHandler.py`.

**P3 - Soporte para Dos Casos de Prueba:**
Se le pidió a la IA que reconfigurara `main.py` para soportar dos casos de prueba diferenciados (Caso1 y Caso2). La IA implementó `run_case()` con generación dinámica de matrices usando `MIN_DIGITS = 7` para garantizar 6+ dígitos. **Archivos editados:** `main.py`.

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
| Persistencia XML | 0% | 100% | Clases de lectura/escritura |
| Persistencia Excel | 0% | 100% | Reemplazo total de XML por Excel |
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
| Padding no potencia de 2 | StrassenNaiv | newSize=17 para input 16×16 | newSize=16 (potencia de 2) |
| Padding no potencia de 2 | StrassenWinograd | newSize=17 para input 16×16 | newSize=16 (potencia de 2) |
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

**Problema 2:** El algoritmo implementaba fórmulas de Winograd de forma incorrecta, causando resultados erróneos para tamaños de 32×32 y mayores.

**Solución:** Reescritura completa del algoritmo usando la fórmula estándar de Strassen-Winograd con variables temporales separadas para cada producto M1-M7.

### 15.7 Aclaración importante

Los 15 algoritmos de multiplicación de matrices (Naiv, Winograd, Strassen, Block) son implementaciones conocidas de la literatura académica y fueron obtenidos de un repositorio GitHub público por el estudiante. La IA协助 únicamente en tareas técnicas de organización, medición, documentación y corrección de bugs, **no en la invención o diseño de los algoritmos**.

---

*Documento actualizado para el Seguimiento 2 - 2026*
