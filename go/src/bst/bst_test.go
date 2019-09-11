package bst

import (
    "geom"
    "testing"
)

func compareTuples(a, b []GeomPairGeomSegmentTuple) bool {
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

var a = geom.Pair{X: 0.0, Y: 0.0}
var b = geom.Pair{X: 1.0, Y: 1.0}
var c = geom.Pair{X: 2.0, Y: 2.0}
var d = geom.Pair{X: 3.0, Y: 3.0}

var items = []GeomPairGeomSegmentTuple{
    {geom.Pair{X: 0.0, Y: 0.0}, geom.Segment{A: a, B: a}},
    {geom.Pair{X: 1.0, Y: 0.0}, geom.Segment{A: b, B: b}},
    {geom.Pair{X: 2.0, Y: 0.0}, geom.Segment{A: c, B: c}},
    {geom.Pair{X: 2.0, Y: 1.0}, geom.Segment{A: d, B: d}},
}

func initTree() *GeomPairGeomSegmentTree {
    tree := &GeomPairGeomSegmentTree{Equal: PairEqual, Less: PairLess}
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
    if compareTuples(tree.Collect(), []GeomPairGeomSegmentTuple{
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
    if _, err := tree.Find(geom.Pair{X: 3.0, Y: 0.0}); err == nil {
        t.Error("tree.Find(...)")
    }
}

func deletePipeline(
    t *testing.T,
    key geom.Pair,
    remainingItems []GeomPairGeomSegmentTuple,
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
    deletePipeline(t, items[0].Key, []GeomPairGeomSegmentTuple{
        items[1],
        items[2],
        items[3],
    })
    deletePipeline(t, items[1].Key, []GeomPairGeomSegmentTuple{
        items[0],
        items[2],
        items[3],
    })
    deletePipeline(t, items[2].Key, []GeomPairGeomSegmentTuple{
        items[0],
        items[1],
        items[3],
    })
    deletePipeline(t, items[3].Key, []GeomPairGeomSegmentTuple{
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
    if tree := (&GeomPairGeomSegmentTree{}); !tree.Empty() {
        t.Error("tree.Empty()")
    }
    if tree := initTree(); tree.Empty() {
        t.Error("tree.Empty()")
    }
}

func popPipeline(
    t *testing.T,
    tree *GeomPairGeomSegmentTree,
    item GeomPairGeomSegmentTuple,
    remainingItems []GeomPairGeomSegmentTuple,
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
