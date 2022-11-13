from math import sqrt

class InvalidInput(Exception):
    pass

class BadTriangle(Exception):
    pass

class Triangle:

    def __init__(self):
        while True:
            try:
                buff = input()
                res = self.triangleSquare(buff)
            except InvalidInput:
                print("InvalidInput")
            except BadTriangle:
                print("Not a triangle")
            else:
                print("%.2f"%res)
                break

    @staticmethod
    def length(x, y):
        return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    @staticmethod
    def triangleSquare(buff):
        try:
            (x1, y1), (x2, y2), (x3, y3) = eval(buff)
        except Exception:
            raise InvalidInput

        s1 = Triangle.length((x1, y1), (x2, y2))
        s2 = Triangle.length((x1, y1), (x3, y3))
        s3 = Triangle.length((x2, y2), (x3, y3))

        if max(s1, s2, s3) >= min(s1 + s2, s1 + s3, s2 + s3):
            raise BadTriangle

        return 1/2 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

Triangle()