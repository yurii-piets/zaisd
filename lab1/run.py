import csv
import matplotlib.pyplot as plt
import math
from operator import add, sub


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
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def __add__(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

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
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x) >= 0


def get_angle(point):
    return math.atan2(point.y, point.x)


def graham(points):
    min_p = min(points, key=lambda p: p.y)
    points.remove(min_p)
    data_shifted_coords = [sub(point, min_p) for point in points]
    sorted_shifted_data = sorted(data_shifted_coords, key=get_angle)
    sorted_data = [add(point, min_p) for point in sorted_shifted_data][::-1]
    stack = [min_p]
    while sorted_data:
        if len(stack) >= 3:
            if is_left(stack[-3], stack[-2], stack[-1]):
                stack.append(sorted_data.pop())
            else:
                stack.pop(-2)
        else:
            stack.append(sorted_data.pop())
    if not is_left(stack[-3], stack[-2], stack[-1]):
        stack.pop(-2)
    return stack


def put_points(points, color):
    for point in points:
        plt.scatter(point.x, point.y, c=color)


if __name__ == '__main__':
    all_points = read_points("punktyPrzykladowe.csv")
    plt.figure(1)
    put_points(all_points, color='blue')
    graham_points = graham(all_points)
    put_points(graham_points, color='red')
    plt.show()
