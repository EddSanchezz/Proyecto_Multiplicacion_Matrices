"""
Algoritmo III_5_Enhanced_Parallel_Block - Multiplicación por Bloques Paralela Optimizada (Nivel 3)

Variante optimizada del algoritmo de bloques paralelos con exactamente
2 workers para mayor estabilidad y rendimiento controlado.

Complejidad Computacional:
    - Temporal: O(n³/2) (2 workers fijos)
    - Espacial: O(n²) para la matriz resultado
    - Multiplicaciones: n³/2

Descripción:
    Versión "Enhanced" del algoritmo de bloques paralelos (III.4).
    En lugar de crear un worker por bloque de filas, usa exactamente
    2 workers que procesanmitades de la matriz.
    
    Esta simplificación reduce overhead de thread management y es útil
    cuando se quiere un speedup predecible sin importar el hardware.

Técnica:
    - ThreadPoolExecutor con max_workers=2
    - Cada worker procesa la mitad de las filas (mid_point = N//2)
    - Dentro de cada sección, aplica método de bloques
    - Sin dependencias entre workers (ejecución verdaderamente paralela)

Parámetros:
    matrizA (list): Matriz de dimensiones N×P
    matrizB (list): Matriz de dimensiones P×M
    N (int): Número de filas de A
    P (int): Columnas de A / Filas de B
    M (int): Número de columnas de B
    block_size (int): Tamaño de los bloques

Retorna:
    list: Matriz resultado de dimensiones N×M

Nota:
    - 2 workers es una elección de diseño para estabilidad
    - Más workers pueden mejorar rendimiento pero aumentan overhead
    - El speedup máximo teórico es 2x en este caso
"""


from concurrent.futures import ThreadPoolExecutor


def block_multiply_section(matrizA, matrizB, matrizRes, start, end, N, P, M, block_size):
    """
    Multiplicación de una sección de filas en paralelo.
    
    Args:
        matrizA (list): Matriz A (N×P)
        matrizB (list): Matriz B (P×M)
        matrizRes (list): Matriz resultado (N×M)
        start (int): Índice inicial de fila
        end (int): Índice final de fila
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    
    Note:
        Esta función es llamada por exactamente 2 workers:
        - Worker 1: range(0, mid_point)
        - Worker 2: range(mid_point, N)
    """
    for i1 in range(start, end, block_size):
        for j1 in range(0, M, block_size):
            for k1 in range(0, P, block_size):
                i_end = min(i1 + block_size, N)
                j_end = min(j1 + block_size, M)
                k_end = min(k1 + block_size, P)
                
                for i in range(i1, i_end):
                    for j in range(j1, j_end):
                        for k in range(k1, k_end):
                            matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]


def alg_III_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size):
    """
    Multiplicación de matrices por bloques paralela optimizada.
    
    Args:
        matrizA (list): Matriz A de tamaño N×P
        matrizB (list): Matriz B de tamaño P×M
        N (int): Filas de A
        P (int): Columnas de A / Filas de B
        M (int): Columnas de B
        block_size (int): Tamaño del bloque
    
    Returns:
        list: Matriz resultado N×M
    """
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    mid_point = N // 2
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, 0, mid_point, N, P, M, block_size)
        executor.submit(block_multiply_section, matrizA, matrizB, matrizRes, mid_point, N, P, M, block_size)
    
    return matrizRes


def multiply(matrizA, matrizB):
    """
    Función de interfaz para el algoritmo III_5_Enhanced_Parallel_Block.
    
    Args:
        matrizA (list): Matriz N×P
        matrizB (list): Matriz P×M
    
    Returns:
        list: Matriz resultado N×M
    """
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    block_size = N
    return alg_III_5_Enhanced_Parallel_Block(matrizA, matrizB, N, P, M, block_size)
