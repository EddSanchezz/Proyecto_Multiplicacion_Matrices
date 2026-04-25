"""
Algoritmo III_3_Sequential_Block - Multiplicación por Bloques Secuencial (Nivel 3)

Implementación de multiplicación de matrices mediante el método de bloques
(block matrix multiplication) de forma secuencial.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³

Descripción:
    El algoritmo de multiplicación por bloques divide las matrices en
    submatrices más pequeñas (bloques) para mejorar el uso de caché CPU.
    
    El principio básico es que al procesar bloques que caben en la caché L2,
    se reducen los caché misses compared to multiplicación naïve.
    
    Este algoritmo (III.3) es la versión secuencial del primer nivel
    de optimizaciones por bloques.

Técnica:
    - Triple bucle externo para iterar sobre bloques
    - Triple bucle interno para calcular productos de bloques
    - Tamaño de bloque configurable (default: N, toda la matriz)
    - Acceso a memoria optimizado para locality

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
    Para block_size = N, el algoritmo equivale a naïve.
    block_size óptimo típicamente 32-64 para matrices grandes.
"""


def alg_III_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques secuencial.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    
    Returns:
        list: Matriz resultado N×M
    
    Note:
        Los límites de los bloques se calculan con min() para manejar
        casos donde N no es divisible exactamente por block_size.
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    
    for i1 in range(0, N, block_size):
        for j1 in range(0, M, block_size):
            for k1 in range(0, P, block_size):
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, M)
                k_end = min(k1 + block_size, P)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]
    
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo III_3_Sequential_Block.
    
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
    return alg_III_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size)
