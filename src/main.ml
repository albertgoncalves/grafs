module B = Breakpoint
module P = Psqueue
module F = Fortune

let create_point ((x, y) : (float * float)) : P.point = {P.x = x; P.y = y}

let print_index_edge (edge : F.index_edge) : string =
    Printf.sprintf
        "((%f, %f), (%f, %f))"
        edge.F.a.P.x
        edge.F.a.P.y
        edge.F.b.P.x
        edge.F.b.P.y

let (_ : 'a) : unit =
    let points : P.point list =
        List.map
            create_point
            [
                (1.0, 0.0);
                (0.5, 0.25);
                (0.0, 1.0);
                (0.75, 0.65);
                (0.9, 0.45);
                (0.3, 0.7);
                (0.4, 0.6);
                (0.1, -0.1);
                (0.4, 0.2);
                (1.0, 0.35);
                (0.8, 0.5);
                (0.6, 0.37);
                (0.8, 1.0);
                (0.1, 0.25);
                (0.8, 0.0);
                (0.2, 0.3);
                (0.49, 0.78);
                (-0.9, 1.1);
                (0.1, 1.2);
            ] in
    List.map print_index_edge (F.voronoi points)
    |> String.concat ",\n"
    |> fun x -> "[" ^ x ^ "]"
                |> print_endline
