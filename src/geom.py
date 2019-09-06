#!/usr/bin/env python

from numpy import sqrt


def det2(ab, cd):
    (a, b) = ab
    (c, d) = cd
    return (a * d) - (b * c)


def det3(abc, def_, ghi):
    (a, b, c) = abc
    (d, e, f) = def_
    (g, h, i) = ghi
    return (a * det2((e, f), (h, i))) \
        - (b * det2((d, f), (g, i))) \
        + (c * det2((d, e), (g, h)))


def det4(abcd, efgh, ijkl, mnop):
    (a, b, c, d) = abcd
    (e, f, g, h) = efgh
    (i, j, k, l) = ijkl
    (m, n, o, p) = mnop
    return (a * det3((f, g, h), (j, k, l), (n, o, p))) \
        - (b * det3((e, g, h), (i, k, l), (m, o, p))) \
        + (c * det3((e, f, h), (i, j, l), (m, n, p))) \
        - (d * det3((e, f, g), (i, j, k), (m, n, o)))


def ccw(a, b, c):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    return ((cy - ay) * (bx - ax)) > ((by - ay) * (cx - ax))


def intersect(ab, cd):
    (a, b) = ab
    (c, d) = cd
    return (ccw(a, c, d) != ccw(b, c, d)) and (ccw(a, b, c) != ccw(a, b, d))


def slope_intercept(a, b):
    (ax, ay) = a
    (bx, by) = b
    if ax == bx:
        return (None, None)
    else:
        m = (by - ay) / (bx - ax)
        b = ay - (m * ax)
        return (m, b)


def point_of_intersection(ab, cd):
    if intersect(ab, cd):
        ((ax, ay), (bx, by)) = ab
        ((cx, cy), (dx, dy)) = cd
        xdelta = (ax - bx, cx - dx)
        ydelta = (ay - by, cy - dy)
        denominator = det2(xdelta, ydelta)
        if denominator != 0.0:
            d = (det2(*ab), det2(*cd))
            x = det2(d, xdelta) / denominator
            y = det2(d, ydelta) / denominator
            return (x, y)
    return None


def circle_of_points(a, b, c):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    if (a == b) or (b == c) or (a == c) or ((ax == bx) and (bx == cx)) \
            or ((ay == by) and (by == cy)):
        return None
    else:
        ax2 = ax * ax
        ay2 = ay * ay
        bx2 = bx * bx
        by2 = by * by
        cx2 = cx * cx
        cy2 = cy * cy
        axy2 = ax2 + ay2
        bxy2 = bx2 + by2
        cxy2 = cx2 + cy2
        A2 = 2.0 * det3((ax, ay, 1.0), (bx, by, 1.0), (cx, cy, 1.0))
        B = det3((axy2, ay, 1.0), (bxy2, by, 1.0), (cxy2, cy, 1.0))
        C = det3((axy2, ax, 1.0), (bxy2, bx, 1.0), (cxy2, cx, 1.0))
        x = (B / A2)
        y = -(C / A2)
        r = sqrt(((x - ax) * (x - ax)) + ((y - ay) * (y - ay)))
        return ((x, y), r)


def point_in_circle(a, b, c, d):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    (dx, dy) = d
    # det4(...) <  0  ->  d is within circle(a, b, c)
    # det4(...) == 0  ->  d is co-circular with a, b, c
    # det4(...)  > 0  ->  d is outside circle(a, b, c)
    return det4(
        (ax, ay, ((ax * ax) + (ay * ay)), 1.0),
        (bx, by, ((bx * bx) + (by * by)), 1.0),
        (cx, cy, ((cx * cx) + (cy * cy)), 1.0),
        (dx, dy, ((dx * dx) + (dy * dy)), 1.0),
    )
