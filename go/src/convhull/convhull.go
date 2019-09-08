package convhull

import (
    "geom"
    "sort"
)

func deleteIndex(pairs []geom.Pair, i int) []geom.Pair {
    newPairs := make([]geom.Pair, 0)
    newPairs = append(newPairs, pairs[:i]...)
    return append(newPairs, pairs[i+1:]...)
}

func ConvexHull(pairs []geom.Pair) ([]geom.Pair, []geom.Pair) {
    n := len(pairs)
    sort.Sort(geom.PairByX(pairs))
    upper := pairs[:2]
    for i := 2; i < n; i++ {
        upper = append(upper, pairs[i])
        for (len(upper) > 2) && !geom.Ccw(
            upper[len(upper)-3],
            upper[len(upper)-2],
            upper[len(upper)-1],
        ) {
            upper = deleteIndex(upper, len(upper)-2)
        }
    }
    lower := []geom.Pair{pairs[n-1], pairs[n-2]}
    for i := n - 2; -1 < i; i-- {
        lower = append(lower, pairs[i])
        for (len(lower) > 2) && !geom.Ccw(
            lower[len(lower)-3],
            lower[len(lower)-2],
            lower[len(lower)-1],
        ) {
            lower = deleteIndex(lower, len(lower)-2)
        }
    }
    return upper, lower
}
