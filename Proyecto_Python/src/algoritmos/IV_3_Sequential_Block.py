"""
Algoritmo IV_3_Sequential_Block - Multiplicación por Bloques Secuencial (Nivel 4)

Implementación de multiplicación de matrices por bloques en su variante
secuencial de cuarto nivel de optimización.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³

Descripción:
    Cuarta iteración del algoritmo de multiplicación por bloques.
    Las diferencias con versiones anteriores (III.x) están en el
    orden de los bucles externos y la forma en que se acceden
    los elementos de las matrices.
    
    El orden de iteración i1→j1→k1 es el mismo que III.3,
    pero la fórmula de acceso a B[k][j] vs B[j][k] varía.

Técnica:
    - Triple bucle externo para bloques
    - Triple bucle interno con fórmula modificada
    - block_size = N (toda la matriz como un bloque)

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


def alg_IV_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques secuencial (variante IV).
    
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
    
    for i1 in range(0, N, block_size):
        for j1 in range(0, P, block_size):
            for k1 in range(0, M, block_size):
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, P)
                k_end = min(k1 + block_size, M)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][k] += matrizA[i][j] * matrizB[j][k]
                            
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo IV_3_Sequential_Block.
    
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
    return alg_IV_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size)
