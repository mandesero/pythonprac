from string import ascii_lowercase


class Alpha:
    __slots__ = tuple(ascii_lowercase)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        ans = []
        for k in self.__class__.__slots__:
            if hasattr(self, str(k)):
                ans.append(f"{k}: {getattr(self, str(k))}")
        return ", ".join(ans)


class AlphaQ(dict):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k not in ascii_lowercase:
                raise AttributeError
        super().__init__(kwargs)

    def __getattr__(self, item):
        if item not in self:
            raise AttributeError
        return self[item]

    def __setattr__(self, key, value):
        if key in ascii_lowercase:
            self[key] = value
        else:
            raise AttributeError

    def __str__(self):
        ans = []
        for k, v in sorted(self.items(), key=lambda x: x[0]):
            ans.append(f"{k}: {v}")
        return ", ".join(ans)


import sys

if __name__ == '__main__':
    exec(sys.stdin.read())
