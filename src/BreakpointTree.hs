{-# LANGUAGE Strict #-}

-- https://github.com/SimplyNaOH/voronoi/blob/master/src/BreakpointTree.hs
module BreakpointTree
    ( BTree(..)
    , Breakpoint(..)
    , Point(..)
    , insertPar
    , joinPairAt
    , inOrderSuccessor
    , inOrderPredecessor
    , inOrder
    ) where

import Control.Arrow (first)
import Prelude hiding (pi, succ)

type Index = Int

data Point =
    Point !Index !Double !Double
    deriving (Show)

data Breakpoint =
    Breakpoint !Point !Point

instance Show Breakpoint where
    show (Breakpoint (Point i _ _) (Point j _ _)) = show (i, j)

-- instance Eq Breakpoint where
--     (Breakpoint (Point i _ _) (Point j _ _)) == (Breakpoint (Point i' _ _) (Point j' _ _)) =
--         i == i' && j == j'
data BTree
    = Nil
    | Node BTree Breakpoint BTree

nilEnd :: Breakpoint -> BTree
nilEnd x = Node Nil x Nil

{-  Find the intersection between the parabolas with focus `f1` and `f2` and
    directrix `d`. -}
intersection :: Point -> Point -> Double -> Double
intersection (Point _ f1x f1y) (Point _ f2x f2y) d =
    if abs (f1y - f2y) < 0.0000001
        then if f1x < f2x
                 then (f1x + f2x) / 2
                 else 1 / 0
        else x
  where
    dist = (f1x - f2x) * (f1x - f2x) + (f1y - f2y) * (f1y - f2y)
    sqroot = sqrt $ dist * (f1y - d) * (f2y - d)
    lastterm = f1x * (d - f2y) - f2x * d
    x = (f1y * f2x + sqroot + lastterm) / (f1y - f2y)

insert :: Double -> Breakpoint -> Double -> BTree -> BTree
insert _ b' _ Nil = Node Nil b' Nil
insert x b' d (Node l b r)
    | x < updated = Node (insert x b' d l) b r
    | otherwise = Node l b (insert x b' d r)
  where
    Breakpoint pl pr = b
    updated = intersection pl pr d

insertPar :: Point -> Double -> BTree -> (BTree, Either Breakpoint Breakpoint)
insertPar p@(Point _ x _) d (Node Nil b Nil)
    | x < updated = (Node (Node Nil newl (nilEnd newl')) b Nil, Left b)
    | otherwise = (Node Nil b (Node Nil newr (nilEnd newr')), Right b)
  where
    Breakpoint pl@(Point _ _ _) pr@(Point _ _ _) = b
    updated = intersection pl pr d
    newl = Breakpoint pl p
    newl' = Breakpoint p pl
    newr = Breakpoint pr p
    newr' = Breakpoint p pr
insertPar p@(Point _ x _) d (Node Nil b r)
    | x < updated = (Node (Node Nil newl (nilEnd newl')) b r, Left b)
    -- first :: a b c -> a (b, d) (c, d)
    | otherwise = first (Node Nil b) (insertPar p d r)
  where
    Breakpoint pl@(Point _ _ _) pr = b
    updated = intersection pl pr d
    newl = Breakpoint pl p
    newl' = Breakpoint p pl
insertPar p@(Point _ x _) d (Node l b Nil)
    | x < updated = first (flip (flip Node b) Nil) $ insertPar p d l
    | otherwise = (Node l b $ Node Nil newr (nilEnd newr'), Right b)
  where
    Breakpoint pl pr@(Point _ _ _) = b
    updated = intersection pl pr d
    newr = Breakpoint pr p
    newr' = Breakpoint p pr
insertPar p@(Point _ x _) d (Node l b r)
    | x < updated = first (flip (flip Node b) r) $ insertPar p d l
    | otherwise =
        let next = insertPar p d r -- first (Node l b) $ insertPar p d r
         in (Node l b (fst next), snd next)
  where
    Breakpoint pl pr = b
    updated = intersection pl pr d
insertPar _ _ Nil = error "insertPar: Cannot insert into empty tree."

tail' :: BTree -> BTree
tail' Nil = error "Tail of empty tree."
tail' (Node Nil _ r) = r
tail' (Node l b r) = Node (tail' l) b r

leftistElement :: BTree -> Breakpoint
leftistElement (Node Nil b _) = b
leftistElement (Node l _ _) = leftistElement l
leftistElement Nil = undefined

rightestElement :: BTree -> Breakpoint
rightestElement (Node _ b Nil) = b
rightestElement (Node _ _ r) = rightestElement r
rightestElement Nil = undefined

deleteX :: BTree -> BTree
deleteX Nil = error "deleteX: Cannot delete Nil"
deleteX (Node Nil _ r) = r
deleteX (Node l _ Nil) = l
deleteX (Node l _ r) = Node l (leftistElement r) (tail' r)

delete :: Breakpoint -> Double -> BTree -> BTree
delete b' d n@(Node l b r)
    | i == i' && j == j' = deleteX n
    | x < updated = Node (delete b' d l) b r
    | x >= updated = Node l b (delete b' d r)
  where
    Breakpoint pl@(Point i _ _) pr@(Point j _ _) = b
    Breakpoint pl'@(Point i' _ _) pr'@(Point j' _ _) = b'
    updated = intersection pl pr d
    x = intersection pl' pr' d
delete _ _ _ = error "delete: Reached Nil"

delete2 :: Breakpoint -> Breakpoint -> Double -> BTree -> BTree
delete2 b1 b2 d n@(Node l b r)
    | i1 == i && j1 == j = delete b2 d $ deleteX n
    | i2 == i && j2 == j = delete b1 d $ deleteX n
    | x1 < u =
        if x2 < u
            then Node (delete2 b1 b2 d l) b r
            else Node (delete b1 d l) b (delete b2 d r)
    | x2 < u = Node (delete b2 d l) b (delete b1 d r)
    | otherwise = Node l b $ delete2 b1 b2 d r
  where
    Breakpoint pl1@(Point i1 _ _) pr1@(Point j1 _ _) = b1
    Breakpoint pl2@(Point i2 _ _) pr2@(Point j2 _ _) = b2
    Breakpoint pl@(Point i _ _) pr@(Point j _ _) = b
    u = intersection pl pr d
    x1 = intersection pl1 pr1 d
    x2 = intersection pl2 pr2 d
delete2 _ _ _ Nil = error "delete2: reached nil."

joinPairAt ::
       Double
    -> Breakpoint
    -> Breakpoint
    -> Double
    -> Double
    -> BTree
    -> BTree
joinPairAt x b1 b2 d d' tree = insert x newB d $ delete2 b1 b2 d' tree
  where
    Breakpoint pi@(Point _ _ _) _ = b1
    Breakpoint _ pk@(Point _ _ _) = b2
    newB = Breakpoint pi pk

lookFor :: Breakpoint -> Double -> BTree -> BTree
lookFor _ _ Nil = Nil
lookFor b' d n@(Node l b r)
    | i == i' && j == j' = n
    | x < updated = lookFor b' d l
    | x >= updated = lookFor b' d r
    | otherwise = error "lookFor: Breakpoint does not exist."
  where
    Breakpoint pl@(Point i _ _) pr@(Point j _ _) = b
    Breakpoint pl'@(Point i' _ _) pr'@(Point j' _ _) = b'
    updated = intersection pl pr d
    x = intersection pl' pr' d

inOrderSuccessor :: Breakpoint -> Double -> BTree -> Breakpoint
inOrderSuccessor b' d tree =
    case lookFor b' d tree of
        Node _ _ n@Node {} -> leftistElement n
        _ -> go (Breakpoint (Point 0 0 0) (Point 0 0 0)) tree
  where
    go :: Breakpoint -> BTree -> Breakpoint
    go s Nil = s
    go succ (Node l b r)
        | i == i' && j == j' = succ
        | x < updated = go b l
        | x > updated = go succ r
        | otherwise = succ
      where
        Breakpoint pl@(Point i _ _) pr@(Point j _ _) = b
        Breakpoint pl'@(Point i' _ _) pr'@(Point j' _ _) = b'
        updated = intersection pl pr d
        x = intersection pl' pr' d

inOrderPredecessor :: Breakpoint -> Double -> BTree -> Breakpoint
inOrderPredecessor b' d tree =
    case lookFor b' d tree of
        Node n@Node {} _ _ -> rightestElement n
        _ -> go (Breakpoint (Point 0 0 0) (Point 0 0 0)) tree
  where
    go s Nil = s
    go succ (Node l b r)
        | i == i' && j == j' = succ
        | x < updated = go succ l
        | x > updated = go b r
        | otherwise = succ
      where
        Breakpoint pl@(Point i _ _) pr@(Point j _ _) = b
        Breakpoint pl'@(Point i' _ _) pr'@(Point j' _ _) = b'
        updated = intersection pl pr d
        x = intersection pl' pr' d

inOrder :: BTree -> [Breakpoint]
inOrder Nil = []
inOrder (Node l b r) = inOrder l ++ [b] ++ inOrder r
