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

    def next_left(self, parent):
        if self.left is not None:
            (node, _) = self.left.first(self)
            return node
        elif parent is not None:
            if self != parent.left:
                if parent.left is None:
                    return parent
                else:
                    (node, _) = parent.left.first(parent)
                    return node
            else:
                return None
        else:
            return None

    def next_right(self, parent):
        if self.right is not None:
            (node, _) = self.right.last(self)
            return node
        elif parent is not None:
            if self != parent.right:
                if parent.right is None:
                    return parent
                else:
                    (node, _) = parent.right.last(parent)
                    return node
            else:
                return None
        else:
            return None

    def local_swap(self, replacement, parent):
        # parent => Node()
        if hasattr(parent, "left"):
            if self == parent.left:
                parent.left = replacement
            else:
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
            return self.root.first(self)

    def last(self):
        if self.root is None:
            return None
        else:
            return self.root.last(self)

    def pop(self):
        if self.root is None:
            return None
        else:
            (node, parent) = self.first()
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

    def __str__(self):
        if self.root is None:
            return str(None)
        else:
            return "\n".join(map(str, self.iter()))
