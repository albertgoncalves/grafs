#!/usr/bin/env python


def left_turn(a, b, c):
    (ax, ay) = a
    (bx, by) = b
    (cx, cy) = c
    return (((bx - ax) * (cy - ay)) - ((by - ay) * (cx - ax))) >= 0


def convex_hull(points):
    n = len(points)
    p = sorted(points)
    upper = p[:2]
    for i in range(2, n):
        upper.append(p[i])
        while len(upper) > 2 and left_turn(*upper[-3:]):
            del upper[-2]
    lower = [p[-1], p[-2]]
    for i in range(n - 2, -1, -1):
        lower.append(p[i])
        while len(lower) > 2 and left_turn(*lower[-3:]):
            del lower[-2]
    return [upper + lower[:1], lower]
