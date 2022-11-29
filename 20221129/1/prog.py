import sys


class dump(type):

    @staticmethod
    def wrapped(func):
        def inner(*args, **kwargs):
            if func.__name__ != "my_setattr":
                try:
                    if not isinstance(args[0], (int, float, str, bool)):
                        print(f"{func.__name__}: {args[1:]}, {kwargs}")
                    else:
                        print(f"{func.__name__}: {args}, {kwargs}")
                except IndexError:
                    print(f"{func.__name__}: {args}, {kwargs}")
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

    @classmethod
    def __prepare__(mcs, name, _):
        def my_setattr(self, attrname, value):
            if callable(value):
                self.__dict__[attrname] = dump.wrapped(value)
            else:
                self.__dict__[attrname] = value

        return {'__setattr__': my_setattr}


if __name__ == '__main__':
    exec(sys.stdin.read())