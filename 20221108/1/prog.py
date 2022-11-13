import sys
from collections import UserString


class DivStr(UserString):
    def __init__(self, seq=""):
        super().__init__(seq)

    def __floordiv__(self, other):
        l = len(self) // other
        return iter(self[i: i + l] for i in range(0, other * l, l))

    def __mod__(self, other):
        return self[-(len(self) % other):]


if __name__ == '__main__':
    exec(sys.stdin.read())
