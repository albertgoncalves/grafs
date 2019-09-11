package gen

import (
    "geom"
    "math/rand"
)

func RandomPair() geom.Pair {
    return geom.Pair{X: rand.Float64(), Y: rand.Float64()}
}

func RandomPairs(n int) []geom.Pair {
    pairs := make([]geom.Pair, n)
    for i := 0; i < n; i++ {
        pairs[i] = RandomPair()
    }
    return pairs
}

func RandomSegment() geom.Segment {
    return geom.Segment{A: RandomPair(), B: RandomPair()}
}

func RandomSegments(n int) []geom.Segment {
    segments := make([]geom.Segment, n)
    for i := 0; i < n; i++ {
        segments[i] = RandomSegment()
    }
    return segments
}
