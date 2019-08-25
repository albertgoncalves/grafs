#!/usr/bin/env python


class BST:
    def __init__(self, compare, value):
        self.left = None
        self.right = None
        self.value = value
        self.compare = compare

    def __str__(self):
        margin = 4
        stack = []

        def closure(self, flag, i):
            if self.left is not None:
                closure(self.left, True, i + 1)
            stem = "_/" if flag else "\\_"
            stack.append((" {}{}".format(stem, self.value).rjust(margin * i)))
            if self.right is not None:
                closure(self.right, False, i + 1)

        closure(self, True, 1)
        return "\n{}\n".format("\n".join(stack))

    def insert(self, value):
        if self.compare(self.value, value):
            if self.left is None:
                self.left = BST(self.compare, value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BST(self.compare, value)
            else:
                self.right.insert(value)

    def lookup(self, value):
        if self.value == value:
            return self
        elif self.compare(self.value, value):
            if self.left is None:
                return None
            else:
                return self.left.lookup(value)
        else:
            if self.right is None:
                return None
            else:
                return self.right.lookup(value)
