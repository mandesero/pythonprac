class Triangle:

    def __init__(self, a1, a2, b1, b2, c1, c2):
        self.x = a1, a2 # 1
        self.y = b1, b2 # 2
        self.z = c1, c2 # 3
        self.square = abs(self)
    
    def __abs__(self):
        return 0.5 * abs(
            (self.y[0] - self.x[0]) * (self.z[1] - self.x[1]) - 
            (self.z[0] - self.x[0]) * (self.y[1] - self.x[1])
        )

    def __lt__(self, other):
        return self.square < other.square

    def __gt__(self, other):
        return self.square  > other.square

    def __contains__(self, other):
        if self > other:
            x1, y1 = self.x
            x2, y2 = self.y
            x3, y3 = self.z
            
            tmp = []
            for x0, y0 in (other.x, other.y, other.z):
                t1 = (x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0)
                t2 = (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0)
                t3 = (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0)
                if (t1 > 0 and t2 > 0 and t3 > 0) or (t1 < 0 and t2 < 0 and t3 < 0):
                    tmp.append(True)
                else:
                    tmp.append(False)
            return all(tmp)
        return False
 
    def __and__(self, other):
        if self.square == 0 or other.square == 0:
            return False
        if other in self or self in other:
            return False

        x1, y1 = self.x
        x2, y2 = self.y
        x3, y3 = self.z
        
        tmp = []
        for x0, y0 in (other.x, other.y, other.z):
            t1 = (x1 - x0) * (y2 - y1) - (x2 - x1) * (y1 - y0)
            t2 = (x2 - x0) * (y3 - y2) - (x3 - x2) * (y2 - y0)
            t3 = (x3 - x0) * (y1 - y3) - (x1 - x3) * (y3 - y0)
            if (t1 > 0 and t2 > 0 and t3 > 0) or (t1 < 0 and t2 < 0 and t3 < 0):
                tmp.append(True)
            elif t1 == 0 or t2 == 0 or t3 == 0:
                tmp.append(True)
            else:
                tmp.append(False)
        return any(tmp)

    def __matmul__(self, dot):
        x1, y1 = self.x
        x2, y2 = self.y
        x3, y3 = self.z

        x0, y0 = dot

        v1 = - x1 + x0, - y1 + y0
        v2 = - x2 + x0, - y2 + y0
        v3 = - x3 + x0, - y3 + y0

        x1, y1 = x1 + 2 * v1[0], y1 + 2 * v1[1]
        x2, y2 = x2 + 2 * v2[0], y2 + 2 * v2[1]
        x3, y3 = x3 + 2 * v3[0], y3 + 2 * v3[1]

        return Triangle(
            x1, y1,
            x2, y2,
            x3, y3
        )

    def __str__(self):
        return f'''
        Triangle:
            {self.x}
            {self.y}
            {self.z}
        '''

    def __repr__(self):
        return str(self)

        
    

