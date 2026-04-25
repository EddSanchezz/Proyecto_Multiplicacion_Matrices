"""
Algoritmo StrassenNaiv - Multiplicación de Matrices Divide y Vencerás

Implementación del algoritmo de Strassen para multiplicación de matrices
usando el enfoque divide y vencerás.

Complejidad Computacional:
    - Temporal: O(n^log₂7) ≈ O(n^2.807)
    - Espacial: O(n²) para la matriz resultado + O(n²) auxiliares
    - Multiplicaciones: 7n^2.807 (vs n³ del naïve)

Descripción:
    El algoritmo de Strassen reduce el número de multiplicaciones
    escalares de 8 a 7 mediante la computación de productos intermedios
    M1 a M7 que exploit la estructura algebraica de la multiplicación.
    
    Para matrices de tamaño N×N que son potencias de 2:
    1. Dividir las matrices en 4 submatrices (división)
    2. Calcular 7 productos de submatrices (conquista)
    3. Combinar los resultados (combinación)
    
    El caso base (matrices pequeñas) usa el algoritmo naïve.

Técnica:
    - Recursión con división en 4 submatrices
    - 7 productos escalares por nivel de recursión
    - Padding a siguiente potencia de 2 para matrices no-potencia-de-dos
    - Umbral m como tamaño mínimo para aplicar Strassen (m=16)

Parámetros:
    matrizA (list): Matriz de dimensiones N×N
    matrizB (list): Matriz de dimensiones N×N
    N (int): Dimensión de las matrices (deben ser cuadradas)
    P (int): Columnas de A (debe ser igual a N)
    M (int): Columnas de B (debe ser igual a N)

Retorna:
    list: Matriz resultado de dimensiones N×N

Referencia:
    Strassen, V. (1969). Gaussian Elimination is not Optimal.
    Numerische Mathematik, 13(4), 354-356.
"""


import math


def max(N, P):
    """Retorna el máximo entre dos valores."""
    return P if N < P else N


def add(A, B, C, size):
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


def subtract(A, B, C, size):
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


def algStrassenNaiv(matrizA, matrizB, matrizRes, N, P, M):
    """
    Implementación principal del algoritmo StrassenNaiv.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        matrizRes (list): Matriz resultado preallocada N×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        None (el resultado se almacena en matrizRes)
    
    Note:
        El algoritmo hace padding de las matrices a la siguiente potencia
        de 2 para garantizar que la división sea exacta.
    """
    maxSize = max(N, P)
    if maxSize < 16:
        maxSize = 16

    if (maxSize & (maxSize - 1)) == 0:
        newSize = maxSize
    else:
        import math
        k = int(math.log2(maxSize - 1)) + 1
        newSize = 2 ** k

    m = 16
    
    newA = [[0.0] * newSize for _ in range(newSize)]
    newB = [[0.0] * newSize for _ in range(newSize)]
    auxResult = [[0.0] * newSize for _ in range(newSize)]
    
    for i in range(newSize):
        for j in range(newSize):
            newA[i][j] = 0.0
            newB[i][j] = 0.0
            
    for i in range(N):
        for j in range(P):
            newA[i][j] = matrizA[i][j]
            
    for i in range(N):
        for j in range(M):
            newB[i][j] = matrizB[i][j]
            
    strassenNaivStep(newA, newB, auxResult, newSize, m)
    
    for i in range(N):
        for j in range(M):
            matrizRes[i][j] = auxResult[i][j]


