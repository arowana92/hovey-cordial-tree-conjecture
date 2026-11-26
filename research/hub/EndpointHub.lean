import Std

namespace EndpointHub

theorem path (p l y : Int) :
    [p+(y-p), (y-p)+l, l+(-l), (-l)+(l+y-p)] =
    [y, l+y-p, 0, y-p] := by
  simp only [List.cons.injEq, and_true]
  omega

theorem threeArms (p l y : Int) :
    [p+(-p-l), (-p-l)+l, p+(l+y), (l+y)+(-l), p+(-p), (-p)+(p+l+y)] =
    [-l, -p, p+l+y, y, 0, l+y] := by
  simp only [List.cons.injEq, and_true]
  omega

theorem fiveSites (p l y : Int) :
    [p+l, l+(-l), (-l)+(y-p), l+(y-p-l), (y-p-l)+(p+l)] =
    [p+l, 0, y-p-l, y-p, y] := by
  simp only [List.cons.injEq, and_true, true_and]
  omega

theorem bareFork (p l y : Int) :
    [p+(-l), (-l)+l, l+(y-p), (-l)+(l+y-p), (l+y-p)+(p-l)] =
    [p-l, 0, l+y-p, y-p, y] := by
  simp only [List.cons.injEq, and_true]
  omega

theorem largeFork (p l y : Int) :
    [p+(y-l), (y-l)+l, p+(-p), (-p)+(p+y-l)] =
    [p+y-l, y, 0, y-l] := by
  simp only [List.cons.injEq, and_true]
  omega

theorem separated (p l y : Int) (hy : 0 < y) (hp : y < p)
    (hl : p+(p-y) < l) :
    -l < p-l ∧ p-l < -(p-y) ∧ -(p-y) < 0 ∧ 2*(p-y) < l := by omega

theorem firstPair (p l y : Int) (hy : 0 < y) (hp : y < p)
    (hl : p+(p-y) < l) :
    -l < -l+(p-y) ∧ -l+(p-y) < -(p-y) ∧
    -l-(l+y)+(p-y) < -l-(p-y) := by omega

-- Final gaps differ by the period l+y. An intermediate position is inside
-- the interval from its preceding final gap to the preceding gap's successor.
theorem pairStep (g z l y : Int) (hz : 0 < z) (hs : z < l+y) :
    g-(l+y) < g-(l+y)+z ∧ g-(l+y)+z < g ∧ g < g+z ∧
    (g+z)-(l+y+z)=g-(l+y) := by omega

end EndpointHub
