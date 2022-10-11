from math import *
from fractions import Fraction
from decimal import *
data = input().split()
w, h, a, b = map(int, data[:-1])
func = lambda x: -eval(data[-1])


dx = Fraction(f"{b - a}/{w}")
print(dx)




t = [func(dx * i) for i in range(-w//2, w//2 + 1)]
if min(t) < 0:
    a = abs(min(t))
    t = [elem + a for elem in t]
length = max(t) - min(t)
tmp = [Decimal(float(elem / length * (h - 1))).quantize(Decimal(1.))  for elem in t]

field = [[" " for _ in range(w)] for _ in range(h)]
for i in range(w):
    field[int(tmp[i])][i] = '*'
for line in field:
    print(*line, sep='')
