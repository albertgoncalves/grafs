package bst

import (
    "fmt"
)

type Value interface{}

type Key interface {
    equal(Key) (bool, error)
    less(Key) (bool, error)
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
    if result, err := key.equal(node.Key); result && (err == nil) {
        node.Value = value
        return nil
    } else if err != nil {
        return err
    }
    if result, err := key.less(node.Key); result && (err == nil) {
        if node.Left == nil {
            node.Left = &Node{Key: key, Value: value}
            return nil
        }
        return node.Left.Insert(key, value)
    } else if err != nil {
        return fmt.Errorf("(%v).Insert(%v, %v)", node, key, value)
    }
    if node.Right == nil {
        node.Right = &Node{Key: key, Value: value}
        return nil
    }
    return node.Right.Insert(key, value)
}

func (node *Node) Find(key Key) (Value, error) {
    if node == nil {
        return nil, fmt.Errorf("(%v).Find(%v)", node, key)
    }
    if result, err := key.equal(node.Key); result && (err == nil) {
        return node.Value, nil
    } else if err != nil {
        return node.Value, err
    }
    if result, err := key.less(node.Key); result && (err == nil) {
        return node.Left.Find(key)
    } else if err != nil {
        return node.Value, err
    }
    return node.Right.Find(key)
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
    if result, err := key.less(node.Key); result && (err == nil) {
        return node.Left.Delete(key, node)
    } else if err != nil {
        return err
    }
    if result, err := key.equal(node.Key); result && (err == nil) {
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
    } else if err != nil {
        return err
    }
    return node.Right.Delete(key, node)
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

func (tree *Tree) Find(key Key) (Value, error) {
    if tree.Root == nil {
        return nil, fmt.Errorf("(%v).Find(%v)", tree, key)
    }
    value, err := tree.Root.Find(key)
    if err == nil {
        return value, nil
    }
    return nil, err
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
    if node != nil {
        tree.Traverse(node.Left)
        tree.Stack = append(tree.Stack, KeyValue{node.Key, node.Value})
        tree.Traverse(node.Right)
    }
}

func (tree *Tree) Collect() []KeyValue {
    tree.Stack = make([]KeyValue, 0)
    if tree.Root != nil {
        tree.Traverse(tree.Root)
    }
    return tree.Stack
}
