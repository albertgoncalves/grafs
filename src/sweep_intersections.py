#!/usr/bin/env python

from bst import Tree
from geom import point_of_intersection
from term import Terminal


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
    counter = 0
    points = []
    event_queue = Tree(event_lt)
    status_queue = {}
    for segment in segments:
        event_queue.insert(upper_end(*segment), segment)
    while not event_queue.empty():
        (event, segment) = event_queue.pop()
        (_, y) = event
        deletes = []
        for other in status_queue.keys():
            counter += 1
            point = point_of_intersection(segment, other)
            if point is not None:
                points.append(point)
            if y <= snd(lower_end(*other)):
                deletes.append(other)
        status_queue[segment] = None
        for other in set(deletes):
            del status_queue[other]
    dupe = not len(points) == len(set(points))
    print("counter    : {}{}{}\nduplicates : {}{}{}{}".format(
        Terminal.bold,
        counter,
        Terminal.end,
        Terminal.bold,
        Terminal.red if dupe else Terminal.green,
        dupe,
        Terminal.end,
    ))
    return (segments, points)


def status_lt(k1, k2):
    (x1, s1) = k1
    (x2, s2) = k2
    if x1 == x2:
        (l1, _) = lower_end(*s1)
        (l2, _) = lower_end(*s2)
        return l1 < l2
    else:
        return x1 < x2


def update_points(event_queue, y, left, right, status):
    point = point_of_intersection(left, right)
    if point is not None:
        if snd(point) < y:
            event_queue.insert(point, (status, (left, right)))


def sweep_intersections(segments):
    status = {
        "upper": 0,
        "intersection": 1,
        "lower": 2,
    }
    counter = 0
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
            print(event)
            memo[payload] = event
            status_queue.insert((event, payload), None)
            (left, right) = status_queue.neighbors((event, payload))
            if event == (61, 45):
                print(left, right)
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
            status_queue.insert((event, right), None)
            status_queue.insert((event, left), None)
            (far_left, _) = status_queue.neighbors((event, left))
            (_, far_right) = status_queue.neighbors((event, right))
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
    dupe = not len(points) == len(set(points))
    print("counter    : {}{}{}\nduplicates : {}{}{}{}".format(
        Terminal.bold,
        counter,
        Terminal.end,
        Terminal.bold,
        Terminal.red if dupe else Terminal.green,
        dupe,
        Terminal.end,
    ))
    return (segments, points)
