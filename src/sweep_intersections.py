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
    if (by < ay) or ((ay == by) and (ax < bx)):
        return b
    else:
        return a


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


def status_lt(ab, cd):
    (u1, _) = upper_end(*ab)
    (u2, _) = upper_end(*cd)
    if u1 == u2:
        (l1, _) = lower_end(*ab)
        (l2, _) = lower_end(*cd)
        return l1 < l2
    else:
        return u1 < u2


def update_points(event_queue, y, left, right):
    point = point_of_intersection(left, right)
    intersection = "intersection"
    if point is not None:
        if snd(point) < y:
            event_queue.insert(point, (intersection, (left, right)))


def sweep_intersections(segments):
    points = []
    return (segments, points)
