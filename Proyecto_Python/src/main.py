"""
================================================================================
MAIN - MULTIPLICACIÓN DE MATRICES GRANDES
Universidad del Quindío - Ingeniería de Sistemas y Computación
================================================================================

Este módulo ejecuta los 15 algoritmos de multiplicación de matrices con
2 casos de prueba (matrices cuadradas 2^n x 2^n).

MODIFICACIONES REALIZADAS POR IA (Prompts):
- Prompt 1: Estructura principal con soporte para 2 casos
- Prompt 3: Imports de los 15 algoritmos
- Prompt 6: Documentación de funciones

================================================================================
"""
import numpy as np
import time

# ================================================================================
# IMPORTS DE ALGORITMOS (prompt 3 - IA agregó todos los imports)
# ================================================================================
from algoritmos import (
    NaivOnArray, NaivLoopUnrollingTwo, NaivLoopUnrollingFour,
    WinogradOriginal, WinogradScaled, StrassenNaiv, StrassenWinograd,
    III_3_Sequential_Block, III_4_Parallel_Block, III_5_Enhanced_Parallel_Block,
    IV_3_Sequential_Block, IV_4_Parallel_Block, IV_5_Enhanced_Parallel_Block,
    V_3_Sequential_Block, V_4_Parallel_Block
)

from persistence import ResultFileHandler, MatrixFileHandler, ResultsManager
from views import ResultsViewer


# ================================================================================
# CONFIGURACIÓN GLOBAL (prompt 1 - IA modificó para casos de prueba)
# ================================================================================
# Mínimo de dígitos para cada valor de la matriz (>6 según requerimiento)
# Con 7 dígitos: valores de 1,000,000 a 9,999,999
MIN_DIGITS = 7

# Casos de prueba: matrices cuadradas n x n donde n es factor de 2^n
# Caso 1: 512x512 = 2^9 (262,144 elementos por matriz)
# Caso 2: 1024x1024 = 2^10 (1,048,576 elementos por matriz)
SIZES_CASO_1 = [512]
SIZES_CASO_2 = [1024]


# ================================================================================
# LISTA DE ALGORITMOS (orden según tabla del documento)
# ================================================================================
ALGORITHMS = [
    NaivOnArray,              # 1
    NaivLoopUnrollingTwo,     # 2
    NaivLoopUnrollingFour,    # 3
    WinogradOriginal,        # 4
    WinogradScaled,           # 5
    StrassenNaiv,            # 6
    StrassenWinograd,        # 7
    III_3_Sequential_Block,  # 8
    III_4_Parallel_Block,    # 9
    III_5_Enhanced_Parallel_Block,  # 10
    IV_3_Sequential_Block,   # 11
    IV_4_Parallel_Block,     # 12
    IV_5_Enhanced_Parallel_Block,   # 13
    V_3_Sequential_Block,    # 14
    V_4_Parallel_Block,      # 15
]


# ================================================================================
# FUNCIONES DE GENERACIÓN Y PERSISTENCIA
# ================================================================================

def matrix_generator(n, min_digits):
    """
    Genera una matriz cuadrada n x n con valores aleatorios.

    Args:
        n: Dimensión de la matriz (n x n)
        min_digits: Cantidad mínima de dígitos para los valores

    Returns:
        np.ndarray: Matriz n x n con valores aleatorios

    Notas (prompt 1 - IA modificó):
    - Genera valores con mínimo de dígitos configurable
    - Usa numpy para mejor rendimiento
    """
    max_val = 10 ** min_digits - 1
    return np.random.randint(1, max_val, size=(n, n))


def save_matrix(matrix, size, case):
    """
    Guarda una matriz en un archivo XML.

    Args:
        matrix: Matriz a guardar
        size: Tamaño n de la matriz n x n
        case: Identificador del caso ("Caso1" o "Caso2")
    """
    MatrixFileHandler.MatrixFileHandler.save_matrix(
        matrix, f"matrix_{case}_{size}x{size}"
    )


