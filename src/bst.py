#!/usr/bin/env python

# based on https://github.com/AppliedGo/bintree/blob/master/bintree.go


class Node:
    def __init__(self, key, value, less_than):
        self.key = key
        self.values = [value]
        self.right = None   # higher
        self.left = None    # lower
        self.less_than = less_than

    def insert(self, key, value):
        if self.key == key:
            if value is not None:
                self.values.append(value)
        elif self.less_than(key, self.key):
            if self.left is None:
                self.left = Node(key, value, self.less_than)
            else:
                self.left.insert(key, value)
        else:
            if self.right is None:
                self.right = Node(key, value, self.less_than)
            else:
                self.right.insert(key, value)

    def find(self, key, parent):
        if (self.key is None) or (self.key == key):
            return (self, parent)
        elif self.less_than(key, self.key):
            return self.left.find(key, self)
        else:
            return self.right.find(key, self)

    def first(self, parent):
        if self.right is None:
            return (self, parent)
        else:
            return self.right.first(self)

    def last(self, parent):
        if self.left is None:
            return (self, parent)
        else:
            return self.left.last(self)

    def local_swap(self, replacement, parent):
        # parent => Node()
        if hasattr(parent, "left"):
            if self == parent.left:
                parent.left = replacement
            elif self == parent.right:
                parent.right = replacement
        # parent => Tree()
        else:
            parent.root = replacement

    def delete(self, key, parent):
        if self.key == key:
            if (self.left is None) and (self.right is None):
                self.local_swap(None, parent)
            elif self.left is None:
                self.local_swap(self.right, parent)
            elif self.right is None:
                self.local_swap(self.left, parent)
            else:
                (replacement, parent) = self.left.first(self)
                self.key = replacement.key
                self.values = replacement.values
                replacement.delete(replacement.key, parent)
        elif self.less_than(key, self.key):
            self.left.delete(key, self)
        else:
            self.right.delete(key, self)


class Tree:
    def __init__(self, less_than):
        self.root = None
        self.less_than = less_than

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value, self.less_than)
        else:
            self.root.insert(key, value)

    def delete(self, key):
        if self.root is not None:
            self.root.delete(key, self)

    def first(self):
        if self.root is None:
            return None
        else:
            (node, _) = self.root.first(self)
            return (node.key, node.values)

    def last(self):
        if self.root is None:
            return None
        else:
            (node, _) = self.root.last(self)
            return (node.key, node.values)

    def pop(self):
        if self.root is None:
            return None
        else:
            (node, parent) = self.root.first(self)
            node.delete(node.key, parent)
            return (node.key, node.values)

    def empty(self):
        return self.root is None

    def iter(self):
        if self.root is not None:
            stack = []
            node = self.root
            while (stack != []) or (node is not None):
                if node is not None:
                    stack.append(node)
                    node = node.right
                else:
                    node = stack.pop()
                    yield (node.key, node.values)
                    node = node.left

    def swap_values(self, key_a, key_b):
        if self.root is not None:
            (node_a, _) = self.root.find(key_a, None)
            (node_b, _) = self.root.find(key_b, None)
            tmp_values = node_a.values
            node_a.values = node_b.values
            node_b.values = tmp_values

    def __neighbors(self, key):
        # tree is iterated from right to left
        key_right = None
        right = None
        nodes = self.iter()
        for (key_next, _) in nodes:
            if key_next == key:
                if key_right is None:
                    right = None
                else:
                    (right, _) = self.root.find(key_right, None)
                break
            else:
                key_right = key_next
        try:
            (key_left, _) = next(nodes)
            (left, _) = self.root.find(key_left, None)
        except StopIteration:
            left = None
        return (left, right)

    def neighbors(self, key):
        if self.root is not None:
            (left, right) = self.__neighbors(key)
            if (left is not None) and (right is not None):
                return ((left.key, left.values), (right.key, right.values))
            elif left is not None:
                return ((left.key, left.values), None)
            elif right is not None:
                return (None, (right.key, right.values))
        return (None, None)

    def __str__(self):
        if self.root is None:
            return str(None)
        else:
            return "\n".join(map(str, self.iter()))
