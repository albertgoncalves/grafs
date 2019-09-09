package bst

import (
    "fmt"
    "testing"
)

type PairKey struct {
    X float64
    Y float64
}

func (a PairKey) equal(b Key) (bool, error) {
    switch b := b.(type) {
    case PairKey:
        return (a.X == b.X) && (a.Y == b.Y), nil
    default:
        return false, fmt.Errorf("(%v).equal(%v)", a, b)
    }
}

func (a PairKey) less(b Key) (bool, error) {
    switch b := b.(type) {
    case PairKey:
        if a.X == b.X {
            return a.Y < b.Y, nil
        }
        return a.X < b.X, nil
    default:
        return false, fmt.Errorf("(%v).less(%v)", a, b)
    }
}

func compareKeyValues(a, b []KeyValue) bool {
    if len(a) != len(b) {
        return false
    }
    for i := range a {
        if a[i] != b[i] {
            return false
        }
    }
    return true
}

var items = []KeyValue{
    {PairKey{0.0, 0.0}, "a"},
    {PairKey{1.0, 0.0}, "b"},
    {PairKey{2.0, 0.0}, "c"},
    {PairKey{2.0, 1.0}, "d"},
}

func initTree() *Tree {
    tree := &Tree{}
    for _, item := range items {
        tree.Insert(item.Key, item.Value)
    }
    return tree
}

func TestInsert(t *testing.T) {
    tree := initTree()
    if !compareKeyValues(tree.Collect(), items) {
        t.Error("tree.Insert(...)")
    }
    if compareKeyValues(tree.Collect(), []KeyValue{
        items[0],
        items[1],
        items[3],
        items[2],
    }) {
        t.Error("tree.Insert(...)")
    }
}

func TestFind(t *testing.T) {
    tree := initTree()
    for i := range items {
        if value, err := tree.Find(items[i].Key); (value != items[i].Value) ||
            (err != nil) {
            t.Error("tree.Find(...)")
            break
        }
    }
    if _, err := tree.Find(PairKey{3.0, 0.0}); err == nil {
        t.Error("tree.Find(...)")
    }
}

func deletePipeline(t *testing.T, key Key, remainingItems []KeyValue) {
    tree := initTree()
    if err := tree.Delete(key); err != nil {
        t.Error("tree.Delete(...)")
    }
    if !compareKeyValues(tree.Collect(), remainingItems) {
        t.Error("tree.Delete(...)")
    }
}

func TestDelete(t *testing.T) {
    deletePipeline(t, items[0].Key, []KeyValue{
        items[1],
        items[2],
        items[3],
    })
    deletePipeline(t, items[1].Key, []KeyValue{
        items[0],
        items[2],
        items[3],
    })
    deletePipeline(t, items[2].Key, []KeyValue{
        items[0],
        items[1],
        items[3],
    })
    deletePipeline(t, items[3].Key, []KeyValue{
        items[0],
        items[1],
        items[2],
    })
    tree := initTree()
    if err := tree.Delete(items[0].Key); err != nil {
        t.Error("tree.Delete(...)")
    }
    tree.Insert(items[0].Key, items[0].Value)
    if !compareKeyValues(tree.Collect(), items) {
        t.Error("tree.Delete(...)")
    }
}
