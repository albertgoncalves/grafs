module Main where

import Fortune (Edge'(..), Point', voronoi)

floatsFromEdge :: Edge' -> ((Float, Float), (Float, Float))
floatsFromEdge (Edge' _ _ a b) =
    ((realToFrac ax, realToFrac ay), (realToFrac bx, realToFrac by))
  where
    (ax, ay) = a :: (Double, Double)
    (bx, by) = b :: (Double, Double)

main :: IO ()
main = print xs >> print (map floatsFromEdge $ voronoi xs)
  where
    xs =
        [ (1.0, 0.0)
        , (0.5, 0.25)
        , (0.0, 1.0)
        , (0.75, 0.65)
        , (0.9, 0.45)
        , (0.3, 0.7)
        , (0.4, 0.6)
        , (0.10, -0.1)
        , (0.4, 0.2)
        , (1.0, 0.35)
        , (0.8, 0.5)
        ] :: [Point']
