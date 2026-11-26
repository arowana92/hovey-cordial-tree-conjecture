import Std

namespace FlexiblePath

-- The thirteen sums on the path use the twelve inserted entries and p+q.
theorem weights (p q u v : Int) :
    [p+u, u+v, v+(-u-v), (-u-v)+(p+u),
     (p+u)+(-p-q-u-v), (-p-q-u-v)+(q+v), (q+v)+(p-v),
     (p-v)+(-p-u), (-p-u)+(-q-v), (-q-v)+(q+u+v),
     (q+u+v)+(-u), (-u)+(u+v), (u+v)+q] =
    [p+u, u+v, -u, p-v, -q-v, -p-u, p+q,
     -u-v, -p-q-u-v, u, q+v, v, q+u+v] := by
  simp only [List.cons.injEq, and_true, true_and]
  omega

-- If h hard bins each charge strictly more than 2s across N columns of mass
-- at most s, the h bin equations leave room alongside the group equations.
theorem floatingRoom (h groups n : Nat) (hard : 2*h < n)
    (fractional : 2*groups ≤ n) : h+groups < n := by omega

theorem shrink (b terminals reduced : Nat) (hb : 4 ≤ b)
    (ht : 97*terminals ≤ b) (hr : reduced ≤ 1+24*terminals) :
    2*reduced ≤ b := by omega

end FlexiblePath
