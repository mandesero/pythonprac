from collections import defaultdict


class Omnibus:
    attribs = defaultdict(int)

    def __init__(self):
        self.__attrs = defaultdict(int)

    def __setattr__(self, key, value):

        if key in self.__dict__:
            self.__attrs[key] += 1
            Omnibus.attribs[key] += 1
        else:
            self.__dict__[key] = value
            Omnibus.attribs[key] += 1

    def __getattribute__(self, key):
        print(f"{key = }")
        if key in Omnibus.attribs and key != '_Omnibus__attrs':
            return Omnibus.attribs[key]

        return object.__getattribute__(self, key)

    def __delattr__(self, key):
        if key in self.__dict__:
            self.__attrs[key] -= 1
            Omnibus.attribs[key] -= 1

            self.__dict__.pop(key)

    def __del__(self):
        for key in self.__dict__:
            Omnibus.attribs[key] -= 1 
if __name__ == '__main__':
    import sys
    exec(sys.stdin.read())
        