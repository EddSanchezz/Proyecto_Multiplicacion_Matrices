"""
Algoritmo StrassenWinograd - Strassen con Optimización de Winograd

Variante del algoritmo de Strassen que incorpora optimizaciones
derivadas del algoritmo de Winograd para reducir operaciones.

Complejidad Computacional:
    - Temporal: O(n^log₂7) ≈ O(n^2.807)
    - Espacial: O(n²) para la matriz resultado + O(n²) auxiliares
    - Multiplicaciones: 7n^2.807 (igual que StrassenNaiv)

Descripción:
    Este algoritmo combina las optimizaciones de Strassen y Winograd.
    Usa la formula clásica de Strassen-Winograd para los 7 productos
    intermedios M1-M7.

Técnica:
    - División en 4 submatrices
    - 7 productos de Strassen-Winograd
    - Caso base con multiplicación naïve

Parámetros:
    matrizA (list): Matriz de dimensiones N×N
    matrizB (list): Matriz de dimensiones N×N
    N (int): Dimensión de las matrices

Retorna:
    list: Matriz resultado de dimensiones N×N

Referencia:
    Strassen, V. (1969). Gaussian Elimination is not Optimal.
    Winograd, S. (1968). On the Number of Multiplications Required.
"""


import math


def max_val(a, b):
    """Retorna el máximo entre dos valores."""
    return a if a > b else b


def add_matrix(A, B, C, size):
    """
    Suma dos matrices A + B y almacena el resultado en C.

    Args:
        A (list): Matriz operando A (size×size)
        B (list): Matriz operando B (size×size)
        C (list): Matriz resultado (size×size)
        size (int): Dimensión de las matrices
    """
    for i in range(size):
        for j in range(size):
            C[i][j] = A[i][j] + B[i][j]


def subtract_matrix(A, B, C, size):
    """
    Resta dos matrices A - B y almacena el resultado en C.

    Args:
        A (list): Matriz operando A (size×size)
        B (list): Matriz operando B (size×size)
        C (list): Matriz resultado (size×size)
        size (int): Dimensión de las matrices
    """
    for i in range(size):
        for j in range(size):
            C[i][j] = A[i][j] - B[i][j]


def standard_multiply(A, B, C, N, P, M):
    """
    Multiplicación naïve estándar para el caso base.

    Args:
        A (list): Matriz A (N×P)
        B (list): Matriz B (P×M)
        C (list): Matriz resultado (N×M)
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    """
    for i in range(N):
        for j in range(M):
            C[i][j] = 0.0
            for k in range(P):
                C[i][j] += A[i][k] * B[k][j]


