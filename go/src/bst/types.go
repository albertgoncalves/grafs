package bst

import (
    "geom"
)

type LabelSegment struct {
    Label   uint8
    Segment geom.Segment
}

type PairSegment struct {
    Pair    geom.Pair
    Segment geom.Segment
}

type Any = interface{}
