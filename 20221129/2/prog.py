import sys
from inspect import get_annotations


class check(type):
    def __new__(mcs, name, bases, classdict):
        def check_annotations(self, *args):
            annotations = get_annotations(self.__class__)
            for field, tpy in annotations.items():
                try:
                    if not isinstance(getattr(self, field), tpy):
                        break
                except AttributeError:
                    break
            else:
                return True
            return False

        classdict["check_annotations"] = check_annotations
        return super().__new__(mcs, name, bases, classdict)


if __name__ == '__main__':
    exec(sys.stdin.read())
