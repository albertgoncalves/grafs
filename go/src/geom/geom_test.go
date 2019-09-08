package geom

import (
    "testing"
)

var a = Pair{-1.0, 0.0}
var b = Pair{1.0, 0.0}
var c = Pair{0.0, 1.0}
var A = Segment{Pair{0.0, 0.0}, Pair{2.0, 2.0}}
var B = Segment{Pair{1.0, 0.0}, Pair{1.0, 3.0}}
var C = Segment{Pair{1.0, 0.0}, Pair{2.0, 0.0}}
var D = Segment{Pair{0.0, 1.0}, Pair{1.0, 3.0}}

func TestCcw(t *testing.T) {
    if !Ccw(a, b, c) {
        t.Error("ccw(a, b, c)")
    }
    if Ccw(a, c, b) {
        t.Error("ccw(a, c, b)")
    }
}

func TestPointOfIntersection(t *testing.T) {
    if point, err := PointOfIntersection(A, B); (point != (Pair{1.0, 1.0})) &&
        (err != nil) {
        t.Error("PointOfIntersection(A, B)")
    }
    if _, err := PointOfIntersection(A, C); err == nil {
        t.Error("PointOfIntersection(A, C)")
    }
}

func BenchmarkPointOfIntersection(b *testing.B) {
    for i := 0; i < b.N; i++ {
        PointOfIntersection(A, B)
    }
}

func TestSlopeIntercept(t *testing.T) {
    if m, b, err := SlopeIntercept(A); (m != 1.0) && (b != 0.0) &&
        (err != nil) {
        t.Error("SlopeIntercept(A)")
    }
    if _, _, err := SlopeIntercept(B); err == nil {
        t.Error("SlopeIntercept(B)")
    }
    if m, b, err := SlopeIntercept(C); (m != 0.0) && (b != 0.0) &&
        (err != nil) {
        t.Error("SlopeIntercept(C)")
    }
    if m, b, err := SlopeIntercept(D); (m != 2.0) && (b != 1.0) &&
        (err != nil) {
        t.Error("SlopeIntercept(D)")
    }
}

func TestCircleOfPoints(t *testing.T) {
    if circle, _ := CircleOfPoints(a, b, c); (circle != Circle{Pair{0.0, 0.0}, 1.0}) {
        t.Error("CircleOfPoints(a, b, c)")
    }
    if _, err := CircleOfPoints(
        Pair{-3.0, 4.0},
        Pair{-3.0, 4.0},
        Pair{4.0, 5.0},
    ); err == nil {
        t.Error("CircleOfPoints(...)")
    }
    if _, err := CircleOfPoints(
        Pair{1.0, -4.0},
        Pair{4.0, 5.0},
        Pair{1.0, -4.0},
    ); err == nil {
        t.Error("CircleOfPoints(...)")
    }
    if _, err := CircleOfPoints(
        Pair{-3.0, 4.0},
        Pair{4.0, 5.0},
        Pair{4.0, 5.0},
    ); err == nil {
        t.Error("CircleOfPoints(...)")
    }
    if _, err := CircleOfPoints(
        Pair{1.0, 1.0},
        Pair{1.0, 2},
        Pair{1.0, 3.0},
    ); err == nil {
        t.Error("CircleOfPoints(...)")
    }
    if _, err := CircleOfPoints(
        Pair{1.0, 1.0},
        Pair{2, 1.0},
        Pair{3.0, 1.0},
    ); err == nil {
        t.Error("CircleOfPoints(...)")
    }
}

func TestPointInCircle(t *testing.T) {
    if result, _ := PointInCircle(
        Pair{0.0, 0.0},
        Pair{2.0, 0.0},
        Pair{0.0, 2.0},
        Pair{2.0, 2.0},
    ); result != 0.0 {
        t.Error("PointInCircle(...)")
    }
    if result, _ := PointInCircle(
        Pair{0.0, 0.0},
        Pair{0.0, 1.0},
        Pair{1.0, 1.0},
        Pair{0.0, 1.0},
    ); result != 0 {
        t.Error("PointInCircle(...)")
    }
    if result, _ := PointInCircle(
        Pair{0.0, 0.0},
        Pair{2.0, 0.0},
        Pair{0.0, 2.0},
        Pair{2.0, 1.0},
    ); result <= 0 {
        t.Error("PointInCircle(...)")
    }
    if result, _ := PointInCircle(
        Pair{0.0, 0.0},
        Pair{2.0, 0.0},
        Pair{0.0, 2.0},
        Pair{2.0, 3.0},
    ); result >= 0 {
        t.Error("PointInCircle(...)")
    }
    if _, err := PointInCircle(
        Pair{0.0, 1.0},
        Pair{1.0, 1.0},
        Pair{2.0, 1.0},
        Pair{0.0, 1.0},
    ); err == nil {
        t.Error("PointInCircle(...)")
    }
    if _, err := PointInCircle(
        Pair{0.0, 1.0},
        Pair{0.0, 2.0},
        Pair{0.0, 3.0},
        Pair{0.0, 1.0},
    ); err == nil {
        t.Error("PointInCircle(...)")
    }
    if _, err := PointInCircle(
        Pair{0.0, 0.0},
        Pair{0.0, 0.0},
        Pair{0.0, 0.0},
        Pair{0.0, 1.0},
    ); err == nil {
        t.Error("PointInCircle(...)")
    }
    if _, err := PointInCircle(
        Pair{0.0, 0.0},
        Pair{0.0, 0.0},
        Pair{0.0, 1.0},
        Pair{0.0, 1.0},
    ); err == nil {
        t.Error("PointInCircle(...)")
    }

}
