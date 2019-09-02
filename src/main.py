#!/usr/bin/env python

from os import environ
from random import seed
from sys import argv

from algo import convex_hull, brute_sweep_intersections
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
        seed(i)
        segments = random_segments(2)
        point = point_of_intersection(*segments)
        ax = init_plot()
        if point:
            plot_points(ax, [point])
        plot_segments(ax, segments)
        export("{}/point_of_intersection_{}.png".format(out, i))


def demo_brute_sweep_intersections(n, out):
    for i in range(n):
        seed(i)
        (segments, points) = brute_sweep_intersections(random_segments(20))
        ax = init_plot()
        plot_points(ax, points)
        plot_segments(ax, segments)
        export("{}/sweep_intersections_{}.png".format(out, i))


def main():
    if len(argv) > 1:
        out = "{}/out".format(environ["WD"])
        for arg in set(argv[1:]):
            if arg == "-c":
                demo_convex_hulls(50, out)
            elif arg == "-p":
                demo_point_of_intersection(50, out)
            elif arg == "-i":
                demo_brute_sweep_intersections(50, out)


if __name__ == "__main__":
    main()
