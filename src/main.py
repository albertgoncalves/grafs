#!/usr/bin/env python

from math import sqrt
from os import environ
from random import random, seed

from matplotlib.pyplot import close, savefig, subplots, tight_layout


def point():
    return (random(), random())


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


def plot(edges, filename):
    _, ax = subplots(figsize=(8, 8))
    for edge in edges:
        ax.plot([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], color="k")
    ax.set_aspect("equal")
    tight_layout()
    savefig(filename)
    close()


def main():
    seed(1)
    plot(
        relative_neighborhoods([point() for _ in range(300)]),
        "{}/out/main.png".format(environ["WD"]),
    )


if __name__ == "__main__":
    main()
