#!/usr/bin/env python

from operator import eq, lt

from bst import Tree
from geom import ccw, point_of_intersection
from term import Terminal


def convex_hull(points):
    n = len(points)
    p = sorted(points)
    upper = p[:2]
    for i in range(2, n):
        upper.append(p[i])
        while len(upper) > 2 and not ccw(*upper[-3:]):
            del upper[-2]
    lower = [p[-1], p[-2]]
    for i in range(n - 2, -1, -1):
        lower.append(p[i])
        while len(lower) > 2 and not ccw(*lower[-3:]):
            del lower[-2]
    return [upper + lower[:1], lower]


def upper_end(a, b):
    (_, ay) = a
    (_, by) = b
    if ay < by:
        return b
    else:
        return a


def lower_end(a, b):
    (_, ay) = a
    (_, by) = b
    if ay < by:
        return a
    else:
        return b


def snd(ab):
    (_, b) = ab
    return b


def event_lt(a, b):
    (ax, ay) = a
    (bx, by) = b
    if ay == by:
        return ax < bx
    else:
        return ay < by


def brute_sweep_intersections(segments):
    counter = 0
    points = []
    event_queue = Tree(eq, event_lt)
    status_queue = Tree(eq, lt)
    for segment in segments:
        event_queue.insert(upper_end(*segment), segment)
    while not event_queue.empty():
        (event, values) = event_queue.pop()
        (_, y) = event
        for segment in sorted(values):
            for (other, _) in status_queue.iter():
                counter += 1
                if snd(lower_end(*other)) < y:
                    point = point_of_intersection(segment, other)
                    if point is not None:
                        points.append(point)
                else:
                    status_queue.delete(other)
            status_queue.insert(segment, None)
    dupe = not len(points) == len(set(points))
    print("counter    : {}{}{}\nduplicates : {}{}{}{}".format(
        Terminal.bold,
        counter,
        Terminal.end,
        Terminal.bold,
        Terminal.red if dupe else Terminal.green,
        dupe,
        Terminal.end,
    ))
    return (segments, points)
