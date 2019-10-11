import csv
from collections import OrderedDict

import matplotlib.pyplot as plt

from common.point import Point


def slope(a, b):
    if a.x == b.x:
        return float('inf')
    if a.y == b.y:
        return 0.0
    return round((b.y - a.y) / (b.x - a.x), 2)


def read_points(file_name):
    points = []
    with open(file_name, encoding="mbcs") as csv_file:
        rows = csv.reader(csv_file, delimiter=';')
        for row in rows:
            if len(row) != 0:
                points.append(Point(row[0], row[1]))
    return points


def most_popular_indexes(slopes):
    ds = {}
    for s in slopes:
        if s in ds.keys():
            ds[s] += 1
        else:
            ds[s] = 1

    indexes = []
    if ds:
        max_slopes = sorted(ds.items(), key=lambda x: x[1])[-1][0]
        for i in range(0, len(slopes)):
            if max_slopes == slopes[i]:
                indexes.append(i)
    return indexes


def col(points):
    slopes = []
    max_points = []
    for i in range(0, len(points)):
        for j in range(i + 1, len(points)):
            slopes.append(slope(points[i], points[j]))

        pop_indexes = most_popular_indexes(slopes)
        if len(pop_indexes) > len(max_points):
            max_points.clear()
            for pop in pop_indexes:
                max_points.append(points[i + pop])

        slopes.clear()
    return max_points


if __name__ == '__main__':
    all_points = read_points("punkty_small.csv")
    plt.figure(1)
    for point in all_points:
        plt.scatter(point.x, point.y, c='blue')
    col = col(all_points)
    for i in range(0, len(col) - 1):
        plt.plot((col[i].x, col[i + 1].x), (col[i].y, col[i + 1].y), 'g-')
    plt.show()
