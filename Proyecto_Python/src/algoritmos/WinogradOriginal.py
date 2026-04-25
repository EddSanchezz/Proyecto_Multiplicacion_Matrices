"""
Algoritmo WinogradOriginal - Multiplicación de Matrices Optimizada

Implementación del algoritmo de Winograd para multiplicación de matrices,
que reduce el número de multiplicaciones escalares aproximadamente a la mitad.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: ~n³/2 (reducción de ~50% vs naïve)

Descripción:
    El algoritmo de Winograd precalcula dos vectores:
    - y[i] = Σ A[i][2k] * A[i][2k+1]  (para filas de A)
    - z[k] = Σ B[2k][j] * B[2k+1][j]  (para columnas de B)
    
    Luego calcula el resultado usando la identidad:
    (a+b)(c+d) = ac + ad + bc + bd
    
    Esto permite reducir multiplicaciones a costa de más adiciones.

Técnica:
    - Precomputación de vectores y, z
    - Reordenamiento de operaciones para reducir multiplicaciones
    - Manejo del caso cuando P es impar (upsilon = 1)

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


def alg_winograd_original(matrizA, matrizB, N, P, M):
    """
    Implementación del algoritmo de Winograd original.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    
    Note:
        El parámetro upsilon indica si P es impar.
        Si upsilon=1, existe un elemento extra que se procesa al final.
    """
    upsilon = P % 2
    gamma = P - upsilon
    y = [0.0] * N
    z = [0.0] * M
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    
    for i in range(N):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += matrizA[i][j] * matrizA[i][j + 1]
        y[i] = aux
    
    for k in range(M):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += matrizB[j][k] * matrizB[j + 1][k]
        z[k] = aux
    
    if upsilon == 1:
        PP = P - 1
        for i in range(N):
            for k in range(M):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (matrizA[i][j] + matrizB[j + 1][k]) * (matrizA[i][j + 1] + matrizB[j][k])
                matrizRes[i][k] = aux - y[i] - z[k] + matrizA[i][PP] * matrizB[PP][k]
    else:
        for i in range(N):
            for k in range(M):
                aux = 0.0
                for j in range(0, gamma, 2):
                    aux += (matrizA[i][j] + matrizB[j + 1][k]) * (matrizA[i][j + 1] + matrizB[j][k])
                matrizRes[i][k] = aux - y[i] - z[k]

    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo WinogradOriginal.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return alg_winograd_original(matrizA, matrizB, N, P, M)
