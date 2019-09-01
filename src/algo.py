#!/usr/bin/env python

from operator import eq

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

    def event_lt(a, b):
        (ax, ay) = a
        (bx, by) = b
        if ay == by:
            return ax < bx
        else:
            return ay < by

    def status_lt(ab, cd):
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

    def status_sort(min_x, max_x, x, y):
        def f(status):
            (segment, _) = status
            point = point_of_intersection(segment, ((min_x, y), (max_x, y)))
            (lx, _) = lower_end(*segment)
            if point is not None:
                (px, _) = point
                return (px, lx)
            else:
                return (x, lx)
        return f

    def bounds(status_queue):
        points = []
        for (segment, _) in status_queue.iter():
            (ab, cd) = segment
            points.extend([ab, cd])
        (min_x, _) = points[0]
        (max_x, _) = points[0]
        for point in points[1:]:
            (x, _) = point
            if x < min_x:
                min_x = x
            if max_x < x:
                max_x = x
        return (min_x, max_x)

    def sweep_neighbors(status_queue, x, y, segment):
        (min_x, max_x) = bounds(status_queue)
        status_list = iter(sorted(
            list(status_queue.iter()),
            key=status_sort(min_x, max_x, x, y)
        ))
        left = None
        right = None
        for (next_segment, _) in status_list:
            if segment == next_segment:
                break
            else:
                left = next_segment
        try:
            (right, _) = next(status_list)
        finally:
            return (left, right)

    stack = []

    def update_events(event_queue, event, left, right):
        stack.append(None)
        point = point_of_intersection(left, right)
        if (point is not None):
            (ex, ey) = event
            (px, py) = point
            if (py < ey) or ((py == ey) and (ex < px)):
                event_queue.insert(point, (intersection, (left, right)))

    def fst(ab):
        (a, _) = ab
        return a

    upper = "upper"
    lower = "lower"
    intersection = "intersection"
    points = []
    event_queue = Tree(eq, event_lt)
    status_queue = Tree(eq, status_lt)
    for segment in segments:
        event_queue.insert(upper_end(*segment), (upper, segment))
        event_queue.insert(lower_end(*segment), (lower, segment))
    while not event_queue.empty():
        (event, values) = event_queue.pop()
        (x, y) = event
        for (label, value) in values:
            if label == upper:
                status_queue.insert(value, None)
                (left, right) = sweep_neighbors(status_queue, x, y, value)
                if left is not None:
                    update_events(event_queue, event, left, value)
                if right is not None:
                    update_events(event_queue, event, value, right)
            elif label == lower:
                (left, right) = sweep_neighbors(status_queue, x, y, value)
                status_queue.delete(value)
                if (left is not None) and (right is not None):
                    update_events(event_queue, event, left, right)
            else:
                points.append(event)
                (right, left) = value
                (inner_left, _) = sweep_neighbors(status_queue, x, y, left)
                if inner_left is not None:
                    update_events(event_queue, event, inner_left, left)
                    (far_left, _) = sweep_neighbors(status_queue, x, y, inner_left)
                    if far_left is not None:
                        update_events(event_queue, event, far_left, left)
                        update_events(event_queue, event, far_left, inner_left)
                (_, inner_right) = sweep_neighbors(status_queue, x, y, right)
                if inner_right is not None:
                    update_events(event_queue, event, right, inner_right)
                    (_, far_right) = sweep_neighbors(status_queue, x, y, inner_right)
                    if far_right is not None:
                        update_events(event_queue, event, right, far_right)
                        update_events(event_queue, event, inner_right, far_right)
                if (inner_left is not None) and (inner_right is not None):
                    update_events(event_queue, event, inner_left, inner_right)
            break
    dupe = not len(points) == len(set(points))
    print("\n{}duplicates: {}{}{}".format(
        Terminal.bold,
        Terminal.red if dupe else Terminal.green,
        dupe,
        Terminal.end,
    ))
    print(len(stack))
    return (segments, list(set(points)))
