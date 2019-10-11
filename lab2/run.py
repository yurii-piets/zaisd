import csv

from common.point import Point


def read_points(file_name):
    points = []
    with open(file_name, encoding="mbcs") as csv_file:
        rows = csv.reader(csv_file, delimiter=';')
        for row in rows:
            if len(row) != 0:
                points.append(Point(row[0], row[1]))
    return points


if __name__ == '__main__':
    all_points = read_points("punkty.csv")
    print(all_points)