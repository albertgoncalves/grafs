package intersect

import (
    "bst"
    "fmt"
    "geom"
)

const UPPER = 0
const LOWER = 1

func upperLower(segment geom.Segment) (geom.Pair, geom.Pair) {
    if (segment.B.Y < segment.A.Y) ||
        ((segment.A.Y == segment.B.Y) && (segment.A.X < segment.B.X)) {
        return segment.A, segment.B
    }
    return segment.B, segment.A
}

func BruteSweep(segments []geom.Segment) ([]geom.Pair, error) {
    points := make([]geom.Pair, 0)
    eventQueue := &bst.GeomPairLabelSegmentTree{
        Equal:    geom.PairEqual,
        Less:     geom.PairLess,
        Fallback: bst.LabelSegment{},
    }
    statusQueue := make(map[geom.Segment]interface{})
    for _, segment := range segments {
        upper, lower := upperLower(segment)
        eventQueue.Insert(
            upper,
            bst.LabelSegment{Label: UPPER, Segment: segment},
        )
        eventQueue.Insert(
            lower,
            bst.LabelSegment{Label: LOWER, Segment: segment},
        )
    }
    for !eventQueue.Empty() {
        _, status, err := eventQueue.Pop()
        if err != nil {
            return points, fmt.Errorf("BruteSweep(%v)", segments)
        }
        switch status.Label {
        case UPPER:
            for segment := range statusQueue {
                if point, err := geom.PointOfIntersection(
                    status.Segment,
                    segment,
                ); err == nil {
                    points = append(points, point)
                }
            }
            statusQueue[status.Segment] = nil
        case LOWER:
            delete(statusQueue, status.Segment)
        }
    }
    return points, nil
}

func segmentEqual(l, r bst.PairSegment) bool {
    return l == r
}

func segmentLess(l, r bst.PairSegment) bool {
    var y float64
    if l.Pair.Y < r.Pair.Y {
        y = l.Pair.Y
    } else {
        y = r.Pair.Y
    }
    ml, bl, err := geom.SlopeIntercept(l.Segment)
    if err != nil {
        return false
    }
    mr, br, err := geom.SlopeIntercept(r.Segment)
    if err != nil {
        return true
    }
    xl := (y - bl) / ml
    xr := (y - br) / mr
    return xl < xr
}

func Sweet(segments []geom.Segment) ([]geom.Pair, error) {
    points := make([]geom.Pair, 0)
    eventQueue := &bst.GeomPairLabelSegmentTree{
        Equal:    geom.PairEqual,
        Less:     geom.PairLess,
        Fallback: bst.LabelSegment{},
    }
    statusQueue := &bst.PairSegmentAnyTree{
        Equal:    segmentEqual,
        Less:     segmentLess,
        Fallback: nil,
    }
    memo := make(map[geom.Segment]geom.Pair)
    fmt.Println(eventQueue)
    fmt.Println(statusQueue)
    fmt.Println(memo)
    return points, nil
}
