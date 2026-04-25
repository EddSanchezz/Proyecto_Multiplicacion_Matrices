# Documento de Diseño: Multiplicación de Matrices Grandes

## Universidad del Quindío
### Programa de Ingeniería de Sistemas y Computación
### Análisis de Algoritmos - Seguimiento 2

---

## 1. Introducción

Este documento presenta el diseño técnico del proyecto de multiplicación de matrices grandes, implementando y analizando 15 algoritmos mediante enfoques iterativos y divide y vencerás.

### 1.1 Propósito

Implementar y analizar algoritmos para la multiplicación de matrices grandes con el objetivo de:
- Comparar rendimiento entre algoritmos iterativos y divide y vencerás
- Analizar el comportamiento según el tamaño de entrada
- Documentar la complejidad algorítmica de cada método

### 1.2 Alcance

- 15 algoritmos implementados
- 2 casos de prueba (128x128 y 256x256)
- Análisis de complejidad O(n³) vs O(n^2.807)
- Persistencia de datos y resultados

---

## 2. Especificación de Requerimientos

### 2.1 Requerimientos Funcionales

| ID | Requerimiento | Estado | Implementación |
|----|---------------|--------|---------------|
| RF-01 | Implementar 15 algoritmos | Completo | Paquete algoritmos/ |
| RF-02 | 2 casos de prueba n x n | Completo | main.py run_case() |
| RF-03 | Valores mínimo 6 dígitos | Completo | MIN_DIGITS = 7 |
| RF-04 | Casos persistentes | Completo | MatrixFileHandler |
| RF-05 | Tiempos persistentes | Completo | ResultFileHandler |
| RF-06 | Diagrama de barras | Completo | ResultsViewer |

### 2.2 Requerimientos No Funcionales

| ID | Requerimiento | Cumplimiento |
|----|---------------|--------------|
| RNF-01 | Tiempo de ejecución medible | time.perf_counter_ns() |
| RNF-02 | Precisión en nanosegundos | 1 ns |
| RNF-03 | Almacenamiento en Excel | openpyxl |
| RNF-04 | Documentación completa | README.md |

---

## 3. Diseño del Sistema

### 3.1 Arquitectura General

```
+-------------------+
|      main.py      |
|  (Punto entrada)  |
+--------+---------+
          |
          v
+--------+--------+---------+
|                       |
+--------+               +--------+
|               |                       |
v               v                       v
+--------+ +--------+ +--------+
|Algoritmos| |Persis-| | Views |
| (15)   | |tence  | |(Graf) |
+--------+ +--------+ +--------+
```

### 3.2 Diagrama de Flujo

```
+------------------+
| Iniciar programa |
+--------+---------+
          |
          v
+--------+---------+
| Configurar casos |
| (Caso1, Caso2)  |
+--------+---------+
          |
          v
+--------+---------+
| Para cada caso   |
|   generar       |
|   matrices      |
+--------+---------+
          |
          v
+--------+---------+
| Para cada        |
| algoritmo       |
| ejecutar y      |
| medir tiempo    |
+--------+---------+
          |
          v
+--------+---------+
| Guardar         |
| resultados     |
+--------+---------+
          |
          v
+--------+---------+
| Mostrar         |
| gráfico        |
+--------+---------+
          |
          v
+--------+---------+
| Fin            |
+----------------+
```

### 3.3 Estructura de Datos

#### Matriz
```python
# Representación de matriz cuadrada
matriz = [[float64, float64, ...],  # Fila 0
          [float64, float64, ...],  # Fila 1
          ...
          [float64, float64, ...]]   # Fila n-1
# Tamaño: n x n elementos
```

#### Resultado de Ejecución
```python
@dataclass
class ResultData:
    size: int          # Tamaño n (128, 256)
    algorithm: str     # Nombre del algoritmo
    language: str     # "python"
    executionTime: int # Nanosegundos
    case: str         # "Caso1" o "Caso2"
    rows: int         # Filas
    cols: int         # Columnas
```

