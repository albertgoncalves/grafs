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

type state =
    {
        events : events;
        breaks : B.btree;
        edges : (B.index, B.index) Hashtbl.t;
        prev_distance : float
    }

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
            let l : B.breakpoint =
                {
                    B.l = value.P.a;
                    B.r = value.P.b;
                } in
            let r : B.breakpoint =
                {
                    B.l = value.P.b;
                    B.r = value.P.c;
                } in
            let new_btree : B.btree =
                B.join_pair_at value.P.p.P.x l r value.P.f f state.breaks in
            let prev : B.breakpoint = (B.predecessor l f state.breaks) in
            let next : B.breakpoint = (B.predecessor r f state.breaks) in
            let (new_circle_events, _)
                : ((P.circle_event) list * (P.key list)) =
                let i : (P.circle_event) option =
                    circle_from value.P.a value.P.c next.B.r in
                let j : (P.circle_event) option =
                    circle_from prev.B.l value.P.a value.P.c in
                let ijk : P.key =
                    {
                        P.a = a.B.index;
                        P.b = b.B.index;
                        P.c = c.B.index;
                    } in
                let prev_ij : P.key =
                    {
                        P.a = prev.B.l.B.index;
                        P.b = a.B.index;
                        P.c = b.B.index;
                    } in
                let next_jk : P.key =
                    {
                        P.a = b.B.index;
                        P.b = c.B.index;
                        P.c = next.B.r.B.index;
                    } in
                if (prev.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (i |> maybe_to_list, [ijk; next_jk])
                else if (next.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (j |> maybe_to_list, [ijk; prev_ij])
                else
                    (cat_maybes [i; j], [ijk; prev_ij; next_jk]) in
            {
                state with events =
                    {
                        new_points = state.events.new_points;
                        circle_events = circle_events;
                    };
            }
