package geom

func PairEqual(a, b Pair) bool {
    return (a.X == b.X) && (a.Y == b.Y)
}

func PairLess(a, b Pair) bool {
    if a.Y == b.Y {
        return a.X < b.X
    }
    return a.Y < b.Y
}
