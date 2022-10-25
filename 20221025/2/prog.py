from itertools import tee, islice

def slide(seq, n):
    def create_iters(it, i):
        yield from islice(it, i, i + n)
    for i, it in enumerate([i for i in tee(seq, len(seq))]):
        yield from create_iters(it, i)



if __name__ == '__main__':
    seq, n = eval(input())
    print(*slide(seq, n))
    