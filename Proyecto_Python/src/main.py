"""
Main para ejecutar los algoritmos de multiplicación de matrices.
Cada algoritmo se prueba con 2 casos de matrices cuadradas 2^n x 2^n.
"""
import numpy as np
import time

from algoritmos import (
    NaivOnArray, NaivLoopUnrollingTwo, NaivLoopUnrollingFour,
    WinogradOriginal, WinogradScaled, StrassenNaiv, StrassenWinograd,
    III_3_Sequential_Block, III_4_Parallel_Block, III_5_Enhanced_Parallel_Block,
    IV_3_Sequential_Block, IV_4_Parallel_Block, IV_5_Enhanced_Parallel_Block,
    V_3_Sequential_Block, V_4_Parallel_Block
)

from persistence import ResultFileHandler, MatrixFileHandler, ResultsManager
from views import ResultsViewer


# ===================== CONFIGURACIÓN =====================
# Cantidad mínima de dígitos para cada valor de la matriz (>6)
MIN_DIGITS = 7  # Genera valores de 1,000,000 a 9,999,999

# ===================== CASOS DE PRUEBA =====================
# Caso 1: matrices cuadradas n*n donde n es factor de 2^n
# Ejemplo: 512x512 = 2^9
SIZES_CASO_1 = [512]

# Caso 2: matrices cuadradas de diferente tamaño
# Ejemplo: 1024x1024 = 2^10
SIZES_CASO_2 = [1024]


# ===================== ALGORITMOS =====================
ALGORITHMS = [
    NaivOnArray,
    NaivLoopUnrollingTwo,
    NaivLoopUnrollingFour,
    WinogradOriginal,
    WinogradScaled,
    StrassenNaiv,
    StrassenWinograd,
    III_3_Sequential_Block,
    III_4_Parallel_Block,
    III_5_Enhanced_Parallel_Block,
    IV_3_Sequential_Block,
    IV_4_Parallel_Block,
    IV_5_Enhanced_Parallel_Block,
    V_3_Sequential_Block,
    V_4_Parallel_Block,
]


def matrix_generator(n, min_digits):
    """
    Genera una matriz cuadrada n x n con valores aleatorios.

    Args:
        n: Dimensión de la matriz (n x n)
        min_digits: Cantidad mínima de dígitos para los valores

    Returns:
        np.ndarray: Matriz n x n con valores aleatorios de min_digits dígitos
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
    """
    print(f"\n{'='*50}")
    print(f"Ejecutando {case_name}")
    print(f"{'='*50}")

    for size in sizes:
        print(f"\n--- Tamaño: {size}x{size} ---")

        matrix_a = matrix_generator(size, MIN_DIGITS)
        matrix_b = matrix_generator(size, MIN_DIGITS)
        save_matrix(matrix_a, size, case_name)
        save_matrix(matrix_b, size, case_name)

        matrix_a = load_matrix(size, case_name)
        matrix_b = load_matrix(size, case_name)

        for algorithm_class in ALGORITHMS:
            print(f"  Ejecutando {algorithm_class.__name__}...", end=" ")
            process_algorithm(matrix_a, matrix_b, algorithm_class, size, case_name)
            print("OK")


def display_results():
    """Carga y muestra los resultados en un gráfico de barras."""
    results = ResultsManager.ResultsManager.get_combined_results()
    if not results:
        print("No hay resultados para mostrar.")
        return

    app = ResultsViewer.ResultsViewer(results)
    app.mainloop()


if __name__ == "__main__":
    # Descomentar para generar matrices y ejecutar algoritmos
    # run_case(SIZES_CASO_1, "Caso1")
    # run_case(SIZES_CASO_2, "Caso2")

    display_results()