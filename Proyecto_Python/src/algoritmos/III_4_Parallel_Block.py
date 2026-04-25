"""
Algoritmo III_4_Parallel_Block - Multiplicación por Bloques Paralela (Nivel 3)

Implementación de multiplicación de matrices mediante el método de bloques
con paralelización por ThreadPoolExecutor.

Complejidad Computacional:
    - Temporal: O(n³/p) donde p = número de threads
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³/p

Descripción:
    Variante paralela del algoritmo de bloques (III.3). El algoritmo
    divide la matriz A por filas en bloques y procesa cada bloque
    en un thread separado.
    
    Cada worker procesa un conjunto de filas, y dentro de su conjunto
    aplica el método de bloques completo.

Técnica:
    - ThreadPoolExecutor para paralelismo
    - División por filas de A
    - Un thread por bloque de filas
    - Sincronización implícita con future.result()

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Columnas de A / Filas de B
    M (int): Número de columnas de B
    block_size (int): Tamaño de los bloques

Retorna:
    list: Matriz resultado de dimensiones N×M

Nota:
    - El número de workers depende de N/block_size
    - La matriz resultado se comparte entre threads (no es thread-safe
      para escritura concurrencia, pero aquí se evita con la división)
"""


from concurrent.futures import ThreadPoolExecutor, as_completed


def block_multiply(matrizA, matrizB, matrizRes, i1, N, P, M, block_size):
    """
    Multiplicación de un bloque de filas.
    
    Args:
        matrizA (list): Matriz A (N×P)
        matrizB (list): Matriz B (P×M)
        matrizRes (list): Matriz resultado (N×M)
        i1 (int): Índice inicial de fila para este bloque
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    
    Note:
        Cada thread procesa un rango diferente de filas (i1 a i1+block_size).
        Dentro de ese rango, aplica el método de bloques completo.
    """
    for j1 in range(0, M, block_size):
        for k1 in range(0, P, block_size):
            i_end = min(i1 + block_size, N)
            j_end = min(j1 + block_size, M)
            k_end = min(k1 + block_size, P)
            
            for i in range(i1, i_end):
                for j in range(j1, j_end):
                    for k in range(k1, k_end):
                        matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]


def alg_III_4_Parallel_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela.
    
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
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(block_multiply, matrizA, matrizB, matrizRes, i1, N, P, M, block_size)
            for i1 in range(0, N, block_size)
        ]
        for future in as_completed(futures):
            pass
    
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo III_4_Parallel_Block.
    
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
    return alg_III_4_Parallel_Block(matrizA, matrizB, N, P, M, block_size)
