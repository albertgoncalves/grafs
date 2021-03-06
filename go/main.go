package main

import (
    "flag"
    "fmt"
    "gen"
    "geom"
    "gonum.org/v1/plot"
    "gonum.org/v1/plot/plotter"
    "gonum.org/v1/plot/vg"
    "gonum.org/v1/plot/vg/draw"
    "hull"
    "image/color"
    "intersect"
    "log"
    "math/rand"
    "os"
    "path/filepath"
)

const BOLD = "\033[1m"
const END = "\033[0m"
const TAB = "    "

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

func initPlot() *plot.Plot {
    p, err := plot.New()
    if err != nil {
        log.Fatal(err)
    }
    return p
}

func savePlot(p *plot.Plot, out string) {
    if err := p.Save(8*vg.Inch, 8*vg.Inch, out); err != nil {
        log.Fatal(err)
    }
}

func addPairs(p *plot.Plot, pairs []geom.Pair) {
    scatter, err := plotter.NewScatter(pairsToXYs(pairs))
    scatter.GlyphStyle.Shape = draw.CircleGlyph{}
    scatter.Color = color.RGBA{R: 0, G: 0, B: 0, A: 90}
    scatter.GlyphStyle.Radius = 4.0
    if err != nil {
        log.Fatal(err)
    }
    p.Add(scatter)
}

func addPolyLine(p *plot.Plot, pairs []geom.Pair) {
    line, err := plotter.NewLine(pairsToXYs(pairs))
    if err != nil {
        log.Fatal(err)
    }
    p.Add(line)
}

func addSegments(p *plot.Plot, segments []geom.Segment) {
    lines := segmentsToXYs(segments)
    for _, line := range lines {
        line, err := plotter.NewLine(line)
        line.LineStyle.Color = randomRGB()
        line.LineStyle.Width = 1.5
        if err != nil {
            log.Fatal(err)
        }
        p.Add(line)
    }
}

func flagProvided(name string) bool {
    found := false
    flag.Visit(func(f *flag.Flag) {
        if f.Name == name {
            found = true
        }
    })
    return found
}

func destination(handle string) string {
    return filepath.Join(os.Getenv("GOPATH"), "out", handle)
}

func displayInfo(header, out string, seed int) {
    fmt.Printf(
        "$ %s%s%s\n%sseed=%d\n%sout=%s\n",
        BOLD,
        header,
        END,
        TAB,
        seed,
        TAB,
        out,
    )
}

func main() {
    seed := flag.Int("s", 1, "seed")
    n := flag.Int("n", 10, "n")
    flag.Bool("d", false, "Plotting Demo")
    flag.Bool("c", false, "Convex Hull")
    flag.Bool("b", false, "Sweep Intersections (Brute)")
    flag.Bool("i", false, "Sweep Intersections")
    flag.Parse()
    if flagProvided("d") {
        out := destination("demo.png")
        displayInfo("Plotting Demo", out, *seed)
        rand.Seed(int64(*seed))
        p := initPlot()
        p.Add(plotter.NewGrid())
        addSegments(p, gen.RandomSegments(*n))
        addPairs(p, gen.RandomPairs(*n))
        savePlot(p, out)
    }
    if flagProvided("c") {
        out := destination("hull.png")
        displayInfo("Convex Hull", out, *seed)
        rand.Seed(int64(*seed))
        points := gen.RandomPairs(*n)
        upper, lower := hull.ConvexHull(points)
        p := initPlot()
        p.Add(plotter.NewGrid())
        addPairs(p, points)
        addPolyLine(p, upper)
        addPolyLine(p, lower)
        savePlot(p, out)
    }
    if flagProvided("b") {
        out := destination("brutesweep.png")
        displayInfo("Segment Intersections (Brute)", out, *seed)
        rand.Seed(int64(*seed))
        segments := gen.RandomSegments(*n)
        points, err := intersect.BruteSweep(segments)
        if err != nil {
            log.Fatal(err)
        }
        p := initPlot()
        p.Add(plotter.NewGrid())
        addSegments(p, segments)
        addPairs(p, points)
        savePlot(p, out)
    }
    if flagProvided("i") {
        out := destination("sweep.png")
        displayInfo("Segment Intersections", out, *seed)
        rand.Seed(int64(*seed))
        segments := gen.RandomSegments(*n)
        points, err := intersect.Sweep(segments)
        if err != nil {
            log.Fatal(err)
        }
        p := initPlot()
        p.Add(plotter.NewGrid())
        addSegments(p, segments)
        addPairs(p, points)
        savePlot(p, out)
    }
}
