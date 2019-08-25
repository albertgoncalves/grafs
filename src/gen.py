#!/usr/bin/env python

from random import randint

MIN = 0
MAX = 100


def random_point():
    return (randint(MIN, MAX), randint(MIN, MAX))


def random_points(n):
    return [random_point() for _ in range(n)]


def random_lines(n):
    return [(random_point(), random_point()) for _ in range(n)]
