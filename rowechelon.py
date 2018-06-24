from fractions import Fraction
matrix = eval(input())
matrix = list(map(lambda row:list(map(Fraction,row)),matrix))
r = 0
k = 0
while r < len(matrix) and k < len(matrix[0]):
    t = r+1
    m = r
    v = matrix[r][k]
    while(t < len(matrix)):
        if(matrix[t][k] > v):
            m = t
            v = matrix[t][k]
        t += 1
    if(v == 0):
        k += 1
        continue
    matrix[m],matrix[r] = matrix[r],matrix[m]
    i = 0
    while(i < len(matrix[0])):
        matrix[r][i] /= v
        i += 1
    q = 0
    while(q < len(matrix)):
        if(q == r):
            q += 1
            continue
        i = 0
        a = matrix[q][k]
        while(i < len(matrix[0])):
            matrix[q][i] -= a*matrix[r][i]
            i += 1
        q += 1
    r += 1
    k += 1
print(matrix)
