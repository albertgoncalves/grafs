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

var A Segment = Segment{Pair{0.0, 0.0}, Pair{2.0, 2.0}}
var B Segment = Segment{Pair{1.0, 0.0}, Pair{1.0, 3.0}}
var C Segment = Segment{Pair{1.0, 0.0}, Pair{2.0, 0.0}}

func TestIntersect(t *testing.T) {
    if !intersect(A, B) {
        t.Error("intersect(A, B)")
    }
    if intersect(A, C) {
        t.Error("intersect(A, C)")
    }
}

func TestPointOfIntersection(t *testing.T) {
    point, _ := PointOfIntersection(A, B)
    expected := Pair{1.0, 1.0}
    if point != expected {
        t.Error("PointOfIntersection(A, B)")
    }
    _, err := PointOfIntersection(A, C)
    if err == nil {
        t.Error("PointOfIntersection(A, C)")
    }
}
