# grafs (go)

![](cover.png)

Needed things
---
 * [Nix](https://nixos.org/nix/)

Quick start
---
```
$ nix-shell
[nix-shell:path/to/grafs/go]$ go test geom bst
[nix-shell:path/to/grafs/go]$ go test geom -bench .
[nix-shell:path/to/grafs/go]$ go build -o bin/main main.go && ./bin/main -c -d -i -n 25 -s 1
```
