#!/usr/bin/env python

from math import cos, pi, sin, sqrt
from random import random, seed

PI2 = pi * 2


def point(radius):
    a = random() * PI2
    r = radius * sqrt(random())
    return (r * cos(a), r * sin(a))


def distance(ax, ay, bx, by):
    return sqrt(pow(bx - ax, 2) + pow(by - ay, 2))


def relative_neighborhoods(points):
    edges = []
    memo = {}
    n = len(points)
    for i in range(n):
        for j in range(n):
            if i != j:
                try:
                    memo[(i, j)]
                except:
                    a = points[i]
                    b = points[j]
                    flag = True
                    ts = []
                    for k in range(n):
                        if ((i != k) and (j != k)):
                            c = points[k]
                            ts.append(max(distance(*a, *c), distance(*b, *c)))
                    flag = True
                    for t in ts:
                        if distance(*a, *b) > t:
                            flag = False
                            break
                    if flag:
                        edges.append((a, b))
                    memo[(j, i)] = None
    return edges


def main():
    seed(1)
    radius = 1
    points = [point(radius) for _ in range(200)]
    print(points[:10])
    print(relative_neighborhoods(points)[:10])


if __name__ == "__main__":
    main()
