#!/usr/bin/env python

LEFT = "left"
RIGHT = "right"
VALUE = "value"


def leaf(value):
    return {
        LEFT: None,
        RIGHT: None,
        VALUE: value,
    }


def insert(tree, compare, leaf):
    if tree is None:
        tree = leaf
    else:
        if compare(tree[VALUE], leaf[VALUE]):
            if tree[RIGHT] is None:
                tree[RIGHT] = leaf
            else:
                insert(tree[RIGHT], compare, leaf)
        else:
            if tree[LEFT] is None:
                tree[LEFT] = leaf
            else:
                insert(tree[LEFT], compare, leaf)


def show(tree):
    margin = 5

    def f(tree, left, i):
        if tree:
            f(tree[LEFT], True, i + 1)
            if left:
                stem = "_/"
            else:
                stem = "\\_"
            print("{}{}".format(stem, tree[VALUE]).rjust(margin * i))
            f(tree[RIGHT], False, i + 1)

    if tree:
        f(tree[LEFT], True, 1)
        print("{}".format(tree[VALUE]))
        f(tree[RIGHT], False, 1)
