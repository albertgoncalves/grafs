module B = Breakpoint
module P = Psqueue
module F = Fortune

let (_ : 'a) : unit =
    let p : B.index_point = {B.index = 1; B.x = 0.0; B.y = 0.0} in
    let b : B.breakpoint = {B.l = p; B.r = p} in
    let _ : B.btree = B.Node (B.Nil, b, B.Nil) in
    let _ : F.events =
        {
            F.points = [p];
            F.circles = P.PSQ.empty;
        } in
    ()
