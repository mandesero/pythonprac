matrx1 = []
matrx2 = []
s1 = list(eval(input()))
n = len(s1)
matrx1.append(s1)
for _ in range(n - 1):
    matrx1.append(list(eval(input())))
for _ in range(n):
    matrx2.append(list(eval(input())))

ans = [[0 for i in range(n)] for i in range(n)]
for i in range(n):
    for j in range(n):
        e = 0
        for t in range(n):
            e += matrx1[i][t] * matrx2[t][j]
        ans[i][j] = e
for s in ans:
    print(*s, sep=',')
