module B = Breakpoint

type point =
    {
        x : float;
        y : float;
    }

type circle_event =
    {
        a : B.index_point;
        b : B.index_point;
        c : B.index_point;
        f : float;
        p : point;
    }

type key =
    {
        a : B.index;
        b : B.index;
        c : B.index;
    }

module K = struct
    type t = key
    let compare (a : t) (b : t) =
        let first : int = compare a.a b.a in
        if first = 0 then
            let second : int = compare a.b b.b in
            if second = 0 then
                compare a.c b.c
            else
                second
        else
            first
end

let compare_point (a : point) (b : point) : int =
    let first : int = compare a.x b.x in
    if first = 0 then
        compare a.y b.y
    else
        first

module V = struct
    type t = circle_event
    let compare (a : t) (b : t) =
        let first : int = compare a.a.B.index b.a.B.index in
        if first = 0 then
            let second : int = compare a.b.B.index b.b.B.index in
            if second = 0 then
                let third : int = compare a.c.B.index b.c.B.index in
                if third = 0 then
                    let fourth : int = compare a.f b.f in
                    if fourth = 0 then
                        compare_point a.p b.p
                    else
                        fourth
                else
                    third
            else
                second
        else
            first
end

module PSQ = Psq.Make (K) (V)
