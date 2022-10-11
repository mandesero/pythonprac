from math import *
from fractions import Fraction
from decimal import *
data = input().split()
w, h, a, b = map(int, data[:-1])
func = lambda x: eval(data[-1])
def func(x):
    try:
        return eval(data[-1])
    except Exception:
        return func(x + 1/1000)


dx = Fraction(f"{b - a}/{w}")

def olala(screen):
    for i in range(len(screen[0]) - 1):
        stolb1 = [screen[j][i] for j in range(len(screen))]
        start_1 = stolb1.index('*')

        stolb2 = [screen[j][i + 1] for j in range(len(screen))]
        stop_1 = stolb2.index('*')
        for j in range(min(start_1, stop_1) + 1, max(start_1, stop_1)):
            screen[j][i] = '*'






t = [func(dx * i) for i in range(-w // 2, w // 2 + 1)]
if min(t) < 0:
    a = abs(min(t))
    t = [elem + a for elem in t]
length = max(t) - min(t)
tmp = [Decimal(float(elem / length * (h - 1))).quantize(Decimal(1.))  for elem in t]

field = [[" " for _ in range(w)] for _ in range(h)]
for i in range(w):
    field[h - 1 - int(tmp[i])][i] = '*'

olala(field)
for line in field:
    print(*line, sep='')
