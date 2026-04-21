"""
================================================================================
MAIN - Multiplicación de Matrices Grandes
================================================================================
Este script ejecuta los algoritmos de multiplicación de matrices y guarda los 
resultados para su análisis posterior.

Configuración:
    - MIN_DIGITS: Número mínimo de dígitos para cada valor en la matriz (>6)
    - CASO_1 / CASO_2: Tamaños de matrices para cada caso de prueba

Ejemplo de uso:
    python main.py
================================================================================
"""

import numpy as np
import time
from typing import List, Callable

# Importar todos los algoritmos disponibles
from algoritmos import (
    NaivOnArray, 
    NaivLoopUnrollingTwo, 
    NaivLoopUnrollingFour, 
    III_3_Sequential_Block, 
    III_4_Parallel_Block, 
    III_5_Enhanced_Parallel_Block, 
    IV_3_Sequential_Block, 
    IV_4_Parallel_Block, 
    IV_5_Enhanced_Parallel_Block, 
    V_3_Sequential_Block, 
    V_4_Parallel_Block,
    StrassenNaiv, 
    WinogradOriginal, 
    WinogradScaled, 
    StrassenWinograd
)

from persistence import ResultFileHandler, MatrixFileHandler, ResultsManager
from views import ResultsViewer


# ================================================================================
# CONFIGURACIÓN - Modificar según sea necesario
# ================================================================================

# Dígitos mínimos para cada valor en la matriz (el requerimiento dice >6)
# MIN_DIGITS = 7 significa valores entre 1,000,000 y 9,999,999 (7 dígitos)
MIN_DIGITS = 7

# ================================================================================
# CASOS DE PRUEBA
# ================================================================================
# Cada caso es una lista de enteros que representan el tamaño n de matrices n×n
# donde n es una potencia de 2 (2^n): 8, 16, 32, 64, 128, 256, etc.
#
# La estructura es: (tamano_matriz_A, tamano_matriz_B)
# Para multiplicar matrices cuadradas: tamano_A == tamano_B
# Para multiplicar rectangulares: tamano_A != tamano_B (solo algunos algoritmos lo soportan)
#
# CASO 1: Matrices de prueba (tamaños diferentes a Caso 2)
# Ejemplo: matriz1 (8x8) * matriz2 (8x8) = 8x8
#         matriz1 (16x16) * matriz2 (16x16) = 16x16
CASO_1_TAMANOS = [
    8,    # 8x8 * 8x8
    16,   # 16x16 * 16x16
    32,   # 32x32 * 32x32
    64,   # 64x64 * 64x64
]

# CASO 2: Matrices diferentes (otros tamaños)
# Ejemplo: matriz1 (64x64) * matriz2 (64x64) = 64x64
#         matriz1 (128x128) * matriz2 (128x128) = 128x128
CASO_2_TAMANOS = [
    64,    # 64x64 * 64x64
    128,   # 128x128 * 128x128
    256,   # 256x256 * 256x256
    512,   # 512x512 * 512x512
]

# ================================================================================
# ALGORITMOS A EJECUTAR
# ================================================================================
# Lista de tuplas (nombre_del_algoritmo, funcion_multiply)
# Descomenta los algoritmos que quieras ejecutar:
ALGORITHMS = [
    # Algoritmos iterativos básicos (O(n³))
    ("NaivOnArray", NaivOnArray.multiply),
    ("NaivLoopUnrollingTwo", NaivLoopUnrollingTwo.multiply),
    ("NaivLoopUnrollingFour", NaivLoopUnrollingFour.multiply),
    
    # Algoritmos de Winograd (optimización de multiplicaciones)
    ("WinogradOriginal", WinogradOriginal.multiply),
    ("WinogradScaled", WinogradScaled.multiply),
    
    # Algoritmos de Strassen (Divide y Vencerás, O(n^2.807))
    ("StrassenNaiv", StrassenNaiv.multiply),
    ("StrassenWinograd", StrassenWinograd.multiply),
    
    # Algoritmos de Bloque - Nivel III
    ("III_3_Sequential_Block", III_3_Sequential_Block.multiply),
    ("III_4_Parallel_Block", III_4_Parallel_Block.multiply),
    ("III_5_Enhanced_Parallel_Block", III_5_Enhanced_Parallel_Block.multiply),
    
    # Algoritmos de Bloque - Nivel IV
    ("IV_3_Sequential_Block", IV_3_Sequential_Block.multiply),
    ("IV_4_Parallel_Block", IV_4_Parallel_Block.multiply),
    ("IV_5_Enhanced_Parallel_Block", IV_5_Enhanced_Parallel_Block.multiply),
    
    # Algoritmos de Bloque - Nivel V
    ("V_3_Sequential_Block", V_3_Sequential_Block.multiply),
    ("V_4_Parallel_Block", V_4_Parallel_Block.multiply),
]

# Bandera para generar nuevas matrices o usar existentes
# True = generar nuevas matrices, False = usar existentes
GENERATE_MATRICES = True


# ================================================================================
# FUNCIONES AUXILIARES
# ================================================================================

