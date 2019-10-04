import csv


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

    __repr__ = __str__


def read_points(file_name):
    points = []
    with open(file_name, encoding="mbcs") as csv_file:
        rows = csv.reader(csv_file, delimiter=',')
        for row in rows:
            if len(row) != 0:
                points.append(Point(row[0], row[1]))
    return points


def is_left(a, b, p):
    return ((p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)) < 0


def sort_points(s):
    s.sort()
    point_array = s[:1] + sorted(s[1:], key=lambda p: (s[0].y - p.y) / (s[0].x - p.x))
    return point_array


def graham(points):
    points = sort_points(points)
    stack = []
    for point in points:
        while len(stack) > 1 and is_left(points[-1], points[-2], point):
            stack.pop()
        stack.append(point)
    return stack


print(graham(read_points("punktyPrzykladowe.csv")))
