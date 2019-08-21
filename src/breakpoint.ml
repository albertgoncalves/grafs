exception BreakpointError of string

type index = int

type point =
    {
        index: index;
        x: float;
        y: float;
    }

type breakpoint =
    {
        l: point;
        r: point;
    }

type btree =
    | Nil
    | Node of (btree * breakpoint * btree)

let nil_end (x : breakpoint) : btree = Node (Nil, x, Nil)

let intersect (a : point) (b : point) (f : float) : float =
    if abs_float (a.y -. b.y) < min_float  then
        if a.x < b.x then
            (a.x +. b.x) /. 2.0
        else
            BreakpointError "intersect" |> raise (* originally: 1/0 (???) *)
    else
        let distance : float =
            ((a.x -. b.x) ** 2.0) +. ((a.y -. b.y) ** 2.0) in
        let sqrt : float = distance *. (a.y -. f) *. (b.y -. f) |> sqrt in
        let last : float = (a.x *. (f -. b.y)) -. (b.x *. f) in
        ((b.y *. a.x) +. sqrt +. last) /. (a.y -. b.y)

let rec insert (b : breakpoint) (f1 : float) (f2 : float) : (btree -> btree) =
    function
        | Nil -> Node (Nil, b, Nil)
        | Node (l, t, r) ->
            let updated : float = intersect b.l b.r f2 in
            if f1 < updated then
                Node (insert b f1 f2 l, t, r)
            else
                Node (l, t, insert b f1 f2 r)

let (_ : 'a) : unit =
    let p : point = {index = 1; x = 0.0; y = 0.0} in
    let b : breakpoint = {l = p; r = p} in
    let _ : btree = Node (Nil, b, Nil) in
    ()
