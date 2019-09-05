#!/usr/bin/env python

from time import time

from bst import Tree
from geom import point_of_intersection, slope_intercept
from term import Terminal


def results(brute, counter, dupe, start):
    debrief = [
        "brute       : {}{}{}",
        "counter     : {}{}{}",
        "duplicates  : {}{}{}{}",
        "duration    : {}\n",
    ]
    return "\n".join(debrief).format(
        Terminal.bold,
        brute,
        Terminal.end,
        Terminal.bold,
        counter,
        Terminal.end,
        Terminal.bold,
        Terminal.red if dupe else Terminal.green,
        dupe,
        Terminal.end,
        round(time() - start, 4),
    )


def upper_end(a, b):
    (ax, ay) = a
    (bx, by) = b
    if (by < ay) or ((ay == by) and (ax < bx)):
        return a
    else:
        return b


def lower_end(a, b):
    (ax, ay) = a
    (bx, by) = b
    if (by < ay) or ((ay == by) and (ax < bx)):
        return b
    else:
        return a


def fst(ab):
    (a, _) = ab
    return a


def snd(ab):
    (_, b) = ab
    return b


def event_lt(a, b):
    (ax, ay) = a
    (bx, by) = b
    if ay == by:
        return ax < bx
    else:
        return ay < by


def brute_sweep_intersections(segments):
    start = time()
    counter = 0
    status = {
        "upper": 0,
        "lower": 1,
    }
    points = []
    event_queue = Tree(event_lt)
    status_queue = {}
    for segment in segments:
        event_queue.insert(upper_end(*segment), (status["upper"], segment))
        event_queue.insert(lower_end(*segment), (status["lower"], segment))
    while not event_queue.empty():
        (event, (label, segment)) = event_queue.pop()
        (_, y) = event
        if label == status["upper"]:
            for other in list(status_queue.keys()):
                counter += 1
                point = point_of_intersection(segment, other)
                if point is not None:
                    points.append(point)
            status_queue[segment] = None
        else:
            del status_queue[segment]
    print(results(True, counter, not len(points) == len(set(points)), start))
    return (segments, points)


def status_lt(k1, k2):
    ((_, y1), s1) = k1
    ((_, y2), s2) = k2
    y = y1 if y1 < y2 else y2
    (m1, b1) = slope_intercept(*s1)
    (m2, b2) = slope_intercept(*s2)
    x1 = round((y - b1) / m1, 8)
    x2 = round((y - b2) / m2, 8)
    return x1 < x2


def update_points(event_queue, y, left, right, status):
    point = point_of_intersection(left, right)
    if point is not None:
        if snd(point) < y:
            event_queue.insert(point, (status, (left, right)))


def sweep_intersections(segments):
    start = time()
    counter = 0
    status = {
        "upper": 0,
        "intersection": 1,
        "lower": 2,
    }
    points = []
    memo = {}
    event_queue = Tree(event_lt)
    status_queue = Tree(status_lt)
    for segment in segments:
        event_queue.insert(upper_end(*segment), (status["upper"], segment))
        event_queue.insert(lower_end(*segment), (status["lower"], segment))
    while not event_queue.empty():
        (event, (label, payload)) = event_queue.pop()
        (_, y) = event
        if label == status["upper"]:
            memo[payload] = event
            status_queue.insert((event, payload), None)
            (left, right) = status_queue.neighbors((event, payload))
            if left is not None:
                ((_, left_segment), _) = left
                counter += 1
                update_points(
                    event_queue,
                    y,
                    left_segment,
                    payload,
                    status["intersection"],
                )
            if right is not None:
                ((_, right_segment), _) = right
                counter += 1
                update_points(
                    event_queue,
                    y,
                    payload,
                    right_segment,
                    status["intersection"],
                )
        elif label == status["lower"]:
            (left, right) = status_queue.neighbors((memo[payload], payload))
            status_queue.delete((memo[payload], payload))
            if (left is not None) and (right is not None):
                ((_, left_segment), _) = left
                ((_, right_segment), _) = right
                counter += 1
                update_points(
                    event_queue,
                    y,
                    left_segment,
                    right_segment,
                    status["intersection"],
                )
        else:
            points.append(event)
            (right, left) = payload
            status_queue.delete((memo[left], left))
            status_queue.delete((memo[right], right))
            memo[left] = event
            memo[right] = event
            status_queue.insert((memo[left], left), None)
            status_queue.insert((memo[right], right), None)
            (far_left, _) = status_queue.neighbors((memo[left], left))
            (_, far_right) = status_queue.neighbors((memo[right], right))
            if far_left is not None:
                ((_, far_left_segment), _) = far_left
                counter += 1
                update_points(
                    event_queue,
                    y,
                    far_left_segment,
                    left,
                    status["intersection"],
                )
            if far_right is not None:
                ((_, far_right_segment), _) = far_right
                counter += 1
                update_points(
                    event_queue,
                    y,
                    right,
                    far_right_segment,
                    status["intersection"],
                )
    print(results(False, counter, not len(points) == len(set(points)), start))
    return (segments, points)
