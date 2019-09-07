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

func det2(ab Pair, cd Pair) float64 {
    return (ab.X * cd.Y) - (ab.Y * cd.X)
}

func det3(a, b, c Triple) float64 {
    return (a.X * det2(Pair{b.Y, b.Z}, Pair{c.Y, c.Z})) -
        (a.Y * det2(Pair{b.X, b.Z}, Pair{c.X, c.Z})) +
        (a.Z * det2(Pair{b.X, b.Y}, Pair{c.X, c.Y}))
}

func det4(a, b, c, d Quad) float64 {
    var A float64 = a.X * det3(
        Triple{b.Y, b.Z, b.W},
        Triple{c.Y, c.Z, c.W},
        Triple{d.Y, d.Z, d.W},
    )
    var B float64 = a.Y * det3(
        Triple{b.X, b.Z, b.W},
        Triple{c.X, c.Z, c.W},
        Triple{d.X, d.Z, d.W},
    )
    var C float64 = a.Z * det3(
        Triple{b.X, b.Y, b.W},
        Triple{c.X, c.Y, c.W},
        Triple{d.X, d.Y, d.W},
    )
    var D float64 = a.W * det3(
        Triple{b.X, b.Y, b.Z},
        Triple{c.X, c.Y, c.Z},
        Triple{d.X, d.Y, d.Z},
    )
    return A - B + C - D
}

func ccw(a, b, c Pair) bool {
    return ((c.Y - a.Y) * (b.X - a.X)) > ((b.Y - a.Y) * (c.X - a.X))
}

func intersect(l, r Segment) bool {
    return (ccw(l.A, r.A, r.B) != ccw(l.B, r.A, r.B)) &&
        (ccw(l.A, l.B, r.A) != ccw(l.A, l.B, r.B))
}

func PointOfIntersection(l, r Segment) (Pair, error) {
    if intersect(l, r) {
        xdelta := Pair{l.A.X - l.B.X, r.A.X - r.B.X}
        ydelta := Pair{l.A.Y - l.B.Y, r.A.Y - r.B.Y}
        var denominator float64 = det2(xdelta, ydelta)
        if denominator != 0.0 {
            d := Pair{det2(l.A, l.B), det2(r.A, r.B)}
            x := det2(d, xdelta) / denominator
            y := det2(d, ydelta) / denominator
            return Pair{x, y}, nil
        }
    }
    message := fmt.Sprintf("No point of intersection found for %+v %+v", l, r)
    return Pair{}, errors.New(message)
}
