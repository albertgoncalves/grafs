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

type LabelSegments struct {
    Label  uint8
    First  geom.Segment
    Second geom.Segment
}

type Any = interface{}
