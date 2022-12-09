m, n = eval(input())
print([x for x in range(m, n) if not any([x % i == 0 for i in range(2, x // 2 + 1)]) and x != 1])
