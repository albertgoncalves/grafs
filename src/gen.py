#!/usr/bin/env python

# from random import random
from random import randint


def random_point():
    # return (random(), random())
    return (randint(0, 1000), randint(0, 1000))


def random_points(n):
    return [random_point() for _ in range(n)]


def random_segments(n):
    return [(random_point(), random_point()) for _ in range(n)]
