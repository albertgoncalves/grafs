package geom

import (
    "errors"
    "fmt"
)

type Pair struct {
    X float64
    Y float64
}

type Segment struct {
    A Pair
    B Pair
}

type Triple struct {
    X float64
    Y float64
    Z float64
}

type Quad struct {
    X float64
    Y float64
    Z float64
    W float64
}

func Det2(ab Pair, cd Pair) float64 {
    return (ab.X * cd.Y) - (ab.Y * cd.X)
}

func Det3(a, b, c Triple) float64 {
    return (a.X * Det2(Pair{b.Y, b.Z}, Pair{c.Y, c.Z})) -
        (a.Y * Det2(Pair{b.X, b.Z}, Pair{c.X, c.Z})) +
        (a.Z * Det2(Pair{b.X, b.Y}, Pair{c.X, c.Y}))
}

func Det4(a, b, c, d Quad) float64 {
    var A float64 = a.X * Det3(
        Triple{b.Y, b.Z, b.W},
        Triple{c.Y, c.Z, c.W},
        Triple{d.Y, d.Z, d.W},
    )
    var B float64 = a.Y * Det3(
        Triple{b.X, b.Z, b.W},
        Triple{c.X, c.Z, c.W},
        Triple{d.X, d.Z, d.W},
    )
    var C float64 = a.Z * Det3(
        Triple{b.X, b.Y, b.W},
        Triple{c.X, c.Y, c.W},
        Triple{d.X, d.Y, d.W},
    )
    var D float64 = a.W * Det3(
        Triple{b.X, b.Y, b.Z},
        Triple{c.X, c.Y, c.Z},
        Triple{d.X, d.Y, d.Z},
    )
    return A - B + C - D
}

func Ccw(a, b, c Pair) bool {
    return ((c.Y - a.Y) * (b.X - a.X)) > ((b.Y - a.Y) * (c.X - a.X))
}

func Intersect(l, r Segment) bool {
    return (Ccw(l.A, r.A, r.B) != Ccw(l.B, r.A, r.B)) &&
        (Ccw(l.A, l.B, r.A) != Ccw(l.A, l.B, r.B))
}

func PointOfIntersection(l, r Segment) (Pair, error) {
    if Intersect(l, r) {
        xdelta := Pair{l.A.X - l.B.X, r.A.X - r.B.X}
        ydelta := Pair{l.A.Y - l.B.Y, r.A.Y - r.B.Y}
        var denominator float64 = Det2(xdelta, ydelta)
        if denominator != 0.0 {
            d := Pair{Det2(l.A, l.B), Det2(r.A, r.B)}
            x := Det2(d, xdelta) / denominator
            y := Det2(d, ydelta) / denominator
            return Pair{x, y}, nil
        }
    }
    message := fmt.Sprintf("No point of intersection found for %+v %+v", l, r)
    return Pair{}, errors.New(message)
}
