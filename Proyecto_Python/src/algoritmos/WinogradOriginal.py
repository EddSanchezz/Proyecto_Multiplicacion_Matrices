def alg_winograd_original(matrizA, matrizB, N, P, M):
    upsilon = P % 2
    gamma = P - upsilon
    y = [0.0] * N
    z = [0.0] * M
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    
    # Precompute y
    for i in range(N):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += matrizA[i][j] * matrizA[i][j + 1]
        y[i] = aux
    
    # Precompute z
    for k in range(M):
        aux = 0.0
        for j in range(0, gamma, 2):
            aux += matrizB[j][k] * matrizB[j + 1][k]
        z[k] = aux
    
    # Compute result
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
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return alg_winograd_original(matrizA, matrizB, N, P, M)

