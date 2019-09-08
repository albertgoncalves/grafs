package main

import (
    "fmt"
    "gen"
    "geom"
    "math/rand"
)

func main() {
    rand.Seed(0)
    a := gen.RandomSegment()
    b := gen.RandomSegment()
    point, err := geom.PointOfIntersection(a, b)
    if err == nil {
        fmt.Println(point)
    } else {
        fmt.Println(err)
    }
}
