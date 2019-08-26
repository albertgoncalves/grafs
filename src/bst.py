#!/usr/bin/env python


class BST:
    def __init__(self, compare):
        self.left = None
        self.right = None
        self.key = None
        self.values = []
        self.compare = compare

    def __str__(self):
        stack = []

        def closure(self):
            if self.left is not None:
                closure(self.left)
            stack.append("{:10}\t[ {} ]".format(
                str(self.key),
                ", ".join(map(str, self.values)),
            ))
            if self.right is not None:
                closure(self.right)

        closure(self)
        return "\n".join(map(
            lambda ab: "{}\t{}".format(ab[0], ab[1]),
            zip(range(len(stack)), stack),
        ))

    def push(self, key, value):
        if self.key is None:
            self.key = key
            self.values.append(value)
        elif self.key == key:
            self.values.append(value)
        elif self.compare(self.key, key):
            if self.left is None:
                self.left = BST(self.compare)
            self.left.push(key, value)
        else:
            if self.right is None:
                self.right = BST(self.compare)
            self.right.push(key, value)

    def __lookup(self, key, parent):
        if self.key == key:
            return (self, parent)
        elif self.compare(self.key, key):
            if self.left is None:
                return (None, None)
            else:
                return self.left.__lookup(key, self)
        else:
            if self.right is None:
                return (None, None)
            else:
                return self.right.__lookup(key, self)

    def lookup(self, key):
        if self.key is not None:
            return self.__lookup(key, None)
        else:
            return (None, None)

    def __count(self):
        n = 0
        if self.left is not None:
            n += 1
        if self.right is not None:
            n += 1
        return n

    def delete(self, key):
        (node, parent) = self.__lookup(key, None)
        if node is not None:
            n = node.__count()
            if n == 0:
                if parent is not None:
                    if parent.left is node:
                        parent.left = None
                    else:
                        parent.right = None
                else:
                    self.key = None
                    self.values = []
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
                    self.key = n.key
                    self.values = n.values
            else:
                parent = node
                successor = node.right
                while successor.left is not None:
                    parent = successor
                    successor = successor.left
                node.key = successor.key
                node.values = successor.values
                if parent.left == successor:
                    parent.left = successor.right
                else:
                    parent.right = successor.right

    def __pop(self, parent):
        if self.left is not None:
            return self.left.__pop(self)
        else:
            key = self.key
            values = self.values
            if parent is not None:
                parent.delete(key)
            else:
                self.delete(key)
            return (key, values)

    def pop(self):
        return self.__pop(None)

    def empty(self):
        return self.key is None
