def calc(foo1, foo2, foo3):
    x = lambda x: eval(foo1)
    y = lambda x: eval(foo2)
    u = lambda x, y: eval(foo3)
    return lambda t: u(x(t), y(t))


F = calc(*eval(input()))
print(F(int(input())))
