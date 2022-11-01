from itertools import tee, islice

def slide(seq, n):
    def create_iters(it, i):
        yield from islice(it, i, i + n)

    i = 0
    it, tmp_it = tee(seq, 2)
    while True:
        if not list(create_iters(tmp_it, i)):
            break
        yield from create_iters(it, i)
        it, tmp_it = tee(seq, 2)
        i += 1


if __name__ == '__main__':
    import sys
    exec(sys.stdin.read())
    