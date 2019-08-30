#!/usr/bin/env python

from operator import lt
from os import environ
from random import randint, seed, shuffle

from matplotlib.pyplot import close, savefig, subplots, tight_layout

from algo import convex_hull, sweep_intersections
from bst import Tree
from gen import random_segments, random_points
from geom import point_of_intersection


def init_plot():
    _, ax = subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    return ax


def plot_points(ax, points):
    n = len(points)
    if n > 0:
        color = [randint(0, 10) for _ in range(n)]
        ax.scatter(*zip(*points), c=color, cmap="Accent", zorder=1)


def plot_segments(ax, segments):
    for segment in segments:
        ax.plot(*zip(*segment), alpha=0.75, zorder=0)


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
            plot_segments(ax, convex_hull(points))
            export("{}/convex_hull_{}.png".format(out, i))

    def demo_point_of_intersection(n):
        for i in range(n):
            segments = random_segments(2)
            point = point_of_intersection(*segments)
            ax = init_plot()
            if point:
                plot_points(ax, [point])
            plot_segments(ax, segments)
            export("{}/point_of_intersection_{}.png".format(out, i))

    def demo_bst(n, s):
        seed(s)
        values = list(range(n))
        shuffle(values)
        tree = Tree(lt)
        for i in range(n):
            tree.insert(values[i], i)
        print(tree, "\n")
        for i in range(n):
            print(i, tree.neighbors(i))
        # tree.swap_values(2, 3)

    def demo_sweep_intersections(n, s):
        seed(s)
        (segments, points) = sweep_intersections(random_segments(n))
        ax = init_plot()
        plot_points(ax, points)
        plot_segments(ax, segments)
        export("{}/sweep_intersections.png".format(out))

    # demo_convex_hulls(50)
    # demo_point_of_intersection(50)
    demo_bst(15, 1)
    # demo_sweep_intersections(15, 3)


if __name__ == "__main__":
    main()