---

## 4. Diseño de Algoritmos

### 4.1 Algoritmos Iterativos

#### NaivOnArray
```
ALGORITMO NaivOnArray
ENTRADA: MatrizA[N][P], MatrizB[P][M]
SALIDA: MatrizRes[N][M]

PARA i = 0 HASTA N-1:
    PARA j = 0 HASTA M-1:
        PARA k = 0 HASTA P-1:
            Res[i][j] = Res[i][j] + A[i][k] * B[k][j]
DEVOLVER Res
```

#### WinogradOriginal
```
ALGORITMO WinogradOriginal
ENTRADA: MatrizA[N][P], MatrizB[P][M]
SALIDA: MatrizRes[N][M]

# Precalcular y (filas de A)
PARA i = 0 HASTA N-1:
    y[i] = SUMATORIA(A[i][2k] * A[i][2k+1]) PARA k = 0 HASTA gamma/2-1

# Precalcular z (columnas de B)
PARA k = 0 HASTA M-1:
    z[k] = SUMATORIA(B[2k][i] * B[2k+1][i]) PARA i = 0 HASTA gamma/2-1

# Calcular resultado
SI upsilon == 1:
    PARA i = 0 HASTA N-1:
        PARA k = 0 HASTA M-1:
            Res[i][k] = SUMATORIA((A[i][j]+B[j+1][k])*(A[i][j+1]+B[j][k])) - y[i] - z[k] + A[i][PP]*B[PP][k]
SINO:
    PARA i = 0 HASTA N-1:
        PARA k = 0 HASTA M-1:
            Res[i][k] = SUMATORIA((A[i][j]+B[j+1][k])*(A[i][j+1]+B[j][k])) - y[i] - z[k]
DEVOLVER Res
```

### 4.2 Algoritmos Divide y Vencerás

#### StrassenNaiv
```
ALGORITMO StrassenNaiv
ENTRADA: MatrizA[N][N], MatrizB[N][N]
SALIDA: MatrizRes[N][N]

SI N <= m:
    DEVOLVER NaivEstandar(A, B)
SINO:
    # Dividir en 4 submatrices
    A11, A12, A21, A22 = DIVIDIR(A)
    B11, B12, B21, B22 = DIVIDIR(B)

    # 7 productos de Strassen
    M1 = Strassen(A11 + A22, B11 + B22)
    M2 = Strassen(A21 + A22, B11)
    M3 = Strassen(A11, B12 - B22)
    M4 = Strassen(A22, B21 - B11)
    M5 = Strassen(A11 + A12, B22)
    M6 = Strassen(A21 - A11, B11 + B12)
    M7 = Strassen(A12 - A22, B21 + B22)

    # Combinar resultados
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    DEVOLVER COMBINAR(C11, C12, C21, C22)
```

### 4.3 Algoritmos por Bloques

#### III.3 Sequential Block
```
ALGORITMO III_3_SequentialBlock
ENTRADA: MatrizA[N][N], MatrizB[N][N], tamaño_bloque
SALIDA: MatrizRes[N][N]

PARA i1 = 0 HASTA N-1 PASO tamaño_bloque:
    PARA j1 = 0 HASTA N-1 PASO tamaño_bloque:
        PARA k1 = 0 HASTA N-1 PASO tamaño_bloque:
            PARA i = i1 HASTA min(i1+tamaño_bloque, N):
                PARA j = j1 HASTA min(j1+tamaño_bloque, N):
                    PARA k = k1 HASTA min(k1+tamaño_bloque, N):
                        Res[i][j] = Res[i][j] + A[i][k] * B[k][j]
DEVOLVER Res
```

---

## 5. Análisis de Complejidad

### 5.1 Tabla de Complejidad

