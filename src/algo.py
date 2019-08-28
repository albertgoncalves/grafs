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
        (u1, _) = upper_end(*ab)
        (u2, _) = upper_end(*cd)
        if u1 == u2:
            (l1, _) = lower_end(*ab)
            (l2, _) = lower_end(*cd)
            return l1 < l2
        else:
            return u1 < u2

    counter = 0
    points = []
    event_queue = Tree(compare_event)
    status_queue = Tree(compare_status)
    for segment in segments:
        event_queue.insert(event_point(*segment), segment)
    while not event_queue.empty():
        (key, values) = event_queue.pop()
        (_, horizontal) = key
        for value in values:
            if value is not None:
                status_queue.insert(value, None)
        candidates = list(status_queue.iter())
        n = len(candidates)
        deletes = []
        inserts = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                counter += 1
                (ab, _) = candidates[i]
                (cd, _) = candidates[j]
                point = point_of_intersection(ab, cd)
                if point is not None:
                    points.append(point)
                    (_, y) = point
                    if y <= horizontal:
                        deletes.extend([ab, cd])
                        inserts.extend([(point, ab), (point, cd)])
                else:
                    break
            for j in range(i - 1, -1, -1):
                counter += 1
                (ab, _) = candidates[i + 1]
                (cd, _) = candidates[j]
                point = point_of_intersection(ab, cd)
                if point is not None:
                    points.append(point)
                    (_, y) = point
                    if y <= horizontal:
                        deletes.extend([ab, cd])
                        inserts.extend([(point, ab), (point, cd)])
                else:
                    break
        for segment in set(deletes):
            status_queue.delete(segment)
        for (point, segment) in set(inserts):
            event_queue.insert(point, None)
            status_queue.insert((point, lower_end(*segment)), None)
        for (candidate, _) in status_queue.iter():
            (_, y) = lower_end(*candidate)
            if y > horizontal:
                status_queue.delete(candidate)
    print(counter)
    return (segments, points)