def strassenNaivStep(matrizA, matrizB, matrizRes, N, m):
    """
    Paso recursivo del algoritmo Strassen.
    
    Args:
        matrizA (list): Matriz A (N×N)
        matrizB (list): Matriz B (N×N)
        matrizRes (list): Matriz resultado (N×N)
        N (int): Dimensión actual
        m (int): Tamaño mínimo para caso base
    """
    if N % 2 == 0 and N > m:
        newSize = N // 2

        varA11 = [[0] * newSize for _ in range(newSize)]
        varA12 = [[0] * newSize for _ in range(newSize)]
        varA21 = [[0] * newSize for _ in range(newSize)]
        varA22 = [[0] * newSize for _ in range(newSize)]
        varB11 = [[0] * newSize for _ in range(newSize)]
        varB12 = [[0] * newSize for _ in range(newSize)]
        varB21 = [[0] * newSize for _ in range(newSize)]
        varB22 = [[0] * newSize for _ in range(newSize)]

        resultadoPart11 = [[0] * newSize for _ in range(newSize)]
        resultadoPart12 = [[0] * newSize for _ in range(newSize)]
        resultadoPart21 = [[0] * newSize for _ in range(newSize)]
        resultadoPart22 = [[0] * newSize for _ in range(newSize)]

        helper1 = [[0] * newSize for _ in range(newSize)]
        helper2 = [[0] * newSize for _ in range(newSize)]

        aux1 = [[0] * newSize for _ in range(newSize)]
        aux2 = [[0] * newSize for _ in range(newSize)]
        aux3 = [[0] * newSize for _ in range(newSize)]
        aux4 = [[0] * newSize for _ in range(newSize)]
        aux5 = [[0] * newSize for _ in range(newSize)]
        aux6 = [[0] * newSize for _ in range(newSize)]
        aux7 = [[0] * newSize for _ in range(newSize)]

        for i in range(newSize):
            for j in range(newSize):
                varA11[i][j] = matrizA[i][j]
                varA12[i][j] = matrizA[i][j + newSize]
                varA21[i][j] = matrizA[i + newSize][j]
                varA22[i][j] = matrizA[i + newSize][j + newSize]
                varB11[i][j] = matrizB[i][j]
                varB12[i][j] = matrizB[i][j + newSize]
                varB21[i][j] = matrizB[i + newSize][j]
                varB22[i][j] = matrizB[i + newSize][j + newSize]

        add(varA11, varA22, helper1, newSize)
        add(varB11, varB22, helper2, newSize)
        strassenNaivStep(helper1, helper2, aux1, newSize, m)

        add(varA21, varA22, helper1, newSize)
        strassenNaivStep(helper1, varB11, aux2, newSize, m)

        subtract(varB12, varB22, helper1, newSize)
        strassenNaivStep(varA11, helper1, aux3, newSize, m)

        subtract(varB21, varB11, helper1, newSize)
        strassenNaivStep(varA22, helper1, aux4, newSize, m)

        add(varA11, varA12, helper1, newSize)
        strassenNaivStep(helper1, varB22, aux5, newSize, m)

        subtract(varA21, varA11, helper1, newSize)
        add(varB11, varB12, helper2, newSize)
        strassenNaivStep(helper1, helper2, aux6, newSize, m)

        subtract(varA12, varA22, helper1, newSize)
        add(varB21, varB22, helper2, newSize)
        strassenNaivStep(helper1, helper2, aux7, newSize, m)

        add(aux1, aux4, resultadoPart11, newSize)
        subtract(resultadoPart11, aux5, resultadoPart11, newSize)
        add(resultadoPart11, aux7, resultadoPart11, newSize)

        add(aux3, aux5, resultadoPart12, newSize)
        add(aux2, aux4, resultadoPart21, newSize)

        add(aux1, aux3, resultadoPart22, newSize)
        subtract(resultadoPart22, aux2, resultadoPart22, newSize)
        add(resultadoPart22, aux6, resultadoPart22, newSize)

        for i in range(newSize):
            for j in range(newSize):
                matrizRes[i][j] = resultadoPart11[i][j]
                matrizRes[i][j + newSize] = resultadoPart12[i][j]
                matrizRes[i + newSize][j] = resultadoPart21[i][j]
                matrizRes[i + newSize][j + newSize] = resultadoPart22[i][j]
    else:
        algoritmoNaivStandard(matrizA, matrizB, matrizRes, N, N, N)


def algoritmoNaivStandard(matrizA, matrizB, matrizRes, N, P, M):
    """
    Algoritmo naïivo para el caso base de Strassen.
    
    Args:
        matrizA (list): Matriz A (N×P)
        matrizB (list): Matriz B (P×M)
        matrizRes (list): Matriz resultado (N×M)
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    """
    for i in range(N):
        for j in range(M):
            aux = 0.0
            for k in range(P):
                aux += matrizA[i][k] * matrizB[k][j]
            matrizRes[i][j] = aux


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo StrassenNaiv.
    
    Args:
        matrizA (list): Matriz N×N
        matrizB (list): Matriz N×N
    
    Returns:
        list: Matriz resultado N×N
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    algStrassenNaiv(matrizA, matrizB, matrizRes, N, P, M)
    return matrizRes
