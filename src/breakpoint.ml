exception BreakpointError of string

type index = int

type index_point =
    {
        index : index;
        x : float;
        y : float;
    }

type breakpoint =
    {
        l : index_point;
        r : index_point;
    }

type btree =
    | Nil
    | Node of (btree * breakpoint * btree)

type either_btree =
    | Left of breakpoint
    | Right of breakpoint

let eq_breakpoint (a : breakpoint) (b : breakpoint) : bool =
    a.l.index = b.l.index && a.r.index = b.r.index

let nil_end (x : breakpoint) : btree = Node (Nil, x, Nil)

let intersect (a : index_point) (b : index_point) (f : float) : float =
    if abs_float (a.y -. b.y) < min_float  then
        if a.x < b.x then
            (a.x +. b.x) /. 2.0
        else
            BreakpointError "intersect" |> raise
    else
        let distance : float =
            ((a.x -. b.x) ** 2.0) +. ((a.y -. b.y) ** 2.0) in
        let sqrt : float = distance *. (a.y -. f) *. (b.y -. f) |> sqrt in
        let last : float = (a.x *. (f -. b.y)) -. (b.x *. f) in
        ((b.y *. a.x) +. sqrt +. last) /. (a.y -. b.y)

let rec insert (f1 : float) (b : breakpoint) (f2 : float) : (btree -> btree) =
    function
        | Nil -> Node (Nil, b, Nil)
        | Node (l, b', r) ->
            if f1 < (intersect b.l b.r f2) then
                Node (insert f1 b f2 l, b', r)
            else
                Node (l, b', insert f1 b f2 r)

let rec insert_par (p : index_point) (f : float)
    : (btree -> btree * either_btree) = function
        | Node (Nil, b, Nil) ->
            if p.x < (intersect b.l b.r f) then
                let branch : btree =
                    Node (Nil, {l = b.l; r = p}, nil_end {l = p; r = b.l}) in
                (Node (branch, b, Nil), Left b)
            else
                let branch : btree =
                    Node (Nil, {l = b.r; r = p}, nil_end {l = p; r = b.r}) in
                (Node (Nil, b, branch), Right b)
        | Node (Nil, b, r) ->
            if p.x < (intersect b.l b.r f) then
                let branch : btree =
                    Node (Nil, {l = b.l; r = p}, nil_end {l = p; r = b.l}) in
                (Node (branch, b, r), Left b)
            else
                let next : (btree * either_btree) = insert_par p f r in
                (Node (Nil, b, fst next), snd next)
        | Node (l, b, Nil) ->
            if p.x < (intersect b.l b.r f) then
                let next : (btree * either_btree) = insert_par p f l in
                (Node (fst next, b, Nil), snd next)
            else
                let branch : btree =
                    Node (Nil, {l = b.r; r = p}, nil_end {l = p; r = b.r}) in
                (Node (l, b, branch), Right b)
        | Node (l, b, r) ->
            if p.x < (intersect b.l b.r f) then
                let next : (btree * either_btree) = insert_par p f l in
                (Node (fst next, b, r), snd next)
            else
                let next : (btree * either_btree) = insert_par p f r in
                (Node (l, b, fst next), snd next)
        | _ -> BreakpointError "insert_par" |> raise

let rec tail_btree : (btree -> btree) = function
    | Node (Nil, _, r) -> r
    | Node (l, b, r) -> Node (tail_btree l, b, r)
    | Nil -> BreakpointError "tail_btree" |> raise

let rec left_branch : (btree -> breakpoint) = function
    | Node (Nil, b, _) -> b
    | Node (l, _, _) -> left_branch l
    | Nil -> BreakpointError "left_branch" |> raise

let rec right_branch : (btree -> breakpoint) = function
    | Node (_, b, Nil) -> b
    | Node (_, _, r) -> right_branch r
    | Nil -> BreakpointError "right_branch" |> raise

let delete_x : (btree -> btree) = function
    | Node (Nil, _, r) -> r
    | Node (l, _, Nil) -> l
    | Node (l, _, r) -> Node (l, (left_branch r), (tail_btree r))
    | Nil -> BreakpointError "delete_x" |> raise

let rec delete (b : breakpoint) (f : float) : (btree -> btree) = function
    | Node (l, b', r) as n ->
        if eq_breakpoint b b' then
            delete_x n
        else if (intersect b'.l b'.r f) < (intersect b.l b.r f) then
            Node (delete b' f l, b, r)
        else
            Node (l, b, delete b' f r)
    | _ -> BreakpointError "delete" |> raise

let rec delete_2 (b1 : breakpoint) (b2 : breakpoint) (f : float)
    : (btree -> btree) = function
    | Node (l, b, r) as n ->
        if eq_breakpoint b b1 then
            delete b2 f (delete_x n)
        else if eq_breakpoint b b1 then
            delete b1 f (delete_x n)
        else
            let i : float = intersect b.l b.r f in
            let i1 : float = intersect b1.l b1.r f in
            let i2 : float = intersect b2.l b2.r f in
            if i1 < i then
                if i2 < i then
                    Node (delete_2 b1 b2 f l, b, r)
                else
                    Node (delete b1 f l, b, delete b2 f r)
            else if i2 < i then
                Node (delete b2 f l, b, delete b1 f r)
            else
                Node (l, b, delete_2 b1 b2 f r)
    | _ -> BreakpointError "delete_2" |> raise

let join_pair_at (x : float) (b1 : breakpoint) (b2 : breakpoint) (f1 : float)
        (f2 : float) (t : btree) : btree =
    insert x {l = b1.l; r = b2.r} f1 (delete_2 b1 b2 f2 t)

let rec look_for (b : breakpoint) (f : float) : btree -> btree = function
    | Nil -> Nil
    | Node (l, b', r) as n ->
        if eq_breakpoint b b' then
            n
        else if (intersect b'.l b'.r f) < (intersect b.l b.r f) then
            look_for b' f l
        else
            look_for b' f r

let successor (b' : breakpoint) (f : float) (t : btree) : breakpoint =
    let rec go (b'' : breakpoint) : (btree -> breakpoint) = function
        | Nil -> b''
        | Node (l, b, r) ->
            if eq_breakpoint b b' then
                b''
            else
                let i : float = intersect b.l b.r f in
                let i' : float = intersect b'.l b'.r f in
                if i' < i then
                    go b l
                else if i' > i then
                    go b'' r
                else
                    b'' in
    match look_for b' f t with
        | Node (_, _, n) -> left_branch n
        | _ ->
            let p : index_point = {index = 0; x = 0.0; y = 0.0} in
            go {l = p; r = p} t

let predecessor (b' : breakpoint) (f : float) (t : btree) : breakpoint =
    let rec go (b'' : breakpoint) : (btree -> breakpoint) = function
        | Nil -> b''
        | Node (l, b, r) ->
            if eq_breakpoint b b' then
                b''
            else
                let i : float = intersect b.l b.r f in
                let i' : float = intersect b'.l b'.r f in
                if i' < i then
                    go b'' l
                else if i' > i then
                    go b r
                else
                    b'' in
    match look_for b' f t with
        | Node (_, _, n) -> right_branch n
        | _ ->
            let p : index_point = {index = 0; x = 0.0; y = 0.0} in
            go {l = p; r = p} t

let rec in_order : (btree -> breakpoint list) = function
    | Nil -> []
    | Node (l, b, r) -> (in_order l) @ [b] @ (in_order r)
