#!/usr/bin/env python


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
