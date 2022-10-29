from itertools import islice
def fib(m, n):
    def gen_fib():
        x, y = 1, 0
        while True:
            yield x
            x, y = x + y, x
    return islice(gen_fib(), m, m + n)
    


if __name__ == '__main__':
    m, n = eval(input())
    it = fib(m, n)
    print(*it, sep=', ')
