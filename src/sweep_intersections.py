#!/usr/bin/env python

from bst import Tree
from geom import point_of_intersection
from term import Terminal


def upper_end(a, b):
    (ax, ay) = a
    (bx, by) = b
    if (by < ay) or ((ay == by) and (ax < bx)):
        return a
    else:
        return b


def lower_end(a, b):
    (ax, ay) = a
    (bx, by) = b
    if (ay < by) or ((ay == by) and (bx < ax)):
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
    event_queue = Tree(event_lt)
    status_queue = {}
    for segment in segments:
        event_queue.insert(upper_end(*segment), segment)
    while not event_queue.empty():
        (event, values) = event_queue.pop()
        (_, y) = event
        deletes = []
        for segment in values:
            for other in status_queue.keys():
                counter += 1
                point = point_of_intersection(segment, other)
                if point is not None:
                    points.append(point)
                if y <= snd(lower_end(*other)):
                    deletes.append(other)
            status_queue[segment] = None
        for other in set(deletes):
            del status_queue[other]
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
