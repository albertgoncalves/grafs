package bst

import (
    "geom"
    "testing"
)

func compareTuples(a, b []GeomPairLabelSegmentTuple) bool {
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

var items = []GeomPairLabelSegmentTuple{
    {
        geom.Pair{X: 0.0, Y: 0.0},
        LabelSegment{Label: 0, Segment: geom.Segment{}},
    },
    {
        geom.Pair{X: 1.0, Y: 0.0},
        LabelSegment{Label: 1, Segment: geom.Segment{}},
    },
    {
        geom.Pair{X: 2.0, Y: 0.0},
        LabelSegment{Label: 2, Segment: geom.Segment{}},
    },
    {
        geom.Pair{X: 2.0, Y: 1.0},
        LabelSegment{Label: 3, Segment: geom.Segment{}},
    },
}

func initTree() *GeomPairLabelSegmentTree {
    tree := &GeomPairLabelSegmentTree{
        Equal: geom.PairEqual,
        Less:  geom.PairLess,
        Null:  LabelSegment{},
    }
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
    if compareTuples(tree.Collect(), []GeomPairLabelSegmentTuple{
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
        value, err := tree.Find(items[i].Key, LabelSegment{})
        if (value != items[i].Value) ||
            (err != nil) {
            t.Error("tree.Find(...)")
            break
        }
    }
    _, err := tree.Find(geom.Pair{X: 3.0, Y: 0.0}, LabelSegment{})
    if err == nil {
        t.Error("tree.Find(...)")
    }
}

func deletePipeline(
    t *testing.T,
    key geom.Pair,
    remainingItems []GeomPairLabelSegmentTuple,
) {
    tree := initTree()
    if err := tree.Delete(key); err != nil {
        t.Error("tree.Delete(...)")
    }
    if !compareTuples(tree.Collect(), remainingItems) {
        t.Error("tree.Delete(...)")
    }
}

func TestDelete(t *testing.T) {
    deletePipeline(t, items[0].Key, []GeomPairLabelSegmentTuple{
        items[1],
        items[2],
        items[3],
    })
    deletePipeline(t, items[1].Key, []GeomPairLabelSegmentTuple{
        items[0],
        items[2],
        items[3],
    })
    deletePipeline(t, items[2].Key, []GeomPairLabelSegmentTuple{
        items[0],
        items[1],
        items[3],
    })
    deletePipeline(t, items[3].Key, []GeomPairLabelSegmentTuple{
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
    if tree := (&GeomPairLabelSegmentTree{}); !tree.Empty() {
        t.Error("tree.Empty()")
    }
    if tree := initTree(); tree.Empty() {
        t.Error("tree.Empty()")
    }
}

func popPipeline(
    t *testing.T,
    tree *GeomPairLabelSegmentTree,
    item GeomPairLabelSegmentTuple,
    remainingItems []GeomPairLabelSegmentTuple,
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
    for i := n - 1; -1 < i; i-- {
        popPipeline(t, tree, items[i], items[:i])
    }
    if _, _, err := tree.Pop(); err == nil {
        t.Error("tree.Pop()")
    }
}

func TestNeighbors(t *testing.T) {
    tree := initTree()
    if left, right, err := tree.Neighbors(items[0].Key); (err != nil) ||
        (left != nil) || (right.Key != items[1].Key) {
        t.Error("tree.Neighbors(...)")
    }
    if left, right, err := tree.Neighbors(items[1].Key); (err != nil) ||
        (left.Key != items[0].Key) || (right.Key != items[2].Key) {
        t.Error("tree.Neighbors(...)")
    }
    if left, right, err := tree.Neighbors(items[2].Key); (err != nil) ||
        (left.Key != items[1].Key) || (right.Key != items[3].Key) {
        t.Error("tree.Neighbors(...)")
    }
    tree.Pop()
    if _, _, err := tree.Neighbors(items[3].Key); err == nil {
        t.Error("tree.Neighbors(...)")
    }
}
