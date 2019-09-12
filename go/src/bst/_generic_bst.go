package bst

import (
    "fmt"
    "github.com/cheekybits/genny/generic"
)

type KeyType generic.Type

type ValueType generic.Type

type KeyTypeValueTypeNode struct {
    Key   KeyType
    Value ValueType
    Equal func(KeyType, KeyType) bool
    Less  func(KeyType, KeyType) bool
    Left  *KeyTypeValueTypeNode
    Right *KeyTypeValueTypeNode
}

func (node *KeyTypeValueTypeNode) Insert(key KeyType, value ValueType) error {
    if node == nil {
        return fmt.Errorf("(%v).Insert(%v, %v)", node, key, value)
    }
    if node.Equal(key, node.Key) {
        node.Value = value
        return nil
    }
    if node.Less(key, node.Key) {
        if node.Left == nil {
            node.Left = &KeyTypeValueTypeNode{
                Key:   key,
                Value: value,
                Equal: node.Equal,
                Less:  node.Less,
            }
            return nil
        }
        return node.Left.Insert(key, value)
    }
    if node.Right == nil {
        node.Right = &KeyTypeValueTypeNode{
            Key:   key,
            Value: value,
            Equal: node.Equal,
            Less:  node.Less,
        }
        return nil
    }
    return node.Right.Insert(key, value)
}

func (node *KeyTypeValueTypeNode) Find(key KeyType) (ValueType, error) {
    if node == nil {
        return ValueType{}, fmt.Errorf("(%v).Find(%v)", node, key)
    }
    if node.Equal(key, node.Key) {
        return node.Value, nil
    }
    if node.Less(key, node.Key) {
        return node.Left.Find(key)
    }
    return node.Right.Find(key)
}

func (node *KeyTypeValueTypeNode) last(parent *KeyTypeValueTypeNode) (
    *KeyTypeValueTypeNode, *KeyTypeValueTypeNode, error) {
    if node == nil {
        return nil, nil, fmt.Errorf("(%v).last(%v)", node, parent)
    }
    if node.Left == nil {
        return node, parent, nil
    }
    return node.Left.last(node)
}

func (node *KeyTypeValueTypeNode) first(parent *KeyTypeValueTypeNode) (
    *KeyTypeValueTypeNode, *KeyTypeValueTypeNode, error) {
    if node == nil {
        return nil, nil, fmt.Errorf("(%v).first(%v)", node, parent)
    }
    if node.Right == nil {
        return node, parent, nil
    }
    return node.Right.first(node)
}

func (node *KeyTypeValueTypeNode) swap(
    parent,
    replacement *KeyTypeValueTypeNode,
) error {
    if node == nil {
        return fmt.Errorf("(%v).swap(%v, %v)", node, parent, replacement)
    }
    if node == parent.Left {
        parent.Left = replacement
        return nil
    }
    parent.Right = replacement
    return nil
}

func (node *KeyTypeValueTypeNode) Delete(
    key KeyType,
    parent *KeyTypeValueTypeNode,
) error {
    if node == nil {
        return fmt.Errorf("(%v).Delete(%v, %v)", node, key, parent)
    }
    if node.Equal(key, node.Key) {
        if (node.Left == nil) && (node.Right == nil) {
            node.swap(parent, nil)
            return nil
        }
        if node.Left == nil {
            node.swap(parent, node.Right)
            return nil
        }
        if node.Right == nil {
            node.swap(parent, node.Left)
            return nil
        }
        replacement, replParent, err := node.Left.first(node)
        if err != nil {
            return err
        }
        node.Key = replacement.Key
        node.Value = replacement.Value
        node.Equal = replacement.Equal
        node.Less = replacement.Less
        return replacement.Delete(replacement.Key, replParent)
    }
    if node.Less(key, node.Key) {
        return node.Left.Delete(key, node)
    }
    return node.Right.Delete(key, node)
}

type KeyTypeValueTypeTuple struct {
    Key   KeyType
    Value ValueType
}

type KeyTypeValueTypeTree struct {
    Root  *KeyTypeValueTypeNode
    Stack []KeyTypeValueTypeTuple
    Equal func(KeyType, KeyType) bool
    Less  func(KeyType, KeyType) bool
}

func (tree *KeyTypeValueTypeTree) Insert(key KeyType, value ValueType) error {
    if tree.Root == nil {
        tree.Root = &KeyTypeValueTypeNode{
            Key:   key,
            Value: value,
            Equal: tree.Equal,
            Less:  tree.Less,
        }
        return nil
    }
    return tree.Root.Insert(key, value)
}

func (tree *KeyTypeValueTypeTree) Find(key KeyType) (ValueType, error) {
    if tree.Root == nil {
        return ValueType{}, fmt.Errorf("(%v).Find(%v)", tree, key)
    }
    value, err := tree.Root.Find(key)
    if err != nil {
        return ValueType{}, err
    }
    return value, nil
}

func (tree *KeyTypeValueTypeTree) Pop() (KeyType, ValueType, error) {
    if tree.Root == nil {
        return KeyType{}, ValueType{}, fmt.Errorf("(%v).Pop()", tree)
    }
    node, parent, err := tree.Root.Right.first(tree.Root)
    if err != nil {
        key := tree.Root.Key
        value := tree.Root.Value
        tree.Root = nil
        return key, value, nil
    }
    key := node.Key
    value := node.Value
    node.Delete(node.Key, parent)
    return key, value, nil
}

func (tree *KeyTypeValueTypeTree) Empty() bool {
    return tree.Root == nil
}

func (tree *KeyTypeValueTypeTree) Delete(key KeyType) error {
    if tree.Root == nil {
        return fmt.Errorf("(%v).Delete(%v)", tree, key)
    }
    pseudoParent := &KeyTypeValueTypeNode{Right: tree.Root}
    if err := tree.Root.Delete(key, pseudoParent); err != nil {
        return err
    }
    tree.Root = pseudoParent.Right
    return nil
}

func (tree *KeyTypeValueTypeTree) traverse(node *KeyTypeValueTypeNode) {
    if node != nil {
        tree.traverse(node.Left)
        tree.Stack = append(
            tree.Stack,
            KeyTypeValueTypeTuple{node.Key, node.Value},
        )
        tree.traverse(node.Right)
    }
}

func (tree *KeyTypeValueTypeTree) Collect() []KeyTypeValueTypeTuple {
    tree.Stack = make([]KeyTypeValueTypeTuple, 0)
    if tree.Root != nil {
        tree.traverse(tree.Root)
    }
    return tree.Stack
}
