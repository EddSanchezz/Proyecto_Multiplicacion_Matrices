def alg_III_3_SequentialBlock(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques secuencial.
    
    Args:
        matrizA: Matriz A de tamaño N x P
        matrizB: Matriz B de tamaño P x M
        N: Filas de A
        P: Columnas de A / Filas de B
        M: Columnas de B
        block_size: Tamaño del bloque
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    
    for i1 in range(0, N, block_size):
        for j1 in range(0, M, block_size):
            for k1 in range(0, P, block_size):
                # Límites del bloque
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, M)
                k_end = min(k1 + block_size, P)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]
    
    return matrizRes

def multiply(matrizA, matrizB):
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N  # Usar N como tamaño de bloque por defecto
    return alg_III_3_SequentialBlock(matrizA, matrizB, N, P, M, block_size)