def load_matrix(size, case):
    """
    Carga una matriz desde un archivo XML.

    Args:
        size: Tamaño n de la matriz n x n
        case: Identificador del caso ("Caso1" o "Caso2")

    Returns:
        np.ndarray: Matriz cargada
    """
    return MatrixFileHandler.MatrixFileHandler.load_matrix(
        f"matrix_{case}_{size}x{size}"
    )


def process_algorithm(matrix_a, matrix_b, algorithm_class, size, case):
    """
    Ejecuta un algoritmo y guarda su tiempo de ejecución.

    Args:
        matrix_a: Matriz A
        matrix_b: Matriz B
        algorithm_class: Clase del algoritmo a ejecutar
        size: Tamaño de la matriz
        case: Caso de prueba ("Caso1" o "Caso2")

    Notas (prompt 1 - IA modificó):
    - Usa time.perf_counter_ns() para precisión en nanosegundos
    - Guarda resultado con caso diferenciado
    """
    start_time = time.perf_counter_ns()
    algorithm_class.multiply(matrix_a, matrix_b)
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time

    ResultFileHandler.ResultFileHandler.save_result(
        size=size,
        algorithm=algorithm_class.__name__,
        execution_time=execution_time,
        case=case,
        rows=size,
        cols=size
    )


def run_case(sizes, case_name):
    """
    Ejecuta todos los algoritmos para un caso de prueba.

    Args:
        sizes: Lista de tamaños n para matrices n x n
        case_name: Nombre del caso ("Caso1" o "Caso2")

    Notas (prompt 1 - IA creó):
    - Genera matrices nuevas para cada ejecución
    - Guarda matrices en XML para persistencia
    - Ejecuta los 15 algoritmos secuencialmente
    """
    print(f"\n{'='*50}")
    print(f"Ejecutando {case_name}")
    print(f"{'='*50}")

    for size in sizes:
        print(f"\n--- Tamaño: {size}x{size} ---")

        # Generar matrices con valores aleatorios de 7 dígitos mínimo
        matrix_a = matrix_generator(size, MIN_DIGITS)
        matrix_b = matrix_generator(size, MIN_DIGITS)

        # Guardar matrices en XML para persistencia
        save_matrix(matrix_a, size, case_name)
        save_matrix(matrix_b, size, case_name)

        # Cargar matrices guardadas
        matrix_a = load_matrix(size, case_name)
        matrix_b = load_matrix(size, case_name)

        # Ejecutar cada algoritmo
        for algorithm_class in ALGORITHMS:
            print(f"  Ejecutando {algorithm_class.__name__}...", end=" ")
            process_algorithm(matrix_a, matrix_b, algorithm_class, size, case_name)
            print("OK")


def display_results():
    """
    Carga y muestra los resultados en un gráfico de barras.

    Notas (prompt 1 - IA creó):
    - Usa ResultsViewer para mostrar gráfico comparativo
    - Combina resultados de múltiples lenguajes si existen
    """
    results = ResultsManager.ResultsManager.get_combined_results()
    if not results:
        print("No hay resultados para mostrar.")
        print("Descomenta las líneas de run_case() para generar resultados.")
        return

    app = ResultsViewer.ResultsViewer(results)
    app.mainloop()


# ================================================================================
# PUNTO DE ENTRADA
# ================================================================================

if __name__ == "__main__":
    """
    ================================================================================
    INSTRUCCIONES DE USO:
    ================================================================================

    1. Para generar matrices y ejecutar algoritmos, descomenta las líneas:

        run_case(SIZES_CASO_1, "Caso1")  # Matrices 512x512
        run_case(SIZES_CASO_2, "Caso2")  # Matrices 1024x1024

    2. Los resultados se guardarán automáticamente en:
        - src/main/resources/matrices/ (matrices XML)
        - src/main/resources/results/ (tiempos XML)

    3. El gráfico de barras se mostrará al final.

    4. Para ver solo resultados previos, deja todo comentado.
    ================================================================================
    """
    # ================================================================================
    # (prompt 1 - IA configuró para 2 casos de prueba)
    # ================================================================================
    # Descomentar para ejecutar:
    run_case(SIZES_CASO_1, "Caso1")
    run_case(SIZES_CASO_2, "Caso2")

    # Mostrar gráfico de resultados
    display_results()