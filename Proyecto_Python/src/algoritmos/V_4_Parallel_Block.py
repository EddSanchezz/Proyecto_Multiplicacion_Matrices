from concurrent.futures import ThreadPoolExecutor

def block_multiply(matrizA, matrizB, matrizRes, i_start, N, P, M, block_size):
    """
    Multiplicación de un bloque de filas (variante V).
    
    Args:
        matrizA: Matriz A de tamaño N x P
        matrizB: Matriz B de tamaño P x M
        matrizRes: Matriz resultado de tamaño N x M
        i_start: Índice inicial de fila para este bloque
        N: Filas de A
        P: Columnas de A / Filas de B
        M: Columnas de B
        block_size: Tamaño del bloque
    """
    i_end = min(i_start + block_size, N)
    for j1 in range(0, P, block_size):
        for k1 in range(0, M, block_size):
            for i in range(i_start, i_end):
                for j in range(j1, min(j1 + block_size, P)):
                    for k in range(k1, min(k1 + block_size, M)):
                        matrizRes[i][k] += matrizA[i][j] * matrizB[j][k]

def alg_V_4_ParallelBlock(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela (variante V).
    
    Args:
        matrizA: Matriz A de tamaño N x P
        matrizB: Matriz B de tamaño P x M
        N: Filas de A
        P: Columnas de A / Filas de B
        M: Columnas de B
        block_size: Tamaño del bloque
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(block_multiply, matrizA, matrizB, matrizRes, i_start, N, P, M, block_size)
            for i_start in range(0, N, block_size)
        ]
        for future in futures:
            future.result()
    
    return matrizRes

def multiply(matrizA, matrizB):
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N
    return alg_V_4_ParallelBlock(matrizA, matrizB, N, P, M, block_size)
