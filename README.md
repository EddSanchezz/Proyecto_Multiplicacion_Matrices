# Proyecto: Multiplicación de Matrices Grandes

Universidad del Quindío - Programa de Ingeniería de Sistemas y Computación

## Propósito

Implementar y analizar algoritmos que permitan la multiplicación de matrices grandes mediante algoritmos iterativos y algoritmos divide y vencerás.

## Seguimiento 2 - Casos de Prueba

Matrices cuadradas n×n donde n es factor de 2^n, con valores de mínimo 6 dígitos.

| Caso | Dimensión | Descripción |
|------|---------|-----------|
| 1 | 512×512 (2⁹) | Matrices cuadradas 2^n |
| 2 | 1024×1024 (2¹⁰) | Matrices cuadradas 2^n |

## Algoritmos Implementados

### Algoritmos Básicos (Iterativos)

| # | Algoritmo | Complejidad |
|---|----------|------------|
| 1 | NaivOnArray | O(n³) |
| 2 | NaivLoopUnrollingTwo | O(n³) |
| 3 | NaivLoopUnrollingFour | O(n³) |
| 4 | WinogradOriginal | O(n³) |
| 5 | WinogradScaled | O(n³) |

### Algoritmos Divide y Vencerás

| # | Algoritmo | Complejidad |
|---|----------|------------|
| 6 | StrassenNaiv | O(n^log₂7) ≈ O(n^2.807) |
| 7 | StrassenWinograd | O(n^log₂7) ≈ O(n^2.807) |

### Algoritmos por Bloques (Nivel 3)

| # | Algoritmo | Complejidad |
|---|----------|------------|
| 8 | III.3 Sequential block | O(n³) |
| 9 | III.4 Parallel Block | O(n³/p) |
| 10 | III.5 Enhanced Parallel Block | O(n³/p) |

### Algoritmos por Bloques (Nivel 4)

| # | Algoritmo | Complejidad |
|---|----------|------------|
| 11 | IV.3 Sequential block | O(n³) |
| 12 | IV.4 Parallel Block | O(n³/p) |
| 13 | IV.5 Enhanced Parallel Block | O(n³/p) |

### Algoritmos por Bloques (Nivel 5)

| # | Algoritmo | Complejidad |
|---|----------|------------|
| 14 | V.3 Sequential block | O(n³) |
| 15 | V.4 Parallel Block | O(n³/p) |

## Complejidad Algorítmica - Tabla Resumen

| Algoritmo | O(n³) | O(n^log₂7) | O(n³/p) |
|----------|--------|-------------|---------|
| NaivOnArray | ✓ | | |
| NaivLoopUnrollingTwo | ✓ | | |
| NaivLoopUnrollingFour | ✓ | | |
| WinogradOriginal | ✓ | | |
| WinogradScaled | ✓ | | |
| StrassenNaiv | | ✓ | |
| StrassenWinograd | | ✓ | |
| III/IV/V Sequential | ✓ | | |
| III/IV/V Parallel | | | | ✓ |
| III/IV/V Enhanced | | | ✓ |

## Estructura del Proyecto

```
Proyecto_Python/
├── src/
│   ├── main.py                 # Punto de entrada
│   ├── algoritmos/              # 15 algoritmos implementados
│   │   ├── NaivOnArray.py
│   │   ├── NaivLoopUnrollingTwo.py
│   │   ├── NaivLoopUnrollingFour.py
│   │   ├── WinogradOriginal.py
│   │   ├── WinogradScaled.py
│   │   ├── StrassenNaiv.py
│   │   ├── StrassenWinograd.py
│   │   ├── III_3_Sequential_Block.py
│   │   ├── III_4_Parallel_Block.py
│   │   ├── III_5_Enhanced_Parallel_Block.py
│   │   ├── IV_3_Sequential_Block.py
│   │   ├── IV_4_Parallel_Block.py
│   │   ├── IV_5_Enhanced_Parallel_Block.py
│   │   ├── V_3_Sequential_Block.py
│   │   └── V_4_Parallel_Block.py
│   ├── persistence/             # Manejo de archivos XML
│   └── views/                 # Visualización de resultados
└── .gitignore
```

## Ejecución

1. Configurar los tamaños de matriz en `src/main.py`:
```python
SIZES_CASO_1 = [512]  # o [8, 16, 32, 64]
SIZES_CASO_2 = [1024]  # o [8, 16, 32, 64]
```

2. Descomentar las líneas de ejecución:
```python
run_case(SIZES_CASO_1, "Caso1")
run_case(SIZES_CASO_2, "Caso2")
```

3. Ejecutar:
```bash
cd Proyecto_Python
python src/main.py
```

## Requisitos

- Python 3.8+
- numpy
- tkinter (incluido en Python)

## Autor

Universidad del Quindío - Ingeniería de Sistemas y Computación