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
        Equal: geom.PairEqual,
        Less:  geom.PairLess,
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
        if status.Label == UPPER {
            for segment := range statusQueue {
                if point, err := geom.PointOfIntersection(
                    status.Segment,
                    segment,
                ); err == nil {
                    points = append(points, point)
                }
            }
            statusQueue[status.Segment] = nil
        } else {
            delete(statusQueue, status.Segment)
        }
    }
    return points, nil
}
