import Std

namespace ModularLayer

def weights (p : Int) : List Int → List Int
  | [] => []
  | x :: xs => (p + x) :: weights x xs

-- The first path vertex has label X+c. The old path of prescribed
-- displacements has net change [X+e]-[X].
def arrivals (X c e : Int) : List Int :=
  [X+e, -3*X-c-2*e, 2*X+c+e, 2*X+e, -X-e, -2*X-c-e, 4*X+c+2*e]

theorem actualSums (X c e : Int) :
    weights (X+c) (arrivals X c e) =
      [2*X+c+e, -2*X-c-e, -X-e, 4*X+c+2*e, X, -3*X-c-2*e, 2*X+e] := by
  simp only [weights, arrivals, List.cons.injEq, and_true]
  omega

theorem cancelLayer (X c e : Int) :
    ((X+e) :: weights (X+c) (arrivals X c e)).Perm
      (X :: arrivals X c e) := by
  rw [actualSums, List.perm_iff_count]
  intro y
  simp only [arrivals, List.count_cons, List.count_nil]
  omega

theorem cancelModulo (k X c e : Int) :
    (((X+e) :: weights (X+c) (arrivals X c e)).map (fun y => y % k)).Perm
      ((X :: arrivals X c e).map (fun y => y % k)) :=
  (cancelLayer X c e).map _

-- This is the only repeated slope within the correction path.
theorem repeatedSlope (X c e : Int) :
    (2*X+c+e)-(2*X+e) = c := by omega

end ModularLayer
