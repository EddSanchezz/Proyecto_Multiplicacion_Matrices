# Documento de Diseno: Multiplicacion de Matrices Grandes

## Universidad del Quindio
### Programa de Ingenieria de Sistemas y Computacion
### Analisis de Algoritmos - Seguimiento 2

---

## 1. Introduccion

Este documento presenta el diseno tecnico del proyecto de multiplicacion de matrices grandes, implementando y analizando 15 algoritmos mediante enfoques iterativos y divide y venceras.

### 1.1 Proposito

Implementar y analizar algoritmos para la multiplicacion de matrices grandes con el objetivo de:
- Comparar rendimiento entre algoritmos iterativos y divide y venceras
- Analizar el comportamiento segun el tamano de entrada
- Documentar la complejidad algoritmica de cada metodo

### 1.2 Alcance

- 15 algoritmos implementados
- 2 casos de prueba (512x512 y 1024x1024)
- Analisis de complejidad O(n^3) vs O(n^2.807)
- Persistencia de datos y resultados

---

## 2. Especificacion de Requerimientos

### 2.1 Requerimientos Funcionales

| ID | Requerimiento | Estado | Implementacion |
|----|---------------|--------|---------------|
| RF-01 | Implementar 15 algoritmos | Completo | Paquete algoritmos/ |
| RF-02 | 2 casos de prueba n x n | Completo | main.py run_case() |
| RF-03 | Valores minimo 6 digitos | Completo | MIN_DIGITS = 7 |
| RF-04 | Casos persistentes | Completo | MatrixFileHandler |
| RF-05 | Tiempos persistentes | Completo | ResultFileHandler |
| RF-06 | Diagrama de barras | Completo | ResultsViewer |

### 2.2 Requerimientos No Funcionales

| ID | Requerimiento | Cumplimiento |
|----|---------------|--------------|
| RNF-01 | Tiempo de ejecucion medible | time.perf_counter_ns() |
| RNF-02 | Precision en nanosegundos | 1 ns |
| RNF-03 | Almacenamiento en XML | ElementTree |
| RNF-04 | Documentacion completa | README.md |

---

## 3. Diseno del Sistema

### 3.1 Arquitectura General

```
+-------------------+
|      main.py      |
|  (Punto entrada)  |
+--------+--------+
         |
         v
+--------+--------+--------+
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
| grafico        |
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
# Representacion de matriz cuadrada
matriz = [[float64, float64, ...],  # Fila 0
          [float64, float64, ...],  # Fila 1
          ...
          [float64, float64, ...]]   # Fila n-1
# Tamano: n x n elementos
```

#### Resultado de Ejecucion
```python
@dataclass
class ResultData:
    size: int          # Tamano n (512, 1024)
    algorithm: str     # Nombre del algoritmo
    language: str     # "python"
    executionTime: int # Nanosegundos
    case: str         # "Caso1" o "Caso2"
    rows: int         # Filas
    cols: int         # Columnas
```

---

## 4. Diseno de Algoritmos

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

### 4.2 Algoritmos Divide y Venceras

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
ENTRADA: MatrizA[N][N], MatrizB[N][N], tamano_bloque
SALIDA: MatrizRes[N][N]

PARA i1 = 0 HASTA N-1 PAS0 tamano_bloque:
    PARA j1 = 0 HASTA N-1 PAS0 tamano_bloque:
        PARA k1 = 0 HASTA N-1 PAS0 tamano_bloque:
            PARA i = i1 HASTA min(i1+tamano_bloque, N):
                PARA j = j1 HASTA min(j1+tamano_bloque, N):
                    PARA k = k1 HASTA min(k1+tamano_bloque, N):
                        Res[i][j] = Res[i][j] + A[i][k] * B[k][j]
DEVOLVER Res
```

---

## 5. Analisis de Complejidad

### 5.1 Tabla de Complejidad

| Algoritmo | Multiplicaciones | Adiciones | Complejidad |
|----------|---------------|----------|-----------|
| NaivOnArray | n^3 | n^3(n-1) | O(n^3) |
| NaivLoopUnrollingTwo | n^3 | ~n^3 | O(n^3) |
| NaivLoopUnrollingFour | n^3 | ~n^3 | O(n^3) |
| WinogradOriginal | n^3/2 | ~n^3/2 | O(n^3) |
| WinogradScaled | n^3/2 | ~n^3/2 | O(n^3) |
| StrassenNaiv | 7n^2.807 | 6n^2.807 | O(n^2.807) |
| StrassenWinograd | 7n^2.807 | ~6n^2.807 | O(n^2.807) |
| III.3 Sequential | n^3 | n^3 | O(n^3) |
| III.4 Parallel | n^3/p | n^3/p | O(n^3/p) |
| III.5 Enhanced | n^3/p | n^3/p | O(n^3/p) |
| IV.3 Sequential | n^3 | n^3 | O(n^3) |
| IV.4 Parallel | n^3/p | n^3/p | O(n^3/p) |
| IV.5 Enhanced | n^3/p | n^3/p | O(n^3/p) |
| V.3 Sequential | n^3 | n^3 | O(n^3) |
| V.4 Parallel | n^3/p | n^3/p | O(n^3/p) |

### 5.2 Analisis de Constante Oculta

| Algoritmo | Cte. Oculta | Notas |
|----------|------------|-------|
| NaivOnArray | 1 | Base simple |
| WinogradOriginal | ~0.5 | Menos mult. |
| StrassenNaiv | ~15 | Overhead recursion |
| Block Sequential | ~1.1 | Overhead indices |
| Block Parallel | ~1.1 + sinc. | Sincronizacion |

### 5.3 Punto de Crucce

| Comparacion | Tamano | Razon |
|------------|-------|-------|
| Naiv vs Winograd | ~8x8 | Overhead precalculo |
| Naiv vs Strassen | ~64x64 | Overhead recursion |
| Seq vs Parallel | depende | Num. nucleos |

---

## 6. Diseno de Persistencia

### 6.1 Formato XML

#### Matriz
```xml
<?xml version="1.0"?>
<matrix rows="512" cols="512">
    <row index="0">
        <cell>1234567.0</cell>
        <cell>2345678.0</cell>
        ...
    </row>
    ...
