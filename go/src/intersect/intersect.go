package intersect

import (
    "bst"
    "fmt"
    "geom"
    "math"
)

const (
    UPPER        = 0
    INTERSECTION = 1
    LOWER        = 2
)

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
    return l.Segment == r.Segment
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
    if math.Abs(xr-xl) < 0.001 {
        return false
    }
    return xl < xr
}

func Sweep(segments []geom.Segment) ([]geom.Pair, error) {
    points := make([]geom.Pair, 0)
    eventQueue := &bst.GeomPairLabelSegmentsTree{
        Equal:    geom.PairEqual,
        Less:     geom.PairLess,
        Fallback: bst.LabelSegments{},
    }
    statusQueue := &bst.PairSegmentAnyTree{
        Equal:    segmentEqual,
        Less:     segmentLess,
        Fallback: nil,
    }
    memo := make(map[geom.Segment]geom.Pair)
    for _, segment := range segments {
        upper, lower := upperLower(segment)
        eventQueue.Insert(
            upper,
            bst.LabelSegments{Label: UPPER, First: segment},
        )
        eventQueue.Insert(
            lower,
            bst.LabelSegments{Label: LOWER, First: segment},
        )
    }
    for !eventQueue.Empty() {
        event, status, err := eventQueue.Pop()
        if err != nil {
            return points, fmt.Errorf("Sweep(%v)", segments)
        }
        switch status.Label {
        case UPPER:
            memo[status.First] = event
            pairSegment := bst.PairSegment{
                Pair:    event,
                Segment: status.First,
            }
            statusQueue.Insert(pairSegment, nil)
            left, right, err := statusQueue.Neighbors(pairSegment)
            if err == nil {
                if left != nil {
                    if point, err := geom.PointOfIntersection(
                        left.Key.Segment,
                        status.First,
                    ); (err == nil) && (point.Y < event.Y) {
                        eventQueue.Insert(
                            point,
                            bst.LabelSegments{
                                Label:  INTERSECTION,
                                First:  status.First,
                                Second: left.Key.Segment,
                            },
                        )
                    }
                }
                if right != nil {
                    if point, err := geom.PointOfIntersection(
                        status.First,
                        right.Key.Segment,
                    ); (err == nil) && (point.Y < event.Y) {
                        eventQueue.Insert(
                            point,
                            bst.LabelSegments{
                                Label:  INTERSECTION,
                                First:  right.Key.Segment,
                                Second: status.First,
                            },
                        )
                    }
                }
            }
        case LOWER:
            pairSegment := bst.PairSegment{
                Pair:    memo[status.First],
                Segment: status.First,
            }
            left, right, err := statusQueue.Neighbors(pairSegment)
            if err == nil {
                if err := statusQueue.Delete(pairSegment); err == nil {
                    if (left != nil) && (right != nil) {
                        if point, err := geom.PointOfIntersection(
                            left.Key.Segment,
                            right.Key.Segment,
                        ); (err == nil) && (point.Y < event.Y) {
                            eventQueue.Insert(
                                point,
                                bst.LabelSegments{
                                    Label:  INTERSECTION,
                                    First:  right.Key.Segment,
                                    Second: left.Key.Segment,
                                },
                            )
                        }
                    }
                }
            }
        case INTERSECTION:
            points = append(points, event)
            statusQueue.Delete(bst.PairSegment{
                Pair:    memo[status.First],
                Segment: status.First,
            })
            statusQueue.Delete(bst.PairSegment{
                Pair:    memo[status.Second],
                Segment: status.Second,
            })
            pairSegmentLeft := bst.PairSegment{
                Pair:    event,
                Segment: status.First,
            }
            pairSegmentRight := bst.PairSegment{
                Pair:    event,
                Segment: status.Second,
            }
            memo[status.First] = event
            memo[status.Second] = event
            statusQueue.Insert(pairSegmentLeft, nil)
            statusQueue.Insert(pairSegmentRight, nil)
            farLeft, _, err := statusQueue.Neighbors(pairSegmentLeft)
            if (err == nil) && (farLeft != nil) {
                if point, err := geom.PointOfIntersection(
                    farLeft.Key.Segment,
                    status.First,
                ); (err == nil) && (point.Y < event.Y) {
                    eventQueue.Insert(
                        point,
                        bst.LabelSegments{
                            Label:  INTERSECTION,
                            First:  status.First,
                            Second: farLeft.Key.Segment,
                        },
                    )
                }
            }
            _, farRight, err := statusQueue.Neighbors(pairSegmentRight)
            if (err == nil) && (farRight != nil) {
                if point, err := geom.PointOfIntersection(
                    status.Second,
                    farRight.Key.Segment,
                ); (err == nil) && (point.Y < event.Y) {
                    eventQueue.Insert(
                        point,
                        bst.LabelSegments{
                            Label:  INTERSECTION,
                            First:  farRight.Key.Segment,
                            Second: status.Second,
                        },
                    )
                }
            }
        }
    }
    return points, nil
}
