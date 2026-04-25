"""
Algoritmo NaivLoopUnrollingTwo - Desenrollado de Lazos ×2

Variante del algoritmo naïivo con técnica de loop unrolling desenrollando
el bucle interno en paquetes de 2 elementos.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³ (mismas que naïve, pero con menos iteraciones)

Descripción:
    El algoritmo reduce el número de iteraciones del bucle interno k,
    procesando 2 elementos por iteración:
        aux += A[i][k] * B[k][j] + A[i][k+1] * B[k+1][j]
    
    Maneja casos especiales cuando P es impar.

Técnica:
    - Loop unrolling con factor 2
    - Trata el caso P impar como caso especial (P % 2 == 1)
    - Reduce overhead de跳转 de instrucciones

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Número de columnas de A / filas de B
    M (int): Número de columnas de B

Retorna:
    list: Matriz resultado de dimensiones N×M

Ejemplo:
    >>> A = [[1, 2, 3], [4, 5, 6]]
    >>> B = [[7, 8], [9, 10], [11, 12]]
    >>> algNaivLoopUnrollingTwo(A, B, 2, 3, 2)
    [[58, 64], [139, 154]]
"""


def algNaivLoopUnrollingTwo(matrizA, matrizB, N, P, M):
    """
    Multiplicación de matrices con loop unrolling de factor 2.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    
    Note:
        Cuando P es impar, el último elemento se procesa por separado
        para evitar индекс errores (index out of bounds).
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    if P % 2 == 0:
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, P, 2):
                    aux += matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j]
                matrizRes[i][j] = aux
    else:
        PP = P - 1
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, PP, 2):
                    aux += matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j]
                aux += matrizA[i][PP] * matrizB[PP][j]
                matrizRes[i][j] = aux
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo NaivLoopUnrollingTwo.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return algNaivLoopUnrollingTwo(matrizA, matrizB, N, P, M)
