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

let bind (a : 'a option) (f : 'a -> 'b option) : 'b option =
    match a with
        | Some a -> f a
        | None -> None

let break_null (b : B.breakpoint) : bool =
    (b.B.l.B.index = 0) && (b.B.r.B.index = 0)

let set_vert (a : P.point) : (edge -> edge) = function
    | Empty -> Single a
    | Single b -> Edge (b, a)
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

module type T = sig
    val edges : ((B.index * B.index), edge) Hashtbl.t
end

module Voronoi (X : T) = struct
    include X

    let process_circle (state : state) : state =
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
                    B.join_pair_at
                        value.P.p.P.x
                        l
                        r
                        value.P.f
                        f
                        state.breaks in
                let prev : B.breakpoint = (B.predecessor l f state.breaks) in
                let next : B.breakpoint = (B.successor r f state.breaks) in
                let (new_circles, to_remove)
                    : ((P.circle_event) list * (P.PSQ.k list)) =
                    let i : (P.circle_event) option =
                        circle_from a c next.B.r in
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
                    else
                        let condition : bool =
                            (&&)
                                (next.B.l.B.index = 0)
                                (next.B.r.B.index = 0) in
                        if condition then
                            (j |> option_to_list, [ijk; prev_ij])
                        else
                            (concat_options [i; j], [ijk; prev_ij; next_jk]) in
                let removed : P.PSQ.t =
                    List.fold_left (flip P.PSQ.remove) circles to_remove in
                let inserted : P.PSQ.t =
                    List.fold_left
                        begin
                            fun (circles : P.PSQ.t) (circle_event : P.PSQ.p) ->
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
                            match Hashtbl.find_opt X.edges key with
                                | None -> ()
                                | Some _ ->
                                    let value =
                                        set_vert
                                            value.P.p
                                            (Hashtbl.find X.edges key) in
                                    Hashtbl.replace X.edges key value

                    end
                    [
                        sort_pair (a.B.index, b.B.index);
                        sort_pair (b.B.index, c.B.index);
                    ];
                Hashtbl.add
                    X.edges
                    (sort_pair (a.B.index, c.B.index))
                    (Single value.P.p);
                {
                    breaks = new_btree;
                    events = {state.events with circles = inserted};
                    prev_distance = value.P.f;
                }

    let process_point (state : state) : state =
        let points : B.index_point list = state.events.points in
        let circles : P.PSQ.t = state.events.circles in
        let head : B.index_point = List.hd points in
        let tail : B.index_point list = List.tl points in
        let (new_btree, fallen_on) : (B.btree * B.either_btree) =
            B.insert_par head head.B.y state.breaks in
        let (prev, next, j) : (B.breakpoint * B.breakpoint * B.index_point) =
            match fallen_on with
                | B.Left b -> (B.predecessor b head.B.y state.breaks, b, b.B.l)
                | B.Right b ->
                    (b, B.successor b head.B.y state.breaks, b.B.r) in
        let i : B.index_point option =
            if break_null prev then
                None
            else
                Some (prev.B.l) in
        let k : B.index_point option =
            if break_null next then
                None
            else
                Some (next.B.r) in
        let new_circles : P.circle_event list =
            concat_options
                [
                    bind i (fun i -> circle_from i j head);
                    bind k (circle_from head j);
                ] in
        let removed : P.PSQ.t =
            match (i, j, k) with
                | (Some i, j, Some k) ->
                    P.PSQ.remove
                        (P.create_key i.B.index j.B.index k.B.index)
                        circles
                | _ -> circles in
        let inserted : P.PSQ.t =
            List.fold_left
                begin
                    fun (circles : P.PSQ.t) (circle_event : P.PSQ.p) ->
                        let key : P.PSQ.k =
                            P.create_key
                                circle_event.P.a.B.index
                                circle_event.P.b.B.index
                                circle_event.P.c.B.index in
                        P.PSQ.add key circle_event circles
                end
                removed
                new_circles in
        Hashtbl.add
            X.edges
            (sort_pair (head.B.index, j.B.index))
            Empty;
        {
            breaks = new_btree;
            events = {points = tail; circles = inserted};
            prev_distance = head.B.y;
        }

    let process_event (state : state) : state =
        let empty_points : bool = (List.length state.events.points) = 0 in
        let empty_circles : bool = (P.PSQ.size state.events.circles) = 0 in
        if empty_points && empty_circles then
            state
        else
            let next : bool =
                match P.PSQ.min state.events.circles with
                    | None -> false
                    | Some (_, circle) ->
                        if empty_points then
                            true
                        else
                            (* let circle_y : float = circle.P.p.P.y in *)
                            let circle_y : float = circle.P.f in
                            let point_y : float =
                                (List.hd state.events.points).B.y in
                            circle_y <= point_y in
            if next then
                process_circle state
            else
                process_point state

    let initialize (points : P.point list) : state =
        let index_points : B.index_point list =
            List.mapi
                (fun index xy -> {B.index = index; B.x = xy.P.x; B.y = xy.P.y})
                (List.sort (fun a b -> compare a.P.y b.P.y) points) in
        let tail : B.index_point list = index_points |> List.tl in
        let first : B.index_point = index_points |> List.hd in
        let second : B.index_point = tail |> List.hd in
        let b1 : B.breakpoint = {B.l = first; B.r = second} in
        let b2 : B.breakpoint = {B.l = second; B.r = first} in
        let first_pair : B.btree =
            B.Node (B.Nil, b1, B.Node (B.Nil, b2, B.Nil)) in
        Hashtbl.add X.edges (sort_pair (first.B.index, second.B.index)) Empty;
        let events : events = {points = List.tl tail; circles = P.PSQ.empty} in
        {
            events = events;
            breaks = first_pair;
            prev_distance = second.B.y;
        }

    let edges_to_list (() : unit) : index_edge list =
        Hashtbl.fold
            begin
                fun k v xs ->
                    match v with
                        | Edge (l, r) ->
                            ({i = fst k; j = snd k; a = l; b = r}::xs)
                        | _ -> xs
            end
            X.edges
            []

    let voronoi (points : P.point list) : index_edge list =
        let rec loop (state : state) : index_edge list =
            let empty_points : bool = (List.length state.events.points) = 0 in
            let empty_circles : bool =
                (P.PSQ.size state.events.circles) = 0 in
            if empty_points && empty_circles then
                edges_to_list ()
            else
                process_event state |> loop in
        initialize points |> loop
end
