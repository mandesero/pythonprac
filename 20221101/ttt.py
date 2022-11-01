class Rectangle:
    rectcnt = 0

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        Rectangle.rectcnt += 1
        setattr(self, f"rect_{self.rectcnt}", self.rectcnt)

    def __str__(self):
        return f'''
            {self.x1, self.y1}
            {self.x2, self.y2}
            {self.x1, self.y2}
            {self.x2, self.y1}
        '''

    def square(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def __lt__(self, other):
        return self.square() < other.square()

    def __eq__(self, other):
        return self.square() == other.square()

    def __mul__(self, val):
        return Rectangle(
            self.x1 * val,
            self.y1 * val,
            self.x2 * val,
            self.y2 * val
        )

    def __rmul__(self, val):
        return self.__mul__(val)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return (
            (self.x1, self.y1),
            (self.x2, self.y2),
            (self.x1, self.y2),
            (self.x2, self.y1)
        ).__iter__()


    def __getitem__(self, key):
        return list(self)[key]





