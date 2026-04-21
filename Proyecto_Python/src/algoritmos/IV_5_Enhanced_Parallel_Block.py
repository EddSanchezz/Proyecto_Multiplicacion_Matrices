from concurrent.futures import ThreadPoolExecutor

def block_multiply_section(matrizA, matrizB, matrizRes, start, end, N, P, M, block_size):
    """
    Multiplicación de una sección de filas (variante IV).
    
    Args:
        matrizA: Matriz A de tamaño N x P
        matrizB: Matriz B de tamaño P x M
        matrizRes: Matriz resultado de tamaño N x M
        start: Índice inicial de fila
        end: Índice final de fila
        N: Filas de A
        P: Columnas de A / Filas de B
        M: Columnas de B
        block_size: Tamaño del bloque
    """
    for i1 in range(start, end, block_size):
        for j1 in range(0, P, block_size):
            for k1 in range(0, M, block_size):
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, P)
                k_end = min(k1 + block_size, M)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][k] += matrizA[i][j] * matrizB[j][k]

def alg_IV_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela optimizada (variante IV).
    Usa exactamente 2 workers.
    
    Args:
        matrizA: Matriz A de tamaño N x P
        matrizB: Matriz B de tamaño P x M
        N: Filas de A
        P: Columnas de A / Filas de B
        M: Columnas de B
        block_size: Tamaño del bloque
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    mid_point = N // 2

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, 0, mid_point, N, P, M, block_size)
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, N, P, M, block_size)

    return matrizRes

def multiply(matrizA, matrizB):
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N
    return alg_IV_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size)

