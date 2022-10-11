def mysub(x, y):
    return type(x)(elem for elem in x if elem not in y) if isinstance(x, (tuple, list)) else x - y

print(mysub(*eval(input())))
