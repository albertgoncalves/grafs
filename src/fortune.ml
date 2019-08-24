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
        points : B.index_point list;
        circles : P.PSQ.t;
    }

let edges : ((B.index * B.index), edge) Hashtbl.t = Hashtbl.create 256

type state =
    {
        events : events;
        breaks : B.btree;
        prev_distance : float
    }

let option_to_list : 'a option -> 'a list = function
    | None -> []
    | Some a -> [a]

let rec concat_options : 'a option list -> 'a list = function
    | [] -> []
    | (Some x::xs) -> (x::concat_options xs)
    | (None::xs) -> concat_options xs

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

let process_circle_event (state : state) : state =
    let min_view : ((P.PSQ.k * P.PSQ.p) * P.PSQ.t) option =
        P.PSQ.pop state.events.circles in
    match min_view with
        | None -> FortuneError "process_circle_event" |> raise
        | Some ((_, value), circles) ->
            let a : B.index_point = value.P.a in
            let b : B.index_point = value.P.b in
            let c : B.index_point = value.P.c in
            let f : float = (value.P.f +. state.prev_distance) /. 2.0 in
            let l : B.breakpoint = {B.l = a; B.r = b} in
            let r : B.breakpoint = {B.l = b; B.r = c} in
            let new_btree : B.btree =
                B.join_pair_at value.P.p.P.x l r value.P.f f state.breaks in
            let prev : B.breakpoint = (B.predecessor l f state.breaks) in
            let next : B.breakpoint = (B.successor r f state.breaks) in
            let (new_circles, to_remove)
                : ((P.circle_event) list * (P.PSQ.k list)) =
                let i : (P.circle_event) option =
                    circle_from a value.P.c next.B.r in
                let j : (P.circle_event) option =
                    circle_from prev.B.l a c in
                let ijk : P.PSQ.k =
                    P.create_key a.B.index b.B.index c.B.index in
                let prev_ij : P.PSQ.k =
                    P.create_key prev.B.l.B.index a.B.index b.B.index in
                let next_jk : P.PSQ.k =
                    P.create_key b.B.index c.B.index next.B.r.B.index in
                if (prev.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (i |> option_to_list, [ijk; next_jk])
                else if (next.B.l.B.index = 0) && (prev.B.r.B.index = 0) then
                    (j |> option_to_list, [ijk; prev_ij])
                else
                    (concat_options [i; j], [ijk; prev_ij; next_jk]) in
            let removed : P.PSQ.t =
                List.fold_left (flip P.PSQ.remove) circles to_remove in
            let inserted : P.PSQ.t =
                List.fold_left
                    begin
                        fun circles circle_event ->
                            let circle_event : P.PSQ.p = circle_event in
                            let key : P.PSQ.k =
                                P.create_key
                                    circle_event.P.a.B.index
                                    circle_event.P.b.B.index
                                    circle_event.P.c.B.index in
                            P.PSQ.add key circle_event circles
                    end
                    removed
                    new_circles in
            List.iter
                begin
                    fun key ->
                        Hashtbl.replace
                            edges
                            key
                            (set_vert value.P.p (Hashtbl.find edges key))
                end
                [
                    sort_pair (a.B.index, b.B.index);
                    sort_pair (b.B.index, c.B.index);
                ];
            Hashtbl.add
                edges
                (sort_pair (a.B.index, c.B.index))
                (Single value.P.p);
            {
                breaks = new_btree;
                events = {state.events with circles = inserted};
                prev_distance = value.P.f;
            }

let process_new_point_event (state : state) : state =
    let head : B.index_point = List.hd state.events.points in
    let tail : B.index_point list = List.tl state.events.points in
    let circles : P.PSQ.t = state.events.circles in
    let events : events = state.events in
    let (btree, fallen_on) : (B.btree * B.either_btree) =
        B.insert_par head head.y state.breaks in
    let (prev, next, j) : (B.breakpoint * B.breakpoint * B.index_point) =
        match fallen_on with
            | B.Left b -> (B.predecessor b head.y state.breaks, b, b.l)
            | B.Right b -> (b, B.successor b head.y state.breaks, b.r) in
    let i : B.index_point option =
        if break_null prev then
            None
        else
            Some (prev.l) in
    let k : B.index_point option =
        if break_null next then
            None
        else
            Some (next.r) in
    state
