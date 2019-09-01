#!/usr/bin/env python

from os import environ
from random import seed

from algo import convex_hull, sweep_intersections
from gen import random_segments, random_points
from geom import point_of_intersection
from plot import export, init_plot, plot_points, plot_segments


def demo_convex_hulls(n, out):
    for i in range(n):
        seed(i)
        points = random_points(50)
        ax = init_plot()
        plot_points(ax, points)
        plot_segments(ax, convex_hull(points))
        export("{}/convex_hull_{}.png".format(out, i))


def demo_point_of_intersection(n, out):
    for i in range(n):
        segments = random_segments(2)
        point = point_of_intersection(*segments)
        ax = init_plot()
        if point:
            plot_points(ax, [point])
        plot_segments(ax, segments)
        export("{}/point_of_intersection_{}.png".format(out, i))


def demo_sweep_intersections(n, s, out):
    seed(s)
    (segments, points) = sweep_intersections(random_segments(n))
    ax = init_plot()
    plot_points(ax, points)
    plot_segments(ax, segments)
    export("{}/sweep_intersections.png".format(out))


def main():
    out = "{}/out".format(environ["WD"])
    # demo_convex_hulls(50, out)
    # demo_point_of_intersection(50, out)
    demo_sweep_intersections(8, 4, out)


if __name__ == "__main__":
    main()
