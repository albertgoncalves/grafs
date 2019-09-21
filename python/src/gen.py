#!/usr/bin/env python

from numpy.random import random


def random_point():
    return (random(), random())


def random_points(n):
    return [random_point() for _ in range(n)]


def random_segments(n):
    return [(random_point(), random_point()) for _ in range(n)]
