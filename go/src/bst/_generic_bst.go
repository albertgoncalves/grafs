package bst

import (
    "fmt"
    "github.com/cheekybits/genny/generic"
)

type KeyType generic.Type

type ValueType generic.Type

type KeyTypeValueTypeNode struct {
    Key      KeyType
    Value    ValueType
    Fallback ValueType
    Equal    func(KeyType, KeyType) bool
    Less     func(KeyType, KeyType) bool
    Left     *KeyTypeValueTypeNode
    Right    *KeyTypeValueTypeNode
}

func (node *KeyTypeValueTypeNode) Insert(key KeyType, value ValueType) error {
    if node == nil {
        return fmt.Errorf("(%v).Insert(%v, %v)", node, key, value)
    } else if node.Equal(key, node.Key) {
        node.Value = value
        return nil
    } else if node.Less(key, node.Key) {
        if node.Left == nil {
            node.Left = &KeyTypeValueTypeNode{
                Key:      key,
                Value:    value,
                Fallback: node.Fallback,
                Equal:    node.Equal,
                Less:     node.Less,
            }
            return nil
        }
        return node.Left.Insert(key, value)
    } else if node.Right == nil {
        node.Right = &KeyTypeValueTypeNode{
            Key:      key,
            Value:    value,
            Fallback: node.Fallback,
            Equal:    node.Equal,
            Less:     node.Less,
        }
        return nil
    } else {
        return node.Right.Insert(key, value)
    }
}

func (node *KeyTypeValueTypeNode) Find(
    key KeyType,
    fallback ValueType,
) (ValueType, error) {
    if node == nil {
        return fallback, fmt.Errorf("(%v).Find(%v)", node, key)
    } else if node.Equal(key, node.Key) {
        return node.Value, nil
    } else if node.Less(key, node.Key) {
        return node.Left.Find(key, node.Fallback)
    } else {
        return node.Right.Find(key, node.Fallback)
    }
}

func (node *KeyTypeValueTypeNode) last(parent *KeyTypeValueTypeNode) (
    *KeyTypeValueTypeNode, *KeyTypeValueTypeNode, error) {
    if node == nil {
        return nil, nil, fmt.Errorf("(%v).last(%v)", node, parent)
    } else if node.Left == nil {
        return node, parent, nil
    } else {
        return node.Left.last(node)
    }
}

func (node *KeyTypeValueTypeNode) first(parent *KeyTypeValueTypeNode) (
    *KeyTypeValueTypeNode, *KeyTypeValueTypeNode, error) {
    if node == nil {
        return nil, nil, fmt.Errorf("(%v).first(%v)", node, parent)
    } else if node.Right == nil {
        return node, parent, nil
    } else {
        return node.Right.first(node)
    }
}

func (node *KeyTypeValueTypeNode) swap(
    parent,
    replacement *KeyTypeValueTypeNode,
) error {
    if node == nil {
        return fmt.Errorf("(%v).swap(%v, %v)", node, parent, replacement)
    } else if node == parent.Left {
        parent.Left = replacement
        return nil
    } else {
        parent.Right = replacement
        return nil
    }
}

func (node *KeyTypeValueTypeNode) Delete(
    key KeyType,
    parent *KeyTypeValueTypeNode,
) error {
    if node == nil {
        return fmt.Errorf("(%v).Delete(%v, %v)", node, key, parent)
    } else if node.Equal(key, node.Key) {
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
    } else if node.Less(key, node.Key) {
        return node.Left.Delete(key, node)
    } else {
        return node.Right.Delete(key, node)
    }
}

func (node *KeyTypeValueTypeNode) Neighbors(
    key KeyType,
    left,
    right *KeyTypeValueTypeNode,
) (*KeyTypeValueTypeNode, *KeyTypeValueTypeNode, error) {
    if node == nil {
        return nil, nil, fmt.Errorf("(%v).Neighbors(%v)", node, key)
    } else if node.Equal(key, node.Key) {
        var localLeft *KeyTypeValueTypeNode = nil
        var localRight *KeyTypeValueTypeNode = nil
        var err error = nil
        if (node.Left != nil) {
            localLeft, _, err = node.Left.first(node)
            if err != nil {
                return nil, nil, err
            }
        }
        if (node.Right != nil) {
            localRight, _, err = node.Right.last(node)
            if err != nil {
                return nil, nil, err
            }
        }
        if (localLeft != nil) && (localRight != nil) {
            return localLeft, localRight, nil
        } else if localLeft != nil {
            return localLeft, right, nil
        } else if localRight != nil {
            return left, localRight, nil
        } else {
            return left, right, nil
        }
    } else if node.Less(key, node.Key) {
        return node.Left.Neighbors(key, left, node)
    } else {
        return node.Right.Neighbors(key, node, right)
    }
}

type KeyTypeValueTypeTuple struct {
    Key   KeyType
    Value ValueType
}

type KeyTypeValueTypeTree struct {
    Root     *KeyTypeValueTypeNode
    Stack    []KeyTypeValueTypeTuple
    Fallback ValueType
    Equal    func(KeyType, KeyType) bool
    Less     func(KeyType, KeyType) bool
}

func (tree *KeyTypeValueTypeTree) Insert(key KeyType, value ValueType) error {
    if tree.Root == nil {
        tree.Root = &KeyTypeValueTypeNode{
            Key:      key,
            Value:    value,
            Fallback: tree.Fallback,
            Equal:    tree.Equal,
            Less:     tree.Less,
        }
        return nil
    } else {
        return tree.Root.Insert(key, value)
    }
}

func (tree *KeyTypeValueTypeTree) Find(
    key KeyType,
    fallback ValueType,
) (ValueType, error) {
    if tree.Root == nil {
        return fallback, fmt.Errorf("(%v).Find(%v)", tree, key)
    } else {
        value, err := tree.Root.Find(key, tree.Fallback)
        if err != nil {
            return tree.Fallback, err
        }
        return value, nil
    }
}

func (tree *KeyTypeValueTypeTree) Pop() (KeyType, ValueType, error) {
    if tree.Root == nil {
        return KeyType{}, tree.Fallback, fmt.Errorf("(%v).Pop()", tree)
    } else {
        node, parent, err := tree.Root.Right.first(tree.Root)
        if err != nil {
            key := tree.Root.Key
            value := tree.Root.Value
            tree.Root = tree.Root.Left
            return key, value, nil
        }
        key := node.Key
        value := node.Value
        node.Delete(node.Key, parent)
        return key, value, nil
    }
}

func (tree *KeyTypeValueTypeTree) Empty() bool {
    return tree.Root == nil
}

func (tree *KeyTypeValueTypeTree) Delete(key KeyType) error {
    if tree.Root == nil {
        return fmt.Errorf("(%v).Delete(%v)", tree, key)
    } else {
        pseudoParent := &KeyTypeValueTypeNode{Right: tree.Root}
        if err := tree.Root.Delete(key, pseudoParent); err != nil {
            return err
        }
        tree.Root = pseudoParent.Right
        return nil
    }
}

func (tree *KeyTypeValueTypeTree) Neighbors(key KeyType) (
    *KeyTypeValueTypeNode,
    *KeyTypeValueTypeNode,
    error,
) {
    if tree.Root == nil {
        return nil, nil, fmt.Errorf("(%v).Neighbors(%v)", tree, key)
    } else {
        left, right, err := tree.Root.Neighbors(key, nil, nil)
        if err != nil {
            return nil, nil, err
        }
        return left, right, nil
    }
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
