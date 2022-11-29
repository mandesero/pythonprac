import sys


class dump(type):

    @staticmethod
    def wrapped(func):
        def inner(*args, **kwargs):
            print(
                f"{func.__name__}: {tuple(elem for elem in args if isinstance(elem, (int, float, str, bool)))}, {kwargs}")
            return func(*args, **kwargs)

        return inner

    def __new__(mcs, name, bases, classdict):

        new_cls_dct = {}
        for attr, val in classdict.items():
            if callable(val):
                new_cls_dct[attr] = mcs.wrapped(val)
            else:
                new_cls_dct[attr] = val

        return super().__new__(mcs, name, bases, new_cls_dct)


if __name__ == '__main__':
    exec(sys.stdin.read())