</matrix>
```

#### Resultados
```xml
<?xml version="1.0"?>
<results>
    <result>
        <size>512</size>
        <algorithm>NaivOnArray</algorithm>
        <language>python</language>
        <executionTime>1234567</executionTime>
        <case>Caso1</case>
        <rows>512</rows>
        <cols>512</cols>
    </result>
    ...
</results>
```

### 6.2 Estructura de Archivos

```
src/main/resources/
├── matrices/
│   ├── matrix_Caso1_512x512.xml
│   ├── matrix_Caso1_512x512.xml
│   ├── matrix_Caso2_1024x1024.xml
│   └── matrix_Caso2_1024x1024.xml
└── results/
    └── python_results.xml
```

---

## 7. Analisis de Uso de Memoria

### 7.1 Calculo de Espacio

| Tamano | Elementos | Bytes (float64) | Bytes (float32) |
|--------|----------|---------------|----------------|
| 512x512 | 262,144 | 2,097,152 | 1,048,576 |
| 1024x1024 | 1,048,576 | 8,388,608 | 4,194,304 |

### 7.2 Requisitos de Memoria

| Caso | Matrices | Resultado | Total |
|------|----------|---------|--------|
| 512x512 | 2x2MB | 2MB | 6MB |
| 1024x1024 | 2x8MB | 8MB | 24MB |

### 7.3 Consideraciones de Cache

| Nivel | Tamano Tipico | Observaciones |
|-------|--------------|---------------|
| L1 | 32KB/nucleo | Matrices pequenas |
| L2 | 256KB/nucleo | Bloques pequenos |
| L3 | 8MB compartido | Matrices grandes |
| RAM | GiB | Matrices enormes |

---

## 8. Diseno de Pruebas

### 8.1 Casos de Prueba

| ID | Matriz A | Matriz B | Proposito |
|----|----------|---------|-----------|
| CP-01 | 512x512 | 512x512 | Caso 1 |
| CP-02 | 1024x1024 | 1024x1024 | Caso 2 |

### 8.2 Metricas a Medir

| Metrica | Unidad | Instrumento |
|--------|--------|-------------|
| Tiempo | nanosegundos | time.perf_counter_ns() |
| Memoria | bytes | sys.getsizeof() |
| CPU | porcentaje | psutil (opcional) |

### 8.3 Criterios de Aceptacion

| Criterio | Valor Esperado |
|----------|---------------|
| Todos los algoritmos ejecutan | 15/15 |
| Resultados en XML | Completo |
| Grafico generado | Sin errores |
| Tiempos consistentes | Variance < 10% |

---

## 9. Interfaz de Usuario

### 9.1 Flujo de Interaccion

```
1. Ejecutar programa
   |
   v
2. Generar/Cargar matrices
   |
   v
3. Seleccionar algoritmo (automatico)
   |
   v
4. Mostrar progreso
   |
   v
5. Guardar resultados
   |
   v
6. Mostrar grafico
```

### 9.2 Salida de Consola

```
==================================================
Ejecutando Caso1
==================================================

--- Tamano: 512x512 ---
  Ejecutando NaivOnArray... OK
  Ejecutando NaivLoopUnrollingTwo... OK
  Ejecutando NaivLoopUnrollingFour... OK
  ...
```

### 9.3 Grafico de Resultados

- Eje X: Algoritmos (15)
- Eje Y: Tiempo de ejecucion (nanosegundos)
- Colores: Caso 1 (rojo), Caso 2 (azul)
- Filtrable por tamano y lenguaje

---

## 10. Glosario

| Termino | Definicion |
|---------|-----------|
| n | Dimension de matriz cuadrada |
| O(f(n)) | Notacion de complejidad asintotica |
| Overhead | Tiempo extra por estructura |
| Speedup | Ganancia de rendimiento |
| Block size | Tamano de division de matrices |
| p | Numero de procesos/hilos |

---

## 11. Referencias

1. Cormen, T.H. et al. "Introduction to Algorithms" - Cap. 4, 28
2. Strassen, V. "Gaussian Elimination is not Optimal" - 1969
3. Winograd, S. "On the Number of Multiplications" - 1968
4. Documentacion Python: docs.python.org

---

*Documento de Diseno v1.0 - Seguimiento 2*
*Universidad del Quindio - Ingenieria de Sistemas y Computacion*
*2026*