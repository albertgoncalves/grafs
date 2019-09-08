package gen

import (
    "geom"
    "math/rand"
)

func RandomPair() geom.Pair {
    return geom.Pair{rand.Float64(), rand.Float64()}
}

func RandomPairs(n int) []geom.Pair {
    pairs := make([]geom.Pair, n)
    for i := 0; i < n; i++ {
        pairs[i] = RandomPair()
    }
    return pairs
}

func RandomSegment() geom.Segment {
    return geom.Segment{RandomPair(), RandomPair()}
}

func RandomSegments(n int) []geom.Segment {
    segments := make([]geom.Segment, n)
    for i := 0; i < n; i++ {
        segments[i] = RandomSegment()
    }
    return segments
}
