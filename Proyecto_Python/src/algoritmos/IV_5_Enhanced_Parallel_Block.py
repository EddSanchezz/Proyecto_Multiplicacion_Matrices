"""
Algoritmo IV_5_Enhanced_Parallel_Block - Multiplicación por Bloques Paralela Optimizada (Nivel 4)

Variante optimizada del algoritmo de bloques paralelos (IV.4) con exactamente
2 workers para mayor estabilidad.

Complejidad Computacional:
    - Temporal: O(n³/2) (2 workers fijos)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³/2

Descripción:
    Versión "Enhanced" del algoritmo de bloques paralelos (IV.4).
    Al igual que III.5, usa exactamente 2 workers que procesan
    mitades de la matriz en paralelo.

Técnica:
    - ThreadPoolExecutor con max_workers=2
    - Cada worker procesa la mitad de las filas (mid_point = N//2)
    - Orden de bucles modificado respecto a III.5
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


def block_multiply_section(matrizA, matrizB, matrizRes, start, end, N, P, M, block_size):
    """
    Multiplicación de una sección de filas (variante IV).
    
    Args:
        matrizA (list): Matriz A (N×P)
        matrizB (list): Matriz B (P×M)
        matrizRes (list): Matriz resultado (N×M)
        start (int): Índice inicial de fila
        end (int): Índice final de fila
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    """
    for i1 in range(start, end, block_size):
        for j1 in range(0, P, block_size):
            for k1 in range(0, M, block_size):
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, P)
                k_end = min(k1 + block_size, M)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]


def alg_IV_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela optimizada (variante IV).
    
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
    mid_point = N // 2

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, 0, mid_point, N, P, M, block_size)
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, P, M, block_size)

    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo IV_5_Enhanced_Parallel_Block.
    
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
    return alg_IV_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size)
