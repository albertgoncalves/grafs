#!/usr/bin/env python

from bst import BST
from geom import ccw


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
    def upper(ab):
        ((ax, ay), (bx, by)) = ab
        if ay > by:
            return (ax, ay)
        else:
            return (bx, by)

    def compare_segments(ab, cd):
        (abx, aby) = upper(ab)
        (cdx, cdy) = upper(cd)
        if aby == cdy:
            # when tied, take lower x
            return abx > cdx
        else:
            return aby < cdy

    event_queue = BST(compare_segments)
    for segment in segments:
        event_queue.push(segment)
    while not event_queue.empty():
        print(event_queue.pop())
    for segment in segments:
        event_queue.push(segment)
    print(event_queue)
