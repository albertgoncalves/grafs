#!/usr/bin/env python

from os import environ
from random import random, seed

from matplotlib.pyplot import close, savefig, subplots, tight_layout

from algos import convex_hull


def random_points(n):
    return [(random(), random()) for _ in range(n)]


def init_plot():
    _, ax = subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    return ax


def plot_points(ax, points):
    ax.scatter(*zip(*points))


def plot_lines(ax, lines):
    for line in lines:
        ax.plot(*zip(*line))


def save_plot(filename):
    tight_layout()
    savefig(filename)
    close()


def plot_convex_hull(points, filename):
    ax = init_plot()
    plot_points(ax, points)
    plot_lines(ax, convex_hull(points))
    save_plot(filename)


def main():
    seed(4)
    plot_convex_hull(
        random_points(250),
        "{}/out/convex_hull.png".format(environ["WD"]),
    )


if __name__ == "__main__":
    main()