| Algoritmo | Multiplicaciones | Adiciones | Complejidad |
|----------|---------------|----------|-----------|
| NaivOnArray | n³ | n³(n-1) | O(n³) |
| NaivLoopUnrollingTwo | n³ | ~n³ | O(n³) |
| NaivLoopUnrollingFour | n³ | ~n³ | O(n³) |
| WinogradOriginal | n³/2 | ~n³/2 | O(n³) |
| WinogradScaled | n³/2 | ~n³/2 | O(n³) |
| StrassenNaiv | 7n^2.807 | 6n^2.807 | O(n^2.807) |
| StrassenWinograd | 7n^2.807 | ~6n^2.807 | O(n^2.807) |
| III.3 Sequential | n³ | n³ | O(n³) |
| III.4 Parallel | n³/p | n³/p | O(n³/p) |
| III.5 Enhanced | n³/p | n³/p | O(n³/p) |
| IV.3 Sequential | n³ | n³ | O(n³) |
| IV.4 Parallel | n³/p | n³/p | O(n³/p) |
| IV.5 Enhanced | n³/p | n³/p | O(n³/p) |
| V.3 Sequential | n³ | n³ | O(n³) |
| V.4 Parallel | n³/p | n³/p | O(n³/p) |

### 5.2 Análisis de Constante Oculta

| Algoritmo | Cte. Oculta | Notas |
|----------|------------|-------|
| NaivOnArray | 1 | Base simple |
| WinogradOriginal | ~0.5 | Menos mult. |
| StrassenNaiv | ~15 | Overhead recursión |
| Block Sequential | ~1.1 | Overhead índices |
| Block Parallel | ~1.1 + sinc. | Sincronización |

### 5.3 Punto de Cruce

| Comparación | Tamaño | Razón |
|------------|-------|-------|
| Naiv vs Winograd | ~8×8 | Overhead precalculo |
| Naiv vs Strassen | ~64×64 | Overhead recursión |
| Seq vs Parallel | depende | Núm. núcleos |

---

## 6. Diseño de Persistencia

### 6.1 Formato Excel (.xlsx)

La persistencia se realiza en formato Excel para mayor legibilidad. Este formato reemplaza la implementación anterior en XML.

#### Archivo de Matrices

Cada caso de prueba genera un archivo Excel con la siguiente estructura:

| Hoja | Contenido |
|------|----------|
| Matriz A | Datos de la primera matriz con formato tabular |
| Matriz B | Datos de la segunda matriz con formato tabular |
| Info | Metadatos: caso, tamaño, fecha, formato numérico |

Ejemplo de estructura:
```
matrix_Caso1_128x128.xlsx
├── Matriz A (128×128)
│   ├── Fila 0: [valor, valor, ...]
│   ├── Fila 1: [valor, valor, ...]
│   └── ...
├── Matriz B (128×128)
│   └── ...
└── Info
    ├── Caso: Caso1
    ├── Tamaño: 128×128
    ├── Fecha: 2026-01-01
    └── Elementos por matriz: 16384
```

#### Archivo de Resultados

El archivo `python_results.xlsx` contiene:

| Hoja | Contenido |
|------|----------|
| Caso1 | Tiempos de ejecución para 128×128 |
| Caso2 | Tiempos de ejecución para 256×256 |
| Comparativa | Tabla resumen comparativa |
| Gráfico | Imagen PNG del gráfico comparativo |

#### Gráfico Comparativo

El gráfico de barras comparativo se genera en dos formatos:
- **PNG**: `grafico_comparativo.png` (archivo separado)
- **Embebido**: Imagen insertada en hoja "Gráfico" del Excel

El gráfico muestra:
- Eje X: 15 algoritmos
- Eje Y: Tiempo de ejecución (milisegundos)
- Barras agrupadas: Caso 1 (azul) vs Caso 2 (naranja)
- Etiquetas de valor en cada barra

### 6.2 Estructura de Archivos

