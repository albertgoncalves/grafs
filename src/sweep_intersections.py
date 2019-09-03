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
        (event, values) = event_queue.pop()
        (_, y) = event
        deletes = []
        for segment in values:
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


def status_lt(ab, cd):
    (u1, _) = upper_end(*ab)
    (u2, _) = upper_end(*cd)
    if u1 == u2:
        (l1, _) = lower_end(*ab)
        (l2, _) = lower_end(*cd)
        return l1 < l2
    else:
        return u1 < u2


def update_points(event_queue, y, left, right):
    point = point_of_intersection(left, right)
    intersection = "intersection"
    if point is not None:
        if snd(point) < y:
            event_queue.insert(point, (intersection, (left, right)))


def sweep_intersections(segments):
    upper = "upper"
    lower = "lower"
    counter = 0
    points = []
    table = {}
    event_queue = Tree(event_lt)
    status_queue = Tree(status_lt)
    for segment in segments:
        point = upper_end(*segment)
        event_queue.insert(point, (upper, segment))
        point = lower_end(*segment)
        event_queue.insert(point, (lower, segment))
    while not event_queue.empty():
        (event, values) = event_queue.pop()
        (_, y) = event
        for (label, payload) in values:
            if label == upper:
                status_queue.insert(payload, None)
                (left, right) = status_queue.neighbors(payload)
                if event == (87, 42):
                    print(left, right)
                    try:
                        print(table[left[0]])
                    except:
                        pass
                if left is not None:
                    (left_segment, _) = left
                    counter += 1
                    update_points(event_queue, y, left_segment, payload)
                    try:
                        counter += 1
                        left_segment = table[left_segment]
                        update_points(event_queue, y, left_segment, payload)
                    except KeyError:
                        pass
                if right is not None:
                    (right_segment, _) = right
                    counter += 1
                    update_points(event_queue, y, payload, right_segment)
                    try:
                        counter += 1
                        right_segment = table[right_segment]
                        update_points(event_queue, y, payload, right_segment)
                    except KeyError:
                        pass
            elif label == lower:
                status_queue.neighbors(payload)
                status_queue.delete(payload)
                if (left is not None) and (right is not None):
                    (left_segment, _) = left
                    (right_segment, _) = right
                    try:
                        left_segment = table[left_segment]
                    except KeyError:
                        pass
                    try:
                        right_segment = table[right_segment]
                    except KeyError:
                        pass
                    counter += 1
                    update_points(event_queue, y, left_segment, right_segment)
            else:
                points.append(event)
                (left_segment, right_segment) = payload
                table[left_segment] = right_segment
                table[right_segment] = left_segment
                (far_left, _) = status_queue.neighbors(left_segment)
                (_, far_right) = status_queue.neighbors(right_segment)
                # print(far_left, left_segment, right_segment, far_right)
                if far_left is not None:
                    (far_left_segment, _) = far_left
                    counter += 1
                    update_points(
                        event_queue,
                        y,
                        far_left_segment,
                        right_segment,
                    )
                    try:
                        counter += 1
                        far_left_segment = table[far_left_segment]
                        update_points(
                            event_queue,
                            y,
                            far_left_segment,
                            right_segment,
                        )
                    except KeyError:
                        pass
                    counter += 1
                    update_points(
                        event_queue,
                        y,
                        far_left_segment,
                        left_segment,
                    )
                    try:
                        counter += 1
                        far_left_segment = table[far_left_segment]
                        update_points(
                            event_queue,
                            y,
                            far_left_segment,
                            left_segment,
                        )
                    except KeyError:
                        pass
                if far_right is not None:
                    (far_right_segment, _) = far_right
                    counter += 1
                    update_points(
                        event_queue,
                        y,
                        left_segment,
                        far_right_segment,
                    )
                    try:
                        counter += 1
                        far_right_segment = table[far_right_segment]
                        update_points(
                            event_queue,
                            y,
                            left_segment,
                            far_right_segment,
                        )
                    except KeyError:
                        pass
                    counter += 1
                    update_points(
                        event_queue,
                        y,
                        right_segment,
                        far_right_segment,
                    )
                    try:
                        counter += 1
                        far_right_segment = table[far_right_segment]
                        update_points(
                            event_queue,
                            y,
                            right_segment,
                            far_right_segment,
                        )
                    except KeyError:
                        pass
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
