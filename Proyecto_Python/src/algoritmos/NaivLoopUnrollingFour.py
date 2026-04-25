"""
Algoritmo NaivLoopUnrollingFour - Desenrollado de Lazos ×4

Variante del algoritmo naïivo con técnica de loop unrolling desenrollando
el bucle interno en paquetes de 4 elementos.

Complejidad Computacional:
    - Temporal: O(n³)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³ (mismas que naïve)

Descripción:
    El algoritmo reduce el número de iteraciones del bucle interno k,
    procesando 4 elementos por iteración:
        aux += A[i][k]*B[k][j] + A[i][k+1]*B[k+1][j] +
               A[i][k+2]*B[k+2][j] + A[i][k+3]*B[k+3][j]
    
    Maneja cuatro casos especiales según el residuo de P mod 4:
    - P % 4 == 0: Sin elementos extra
    - P % 4 == 1: Un elemento extra (PP = P-1)
    - P % 4 == 2: Dos elementos extra (PP = P-2, PPP = P-1)
    - P % 4 == 3: Tres elementos extra (PP = P-3, PPP = P-2, PPPP = P-1)

Técnica:
    - Loop unrolling con factor 4
    - Manejo de casos según residuo mod 4
    - Reduce overhead de跳转 de instrucciones

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Número de columnas de A / filas de B
    M (int): Número de columnas de B

Retorna:
    list: Matriz resultado de dimensiones N×M
"""


def algNaivLoopUnrollingFour(matrizA, matrizB, N, P, M):
    """
    Multiplicación de matrices con loop unrolling de factor 4.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
    
    Returns:
        list: Matriz resultado N×M
    
    Note:
        El algoritmo maneja los 4 casos posibles de P mod 4 para
        asegurar que todos los elementos sean procesados correctamente.
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    if P % 4 == 0:
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, P, 4):
                    aux += (matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j] +
                            matrizA[i][k + 2] * matrizB[k + 2][j] + matrizA[i][k + 3] * matrizB[k + 3][j])
                matrizRes[i][j] = aux
    elif P % 4 == 1:
        PP = P - 1
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, PP, 4):
                    aux += (matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j] +
                            matrizA[i][k + 2] * matrizB[k + 2][j] + matrizA[i][k + 3] * matrizB[k + 3][j])
                aux += matrizA[i][PP] * matrizB[PP][j]
                matrizRes[i][j] = aux
    elif P % 4 == 2:
        PP = P - 2
        PPP = P - 1
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, PP, 4):
                    aux += (matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j] +
                            matrizA[i][k + 2] * matrizB[k + 2][j] + matrizA[i][k + 3] * matrizB[k + 3][j])
                aux += matrizA[i][PP] * matrizB[PP][j] + matrizA[i][PPP] * matrizB[PPP][j]
                matrizRes[i][j] = aux
    else:
        PP = P - 3
        PPP = P - 2
        PPPP = P - 1
        for i in range(N):
            for j in range(M):
                aux = 0.0
                for k in range(0, PP, 4):
                    aux += (matrizA[i][k] * matrizB[k][j] + matrizA[i][k + 1] * matrizB[k + 1][j] +
                            matrizA[i][k + 2] * matrizB[k + 2][j] + matrizA[i][k + 3] * matrizB[k + 3][j])
                aux += (matrizA[i][PP] * matrizB[PP][j] + matrizA[i][PPP] * matrizB[PPP][j] +
                        matrizA[i][PPPP] * matrizB[PPPP][j])
                matrizRes[i][j] = aux
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo NaivLoopUnrollingFour.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return algNaivLoopUnrollingFour(matrizA, matrizB, N, P, M)