```
src/main/resources/
├── matrices/
│   ├── matrix_Caso1_128x128.xlsx
│   └── matrix_Caso2_256x256.xlsx
└── results/
    ├── python_results.xlsx
    └── grafico_comparativo.png
```

---

## 7. Análisis de Uso de Memoria

### 7.1 Cálculo de Espacio

| Tamaño | Elementos | Bytes (float64) | Bytes (float32) |
|--------|----------|---------------|----------------|
| 128×128 | 16,384 | 131,072 | 65,536 |
| 256×256 | 65,536 | 524,288 | 262,144 |

### 7.2 Requisitos de Memoria

| Caso | Matrices | Resultado | Total |
|------|----------|---------|--------|
| 128×128 | 2×128KB | 128KB | 384KB |
| 256×256 | 2×512KB | 512KB | 1.5MB |

### 7.3 Consideraciones de Caché

| Nivel | Tamaño Típico | Observaciones |
|-------|--------------|---------------|
| L1 | 32KB/núcleo | Matrices pequeñas |
| L2 | 256KB/núcleo | Bloques pequeños |
| L3 | 8MB compartido | Matrices grandes |
| RAM | GiB | Matrices enormes |

---

## 8. Diseño de Pruebas

### 8.1 Casos de Prueba

| ID | Matriz A | Matriz B | Propósito |
|----|----------|---------|-----------|
| CP-01 | 128×128 | 128×128 | Caso 1 |
| CP-02 | 256×256 | 256×256 | Caso 2 |

### 8.2 Métricas a Medir

| Métrica | Unidad | Instrumento |
|--------|--------|-------------|
| Tiempo | nanosegundos | time.perf_counter_ns() |
| Memoria | bytes | sys.getsizeof() |
| CPU | porcentaje | psutil (opcional) |

### 8.3 Criterios de Aceptación

| Criterio | Valor Esperado |
|----------|---------------|
| Todos los algoritmos ejecutan | 15/15 |
| Resultados en Excel | Completo |
| Gráfico PNG generado | Sin errores |
| Gráfico en Excel | Imagen embebida |
| Tiempos consistentes | Varianza < 10% |

---

## 9. Interfaz de Usuario

### 9.1 Flujo de Interacción

```
1. Ejecutar programa
   |
   v
2. Generar/Cargar matrices
   |
   v
3. Seleccionar algoritmo (automático)
   |
   v
4. Mostrar progreso
   |
   v
5. Guardar resultados
   |
   v
6. Mostrar gráfico
```

### 9.2 Salida de Consola

```
==================================================
Ejecutando Caso1
==================================================

--- Tamaño: 128×128 ---
  Ejecutando NaivOnArray... OK
  Ejecutando NaivLoopUnrollingTwo... OK
  Ejecutando NaivLoopUnrollingFour... OK
  ...
```

### 9.3 Gráfico de Resultados

- Eje X: Algoritmos (15)
- Eje Y: Tiempo de ejecución (nanosegundos)
- Colores: Caso 1 (rojo), Caso 2 (azul)
- Filtrable por tamaño y lenguaje

---

## 10. Glosario

| Término | Definición |
|---------|-----------|
| n | Dimensión de matriz cuadrada |
| O(f(n)) | Notación de complejidad asintótica |
| Overhead | Tiempo extra por estructura |
| Speedup | Ganancia de rendimiento |
| Block size | Tamaño de división de matrices |
| p | Número de procesos/hilos |

---

## 11. Referencias

1. Cormen, T.H. et al. "Introduction to Algorithms" - Cap. 4, 28
2. Strassen, V. "Gaussian Elimination is not Optimal" - 1969
3. Winograd, S. "On the Number of Multiplications" - 1968
4. Documentación Python: docs.python.org

---

*Documento de Diseño v1.0 - Seguimiento 2*
*Universidad del Quindío - Ingeniería de Sistemas y Computación*
*2026*
