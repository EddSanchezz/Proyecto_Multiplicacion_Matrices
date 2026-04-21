def alg_V_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques secuencial (variante V).
    
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
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N
    return alg_V_3_Sequential_Block(matrizA, matrizB, N, P, M, block_size)

