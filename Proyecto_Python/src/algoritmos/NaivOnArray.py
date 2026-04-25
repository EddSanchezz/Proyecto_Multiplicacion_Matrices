"""
Algoritmo NaivOnArray - Multiplicación de Matrices Ingênua

Implementación del algoritmo de multiplicación de matrices mediante triple bucle.
Este es el algoritmo más básico y directo, también conocido como " naïve algorithm".

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³

Descripción:
    El algoritmo itera sobre tres índices (i, j, k) calculando:
    C[i][j] = Σ A[i][k] * B[k][j] para k = 0..P-1

    Para matrices cuadradas N×N, esto resulta en N³ multiplicaciones escalares.

Técnica:
    - Triple bucle anidado sin optimizaciones
    - Acceso secuencial a memoria (row-major order)
    - Sin desenrollado de lazos (loop unrolling)

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Número de columnas de A / filas de B
    M (int): Número de columnas de B

Retorna:
    list: Matriz resultado de dimensiones N×M

Ejemplo:
    >>> A = [[1, 2], [3, 4]]
    >>> B = [[5, 6], [7, 8]]
    >>> algNaivOnArray(A, B, 2, 2, 2)
    [[19, 22], [43, 50]]

Nota:
    Este algoritmo sirve como referencia para validar la correctitud de
    implementaciones optimizadas. Su simplicidad lo hace fácil de verificar.
"""


def algNaivOnArray(matrizA, matrizB, N, P, M):
    """
    Implementación del algoritmo naïivo de multiplicación de matrices.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            for k in range(P):
                matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo NaivOnArray.
    
    Esta función actúa como wrapper unificado, extrayendo las dimensiones
    de las matrices de entrada y llamando al algoritmo principal.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    
    Raises:
        ValueError: Si las dimensiones no son compatibles para multiplicación
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    
    if len(matrizA[0]) != P:
        raise ValueError(f"Dimensiones incompatibles: A es {N}×{len(matrizA[0])}, B es {P}×{M}")
    
    return algNaivOnArray(matrizA, matrizB, N, P, M)
