module B = Breakpoint

let (_ : 'a) : unit =
    let p : B.index_point = {B.index = 1; B.x = 0.0; B.y = 0.0} in
    let b : B.breakpoint = {B.l = p; B.r = p} in
    let _ : B.btree = B.Node (B.Nil, b, B.Nil) in
    ()
