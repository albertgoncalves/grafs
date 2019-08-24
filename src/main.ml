module B = Breakpoint
module P = Psqueue
module F = Fortune

let (_ : 'a) : unit =
    let p : B.index_point = {B.index = 1; B.x = 0.0; B.y = 0.0} in
    let b : B.breakpoint = {B.l = p; B.r = p} in
    let _ : B.btree = B.Node (B.Nil, b, B.Nil) in
    let _ : F.events =
        {
            F.new_points = [|{P.x = 0.0; P.y = 0.0}|];
            F.circle_events = P.PSQ.empty;
        } in
    ()
