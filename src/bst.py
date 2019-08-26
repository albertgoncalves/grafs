#!/usr/bin/env python


class BST:
    def __init__(self, compare):
        self.left = None
        self.right = None
        self.value = None
        self.compare = compare

    def __str__(self):
        stack = []

        def closure(self):
            if self.left is not None:
                closure(self.left)
            stack.append("{}".format(self.value))
            if self.right is not None:
                closure(self.right)

        closure(self)
        return "\n".join(map(
            lambda ab: "{}\t{}".format(ab[0], ab[1]),
            zip(range(len(stack)), stack),
        ))

    def push(self, value):
        if self.value is None:
            self.value = value
        else:
            if self.compare(self.value, value):
                if self.left is None:
                    self.left = BST(self.compare)
                self.left.push(value)
            else:
                if self.right is None:
                    self.right = BST(self.compare)
                self.right.push(value)

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
        if self.value is not None:
            return self.__lookup(value, None)
        else:
            return (None, None)

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
                    self.value = None
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

    def __pop(self, parent):
        if self.left is not None:
            return self.left.__pop(self)
        else:
            value = self.value
            if parent is not None:
                parent.delete(value)
            else:
                self.delete(value)
            return value

    def pop(self):
        return self.__pop(None)

    def empty(self):
        return self.value is None
