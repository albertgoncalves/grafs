module B = Breakpoint
module P = Psqueue

type edge =
    | Empty
    | Single of P.point
    | Edge of (P.point * P.point)

type index_edge =
    {
        i : B.index;
        j : B.index;
        a : P.point;
        b : P.point;
    }

type events =
    {
        new_points : P.point array;
        circle_events : Psq.Make(P.K)(P.V).t;
    }

type state =
    {
        events : events;
        breaks : B.btree;
        edges : (B.index, B.index) Hashtbl.t;
        prev_distance : float
    }
