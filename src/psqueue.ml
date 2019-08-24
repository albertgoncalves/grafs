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

let create_key (a : B.index) (b : B.index) (c : B.index) : key =
    {a = a; b = b; c = c}

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

module V = struct
    type t = circle_event
    let compare (a : t) (b : t) = compare a.f b.f
end

module PSQ = Psq.Make (K) (V)
