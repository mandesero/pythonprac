class Grange:

    def __init__(self, b0, q, bn):
        seq = []
        self.q = q
        elem = b0
        while elem <= bn:
            seq.append(elem)
            elem *= q
        self.seq = seq

    def __iter__(self):
        return self.seq.__iter__()

    def __getitem__(self, key):
        print(type(key), key)
        if isinstance(key, slice):
            if not key.step:
                return Grange(key.start, self.q , key.stop)
            return Grange(key.start, self.q ** key.step , key.stop)

        return self.seq[key]

    def __repr__(self):
        return str(self.seq)
