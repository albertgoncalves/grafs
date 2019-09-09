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

func TestInsert(t *testing.T) {
    tree := &Tree{}
    for _, item := range items {
        tree.Insert(item.Key, item.Value)
    }
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
    tree := &Tree{}
    for _, item := range items {
        tree.Insert(item.Key, item.Value)
    }
    if value, err := tree.Find(PairKey{0.0, 0.0}); (value != "a") ||
        (err != nil) {
        t.Error("tree.Find(...)")
    }
    if _, err := tree.Find(PairKey{3.0, 0.0}); err == nil {
        t.Error("tree.Find(...)")
    }
}
