"""
================================================================================
MAIN - MULTIPLICACIÓN DE MATRICES GRANDES
Universidad del Quindío - Ingeniería de Sistemas y Computación
================================================================================

Este módulo ejecuta los 15 algoritmos de multiplicación de matrices con
2 casos de prueba (matrices cuadradas 2^n x 2^n).

Persistencia en formato Excel para legibilidad:
- Matrices: Archivos .xlsx con hojas "Matriz A", "Matriz B", "Info"
- Resultados: Archivo .xlsx con hojas "Caso1", "Caso2", "Comparativa", "Gráfico"
- Gráfico comparativo: Archivo .png separado

Funcionalidades adicionales:
- Verificación de resultados: Valida que C = A × B usando NumPy como referencia
- Medición de memoria: Registra pico de memoria usado por cada algoritmo

================================================================================
"""
import numpy as np
import time
import tracemalloc

from algoritmos import (
    NaivOnArray, NaivLoopUnrollingTwo, NaivLoopUnrollingFour,
    WinogradOriginal, WinogradScaled, StrassenNaiv, StrassenWinograd,
    III_3_Sequential_Block, III_4_Parallel_Block, III_5_Enhanced_Parallel_Block,
    IV_3_Sequential_Block, IV_4_Parallel_Block, IV_5_Enhanced_Parallel_Block,
    V_3_Sequential_Block, V_4_Parallel_Block
)

from persistence.ResultsExcelHandler import ResultsExcelHandler
from persistence.MatrixFileHandler import MatrixFileHandler


MIN_DIGITS = 7

SIZES_CASO_1 = [16]
SIZES_CASO_2 = [32]


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

ALGORITHM_NAMES = {
    NaivOnArray: "NaivOnArray",
    NaivLoopUnrollingTwo: "NaivLoopUnrollingTwo",
    NaivLoopUnrollingFour: "NaivLoopUnrollingFour",
    WinogradOriginal: "WinogradOriginal",
    WinogradScaled: "WinogradScaled",
    StrassenNaiv: "StrassenNaiv",
    StrassenWinograd: "StrassenWinograd",
    III_3_Sequential_Block: "III_3_Sequential_Block",
    III_4_Parallel_Block: "III_4_Parallel_Block",
    III_5_Enhanced_Parallel_Block: "III_5_Enhanced_Parallel_Block",
    IV_3_Sequential_Block: "IV_3_Sequential_Block",
    IV_4_Parallel_Block: "IV_4_Parallel_Block",
    IV_5_Enhanced_Parallel_Block: "IV_5_Enhanced_Parallel_Block",
    V_3_Sequential_Block: "V_3_Sequential_Block",
    V_4_Parallel_Block: "V_4_Parallel_Block",
}


def matrix_generator(n, min_digits):
    """
    Genera una matriz cuadrada n x n con valores aleatorios.

    Args:
        n: Dimensión de la matriz (n x n)
        min_digits: Cantidad mínima de dígitos para los valores

    Returns:
        np.ndarray: Matriz n x n con valores aleatorios
    """
    max_val = 10 ** min_digits - 1
    return np.random.randint(1, max_val, size=(n, n))


def save_matrix(matrix_a, matrix_b, size, case):
    """
    Guarda dos matrices en un archivo Excel.

    Args:
        matrix_a: Primera matriz (N×N)
        matrix_b: Segunda matriz (N×N)
        size: Tamaño n de la matriz n x n
        case: Identificador del caso ("Caso1" o "Caso2")
    """
    MatrixFileHandler.save_matrix(matrix_a, matrix_b, size, case)


def load_matrix(size, case):
    """
    Carga dos matrices desde un archivo Excel.

    Args:
        size: Tamaño n de la matriz n x n
        case: Identificador del caso ("Caso1" o "Caso2")

    Returns:
        tuple: (matriz_a, matriz_b) ambas como np.ndarray
    """
    return MatrixFileHandler.load_matrix(size, case)


def verify_result(matrix_a, matrix_b, result):
    """
    Verifica que el resultado de la multiplicación sea correcto usando NumPy.

    Args:
        matrix_a: Matriz A (np.ndarray)
        matrix_b: Matriz B (np.ndarray)
        result: Matriz resultado del algoritmo a verificar (list)

    Returns:
        bool: True si el resultado es correcto, False en caso contrario
    """
    expected = np.matmul(matrix_a, matrix_b)
    result_array = np.array(result)
    return np.allclose(expected, result_array, rtol=1e-5, atol=1e-8)


def process_algorithm(matrix_a, matrix_b, algorithm_func, size, case):
    """
    Ejecuta un algoritmo y mide tiempo y memoria.

    Args:
        matrix_a: Matriz A
        matrix_b: Matriz B
        algorithm_func: Función del algoritmo a ejecutar
        size: Tamaño de la matriz
        case: Caso de prueba ("Caso1" o "Caso2")

    Returns:
        dict: Diccionario con tiempo de ejecución, memoria, verificación y metadatos
    """
    alg_name = ALGORITHM_NAMES.get(algorithm_func, algorithm_func.__name__)

    tracemalloc.start()
    start_time = time.perf_counter_ns()
    result = algorithm_func(matrix_a, matrix_b)
    end_time = time.perf_counter_ns()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    execution_time = end_time - start_time

    memory_kb = peak / 1024

    is_correct = verify_result(matrix_a, matrix_b, result)

    return {
        'size': size,
        'algorithm': alg_name,
        'language': 'python',
        'executionTime': execution_time,
        'case': case,
        'rows': size,
        'cols': size,
        'memory_kb': memory_kb,
        'verified': is_correct,
        'time_ms': execution_time / 1_000_000
    }


