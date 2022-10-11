from fractions import Fraction
def foo(s, w, coef_a, coef_b):

    foo1 = ""
    for i, coef in enumerate(coef_a):
        foo1 += f"{coef}*x**{len(coef_a) - i - 1}+"
    foo_1 = lambda x: eval(foo1[:-1])

    foo2 = ""
    for i, coef in enumerate(coef_b):
        foo2 += f"{coef}*x**{len(coef_b) - i - 1}+"
    foo_2 = lambda x: eval(foo2[:-1])
    return False if foo_2(s) == 0 else foo_1(s)/foo_2(s) == w
    # try:
    #     print(t := foo_1(s)/foo_2(s) == w)
    #     return t
    # except ZeroDivisionError:
    #     return False

if __name__ == "__main__":
    data = [Fraction(i) for i in input().split(',')]
    s, w = data[0], data[1]
    n_a = int(data[2])
    n_b = int(data[3 + n_a])
    coef_a = data[3: 4 + n_a]
    coef_b = data[5 + n_a: 6 + n_a + n_b]
    print(foo(s, w, coef_a, coef_b))
