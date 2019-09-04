#!/usr/bin/env python

from os import environ
from sys import argv

from numpy.random import seed

from convex_hull import convex_hull
from gen import random_segments, random_points
from geom import point_of_intersection
from plot import export, init_plot, plot_points, plot_segments
from sweep_intersections import brute_sweep_intersections, sweep_intersections
from term import Terminal


def demo_convex_hull(n, out):
    for i in range(n):
        seed(i)
        points = random_points(25)
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


def demo_sweep_intersections(n, out):
    for i in range(n):
        try:
            print("{}{}{}{}".format(
                Terminal.bold,
                Terminal.blue,
                i,
                Terminal.end,
            ))
            seed(i)
            xs = random_segments(15)
            (segments, points) = sweep_intersections(xs)
            ax = init_plot()
            plot_points(ax, points)
            plot_segments(ax, segments)
            export("{}/sweep_intersections_{}.png".format(out, i))
            (segments, points) = brute_sweep_intersections(xs)
            ax = init_plot()
            plot_points(ax, points)
            plot_segments(ax, segments)
            export("{}/brute_sweep_intersections_{}.png".format(out, i))
        except:
            pass


def header(text):
    return "$ demo_{}{}{}".format(Terminal.bold, text, Terminal.end)


def main():
    if len(argv) > 1:
        out = "{}/out".format(environ["WD"])
        for arg in set(argv[1:]):
            if arg == "-c":
                print(header("convex_hull"))
                demo_convex_hull(10, out)
            elif arg == "-p":
                print(header("point_of_intersection"))
                demo_point_of_intersection(10, out)
            elif arg == "-s":
                print(header("sweep_intersections"))
                demo_sweep_intersections(100, out)


if __name__ == "__main__":
    main()
