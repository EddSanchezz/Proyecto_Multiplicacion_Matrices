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

> **Nota:** Los tamaños 16×16 y 32×32 se usan por limitaciones de hardware. El proyecto escala a 512×512 y 1024×1024 cambiando `SIZES_CASO_1` y `SIZES_CASO_2` en `main.py`.

| Caso | Tamaño | Elementos | Memoria |
|------|---------|-----------|---------|
| 1 | 16×16 | 256 | ~6 KB |
| 2 | 32×32 | 1,024 | ~24 KB |

Para 512×512: ~2 MB por matriz. Para 1024×1024: ~8 MB por matriz.

---

## 3. Algoritmos Implementados

| # | Algoritmo | Descripción | Complejidad |
|---|----------|-------------|-------------|
| 1 | NaivOnArray | Triple bucle ingenuo | O(n³) |
| 2 | NaivLoopUnrollingTwo | Desenrollado ×2 | O(n³) |
| 3 | NaivLoopUnrollingFour | Desenrollado ×4 | O(n³) |
| 4 | WinogradOriginal | Optimización Winograd | O(n³) |
| 5 | WinogradScaled | Winograd con escalado | O(n³) |
| 6 | StrassenNaiv | Divide y vencerás | O(n^2.807) |
| 7 | StrassenWinograd | Strassen optimizado | O(n^2.807) |
| 8 | III.3 Sequential block | Bloques secuenciales | O(n³) |
| 9 | III.4 Parallel Block | Bloques paralelos | O(n³/p) |
| 10 | III.5 Enhanced Parallel | Bloques optimizados | O(n³/p) |
| 11 | IV.3 Sequential block | Bloques optimizados | O(n³) |
| 12 | IV.4 Parallel Block | Bloques paralelos | O(n³/p) |
| 13 | IV.5 Enhanced Parallel | Bloques optimizados | O(n³/p) |
| 14 | V.3 Sequential block | Bloques avanzados | O(n³) |
| 15 | V.4 Parallel Block | Bloques paralelos | O(n³/p) |

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
│   │   ├── main.py                      # Punto de entrada
│   │   ├── algoritmos/                  # 15 algoritmos
│   │   ├── persistence/                  # Persistencia Excel
│   │   │   ├── MatrixFileHandler.py      # Matrices → Excel
│   │   │   └── ResultsExcelHandler.py    # Resultados → Excel + Gráficos
│   │   └── views/                        # Visualización
│   └── requirements.txt
├── README.md
└── DISEÑO.md
```

---

## 9. Prompts Utilizados (IA)

Los prompts fueron realizados **después** de que el estudiante tenía los algoritmos implementados.

| Código | Descripción | Intervención de IA |
|--------|-------------|-------------------|
| P1 | Organizar en paquetes modulares | Creó `persistence/` y `views/` |
| P2 | Medición de tiempos | `time.perf_counter_ns()` |
| P3 | Soporte para 2 casos | `run_case()` con generación dinámica |
| P4 | Documentación de complejidad | Análisis teórico formal |
| P5 | Docstrings en algoritmos | 15 archivos documentados |
| P6 | Medición de memoria | `tracemalloc` para pico de memoria |
| P7 | Verificación de resultados | `np.allclose()` para validar C=A×B |
| P8 | Persistencia Excel | Reemplazó XML por Excel con openpyxl |
| P9 | Corrección de bugs | Bugs identificados y corregidos |

### Participación Real

| Etapa | Estudiante | IA |
|-------|-----------|-----|
| Diseño de algoritmos | 100% | 0% |
| Estructura proyecto | 0% | 100% |
| Persistencia Excel | 0% | 100% |
| Corrección bugs | 30% | 70% |
| Documentación | 30% | 70% |

---

## 10. Bugs Corregidos

| Bug | Algoritmo | Fix |
|-----|-----------|-----|
| Indexación `C[i][k]` | IV.5 Enhanced | → `C[i][j]` |
| Padding incorrecto | StrassenNaiv/Winograd | newSize potencia de 2 |
| Parámetros `submit(N,N,P,M)` | III.5, IV.5 Enhanced | → `submit(N,P,M)` |
| Overflow entero | StrassenWinograd | `[[0]]` → `[[0.0]]` |
| Fórmulas incorrectas | StrassenWinograd | Reescrito completo |

---

## 11. Cómo Ejecutar

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

## 12. Conclusiones

1. **Matrices pequeñas (<64×64)**: Naiv* y Winograd* son más eficientes por bajo overhead
2. **Matrices grandes (>512×512)**: Strassen* y paralelos muestran mejor rendimiento
3. **Strassen**: Trade-off tiempo/memoria - usa ~7x más memoria para ser ~3x más rápido
4. **Paralelización**: Speedup lineal con núcleos, límite práctico ~8-16 hilos

---

## 13. Aclaración Importante

Los 15 algoritmos son implementaciones conocidas de la literatura académica obtenidas de un repositorio GitHub público. La IA协助 únicamente en tareas técnicas de organización, medición, documentación y corrección de bugs, **no en el diseño de los algoritmos**.

---

*Documento actualizado para el Seguimiento 2 - 2026*
