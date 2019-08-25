module R = Random

type point = (float * float)

type edge = (point * point)

let string_of_point ((a, b) : point) : string =
    Printf.sprintf "(%.3f, %.3f)" a b

let string_of_edge ((a, b) : edge) : string =
    Printf.sprintf "(%s, %s)" (string_of_point a) (string_of_point b)

let generate (f : unit -> 'a) (n : int) : 'a list =
    if n < 1 then
        []
    else
        let rec loop (xs : 'a list) : (int -> 'a list) = function
            | 0 -> xs
            | n -> loop (f ()::xs) (n - 1) in
        loop [] n

let random_point (() : unit) : point = (R.float 1.0, R.float 1.0)

let random_edge (() : unit) : edge = (random_point (), random_point ())

let print_list (f : 'a -> string) (xs : 'a list) : unit =
    xs
    |> List.map f
    |> String.concat ", "
    |> (fun x -> "[" ^ x ^ "]")
    |> print_endline
