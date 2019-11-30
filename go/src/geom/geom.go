package geom

import (
    "fmt"
    "math"
)

type Pair struct {
    X, Y float64
}

type Segment struct {
    A, B Pair
}

type Triple struct {
    X, Y, Z float64
}

type Quad struct {
    X, Y, Z, W float64
}

type Circle struct {
    Center Pair
    Radius float64
}

func det2(a Pair, b Pair) float64 {
    return (a.X * b.Y) - (a.Y * b.X)
}

func det3(a, b, c Triple) float64 {
    return (a.X * det2(Pair{b.Y, b.Z}, Pair{c.Y, c.Z})) -
        (a.Y * det2(Pair{b.X, b.Z}, Pair{c.X, c.Z})) +
        (a.Z * det2(Pair{b.X, b.Y}, Pair{c.X, c.Y}))
}

func det4(a, b, c, d Quad) float64 {
    A := a.X * det3(
        Triple{b.Y, b.Z, b.W},
        Triple{c.Y, c.Z, c.W},
        Triple{d.Y, d.Z, d.W},
    )
    B := a.Y * det3(
        Triple{b.X, b.Z, b.W},
        Triple{c.X, c.Z, c.W},
        Triple{d.X, d.Z, d.W},
    )
    C := a.Z * det3(
        Triple{b.X, b.Y, b.W},
        Triple{c.X, c.Y, c.W},
        Triple{d.X, d.Y, d.W},
    )
    D := a.W * det3(
        Triple{b.X, b.Y, b.Z},
        Triple{c.X, c.Y, c.Z},
        Triple{d.X, d.Y, d.Z},
    )
    return A - B + C - D
}

func Ccw(a, b, c Pair) bool {
    return ((c.Y - a.Y) * (b.X - a.X)) > ((b.Y - a.Y) * (c.X - a.X))
}

/* https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection */
func PointOfIntersection(a, b Segment) (Pair, error) {
    x1 := a.A.X
    x2 := a.B.X
    x3 := b.A.X
    x4 := b.B.X
    y1 := a.A.Y
    y2 := a.B.Y
    y3 := b.A.Y
    y4 := b.B.Y
    denominator := ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
    if denominator != 0.0 {
        t := (((x1 - x3) * (y3 - y4)) - ((y1 - y3) * (x3 - x4))) / denominator
        u := -(((x1 - x2) * (y1 - y3)) - ((y1 - y2) * (x1 - x3))) / denominator
        if 0.0 <= t && t <= 1.0 && 0.0 <= u && u <= 1.0 {
            x := x1 + (t * (x2 - x1))
            y := y1 + (t * (y2 - y1))
            return Pair{x, y}, nil
        }
    }
    return Pair{}, fmt.Errorf("PointOfIntersection(%v, %v)", a, b)
}

func SlopeIntercept(a Segment) (float64, float64, error) {
    if a.A.X == a.B.X {
        return 0.0, 0.0, fmt.Errorf("SlopeIntercept(%v)", a)
    }
    m := (a.B.Y - a.A.Y) / (a.B.X - a.A.X)
    b := a.A.Y - (m * a.A.X)
    return m, b, nil
}

func CircleOfPoints(a, b, c Pair) (Circle, error) {
    if (a == b) || (b == c) || (a == c) ||
        ((a.X == b.X) && (b.X == c.X)) ||
        ((a.Y == b.Y) && (b.Y == c.Y)) {
        return Circle{}, fmt.Errorf("CircleOfPoints(%v, %v, %v)", a, b, c)
    }
    ax2 := a.X * a.X
    ay2 := a.Y * a.Y
    bx2 := b.X * b.X
    by2 := b.Y * b.Y
    cx2 := c.X * c.X
    cy2 := c.Y * c.Y
    axy2 := ax2 + ay2
    bxy2 := bx2 + by2
    cxy2 := cx2 + cy2
    A2 := 2.0 * det3(
        Triple{a.X, a.Y, 1.0},
        Triple{b.X, b.Y, 1.0},
        Triple{c.X, c.Y, 1.0},
    )
    B := det3(
        Triple{axy2, a.Y, 1.0},
        Triple{bxy2, b.Y, 1.0},
        Triple{cxy2, c.Y, 1.0},
    )
    C := det3(
        Triple{axy2, a.X, 1.0},
        Triple{bxy2, b.X, 1.0},
        Triple{cxy2, c.X, 1.0},
    )
    x := B / A2
    y := -(C / A2)
    r := math.Sqrt(((x - a.X) * (x - a.X)) + ((y - a.Y) * (y - a.Y)))
    return Circle{Pair{x, y}, r}, nil
}

func PointInCircle(a, b, c, d Pair) (float64, error) {
    if (a == b) || (b == c) || (a == c) ||
        ((a.X == b.X) && (b.X == c.X)) ||
        ((a.Y == b.Y) && (b.Y == c.Y)) {
        return 0.0, fmt.Errorf("PointInCircle(%v, %v, %v, %v)", a, b, c, d)
    }
    // det4(...) <  0   ->  d is within circle(a, b, c)
    // det4(...) == 0   ->  d is co-circular with a, b, c
    // det4(...)  > 0   ->  d is outside circle(a, b, c)
    return det4(
        Quad{a.X, a.Y, (a.X * a.X) + (a.Y * a.Y), 1.0},
        Quad{b.X, b.Y, (b.X * b.X) + (b.Y * b.Y), 1.0},
        Quad{c.X, c.Y, (c.X * c.X) + (c.Y * c.Y), 1.0},
        Quad{d.X, d.Y, (d.X * d.X) + (d.Y * d.Y), 1.0},
    ), nil
}
