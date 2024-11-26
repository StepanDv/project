import math
class Point:
    def __init__(self, x, y=None, polar=False):
        if not polar:
            if type(x) == Point:
                self.x = x.x
                self.y = x.y
            else:
                self.x = x
                self.y = y
        else:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)


    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dist(self, a=None, b=None):
        x, y = 0, 0
        if type(a) == int:
            x, y = a, b
        if type(a) == Point:
            x, y = a.x, a.y
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def __str__(self):
        return f'({self.x}, {self.y})'


class Vector(Point):
    def __init__(self, a, b = None, c = None, d = None):
        if b == None:
            super().__init__(a)
        else:
            if type(a) == Point:
                self.x = b.x - a.x
                self.y = b.y - a.y
            else:
                if d != None:
                    self.x = c - a
                    self.y = d - b
                else:
                    self.x = a
                    self.y = b

    def dot_product(self, a):
        return self.x * a.x + self.y * a.y

    def __mul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y
        return Vector(self.x * other, self.y * other)

    def cross_product(self, a):
        return self.x * a.y - self.y * a.x

    def __xor__(self, other):
        return self.x * other.y - self.y * other.x

    def __rmul__(self, other):
        return self * other

class Line:
    def __init__(self, p1, p2, A = None, B = None):
        if A != None:
            self.a = A
            self.b = B
            self.c = -A * p1 - B * p2
        else:
            self.a = p1.y - p2.y
            self.b = p2.x - p1.x
            self.c = p1.x * (p2.y - p1.y) - p1.y * (p2.x - p1.x)

    def __str__(self):
        return f'{self.a} {self.b} {self.c}'

def inp():
    p = []
    a = list(map(float, input().split()))
    for i in range(0, len(a), 2):
        p.append(Point(a[i], a[i + 1]))
    return p

a, b, c, r = map(float, input().split())
if a == 0:
    vy1 = vy2 = -c / b
    vx1 = 0
    vx2 = 1
else:
    vy1 = 0
    vy2 = 1
    vx1 = -c / a
    vx2 = (-c - b) / a
v = Vector(vx1, vy1, vx2, vy2)
nv = Vector(-v.y, v.x)
nv.x *= r / math.hypot(vx1 - vx2, vy1 - vy2)
nv.y *= r / math.hypot(vx1 - vx2, vy1 - vy2)
p1 = Point(vx1 + nv.x, vy1 + nv.y)
p2 = Point(vx2 + nv.x, vy2 + nv.y)
ans = Line(p1, p2)
print(ans)
