#!/usr/bin/env python

from os import environ
from random import random, seed

from matplotlib.pyplot import close, savefig, subplots, tight_layout


def random_points(n):
    return [(random(), random()) for _ in range(n)]


def plot(points, lines, filename):
    _, ax = subplots(figsize=(8, 8))
    ax.scatter(*zip(*points))
    for line in lines:
        ax.plot(*zip(*line))
    ax.set_aspect("equal")
    tight_layout()
    savefig(filename)
    close()


def left_turn(a, b, c):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    return (((bx - ax) * (cy - ay)) - ((by - ay) * (cx - ax))) >= 0


def convex_hull(points):
    n = len(points)
    p = sorted(points)
    upper = p[:2]
    for i in range(2, n):
        upper.append(p[i])
        while len(upper) > 2 and left_turn(*upper[-3:]):
            del upper[-2]
    lower = [p[-1], p[-2]]
    for i in range(n - 2, -1, -1):
        lower.append(p[i])
        while len(lower) > 2 and left_turn(*lower[-3:]):
            del lower[-2]
    return [upper + lower[:1], lower]


def main():
    seed(4)
    points = random_points(250)
    lines = convex_hull(points)
    filename = "{}/out/plot.png".format(environ["WD"])
    plot(points, lines, filename)


if __name__ == "__main__":
    main()
