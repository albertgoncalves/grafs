#!/usr/bin/env python


from matplotlib.pyplot import close, grid, savefig, subplots, tight_layout
from numpy.random import randint


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
    grid(alpha=0.2)
    tight_layout()
    savefig(filename)
    close()
