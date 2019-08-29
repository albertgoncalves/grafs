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
    def fst(ab):
        (a, _) = ab
        return a

    def snd(ab):
        (_, b) = ab
        return b

    def upper_end(a, b):
        if snd(a) < snd(b):
            return b
        else:
            return a

    def lower_end(a, b):
        if snd(a) < snd(b):
            return a
        else:
            return b

    def event_point(a, b):
        (ax, ay) = a
        (bx, by) = b
        if (ay < by) or ((ay == by) and (ax > bx)):
            return b
        else:
            return a

    def compare_event(a, b):
        (ax, ay) = a
        (bx, by) = b
        if ay == by:
            return ax > bx
        else:
            return ay < by

    def compare_status(ab, cd):
        u1 = fst(upper_end(*ab))
        u2 = fst(upper_end(*cd))
        if u1 == u2:
            l1 = fst(lower_end(*ab))
            l2 = fst(lower_end(*cd))
            return l1 < l2
        else:
            return u1 < u2

    def neighbors(point, segments):
        x = fst(point)
        l = list(filter(lambda ab: fst(upper_end(*ab)) < x, segments))
        r = list(filter(lambda ab: x < fst(upper_end(*ab)), segments))
        if len(l) > 0:
            left = l[0]
        else:
            left = None
        if len(r) > 0:
            right = r[-1]
        else:
            right = None
        return (left, right)

    points = []
    event_queue = Tree(compare_event)
    status_queue = Tree(compare_status)
    for segment in segments:
        event_queue.insert(event_point(*segment), segment)
    while not event_queue.empty():
        (event, uppers) = event_queue.pop()
        for upper in uppers:
            candidates = list(map(fst, status_queue.iter()))
            if len(candidates) > 0:
                (left, right) = neighbors(event, candidates)
                if upper is None:
                    if (left is not None) and (right is not None):
                        point = point_of_intersection(left, right)
                        if (point is not None) and (snd(point) < snd(event)):
                            points.append(point)
                            event_queue.insert(point, None)
                else:
                    if left is not None:
                        point = point_of_intersection(left, upper)
                        if (point is not None) and (snd(point) < snd(event)):
                            points.append(point)
                            event_queue.insert(point, None)
                            status_queue.delete(left)
                            status_queue.insert(
                                (point, lower_end(*left)),
                                None,
                            )
                            status_queue.insert(
                                (point, lower_end(*upper)),
                                None,
                            )
                    if right is not None:
                        point = point_of_intersection(right, upper)
                        if (point is not None) and (snd(point) < snd(event)):
                            points.append(point)
                            event_queue.insert(point, None)
                            status_queue.delete(right)
                            status_queue.insert(
                                (point, lower_end(*right)),
                                None,
                            )
                            status_queue.insert(
                                (point, lower_end(*upper)),
                                None,
                            )
            if upper is not None:
                status_queue.insert(upper, None)
            print(status_queue, "\n")
    print(len(points))
    print(len(list(set(points))))
    return (segments, points)
