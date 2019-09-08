package main

import (
    "gen"
    "geom"
    "gonum.org/v1/plot"
    "gonum.org/v1/plot/plotter"
    "gonum.org/v1/plot/vg"
    "gonum.org/v1/plot/vg/draw"
    "image/color"
    "log"
    "math/rand"
)

func pairsToXYs(pairs []geom.Pair) plotter.XYs {
    n := len(pairs)
    xys := make(plotter.XYs, n)
    for i := 0; i < n; i++ {
        xys[i].X = pairs[i].X
        xys[i].Y = pairs[i].Y
    }
    return xys
}

func segmentsToXYs(segments []geom.Segment) []plotter.XYs {
    n := len(segments)
    xys := make([]plotter.XYs, n)
    for i := 0; i < n; i++ {
        xy := make(plotter.XYs, 2)
        xy[0].X = segments[i].A.X
        xy[0].Y = segments[i].A.Y
        xy[1].X = segments[i].B.X
        xy[1].Y = segments[i].B.Y
        xys[i] = xy
    }
    return xys
}

func randomUInt8() uint8 {
    return uint8(rand.Intn(255))
}

func randomRGB() color.RGBA {
    return color.RGBA{
        R: randomUInt8(),
        G: randomUInt8(),
        B: randomUInt8(),
        A: 255,
    }
}

func addPairs(p *plot.Plot, pairs []geom.Pair) {
    scatter, err := plotter.NewScatter(pairsToXYs(pairs))
    scatter.GlyphStyle.Shape = draw.CircleGlyph{}
    scatter.Color = color.RGBA{R: 0, G: 0, B: 0, A: 200}
    scatter.GlyphStyle.Radius = 5.0
    if err != nil {
        log.Panic(err)
    }
    p.Add(scatter)
}

func addSegments(p *plot.Plot, segments []geom.Segment) {
    lines := segmentsToXYs(segments)
    for _, line := range lines {
        line, err := plotter.NewLine(line)
        line.LineStyle.Color = randomRGB()
        line.LineStyle.Width = 3.25
        if err != nil {
            log.Panic(err)
        }
        p.Add(line)
    }
}

func main() {
    rand.Seed(1)
    n := 20
    p, err := plot.New()
    if err != nil {
        log.Panic(err)
    }
    p.Add(plotter.NewGrid())
    addSegments(p, gen.RandomSegments(n))
    addPairs(p, gen.RandomPairs(n))
    if err := p.Save(8*vg.Inch, 12*vg.Inch, "out/plot.png"); err != nil {
        log.Panic(err)
    }
}
