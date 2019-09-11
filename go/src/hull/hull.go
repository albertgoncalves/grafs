package hull

import (
    "geom"
    "sort"
)

func deleteIndex(pairs []geom.Pair, i int) []geom.Pair {
    newPairs := make([]geom.Pair, 0, len(pairs)-1)
    newPairs = append(newPairs, pairs[:i]...)
    return append(newPairs, pairs[i+1:]...)
}

func ConvexHull(pairs []geom.Pair) ([]geom.Pair, []geom.Pair) {
    var m int
    n := len(pairs)
    sort.Slice(pairs, func(i, j int) bool {
        if pairs[i].X == pairs[j].X {
            return pairs[i].Y < pairs[j].Y
        }
        return pairs[i].X < pairs[j].X
    })
    upper := pairs[:2]
    for i := 2; i < n; i++ {
        upper = append(upper, pairs[i])
        m = len(upper)
        for (m > 2) && !geom.Ccw(upper[m-3], upper[m-2], upper[m-1]) {
            upper = deleteIndex(upper, m-2)
            m = len(upper)
        }
    }
    lower := []geom.Pair{pairs[n-1], pairs[n-2]}
    for i := n - 2; -1 < i; i-- {
        lower = append(lower, pairs[i])
        m = len(lower)
        for (m > 2) && !geom.Ccw(lower[m-3], lower[m-2], lower[m-1]) {
            lower = deleteIndex(lower, m-2)
            m = len(lower)
        }
    }
    return upper, lower
}
