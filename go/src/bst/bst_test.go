package bst

import (
    "testing"
)

type PairKey struct {
    X float64
    Y float64
}

func (a PairKey) equal(b Key) bool {
    switch b := b.(type) {
    case PairKey:
        return (a.X == b.X) && (a.Y == b.Y)
    default:
        return false
    }
}

func (a PairKey) less(b Key) bool {
    switch b := b.(type) {
    case PairKey:
        if a.X == b.X {
            return a.Y < b.Y
        }
        return a.X < b.X
    default:
        return false
    }
}

func compareKeyValues(a, b []KeyValue) bool {
    if len(a) != len(b) {
        return false
    }
    for i := range(a) {
        if a[i] != b[i] {
            return false
        }
    }
    return true
}

func TestInsert(t *testing.T) {
    tree := &Tree{}
    items := []KeyValue{
        KeyValue{PairKey{0.0, 0.0}, "a"},
        KeyValue{PairKey{1.0, 0.0}, "b"},
        KeyValue{PairKey{2.0, 0.0}, "c"},
        KeyValue{PairKey{2.0, 1.0}, "d"},
    }
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
