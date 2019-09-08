package bst

import (
    "fmt"
)

type Value interface{}

type Key interface {
    equal(Key) bool
    less(Key) bool
}

type KeyValue struct {
    Key   Key
    Value Value
}

type Node struct {
    Key   Key
    Value Value
    Left  *Node
    Right *Node
}

func (node *Node) Insert(key Key, value Value) error {
    if node == nil {
        return fmt.Errorf("(%v).Insert(%v, %v)", node, key, value)
    }
    switch {
    case key.equal(node.Key):
        node.Value = value
        return nil
    case key.less(node.Key):
        if node.Left == nil {
            node.Left = &Node{Key: key, Value: value}
            return nil
        }
        return node.Left.Insert(key, value)
    default:
        if node.Right == nil {
            node.Right = &Node{Key: key, Value: value}
            return nil
        }
        return node.Right.Insert(key, value)
    }
}

func (node *Node) Find(key Key) (Value, bool) {
    if node == nil {
        return nil, false
    }
    switch {
    case key.equal(node.Key):
        return node.Value, true
    case key.less(node.Key):
        return node.Left.Find(key)
    default:
        return node.Right.Find(key)
    }
}

func (node *Node) findMax(parent *Node) (*Node, *Node) {
    if node == nil {
        return nil, parent
    }
    if node.Right == nil {
        return node, parent
    }
    return node.Right.findMax(node)
}

func (node *Node) replaceNode(parent, replacement *Node) error {
    if node == nil {
        return fmt.Errorf(
            "(%v).replaceNode(%v, %v)",
            node,
            parent,
            replacement,
        )
    }
    if node == parent.Left {
        parent.Left = replacement
        return nil
    }
    parent.Right = replacement
    return nil
}

func (node *Node) Delete(key Key, parent *Node) error {
    if node == nil {
        return fmt.Errorf("(%v).Delete(%v, %v)", node, key, parent)
    }
    switch {
    case key.less(node.Key):
        return node.Left.Delete(key, node)
    case key.equal(node.Key):
        if node.Left == nil && node.Right == nil {
            node.replaceNode(parent, nil)
            return nil
        }
        if node.Left == nil {
            node.replaceNode(parent, node.Right)
            return nil
        }
        if node.Right == nil {
            node.replaceNode(parent, node.Left)
            return nil
        }
        replacement, replParent := node.Left.findMax(node)
        node.Key = replacement.Key
        node.Value = replacement.Value
        return replacement.Delete(replacement.Key, replParent)
    default:
        return node.Right.Delete(key, node)
    }
}

type Tree struct {
    Root  *Node
    Stack []KeyValue
}

func (tree *Tree) Insert(key Key, value Value) error {
    if tree.Root == nil {
        tree.Root = &Node{Key: key, Value: value}
        return nil
    }
    return tree.Root.Insert(key, value)
}

func (tree *Tree) Find(key Key) (Value, bool) {
    if tree.Root == nil {
        return nil, false
    }
    return tree.Root.Find(key)
}

func (tree *Tree) Delete(key Key) error {
    if tree.Root == nil {
        return fmt.Errorf("(%v).Delete(%v)", tree, key)
    }
    fakeParent := &Node{Right: tree.Root}
    if err := tree.Root.Delete(key, fakeParent); err != nil {
        return err
    }
    if fakeParent.Right == nil {
        tree.Root = nil
    }
    return nil
}

func (tree *Tree) Traverse(node *Node) {
    if node == nil {
        return
    }
    tree.Traverse(node.Left)
    tree.Stack = append(tree.Stack, KeyValue{node.Key, node.Value})
    tree.Traverse(node.Right)
}

func (tree *Tree) Collect() []KeyValue {
    tree.Stack = make([]KeyValue, 0)
    if tree.Root != nil {
        tree.Traverse(tree.Root)
    }
    return tree.Stack
}
