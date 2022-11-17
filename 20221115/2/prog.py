class Num:
    def __set_name__(self, owner, name):
        self.name = name
        self._protected_name = f"_{name}"

    def __set__(self, obj, val):
        if 'real' in dir(val):
            val = val
        elif '__len__' in dir(val):
            val = len(val)
        setattr(obj, self._protected_name, val)

    def __get__(self, obj, owner):
        if hasattr(obj, self._protected_name):
            return getattr(obj, self._protected_name)
        return 0

import sys


if __name__ == '__main__':
    exec(sys.stdin.read())


