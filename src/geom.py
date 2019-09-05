#!/usr/bin/env python

from numpy import sqrt


def ccw(a, b, c):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    return ((cy - ay) * (bx - ax)) > ((by - ay) * (cx - ax))


def intersect(ab, cd):
    (a, b) = ab
    (c, d) = cd
    return (ccw(a, c, d) != ccw(b, c, d)) and (ccw(a, b, c) != ccw(a, b, d))


def determinant(a, b):
    (ax, ay) = a
    (bx, by) = b
    return (ax * by) - (ay * bx)


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
        denominator = determinant(xdelta, ydelta)
        if denominator != 0:
            d = (determinant(*ab), determinant(*cd))
            x = determinant(d, xdelta) / denominator
            y = determinant(d, ydelta) / denominator
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
        A2 = 2 * ((ax * (by - cy)) - (ay * (bx - cx)) + (bx * cy) - (cx * by))
        x = ((axy2 * (by - cy)) + (bxy2 * (cy - ay)) + (cxy2 * (ay - by))) / A2
        y = ((axy2 * (cx - bx)) + (bxy2 * (ax - cx)) + (cxy2 * (bx - ax))) / A2
        a = (x - ax)
        b = (y - ay)
        r = sqrt((a * a) + (b * b))
        return ((x, y), r)