def strassen_winograd_step(A, B, C, size, min_size):
    """
    Paso recursivo del algoritmo Strassen-Winograd.

    Args:
        A (list): Matriz A (size×size)
        B (list): Matriz B (size×size)
        C (list): Matriz resultado (size×size)
        size (int): Dimensión actual
        min_size (int): Tamaño mínimo para caso base
    """
    if size <= min_size:
        standard_multiply(A, B, C, size, size, size)
        return

    new_size = size // 2

    A11 = [[0.0] * new_size for _ in range(new_size)]
    A12 = [[0.0] * new_size for _ in range(new_size)]
    A21 = [[0.0] * new_size for _ in range(new_size)]
    A22 = [[0.0] * new_size for _ in range(new_size)]
    B11 = [[0.0] * new_size for _ in range(new_size)]
    B12 = [[0.0] * new_size for _ in range(new_size)]
    B21 = [[0.0] * new_size for _ in range(new_size)]
    B22 = [[0.0] * new_size for _ in range(new_size)]

    for i in range(new_size):
        for j in range(new_size):
            A11[i][j] = A[i][j]
            A12[i][j] = A[i][j + new_size]
            A21[i][j] = A[i + new_size][j]
            A22[i][j] = A[i + new_size][j + new_size]
            B11[i][j] = B[i][j]
            B12[i][j] = B[i][j + new_size]
            B21[i][j] = B[i + new_size][j]
            B22[i][j] = B[i + new_size][j + new_size]

    M1 = [[0.0] * new_size for _ in range(new_size)]
    M2 = [[0.0] * new_size for _ in range(new_size)]
    M3 = [[0.0] * new_size for _ in range(new_size)]
    M4 = [[0.0] * new_size for _ in range(new_size)]
    M5 = [[0.0] * new_size for _ in range(new_size)]
    M6 = [[0.0] * new_size for _ in range(new_size)]
    M7 = [[0.0] * new_size for _ in range(new_size)]

    temp1 = [[0.0] * new_size for _ in range(new_size)]
    temp2 = [[0.0] * new_size for _ in range(new_size)]

    add_matrix(A11, A22, temp1, new_size)
    add_matrix(B11, B22, temp2, new_size)
    strassen_winograd_step(temp1, temp2, M1, new_size, min_size)

    add_matrix(A21, A22, temp1, new_size)
    strassen_winograd_step(temp1, B11, M2, new_size, min_size)

    subtract_matrix(B12, B22, temp2, new_size)
    strassen_winograd_step(A11, temp2, M3, new_size, min_size)

    subtract_matrix(B21, B11, temp2, new_size)
    strassen_winograd_step(A22, temp2, M4, new_size, min_size)

    add_matrix(A11, A12, temp1, new_size)
    strassen_winograd_step(temp1, B22, M5, new_size, min_size)

    subtract_matrix(A21, A11, temp1, new_size)
    add_matrix(B11, B12, temp2, new_size)
    strassen_winograd_step(temp1, temp2, M6, new_size, min_size)

    subtract_matrix(A12, A22, temp1, new_size)
    add_matrix(B21, B22, temp2, new_size)
    strassen_winograd_step(temp1, temp2, M7, new_size, min_size)

    for i in range(new_size):
        for j in range(new_size):
            C[i][j] = M1[i][j] + M4[i][j] - M5[i][j] + M7[i][j]
            C[i][j + new_size] = M3[i][j] + M5[i][j]
            C[i + new_size][j] = M2[i][j] + M4[i][j]
            C[i + new_size][j + new_size] = M1[i][j] - M2[i][j] + M3[i][j] + M6[i][j]


def algStrassenWinograd(A, B, C, N, P, M):
    """
    Implementación principal del algoritmo Strassen-Winograd.

    Args:
        A (list): Matriz A (N×P)
        B (list): Matriz B (P×M)
        C (list): Matriz resultado (N×M)
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B

    Returns:
        None (el resultado se almacena en C)
    """
    maxSize = max_val(N, P)
    maxSize = max_val(maxSize, M)
    if maxSize < 16:
        maxSize = 16

    if (maxSize & (maxSize - 1)) == 0:
        newSize = maxSize
    else:
        k = int(math.log2(maxSize - 1)) + 1
        newSize = 2 ** k

    newA = [[0.0] * newSize for _ in range(newSize)]
    newB = [[0.0] * newSize for _ in range(newSize)]
    auxResult = [[0.0] * newSize for _ in range(newSize)]

    for i in range(newSize):
        for j in range(newSize):
            newA[i][j] = 0.0
            newB[i][j] = 0.0

    for i in range(N):
        for j in range(P):
            newA[i][j] = A[i][j]

    for i in range(P):
        for j in range(M):
            newB[i][j] = B[i][j]

    strassen_winograd_step(newA, newB, auxResult, newSize, 16)

    for i in range(N):
        for j in range(M):
            C[i][j] = auxResult[i][j]


def multiply(A, B):
    """
    Función de interfaz para el algoritmo StrassenWinograd.

    Args:
        A (list): Matriz N×N
        B (list): Matriz N×N

    Returns:
        list: Matriz resultado N×N
    """
    N = len(A)
    P = len(B)
    M = len(B[0])
    C = [[0.0] * M for _ in range(N)]
    algStrassenWinograd(A, B, C, N, P, M)
    return C
