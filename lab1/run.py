import csv
import matplotlib.pyplot as plt
import math
from operator import add, sub

from common.point import Point


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
    min_point = min(points, key=lambda p: p.y)
    points.remove(min_point)
    data_shifted_coords = [sub(point, min_point) for point in points]
    sorted_shifted_data = sorted(data_shifted_coords, key=get_angle)
    sorted_data = [add(point, min_point) for point in sorted_shifted_data][::-1]
    stack = [min_point]
    while sorted_data:
        if len(stack) > 2:
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
