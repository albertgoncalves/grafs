package main

import (
    "fmt"
    "geom"
)

func main() {
    a := geom.Segment{
        geom.Pair{
            X: 0.0,
            Y: 0.0,
        },
        geom.Pair{
            X: 1.0,
            Y: 1.0,
        },
    }
    b := geom.Segment{
        geom.Pair{
            X: 0.0,
            Y: 2.0,
        },
        geom.Pair{
            X: 1.0,
            Y: 0.0,
        },
    }
    point, err := geom.PointOfIntersection(a, b)
    if err == nil {
        fmt.Println(point)
    } else {
        fmt.Println(err)
    }
}
