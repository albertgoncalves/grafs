exception FortuneError of string

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
        circle_events : P.PSQ.t;
    }

let edges : ((B.index * B.index), edge) Hashtbl.t = Hashtbl.create 256

type state =
    {
        events : events;
        breaks : B.btree;
        prev_distance : float
    }

let sort_pair ((a, b) : (int * int)) : (int * int) =
    if a < b then
        (a, b)
    else
        (b, a)

let flip (f : 'a -> 'b -> 'c) : ('b -> 'a -> 'c) = fun b a -> f a b

let break_null (b : B.breakpoint) : bool =
    (b.B.l.B.index = 0) && (b.B.r.B.index = 0)

let set_vert (a : P.point) : (edge -> edge) = function
    | Empty -> Single a
    | Single b -> Edge (a, b)
    | edge -> edge

let circle_from (a : B.index_point) (b : B.index_point) (c : B.index_point)
    : (P.circle_event) option =
    let bax : float = b.B.x -. a.B.x in
    let bay : float = b.B.y -. a.B.y in
    let cax : float = c.B.x -. a.B.x in
    let cay : float = c.B.y -. a.B.y in
    let ba = (bax ** 2.0) +. (bay ** 2.0) in
    let ca = (cax ** 2.0) +. (cay ** 2.0) in
    let denominator : float = 2.0 *. ((bax *. cay) -. (bay *. cax)) in
    if denominator <= 0.0 then
        None
    else
        let x : float = a.B.x +. ((cay *. ba) -. (bay *. ca) /. denominator) in
        let y : float = a.B.y +. ((bax *. ca) -. (cax *. ba) /. denominator) in
        let r : float =
            ((x -. a.B.x) ** 2.0) +. ((y -. a.B.y) ** 2.0) |> sqrt in
        Some
            {
                P.a = a;
                P.b = b;
                P.c = c;
                P.f = y +. r;
                P.p = {P.x = x; P.y = y};
            }

let maybe_to_list : 'a option -> 'a list = function
    | None -> []
    | Some a -> [a]

let rec cat_maybes : 'a option list -> 'a list = function
    | [] -> []
    | (Some x::xs) -> (x::cat_maybes xs)
    | (None::xs) -> cat_maybes xs

let process_circle_event (state : state) : state =
    let min_view : ((P.PSQ.k * P.PSQ.p) * P.PSQ.t) option =
        P.PSQ.pop state.events.circle_events in
    match min_view with
        | None -> FortuneError "process_circle_event" |> raise
        | Some ((_, value), circle_events) ->
            let a : B.index_point = value.P.a in
            let b : B.index_point = value.P.b in
            let c : B.index_point = value.P.c in
            let f : float = (value.P.f +. state.prev_distance) /. 2.0 in
            let l : B.breakpoint = {B.l = value.P.a; B.r = value.P.b} in
            let r : B.breakpoint = {B.l = value.P.b; B.r = value.P.c} in
            let new_btree : B.btree =
                B.join_pair_at value.P.p.P.x l r value.P.f f state.breaks in
            let prev : B.breakpoint = (B.predecessor l f state.breaks) in
            let next : B.breakpoint = (B.predecessor r f state.breaks) in
            let (new_circle_events, to_remove)
                : ((P.circle_event) list * (P.PSQ.k list)) =
                let i : (P.circle_event) option =
                    circle_from value.P.a value.P.c next.B.r in
                let j : (P.circle_event) option =
                    circle_from prev.B.l value.P.a value.P.c in
                let ijk : P.PSQ.k =
                    P.create_key a.B.index b.B.index c.B.index in
                let prev_ij : P.PSQ.k =
                    P.create_key prev.B.l.B.index a.B.index b.B.index in
                let next_jk : P.PSQ.k =
                    P.create_key b.B.index c.B.index next.B.r.B.index in
                if (prev.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (i |> maybe_to_list, [ijk; next_jk])
                else if (next.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (j |> maybe_to_list, [ijk; prev_ij])
                else
                    (cat_maybes [i; j], [ijk; prev_ij; next_jk]) in
            let removed : P.PSQ.t =
                List.fold_left (flip P.PSQ.remove) circle_events to_remove in
            let inserted : P.PSQ.t =
                List.fold_left
                    (fun circle_events circle_event ->
                        let circle_event : P.PSQ.p = circle_event in
                        let key : P.PSQ.k =
                            P.create_key
                                circle_event.P.a.B.index
                                circle_event.P.b.B.index
                                circle_event.P.c.B.index in
                        P.PSQ.add key circle_event circle_events)
                    removed
                    new_circle_events in
            let new_events : events =
                {state.events with circle_events = inserted} in
            List.iter
                (fun key ->
                    Hashtbl.replace
                        edges
                        key
                        (set_vert value.P.p (Hashtbl.find edges key)))
                [
                    sort_pair (a.B.index, b.B.index);
                    sort_pair (b.B.index, c.B.index);
                ];
            let new_edge : edge = Single value.P.p in
            Hashtbl.add edges (sort_pair (a.B.index, c.B.index)) new_edge;
            {
                breaks = new_btree;
                events = new_events;
                prev_distance = value.P.f;
            }
