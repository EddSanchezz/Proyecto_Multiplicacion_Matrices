def algNaivOnArray(matrizA, matrizB, N, P, M):
    matrizRes = [[0.0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            for k in range(P):
                matrizRes[i][j] += matrizA[i][k] * matrizB[k][j]
    return matrizRes

def multiply(matrizA, matrizB):
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return algNaivOnArray(matrizA, matrizB, N, P, M)