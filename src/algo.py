#!/usr/bin/env python

from bst import Tree
from geom import ccw, point_of_intersection


def convex_hull(points):
    n = len(points)
    p = sorted(points, key=lambda a: (a[0], a[1]))
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


def sweep_intersections(segments):
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

    def compare_event(a, b):
        (ax, ay) = a
        (bx, by) = b
        if ay == by:
            return ax > bx
        else:
            return ay < by

    def compare_status(ab, cd):
        (u1, _) = upper_end(*ab)
        (u2, _) = upper_end(*cd)
        if u1 == u2:
            (l1, _) = lower_end(*ab)
            (l2, _) = lower_end(*cd)
            return l1 < l2
        else:
            return u1 < u2

    def snd(ab):
        (_, b) = ab
        return b

    upper = "upper"
    lower = "lower"
    intersection = "intersection"
    points = []
    event_queue = Tree(compare_event)
    status_queue = Tree(compare_status)
    for segment in segments:
        event_queue.insert(upper_end(*segment), (upper, segment))
        event_queue.insert(lower_end(*segment), (lower, segment))
    while not event_queue.empty():
        (key, values) = event_queue.pop()
        (_, sweep_line) = key
        for (label, value) in values:
            if label == upper:
                status_queue.insert(value, value)
                (l, r) = status_queue.neighbors(value)
                if l is not None:
                    (_, [left]) = l
                    point = point_of_intersection(left, value)
                    if (point is not None) and (snd(point) < sweep_line):
                        event_queue.insert(point, (intersection, (left, value)))
                if r is not None:
                    (_, [right]) = r
                    point = point_of_intersection(value, right)
                    if (point is not None) and (snd(point) < sweep_line):
                        event_queue.insert(point, (intersection, (value, right)))
            elif label == lower:
                (l, r) = status_queue.neighbors(value)
                status_queue.delete(value)
                if (l is not None) and (r is not None):
                    (_, [left]) = l
                    (_, [right]) = r
                    point = point_of_intersection(left, right)
                    if (point is not None) and (snd(point) < sweep_line):
                        event_queue.insert(point, (intersection, (left, right)))
            else:
                points.append(key)
                (left, right) = value
                (fl, _) = status_queue.neighbors(left)
                (_, fr) = status_queue.neighbors(right)
                if fl is not None:
                    (_, [far_left]) = fl
                    point = point_of_intersection(far_left, right)
                    if (point is not None) and (snd(point) < sweep_line):
                        event_queue.insert(point, (intersection, (far_left, right)))
                if fr is not None:
                    (_, [far_right]) = fr
                    point = point_of_intersection(left, far_right)
                    if (point is not None) and (snd(point) < sweep_line):
                        event_queue.insert(point, (intersection, (left, far_right)))
                # status_queue.swap_values(left, right)
    print("duplicates:\t{}".format(not len(points) == len(set(points))))
    list(map(print, sorted(points)))
    return (segments, list(set(points)))
