import sys
from inspect import get_annotations
from typing import get_origin


class check(type):
    def __new__(mcs, name, bases, classdict):
        def check_annotations(self):
            annotations = get_annotations(self.__class__)
            for field, tpy in annotations.items():
                try:
                    attr = getattr(self, field)
                except AttributeError:
                    return False
                attr_type = tpy if get_origin(tpy) is None else get_origin(tpy)
                if not isinstance(attr, attr_type):
                    return False
            return True
        classdict["check_annotations"] = check_annotations
        return super().__new__(mcs, name, bases, classdict)


if __name__ == '__main__':
    exec(sys.stdin.read())
