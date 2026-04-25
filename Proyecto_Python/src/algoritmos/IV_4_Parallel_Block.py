"""
Algoritmo IV_4_Parallel_Block - Multiplicación por Bloques Paralela (Nivel 4)

Implementación de multiplicación de matrices por bloques en su variante
paralela de cuarto nivel de optimización.

Complejidad Computacional:
    - Temporal: O(n³/p) donde p = número de threads
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³/p

Descripción:
    Cuarta iteración del algoritmo de multiplicación por bloques
    con paralelización mediante ThreadPoolExecutor.
    
    A diferencia de III.4, esta variante tiene un orden de bucles
    diferente que puede mejorar la locality del acceso a B.

Técnica:
    - ThreadPoolExecutor para paralelismo
    - División por bloques de filas de A
    - block_multiply() recibe i_start en lugar de rango completo
    - block_size = N por defecto

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Columnas de A / Filas de B
    M (int): Número de columnas de B
    block_size (int): Tamaño de los bloques

Retorna:
    list: Matriz resultado de dimensiones N×M
"""


from concurrent.futures import ThreadPoolExecutor


def block_multiply(matrizA, matrizB, matrizRes, i_start, N, P, M, block_size):
    """
    Multiplicación de un bloque de filas (variante IV).
    
    Args:
        matrizA (list): Matriz A (N×P)
        matrizB (list): Matriz B (P×M)
        matrizRes (list): Matriz resultado (N×M)
        i_start (int): Índice inicial de fila para este bloque
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    """
    i_end = min(i_start + block_size, N)
    for j1 in range(0, P, block_size):
        for k1 in range(0, M, block_size):
            for i in range(i_start, i_end):
                for j in range(j1, min(j1 + block_size, P)):
                    for k in range(k1, min(k1 + block_size, M)):
                        matrizRes[i][k] += matrizA[i][j] * matrizB[j][k]


def alg_IV_4_Parallel_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela (variante IV).
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    
    Returns:
        list: Matriz resultado N×M
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    num_blocks = (N + block_size - 1) // block_size
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(block_multiply, matrizA, matrizB, matrizRes, i_start, N, P, M, block_size)
            for i_start in range(0, N, block_size)
        ]
        for future in futures:
            future.result()
    
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo IV_4_Parallel_Block.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N
    return alg_IV_4_Parallel_Block(matrizA, matrizB, N, P, M, block_size)
