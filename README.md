# Proyecto: Multiplicación de Matrices Grandes

## Universidad del Quindío
### Programa de Ingeniería de Sistemas y Computación

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

### 5.3 paging y Swap

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
│   │   │   ├── __init__.py               # Exports (prompt 3)
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
│   │   ├── persistence/                  # Persistencia XML
│   │   │   ├── ResultData.py
│   │   │   ├── ResultFileHandler.py
│   │   │   ├── Results.py
│   │   │   ├── ResultsManager.py
│   │   │   └── MatrixFileHandler.py
│   │   └── views/                       # Visualización
│   │       └── ResultsViewer.py
│   ├── .gitignore                      # (prompt 2)
│   └── README.md                       # Este archivo
├── .gitignore
└── README.md
```

---

## 9. Prompts Utilizados en el Desarrollo

Documentación de las iteraciones con IA que modificaron el proyecto:

| Código | Prompt | Descripción | Archivos |
|--------|--------|-------------|----------|
| **1** | Reescribir main.py con soporte para 2 casos de prueba con matrices cuadradas 2^n | Creación de estructura principal con casos separados |
| **2** | Crear .gitignore para proyecto Python | Exclusión de archivos temporales |
| **3** | Agregar exports de algoritmos en `__init__.py` | Importación correcta de los 15 algoritmos |
| **4** | Eliminar proyecto Java, enfocarse solo en Python | Reducción del proyecto a un solo lenguaje |
| **5** | Subir cambios al repositorio de GitHub | Publicación en EddSanchezz/Proyecto_Multiplicacion_Matrices |
| **6** | Reescribir README.md completo con análisis descriptivo | Documentación del proyecto |

### Detalle de Prompts

#### Prompt 1: Estructura Principal
```markdown
"Crea un main.py que soporte 2 casos de prueba con matrices cuadradas n×n 
donde n es factor de 2^n, con valores de mínimo 6 dígitos"
```

#### Prompt 2: Git Ignore
```markdown
"Crea un .gitignore para proyecto Python que excluya __pycache__, 
.venv, y archivos XML de resultados"
```

#### Prompt 3: Imports de Algoritmos
```markdown
"Agrega todos los exports de los 15 algoritmos en __init__.py para 
permitir imports limpios"
```

#### Prompt 4: Limpieza del Proyecto
```markdown
"Elimina todo el proyecto Java, enfócate solo en Python con los 
15 algoritmos implementados"
```

#### Prompt 5: Publicación
```markdown
"Sube los cambios al repositorio eddsanchezz/Proyecto_Multiplicacion_Matrices"
```

#### Prompt 6: Documentación
```markdown
"Crea un README.md completo con análisis de complejidad, uso de memoria, 
comportamiento por tamaño, y documentation descriptiva"
```

---

## 10. Cómo Ejecutar el Proyecto

### 10.1 Requisitos
- Python 3.8+
- numpy
- tkinter (incluido en Python)

### 10.2 Instalación
```bash
cd Proyecto_Python
pip install numpy
```

### 10.3 Ejecución

1. **Configurar tamaños** en `src/main.py`:
```python
SIZES_CASO_1 = [512]  # Caso 1: 512×512
SIZES_CASO_2 = [1024]  # Caso 2: 1024×1024
```

2. **Descomentar líneas de ejecución**:
```python
if __name__ == "__main__":
    run_case(SIZES_CASO_1, "Caso1")  # Descomentar
    run_case(SIZES_CASO_2, "Caso2")  # Descomentar
    display_results()
```

3. **Ejecutar**:
```bash
python src/main.py
```

### 10.4 Ver Resultados

Los resultados se guardan en:
- Matrices: `src/main/resources/matrices/`
- Tiempos: `src/main/resources/results/`

El gráfico de barras se muestra automáticamente.

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

*Documento actualizado para el Seguimiento 2 - 2026*