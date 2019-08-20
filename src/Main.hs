module Main where

import Fortune (Point'(..), voronoi)

main :: IO ()
main = (print xs) >> (print $ voronoi xs)
  where
    xs =
        [ (1.0, 0.0)
        , (0.5, 0.25)
        , (0.0, 1.0)
        , (0.75, 0.65)
        , (0.9, 0.45)
        , (0.3, 0.7)
        ] :: [Point']
