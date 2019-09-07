package geom

import (
    "testing"
)

func TestCcw(t *testing.T) {
    a := Pair{0.0, 0.0}
    b := Pair{1.0, 0.0}
    c := Pair{1.0, 1.0}
    if !ccw(a, b, c) {
        t.Error("ccw(a, b, c)")
    }
    if ccw(a, c, b) {
        t.Error("ccw(a, c, b)")
    }
}

func TestIntersect(t *testing.T) {
    a := Segment{Pair{0.0, 0.0}, Pair{2.0, 2.0}}
    b := Segment{Pair{1.0, 0.0}, Pair{1.0, 3.0}}
    c := Segment{Pair{1.0, 0.0}, Pair{2.0, 0.0}}
    if !intersect(a, b) {
        t.Error("intersect(a, b)")
    }
    if intersect(a, c) {
        t.Error("intersect(a, c)")
    }
}

func TestPointOfIntersection(t *testing.T) {
    a := Segment{Pair{0.0, 0.0}, Pair{2.0, 2.0}}
    b := Segment{Pair{1.0, 0.0}, Pair{1.0, 3.0}}
    c := Segment{Pair{1.0, 0.0}, Pair{2.0, 0.0}}
    point, _ := PointOfIntersection(a, b)
    expected := Pair{1.0, 1.0}
    if point != expected {
        t.Error("PointOfIntersection(a, b)")
    }
    _, err := PointOfIntersection(a, c)
    if err == nil {
        t.Error("PointOfIntersection(a, c)")
    }
}
