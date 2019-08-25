#!/usr/bin/env python

from ast import literal_eval
from os import environ
from sys import stdin

from matplotlib.pyplot import close, savefig, subplots, tight_layout


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


def read_input():
    (points, edges) = stdin.readlines()
    return (literal_eval(points), literal_eval(edges))


def main():
    args = read_input()
    filename = "{}/out/plot.png".format(environ["WD"])
    plot(*args, filename)


if __name__ == "__main__":
    main()
