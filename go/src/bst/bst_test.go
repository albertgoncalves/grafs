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

func compareTuples(a, b []Tuple) bool {
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

var items = []Tuple{
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
    if !compareTuples(tree.Collect(), items) {
        t.Error("tree.Insert(...)")
    }
    if compareTuples(tree.Collect(), []Tuple{
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

func deletePipeline(t *testing.T, key Key, remainingItems []Tuple) {
    tree := initTree()
    if err := tree.Delete(key); err != nil {
        t.Error("tree.Delete(...)")
    }
    if !compareTuples(tree.Collect(), remainingItems) {
        t.Error("tree.Delete(...)")
    }
}

func TestDelete(t *testing.T) {
    deletePipeline(t, items[0].Key, []Tuple{
        items[1],
        items[2],
        items[3],
    })
    deletePipeline(t, items[1].Key, []Tuple{
        items[0],
        items[2],
        items[3],
    })
    deletePipeline(t, items[2].Key, []Tuple{
        items[0],
        items[1],
        items[3],
    })
    deletePipeline(t, items[3].Key, []Tuple{
        items[0],
        items[1],
        items[2],
    })
    tree := initTree()
    if err := tree.Delete(items[0].Key); err != nil {
        t.Error("tree.Delete(...)")
    }
    tree.Insert(items[0].Key, items[0].Value)
    if !compareTuples(tree.Collect(), items) {
        t.Error("tree.Delete(...)")
    }
}

func TestEmpty(t *testing.T) {
    if tree := (&Tree{}); !tree.Empty() {
        t.Error("tree.Empty()")
    }
    if tree := initTree(); tree.Empty() {
        t.Error("tree.Empty()")
    }
}

func popPipeline(
    t *testing.T,
    tree *Tree,
    item Tuple,
    remainingItems []Tuple,
) {
    if key, value, err := tree.Pop(); (key != item.Key) ||
        (value != item.Value) || (err != nil) ||
        (!compareTuples(tree.Collect(), remainingItems)) {
        t.Error("tree.Pop()")
    }
}

func TestPop(t *testing.T) {
    tree := initTree()
    n := len(items)
    var m int
    for i := 1; i < 5; i++ {
        m = n - i
        popPipeline(t, tree, items[m], items[:m])
    }
    if _, _, err := tree.Pop(); err == nil {
        t.Error("tree.Pop()")
    }
}
