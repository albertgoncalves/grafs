#!/usr/bin/env python


class Node:
    def __init__(self, key, value, lt):
        self.lt = lt
        self.key = key
        self.value = value
        self.right = None  # higher
        self.left = None   # lower

    def insert(self, key, value):
        if self.key == key:
            self.value = value
        elif self.lt(key, self.key):
            if self.left is None:
                self.left = Node(key, value, self.lt)
            else:
                self.left.insert(key, value)
        else:
            if self.right is None:
                self.right = Node(key, value, self.lt)
            else:
                self.right.insert(key, value)

    def find(self, key, parent):
        if (self.key is None) or (self.key == key):
            return (self, parent)
        elif self.lt(key, self.key):
            return self.left.find(key, self)
        else:
            return self.right.find(key, self)

    def neighbors(self, key, left, right):
        if (self.key is None) or (self.key == key):
            if self.left is not None:
                (local_left, _) = self.left.first(self)
            else:
                local_left = None
            if self.right is not None:
                (local_right, _) = self.right.last(self)
            else:
                local_right = None
            if (local_left is not None) and (local_right is not None):
                return (local_left, local_right)
            elif local_left is not None:
                return (local_left, right)
            elif local_right is not None:
                return (left, local_right)
            else:
                return (left, right)
        elif self.lt(key, self.key):
            return self.left.neighbors(key, left, self)
        else:
            return self.right.neighbors(key, self, right)

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
        # parent Node()
        if hasattr(parent, "left"):
            if self == parent.left:
                parent.left = replacement
            elif self == parent.right:
                parent.right = replacement
        # parent Tree()
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
                self.value = replacement.value
                replacement.delete(replacement.key, parent)
        elif self.lt(key, self.key):
            self.left.delete(key, self)
        else:
            self.right.delete(key, self)


class Tree:
    def __init__(self, lt):
        self.lt = lt
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value, self.lt)
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
            return (node.key, node.value)

    def last(self):
        if self.root is None:
            return None
        else:
            (node, _) = self.root.last(self)
            return (node.key, node.value)

    def pop(self):
        if self.root is None:
            return None
        else:
            (node, parent) = self.root.first(self)
            node.delete(node.key, parent)
            return (node.key, node.value)

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
                    yield (node.key, node.value)
                    node = node.left

    def find(self, key):
        if self.root is not None:
            (node, _) = self.root.find(key, None)
            if node is not None:
                return (node.key, node.value)
            else:
                return None

    def neighbors(self, key):
        if self.root is not None:
            (left, right) = self.root.neighbors(key, None, None)
            if (left is not None) and (right is not None):
                return ((left.key, left.value), (right.key, right.value))
            elif left is not None:
                return ((left.key, left.value), None)
            elif right is not None:
                return (None, (right.key, right.value))
            else:
                return (None, None)

    def __str__(self):
        if self.root is None:
            return str(None)
        else:
            return "\n".join(map(str, self.iter()))
