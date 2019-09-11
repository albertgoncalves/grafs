package intersect

import (
    "bst"
    "fmt"
    "geom"
)

const UPPER = "upper"
const LOWER = "lower"

func upperEnd(segment geom.Segment) geom.Pair {
    if (segment.B.Y < segment.A.Y) ||
        ((segment.A.Y == segment.B.Y) && (segment.A.X < segment.B.X)) {
        return segment.A
    }
    return segment.B
}

func lowerEnd(segment geom.Segment) geom.Pair {
    if (segment.B.Y < segment.A.Y) ||
        ((segment.A.Y == segment.B.Y) && (segment.A.X < segment.B.X)) {
        return segment.B
    }
    return segment.A
}

func BruteSweep(segments []geom.Segment) ([]geom.Pair, error) {
    points := make([]geom.Pair, 0)
    eventQueue := &bst.GeomPairLabelSegmentTree{
        Equal: bst.PairEqual,
        Less:  bst.PairLess,
    }
    statusQueue := make(map[geom.Segment]interface{})
    for _, segment := range segments {
        eventQueue.Insert(
            upperEnd(segment),
            bst.LabelSegment{Label: UPPER, Segment: segment},
        )
        eventQueue.Insert(
            lowerEnd(segment),
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
