def algNaivLoopUnrollingTwo(matrizA, matrizB, N, P, M):
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
                aux += matrizA[i][PP] * matrizB[PP][j]  # handle the last element if P is odd
                matrizRes[i][j] = aux
    return matrizRes

def multiply(matrizA, matrizB):
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return algNaivLoopUnrollingTwo(matrizA, matrizB, N, P, M)
