#!/usr/bin/env python

from operator import lt

from bst import Tree
from geom import ccw, intersect, point_of_intersection


def test_ccw():
    a = (0, 0)
    b = (1, 0)
    c = (1, 1)
    assert ccw(a, b, c)
    assert not ccw(a, c, b)


def test_interset():
    ab = ((0, 0), (2, 2))
    cd = ((1, 0), (1, 3))
    ef = ((1, 0), (2, 0))
    assert intersect(ab, cd)
    assert not intersect(ab, ef)


def test_point_of_intersection():
    ab = ((0, 0), (2, 2))
    cd = ((1, 0), (1, 3))
    ef = ((1, 0), (2, 0))
    assert point_of_intersection(ab, cd) == (1, 1)
    assert point_of_intersection(ab, ef) is None


class TestTree:
    xs = [1, 5, 4, 3, 7, 6, 8, 0, 2]

    def seed_none(self, xs):
        tree = Tree(lt)
        for x in xs:
            tree.insert(x, None)
        return tree

    def iter_none(self, xs):
        return list(map(lambda x: (x, [None]), sorted(xs)))[::-1]

    def test_insert(self):
        assert list(self.seed_none(self.xs).iter()) == self.iter_none(self.xs)

    def test_remove(self):
        tree = self.seed_none(self.xs)
        tree.delete(1)
        tree.delete(5)
        assert list(tree.iter()) == self.iter_none(self.xs[2:])

    def test_first(self):
        assert self.seed_none(self.xs).first() == (8, [None])

    def test_last(self):
        assert self.seed_none(self.xs).last() == (0, [None])

    def test_empty(self):
        tree = Tree(lt)
        assert tree.empty()
        assert not self.seed_none(self.xs).empty()

    def test_pop(self):
        tree = self.seed_none(self.xs)
        assert tree.pop() == (8, [None])
        assert tree.first() == (7, [None])
        assert tree.pop() == (7, [None])
        assert tree.first() == (6, [None])

    def test_swap_values(self):
        tree = Tree(lt)
        for (k, v) in [(0, "0"), (2, "2"), (2, "2"), (1, "1")]:
            tree.insert(k, v)
        tree.swap_values(0, 2)
        assert tree.first() == (2, ["0"])
        assert tree.last() == (0, ["2", "2"])
