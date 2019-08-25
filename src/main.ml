module C = Components

let (_ : 'a) : unit =
    Random.init 1;
    let points : C.point list = C.generate C.random_point 10 in
    let edges : C.edge list = C.generate C.random_edge 10 in
    points |> C.print_list C.string_of_point;
    edges |> C.print_list C.string_of_edge;
