{-# LANGUAGE StrictData #-}

-- https://github.com/SimplyNaOH/voronoi/blob/master/src/Fortune.hs
module Fortune
    ( voronoi
    , Edge'(..)
    , Point'
    ) where

import BreakpointTree
import Data.List (sortOn)
import qualified Data.Map.Strict as Map
import Data.Map.Strict (Map)
import Data.Maybe (catMaybes, maybeToList)
import qualified Data.OrdPSQ as PSQ
import Data.OrdPSQ (OrdPSQ)
import qualified Data.Vector as V
import Prelude hiding (map, pi, succ)

type Index = Int

type Point' = (Double, Double)

data Edge
    = EmptyEdge
    | IEdge !Point'
    | Edge !Point' !Point'

data Edge' =
    Edge' !Index !Index !Point' !Point'
    deriving (Show)

type NewPointEvent = Point

data CircleEvent =
    CircleEvent !Point !Point !Point !Double !Point'

instance Show CircleEvent where
    show (CircleEvent pi pj pk _ _) = show (pindex pi, pindex pj, pindex pk)

data Events =
    Events
        { newPointEvents :: V.Vector NewPointEvent
        , circleEvents :: OrdPSQ (Index, Index, Index) Double CircleEvent
        }

data State =
    State
        { events :: Events
        , breaks :: BTree
        , edges :: Map (Index, Index) Edge
        , prevd :: Double
        }

pindex :: Point -> Index
pindex (Point i _ _) = i

breakNull :: Breakpoint -> Bool
breakNull (Breakpoint (Point i _ _) (Point j _ _)) = i == 0 && j == 0

pointAtLeftOf :: Breakpoint -> Point
pointAtLeftOf (Breakpoint l _) = l

pointAtRightOf :: Breakpoint -> Point
pointAtRightOf (Breakpoint _ r) = r

sortPair :: Ord b => b -> b -> (b, b)
sortPair a b =
    if a < b
        then (a, b)
        else (b, a)

setVert :: Point' -> Edge -> Edge
setVert p EmptyEdge = IEdge p
setVert p (IEdge p') = Edge p' p
setVert _ (Edge _ _) = undefined

{-  Returns `Just (center, radius)` of the circle defined by three given
    points.
    If the points are colinear or counter clockwise, it returns `Nothing`. -}
circleFrom3Points :: Point -> Point -> Point -> Maybe (Point', Double)
circleFrom3Points (Point _ x1 y1) (Point _ x2 y2) (Point _ x3 y3) =
    if denominator <= 0
        then Nothing
        else Just ((x, y), r)
  where
    (bax, bay) = (x2 - x1, y2 - y1)
    (cax, cay) = (x3 - x1, y3 - y1)
    ba = bax * bax + bay * bay
    ca = cax * cax + cay * cay
    denominator = 2 * (bax * cay - bay * cax)
    x = x1 + (cay * ba - bay * ca) / denominator
    y = y1 + (bax * ca - cax * ba) / denominator
    r = sqrt $ (x - x1) * (x - x1) + (y - y1) * (y - y1)

circleEvent :: Point -> Point -> Point -> Maybe CircleEvent
circleEvent pi pj pk =
    (\(c@(_, y), r) -> CircleEvent pi pj pk (y + r) c) <$>
    circleFrom3Points pi pj pk

processCircleEvent :: State -> State
processCircleEvent state =
    state {breaks = newBTree, events = newEvents, edges = newEdges, prevd = d}
  where
    Just (_, _, CircleEvent pi@(Point i _ _) pj@(Point j _ _) pk@(Point k _ _) y p, cevents) =
        PSQ.minView . circleEvents . events $ state
    events' = events state
    bTree = breaks state
    d = y
    d' = (d + prevd state) / 2
    bl = Breakpoint pi pj
    br = Breakpoint pj pk
    newBTree = joinPairAt (fst p) bl br d d' bTree
    Breakpoint prev@(Point previ _ _) (Point prevj _ _) =
        inOrderPredecessor bl d' bTree
    Breakpoint (Point nexti _ _) next@(Point nextj _ _) =
        inOrderSuccessor br d' bTree
    newCEvents'
        | previ == 0 && prevj == 0 = maybeToList $ circleEvent pi pk next
        | nexti == 0 && nextj == 0 = maybeToList $ circleEvent prev pi pk
        | otherwise =
            catMaybes [circleEvent pi pk next, circleEvent prev pi pk]
    toRemove
        | previ == 0 && prevj == 0 = [(i, j, k), (j, k, nextj)]
        | nexti == 0 && nextj == 0 = [(i, j, k), (previ, i, j)]
        | otherwise = [(i, j, k), (previ, i, j), (j, k, nextj)]
    insert' ev@(CircleEvent pi pj pk y _) =
        PSQ.insert (pindex pi, pindex pj, pindex pk) y ev
    removed = foldr PSQ.delete cevents toRemove
    newCEvents = foldr insert' removed newCEvents'
    newEvents = events' {circleEvents = newCEvents}
    newEdge = IEdge p
    edgesToUpdate =
        [sortPair (pindex pi) (pindex pj), sortPair (pindex pj) (pindex pk)]
    updatedEdges = foldr (Map.adjust (setVert p)) (edges state) edgesToUpdate
    newEdges =
        Map.insert (sortPair (pindex pi) (pindex pk)) newEdge updatedEdges

processNewPointEvent :: State -> State
processNewPointEvent state =
    state {breaks = newBTree, events = newEvents, edges = newEdges, prevd = d}
  where
    newp@(Point idx _ d) = V.head . newPointEvents . events $ state
    newPEvents = V.tail . newPointEvents . events $ state
    cEvents = circleEvents . events $ state
    events' = events state
    bTree = breaks state
    (newBTree, fallenOn) = insertPar newp d bTree
    (prev, next) =
        case fallenOn of
            Left b -> (inOrderPredecessor b d bTree, b)
            Right b -> (b, inOrderSuccessor b d bTree)
    pi =
        if breakNull prev
            then Nothing
            else Just $ pointAtLeftOf prev
    pk =
        if breakNull next
            then Nothing
            else Just $ pointAtRightOf next
    pj =
        case fallenOn of
            Left b -> pointAtLeftOf b
            Right b -> pointAtRightOf b
    newCEvents' =
        catMaybes
            [ pi >>= \pi' -> circleEvent pi' pj newp
            , pk >>= circleEvent newp pj
            ]
    toRemove = (pi, pj, pk)
    insert' ev@(CircleEvent pi pj pk y _) =
        PSQ.insert (pindex pi, pindex pj, pindex pk) y ev
    removed =
        case toRemove of
            (Just i, j, Just k) ->
                PSQ.delete (pindex i, pindex j, pindex k) cEvents
            _ -> cEvents
    newCEvents = foldr insert' removed newCEvents'
    newEvents =
        events' {newPointEvents = newPEvents, circleEvents = newCEvents}
    newEdges = Map.insert (sortPair idx (pindex pj)) EmptyEdge $ edges state

processEvent :: State -> State
processEvent state
    | (V.null . newPointEvents . events) state &&
          (PSQ.null . circleEvents . events) state = state
    | otherwise =
        if nextIsCircle
            then processCircleEvent state
            else processNewPointEvent state
  where
    (Point _ _ nextPointY) = V.head . newPointEvents . events $ state
    (Just (_, nextCircleY, _)) = PSQ.findMin . circleEvents . events $ state
    nextIsCircle
        | (V.null . newPointEvents . events) state = True
        | (PSQ.null . circleEvents . events) state = False
        | otherwise = nextCircleY <= nextPointY

{-  voronoi takes a `Vector` of pairs of `Double` and returns a `Vector` of
    `Edge` representing the corresponding voronoi diagram. -}
voronoi :: [Point'] -> [Edge']
voronoi = go . mkState
  where
    go :: State -> [Edge']
    go state =
        if (null . newPointEvents . events) state &&
           (null . circleEvents . events) state
            then mapToList . edges $ state
            else go (processEvent state)

mkState :: [Point'] -> State
mkState points = State (Events newPEvents PSQ.empty) firstPair firstEdge d
  where
    ps = sortOn snd points
    newPEvents' = V.imap (\i' (x, y) -> Point i' x y) . V.fromList $ ps
    newPEvents = V.tail . V.tail $ newPEvents'
    p0@(Point i _ _) = newPEvents' V.! 0
    p1@(Point j _ d) = newPEvents' V.! 1
    b1 = Breakpoint p0 p1
    b2 = Breakpoint p1 p0
    firstPair = Node Nil b1 $ Node Nil b2 Nil
    firstEdge = Map.singleton (sortPair i j) EmptyEdge

mapToList :: Map (Index, Index) Edge -> [Edge']
mapToList map = fmap edge' list
  where
    list' = Map.toList map
    predicate (_, e) =
        case e of
            Edge _ _ -> True
            _ -> False
    list = filter predicate list'
    edge' ((i, j), Edge l r) = Edge' i j l r
    edge' ((_, _), EmptyEdge) = undefined
    edge' ((_, _), IEdge _) = undefined
