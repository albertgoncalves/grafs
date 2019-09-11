package bst

import (
    "geom"
)

func PairEqual(a, b geom.Pair) bool {
    return (a.X == b.X) && (a.Y == b.Y)
}

func PairLess(a, b geom.Pair) bool {
    if a.Y == b.Y {
        return a.X < b.X
    }
    return a.Y < b.Y
}
