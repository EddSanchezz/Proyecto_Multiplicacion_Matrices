"""
Algoritmo WinogradScaled - Winograd con Escalado Numérico

Variante del algoritmo de Winograd que incluye un paso de escalado
para prevenir overflow en operaciones de punto flotante.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado + O(n²) para copias
    - Multiplicaciones: ~n³/2 (igual que Winograd original)

Descripción:
    Este algoritmo combina la optimización de Winograd con un escalado
    basado en la norma infinito de las matrices de entrada.
    
    El factor de escalado λ se calcula como:
        λ = floor(0.5 + log(b/a) / log(4))
    
    donde a = ||A||∞ y b = ||B||∞ (normas infinito).
    
    Las matrices se escalan antes de la multiplicación:
        A' = A * 2^λ
        B' = B * 2^(-λ)
    
    Esto previene overflow en matrices con valores muy grandes.

Técnica:
    - Escalado de matrices según norma infinito
    - Usa la norma del mayor elemento de cada fila/columna
    - Ajuste dinámico del factor de escalado

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Número de columnas de A / filas de B
    M (int): Número de columnas de B

Retorna:
    list: Matriz resultado de dimensiones N×M

Referencia:
    Winograd, S. (1968). On the Number of Multiplications Required
    for Matrix Multiplication. Journal of the ACM.
"""


import math


def multiply_with_scalar(matrix, scalar):
    """
    Multiplica todos los elementos de una matriz por un escalar.
    
    Args:
        matrix (list): Matriz de entrada
        scalar (float): Factor de escalado
    
    Returns:
        list: Matriz escalada
    """
    n, m = len(matrix), len(matrix[0])
    result = [[matrix[i][j] * scalar for j in range(m)] for i in range(n)]
    return result


def norm_inf(matrix):
    """
    Calcula la norma infinito de una matriz.
    
    La norma infinito es el máximo de las sumas absolutas de las filas.
    
    Args:
        matrix (list): Matriz de entrada
    
    Returns:
        float: Norma infinito de la matriz
    """
    max_sum = float('-inf')
    for row in matrix:
        row_sum = sum(abs(x) for x in row)
        if row_sum > max_sum:
            max_sum = row_sum
    return max_sum


def alg_winograd_original(A, B, N, P, M):
    """
    Algoritmo de Winograd original (reutilizado internamente).
    
    Args:
        A (list): Matriz A de tamaño N×P
        B (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    """
    upsilon = P % 2
    gamma = P - upsilon
    y = [0.0] * N
    z = [0.0] * M
    res = [[0.0] * M for _ in range(N)]

    for i in range(N):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += A[i][j] * A[i][j + 1]
        y[i] = aux

    for k in range(M):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += B[j][k] * B[j + 1][k]
        z[k] = aux

    if upsilon == 1:
        PP = P - 1
        for i in range(N):
            for k in range(M):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (A[i][j] + B[j + 1][k]) * (A[i][j + 1] + B[j][k])
                res[i][k] = aux - y[i] - z[k] + A[i][PP] * B[PP][k]
    else:
        for i in range(N):
            for k in range(M):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (A[i][j] + B[j + 1][k]) * (A[i][j + 1] + B[j][k])
                res[i][k] = aux - y[i] - z[k]

    return res


def alg_winograd_scaled(matrizA, matrizB, N, P, M):
    """
    Implementación del algoritmo de Winograd con escalado.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    
    Note:
        El escalado asegura que los valores intermedios no causen
        overflow, útil para matrices con valores muy grandes (>10^6).
    """
    a = norm_inf(matrizA)
    b = norm_inf(matrizB)
    lambda_ = math.floor(0.5 + math.log(b / a) / math.log(4))
    
    copyA = multiply_with_scalar(matrizA, 2 ** lambda_)
    copyB = multiply_with_scalar(matrizB, 2 ** -lambda_)

    return alg_winograd_original(copyA, copyB, N, P, M)


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo WinogradScaled.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return alg_winograd_scaled(matrizA, matrizB, N, P, M)
