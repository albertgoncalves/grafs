#!/usr/bin/env python

from math import cos, pi, sin, sqrt
from os import environ
from random import random, seed

from matplotlib.pyplot import close, savefig, subplots, tight_layout

PI2 = pi * 2


def point(radius):
    a = random() * PI2
    r = radius * sqrt(random())
    return (r * cos(a), r * sin(a))


def distance(ax, ay, bx, by):
    return sqrt(pow(bx - ax, 2) + pow(by - ay, 2))


def relative_neighborhoods(points):
    edges = []
    memo = {}
    n = len(points)
    for i in range(n):
        for j in range(n):
            if i != j:
                try:
                    memo[(i, j)]
                except:
                    a = points[i]
                    b = points[j]
                    flag = True
                    ts = []
                    for k in range(n):
                        if ((i != k) and (j != k)):
                            c = points[k]
                            ts.append(max(distance(*a, *c), distance(*b, *c)))
                    flag = True
                    for t in ts:
                        if distance(*a, *b) > t:
                            flag = False
                            break
                    if flag:
                        edges.append((a, b))
                    memo[(j, i)] = None
    return edges


def plot(points, edges, filename):
    _, ax = subplots(figsize=(8, 8))
    ax.scatter(*zip(*points))
    for edge in edges:
        a = edge[0]
        b = edge[1]
        x = (a[0], b[0])
        y = (a[1], b[1])
        ax.plot(x, y, lw=0.85)
    ax.set_aspect("equal")
    tight_layout()
    savefig(filename)
    close()


def main():
    # seed(1)
    # radius = 1
    # plot(
    #     relative_neighborhoods([point(radius) for _ in range(200)]),
    #     "{}/out/main.png".format(environ["WD"]),
    # )
    points = [
        (1.0, 0.0),
        (0.5, 0.25),
        (0.0, 1.0),
        (0.75, 0.65),
        (0.9, 0.45),
        (0.3, 0.7),
    ]
    edges = [
        ((0.7812, 0.1875), (0.6613, 0.4273)),
        ((0.6613, 0.4272), (0.5081, 0.5230)),
        ((0.5081, 0.5230), (-0.7250,-2.5e-2)),
        ((0.5081, 0.5230), (0.5937, 1.2937)),
        ((-0.7250, -2.5e-2), (0.5937, 1.2937)),
    ]
    plot(points, edges, "{}/out/verify_hs.png".format(environ["WD"]))

if __name__ == "__main__":
    main()
