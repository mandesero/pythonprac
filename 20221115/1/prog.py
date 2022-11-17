def objcount(cls):
    init = cls.__init__
    cls.counter = 0

    def new_init(self, *args):
        init(self, *args)
        cls.counter += 1
    cls.__init__ = new_init

    delete = cls.__del__ if "__del__" in dir(cls) else lambda self, *args: None

    def new_delete(self, *args):
        delete(self, *args)
        cls.counter -= 1
    cls.__del__ = new_delete

    return cls

import sys


if __name__ == '__main__':
    exec(sys.stdin.read())