#!/usr/bin/env python

from operator import eq, lt

from bst import Tree
from geom import point_of_intersection
from term import Terminal


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
        for segment in values:
            status_queue.insert(segment, None)
            for (other, _) in status_queue.iter():
                counter += 1
                if snd(lower_end(*other)) < y:
                    point = point_of_intersection(segment, other)
                    if point is not None:
                        points.append(point)
                else:
                    status_queue.delete(other)
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
