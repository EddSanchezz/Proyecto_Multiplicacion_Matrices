def algNaivLoopUnrollingFour(matrizA, matrizB, N, P, M):
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
    N = len(matrizA)
    P = len(matrizB)
    M = len(matrizB[0])
    return algNaivLoopUnrollingFour(matrizA, matrizB, N, P, M)

