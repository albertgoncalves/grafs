#!/usr/bin/env python

from operator import lt
from os import environ
from random import seed, shuffle

from matplotlib.pyplot import close, savefig, subplots, tight_layout

from algo import convex_hull
from bst import insert, leaf, show
from gen import random_lines, random_points
from geom import point_of_intersection

WD = environ["WD"]


def init_plot():
    _, ax = subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    return ax


def plot_points(ax, points):
    ax.scatter(*zip(*points), zorder=1)


def plot_lines(ax, lines):
    for line in lines:
        ax.plot(*zip(*line), zorder=0)


def export(filename):
    tight_layout()
    savefig(filename)
    close()


def main():
    def demo_convex_hulls(n):
        for i in range(n):
            seed(i)
            points = random_points(50)
            ax = init_plot()
            plot_points(ax, points)
            plot_lines(ax, convex_hull(points))
            export("{}/out/convex_hull_{}.png".format(WD, i))

    def demo_point_of_intersection(n):
        for i in range(n):
            lines = random_lines(2)
            point = point_of_intersection(*lines)
            ax = init_plot()
            if point:
                plot_points(ax, [point])
            plot_lines(ax, lines)
            export("{}/out/point_of_intersection_{}.png".format(WD, i))

    def demo_bst(n, s):
        seed(s)
        xs = list(range(n))
        shuffle(xs)
        tree = leaf(xs[0])
        for i in range(1, n):
            insert(tree, lt, leaf(xs[i]))
        show(tree)

    # demo_convex_hulls(50)
    demo_point_of_intersection(50)
    # demo_bst(15, 0)


if __name__ == "__main__":
    main()
