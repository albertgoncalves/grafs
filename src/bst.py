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

    def neighbors(self, key):
        (node, parent) = self.find(key, None)
        if (node.left is not None) and (node.right is not None):
            (left, _) = node.left.first(node)
            (right, _) = node.right.last(node)
            return (left, right)
        elif (parent is not None) and (node.left is None) \
                and (node.right is None):
            (_, grandparent) = self.find(parent.key, None)
            if grandparent is not None:
                if self.less_than(parent.key, grandparent.key):
                    return (parent, grandparent)
                else:
                    return (grandparent, parent)
            else:
                return (None, None)
        elif (parent is not None) and (node.left is not None) \
                and (node.right is None):
            (left, _) = node.left.first(node)
            if self.less_than(left.key, key) \
                    and self.less_than(key, parent.key):
                return (left, parent)
            else:
                (_, grandparent) = self.find(parent.key, None)
                if (grandparent is not None) \
                        and self.less_than(left.key, key) \
                        and self.less_than(key, grandparent.key):
                    return (left, grandparent)
                else:
                    (None, None)
        elif (parent is not None) and (node.left is None) \
                and (node.right is not None):
            (right, _) = node.right.last(node)
            if self.less_than(parent.key, key) \
                    and self.less_than(key, right.key):
                return (parent, right)
            else:
                (_, grandparent) = self.find(parent.key, None)
                if (grandparent is not None) \
                        and self.less_than(grandparent.key, key) \
                        and self.less_than(key, right.key):
                    return (grandparent, right)
                else:
                    if self.less_than(key, right.key) \
                            and self.less_than(key, parent.key):
                        if self.left is not None:
                            (left, _) = self.left.last(self)
                            if (left is not None) and (left.key != key):
                                return (left, right)
                        return (None, right)
                    else:
                        return (None, None)
        else:
            return (None, None)

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
            (node, parent) = self.root.first(None)
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

    def neighbors(self, key):
        if self.root is not None:
            (left, right) = self.root.neighbors(key)
            if (left is not None) and (right is not None):
                return (left.key, right.key)
            elif left is not None:
                return (left.key, None)
            elif right is not None:
                return (None, right.key)
        return (None, None)

    def __str__(self):
        if self.root is None:
            return str(None)
        else:
            return "\n".join(map(str, self.iter()))
