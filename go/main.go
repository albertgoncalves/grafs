package main

import (
    "fmt"
    "geom"
)

func main() {
    a := geom.Segment{
        geom.Pair{0.0, 0.0},
        geom.Pair{1.0, 1.0},
    }
    b := geom.Segment{
        geom.Pair{0.0, 3.0},
        geom.Pair{1.0, 0.0},
    }
    point, err := geom.PointOfIntersection(a, b)
    if err == nil {
        fmt.Println(point)
    } else {
        fmt.Println(err)
    }
}
