# grafs (go)

![](cover.png)

Needed things
---
 * [Nix](https://nixos.org/nix/)

Quick start
---
```
$ nix-shell
[nix-shell:path/to/grafs/go]$ go test geom
[nix-shell:path/to/grafs/go]$ go test geom -bench .
[nix-shell:path/to/grafs/go]$ go build -o bin/main main.go && ./bin/main -d 0 && open out/demo.png
[nix-shell:path/to/grafs/go]$ go build -o bin/main main.go && ./bin/main -c 0 && open out/convex_hull.png
```
