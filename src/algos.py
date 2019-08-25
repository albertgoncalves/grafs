#!/usr/bin/env python

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


def sweep_sorting(lines):
    def f(ab):
        ((ax, ay), (bx, by)) = ab
        if ay > by:
            return ((ay, ax), (by, bx))
        else:
            return ((by, bx), (ay, ax))
    # order by ((max y, associated x), (min y, associated x)) descending
    return sorted(lines, reverse=True, key=f)
