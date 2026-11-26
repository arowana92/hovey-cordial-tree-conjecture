import Std

namespace GapPath

-- The list contains the new vertices from the boundary p outwards.
def sites (p s t : Int) : List Int :=
  [t, -p-2*t, p+t, s+t, -t, -p-t, p+s+2*t]

def weights (p : Int) : List Int → List Int
  | [] => []
  | x :: xs => (p+x) :: weights x xs

theorem actualWeights (p s t : Int) :
    weights p (sites p s t) = [p+t,-p-t,-t,p+s+2*t,s,-p-2*t,s+t] := by
  simp only [weights, sites, List.cons.injEq, and_true, true_and]
  omega

theorem multisetIdentity (p s t : Int) :
    (t :: weights p (sites p s t)).Perm (s :: sites p s t) := by
  rw [actualWeights, List.perm_iff_count]
  intro x
  simp only [sites, List.count_cons, List.count_nil]
  omega

end GapPath
