#!/usr/bin/env python

from operator import lt
from os import environ
from random import randint, seed

from matplotlib.pyplot import close, savefig, subplots, tight_layout

from algo import convex_hull
from bst import insert, leaf, show
from gen import random_points


def init_plot():
    _, ax = subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    return ax


def plot_points(ax, points):
    ax.scatter(*zip(*points), zorder=1)


def plot_lines(ax, lines):
    for line in lines:
        ax.plot(*zip(*line), zorder=0)


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
    def demo_convex_hulls(n):
        for i in range(n):
            seed(i)
            plot_convex_hull(
                random_points(50),
                "{}/out/convex_hull_{}.png".format(environ["WD"], i),
            )

    def demo_bst(n, s):
        def f():
            return randint(0, 50)

        seed(s)
        tree = leaf(f())
        for _ in range(n):
            insert(tree, lt, leaf(f()))
        show(tree)

    demo_convex_hulls(50)
    demo_bst(15, 1)


if __name__ == "__main__":
    main()