def matrix_generator(n: int, min_digits: int) -> np.ndarray:
    """
    Genera una matriz cuadrada n×n con valores aleatorios.
    
    Args:
        n: Tamaño de la matriz (n × n)
        min_digits: Dígitos mínimos para cada valor
    
    Returns:
        Matriz numpy n×n con valores aleatorios
    """
    max_val = 10 ** min_digits - 1
    return np.random.randint(1, max_val, size=(n, n))


def get_matrix_name(prefix: str, n: int, case: str) -> str:
    """
    Genera el nombre del archivo para la matriz cuadrada.
    
    Args:
        prefix: Prefijo (matrix_A o matrix_B)
        n: Tamaño de la matriz (n × n)
        case: Nombre del caso (Caso1 o Caso2)
    
    Returns:
        Nombre del archivo, ej: "matrix_A_Caso1_8x8"
    """
    return f"{prefix}_{case}_{n}x{n}"


def process_algorithm(
    n: int,
    case: str,
    algorithm_name: str, 
    algorithm_executor: Callable
) -> None:
    """
    Ejecuta un algoritmo de multiplicación y guarda el resultado.
    
    Args:
        n: Tamaño de la matriz (n × n)
        case: Nombre del caso de prueba (Caso1 o Caso2)
        algorithm_name: Nombre del algoritmo
        algorithm_executor: Función que ejecuta el algoritmo
    """
    # Cargar las matrices desde archivos XML
    matrix_a_name = get_matrix_name("matrix_A", n, case)
    matrix_b_name = get_matrix_name("matrix_B", n, case)
    
    matrix_a = MatrixFileHandler.MatrixFileHandler.load_matrix(matrix_a_name)
    matrix_b = MatrixFileHandler.MatrixFileHandler.load_matrix(matrix_b_name)
    
    # Ejecutar el algoritmo y medir tiempo
    start_time = time.perf_counter_ns()
    algorithm_executor(matrix_a, matrix_b)
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time
    
    # Guardar resultado
    ResultFileHandler.ResultFileHandler.save_result(
        size=n*n,  # Para compatibilidad hacia atrás (size = total elementos)
        algorithm=algorithm_name,
        execution_time=execution_time,
        case=case,
        rows=n,
        cols=n
    )


def generate_matrices_for_case(tamanos: List[int], case_name: str) -> None:
    """
    Genera y guarda las matrices cuadradas para un caso de prueba.
    
    Args:
        tamanos: Lista de tamaños n para matrices n×n
        case_name: Nombre del caso (Caso1 o Caso2)
    """
    for n in tamanos:
        # Generar matrices cuadradas n×n
        matrix_a = matrix_generator(n, MIN_DIGITS)
        matrix_b = matrix_generator(n, MIN_DIGITS)
        
        # Guardar matrices
        name_a = get_matrix_name("matrix_A", n, case_name)
        name_b = get_matrix_name("matrix_B", n, case_name)
        
        MatrixFileHandler.MatrixFileHandler.save_matrix(matrix_a, name_a)
        MatrixFileHandler.MatrixFileHandler.save_matrix(matrix_b, name_b)
        
        print(f"Generadas matrices {case_name}: {name_a}, {name_b}")


def run_algorithms_for_case(tamanos: List[int], case_name: str) -> None:
    """
    Ejecuta todos los algoritmos para un caso de prueba.
    
    Args:
        tamanos: Lista de tamaños n para matrices n×n
        case_name: Nombre del caso (Caso1 o Caso2)
    """
    for n in tamanos:
        print(f"\nEjecutando algoritmos para {case_name}: matriz {n}x{n}")
        
        for algorithm_name, algorithm_executor in ALGORITHMS:
            try:
                process_algorithm(
                    n,
                    case_name,
                    algorithm_name, 
                    algorithm_executor
                )
                print(f"  - {algorithm_name}: OK")
            except Exception as e:
                print(f"  - {algorithm_name}: ERROR - {e}")


def display_results() -> None:
    """
    Muestra los resultados en un gráfico de barras.
    """
    results = ResultsManager.ResultsManager.get_combined_results()
    app = ResultsViewer.ResultsViewer(results)
    app.mainloop()


# ================================================================================
# PUNTO DE ENTRADA
# ================================================================================

if __name__ == "__main__":
    # 1. Generar matrices (solo si GENERATE_MATRICES = True)
    if GENERATE_MATRICES:
        print("=" * 60)
        print("GENERANDO MATRICES PARA CASO 1")
        print("=" * 60)
        generate_matrices_for_case(CASO_1_TAMANOS, "Caso1")
        
        print("\n" + "=" * 60)
        print("GENERANDO MATRICES PARA CASO 2")
        print("=" * 60)
        generate_matrices_for_case(CASO_2_TAMANOS, "Caso2")
    
    # 2. Ejecutar algoritmos para cada caso
    print("\n" + "=" * 60)
    print("EJECUTANDO ALGORITMOS PARA CASO 1")
    print("=" * 60)
    run_algorithms_for_case(CASO_1_TAMANOS, "Caso1")
    
    print("\n" + "=" * 60)
    print("EJECUTANDO ALGORITMOS PARA CASO 2")
    print("=" * 60)
    run_algorithms_for_case(CASO_2_TAMANOS, "Caso2")
    
    # 3. Mostrar resultados (opcional)
    print("\n" + "=" * 60)
    print("MOSTRANDO RESULTADOS")
    print("=" * 60)
    display_results()