def run_case(sizes, case_name):
    """
    Ejecuta todos los algoritmos para un caso de prueba.

    Args:
        sizes: Lista de tamaños n para matrices n x n
        case_name: Nombre del caso ("Caso1" o "Caso2")

    Returns:
        list: Lista de diccionarios con resultados de todos los algoritmos
    """
    print(f"\n{'='*70}")
    print(f"Ejecutando {case_name}")
    print(f"{'='*70}")

    all_results = []

    for size in sizes:
        print(f"\n--- Tamaño: {size}x{size} ---")

        matrix_a = matrix_generator(size, MIN_DIGITS)
        matrix_b = matrix_generator(size, MIN_DIGITS)

        print(f"  Guardando matrices en Excel...")
        save_matrix(matrix_a, matrix_b, size, case_name)
        print(f"  Matrices guardadas: src/main/resources/matrices/matrix_{case_name}_{size}x{size}.xlsx")

        matrix_a, matrix_b = load_matrix(size, case_name)

        print(f"\n  {'Algoritmo':<35} {'Tiempo (ms)':<12} {'Memoria':<12} {'Verificado':<12}")
        print(f"  {'-'*35} {'-'*12} {'-'*12} {'-'*12}")

        for algorithm_func in ALGORITHMS:
            result = process_algorithm(matrix_a, matrix_b, algorithm_func, size, case_name)
            all_results.append(result)

            alg_name = result['algorithm']
            time_ms = result['time_ms']
            memory_kb = result['memory_kb']
            verified = "[OK]" if result['verified'] else "[FAIL]"
            mem_str = f"{memory_kb:.1f} KB" if memory_kb < 1024 else f"{memory_kb/1024:.2f} MB"
            print(f"  {alg_name:<35} {time_ms:<12.3f} {mem_str:<12} {verified:<12}")

    return all_results


def display_summary(case1_results, case2_results):
    """
    Muestra el resumen de resultados y genera los archivos Excel y PNG.

    Args:
        case1_results (list): Resultados del caso 1
        case2_results (list): Resultados del caso 2
    """
    print("\n" + "=" * 70)
    print("RESUMEN DE RESULTADOS")
    print("=" * 70)

    case1_by_alg = {r['algorithm']: r for r in case1_results}
    case2_by_alg = {r['algorithm']: r for r in case2_results}

    print(f"\n{'Algoritmo':<35} {'Caso1 (ms)':<12} {'Caso1 Mem':<12} {'Caso2 (ms)':<12} {'Caso2 Mem':<12}")
    print(f" {'-'*35} {'-'*12} {'-'*12} {'-'*12} {'-'*12}")

    for alg_name in ResultsExcelHandler.ALGORITHM_NAMES:
        r1 = case1_by_alg.get(alg_name, {})
        r2 = case2_by_alg.get(alg_name, {})
        c1_time = r1.get('time_ms', 0)
        c2_time = r2.get('time_ms', 0)
        c1_mem = r1.get('memory_kb', 0)
        c2_mem = r2.get('memory_kb', 0)
        c1_mem_str = f"{c1_mem:.1f} KB" if c1_mem < 1024 else f"{c1_mem/1024:.2f} MB"
        c2_mem_str = f"{c2_mem:.1f} KB" if c2_mem < 1024 else f"{c2_mem/1024:.2f} MB"
        print(f" {alg_name:<35} {c1_time:<12.3f} {c1_mem_str:<12} {c2_time:<12.3f} {c2_mem_str:<12}")

    all_results = case1_results + case2_results

    print("\nGenerando archivo Excel con resultados...")
    ResultsExcelHandler.save_all_results(all_results)
    print(f"  Archivo: src/main/resources/results/python_results.xlsx")
    print(f"  Gráfico: src/main/resources/results/grafico_comparativo.png")
    print("\nEl archivo Excel contiene:")
    print(f"  - Hoja 'Caso1': Tiempos y memoria para {SIZES_CASO_1[0]}x{SIZES_CASO_1[0]}")
    print(f"  - Hoja 'Caso2': Tiempos y memoria para {SIZES_CASO_2[0]}x{SIZES_CASO_2[0]}")
    print("  - Hoja 'Comparativa': Resumen comparativo")
    print("  - Hoja 'Gráfico': Imagen del gráfico comparativo")


if __name__ == "__main__":
    print("=" * 70)
    print("MULTIPLICACIÓN DE MATRICES GRANDES")
    print("Universidad del Quindío - Ingeniería de Sistemas")
    print("=" * 70)

    case1_results = run_case(SIZES_CASO_1, "Caso1")
    case2_results = run_case(SIZES_CASO_2, "Caso2")

    display_summary(case1_results, case2_results)
