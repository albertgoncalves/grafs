#!/usr/bin/env python

from operator import lt
from os import environ
from random import seed, shuffle

from matplotlib.pyplot import close, savefig, subplots, tight_layout

from algo import convex_hull
from bst import BST
from gen import random_lines, random_points
from geom import point_of_intersection


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
    out = "{}/out".format(environ["WD"])

    def demo_convex_hulls(n):
        for i in range(n):
            seed(i)
            points = random_points(50)
            ax = init_plot()
            plot_points(ax, points)
            plot_lines(ax, convex_hull(points))
            export("{}/convex_hull_{}.png".format(out, i))

    def demo_point_of_intersection(n):
        for i in range(n):
            lines = random_lines(2)
            point = point_of_intersection(*lines)
            ax = init_plot()
            if point:
                plot_points(ax, [point])
            plot_lines(ax, lines)
            export("{}/point_of_intersection_{}.png".format(out, i))

    def demo_bst(n, s):
        seed(s)
        values = list(range(n))
        shuffle(values)
        tree = BST(lt, values[0])
        for i in range(1, n):
            tree.insert(values[i])
        print(tree)
        if n > 2:
            (node, _) = tree.lookup(n - 2)
            print(node)

    demo_convex_hulls(50)
    demo_point_of_intersection(50)
    demo_bst(15, 1)


if __name__ == "__main__":
    main()
