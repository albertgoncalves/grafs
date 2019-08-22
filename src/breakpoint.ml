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

type either_btree =
  | Left of breakpoint
  | Right of breakpoint

let eq_breakpoint (a : breakpoint) (b : breakpoint) : bool =
  a.l.index = b.l.index && a.r.index = b.r.index

let nil_end (x : breakpoint) : btree = Node (Nil, x, Nil)

let intersect (a : point) (b : point) (f : float) : float =
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

let rec insert (b : breakpoint) (f1 : float) (f2 : float) : (btree -> btree) =
  function
  | Nil -> Node (Nil, b, Nil)
  | Node (l, t, r) ->
    if f1 < (intersect b.l b.r f2) then
      Node (insert b f1 f2 l, t, r)
    else
      Node (l, t, insert b f1 f2 r)

let rec insert_par (p : point) (f : float) : (btree -> btree * either_btree) =
  function
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

let (_ : 'a) : unit =
  let p : point = {index = 1; x = 0.0; y = 0.0} in
  let b : breakpoint = {l = p; r = p} in
  let _ : btree = Node (Nil, b, Nil) in
  ()
