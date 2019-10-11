class Point:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __lt__(self, other):
        return self.y < other.y if (self.x == other.x) else self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    __repr__ = __str__
