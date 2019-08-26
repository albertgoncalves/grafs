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
        return "BST\n===\n{}\n".format("\n".join(stack))

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

    def __lookup(self, value, parent):
        if self.value == value:
            return (self, parent)
        elif self.compare(self.value, value):
            if self.left is None:
                return (None, None)
            else:
                return self.left.__lookup(value, self)
        else:
            if self.right is None:
                return (None, None)
            else:
                return self.right.__lookup(value, self)

    def lookup(self, value):
        return self.__lookup(value, None)

    def __count(self):
        n = 0
        if self.left is not None:
            n += 1
        if self.right is not None:
            n += 1
        return n

    def delete(self, value):
        (node, parent) = self.__lookup(value, None)
        if node is not None:
            n = node.__count()
            if n == 0:
                if parent is not None:
                    if parent.left is node:
                        parent.left = None
                    else:
                        parent.right = None
                else:
                    self = None
            elif n == 1:
                if node.left is not None:
                    n = node.left
                else:
                    n = node.right
                if parent is not None:
                    if parent.left is node:
                        parent.left = n
                    else:
                        parent.right = n
                else:
                    self.left = n.left
                    self.right = n.right
                    self.value = n.value
            else:
                parent = node
                successor = node.right
                while successor.left is not None:
                    parent = successor
                    successor = successor.left
                node.value = successor.value
                if parent.left == successor:
                    parent.left = successor.right
                else:
                    parent.right = successor.right
