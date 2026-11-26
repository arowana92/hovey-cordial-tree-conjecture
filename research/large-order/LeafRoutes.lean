import Std

namespace LeafRoutes

-- Each integer jump prescribes the actual parent of a leaf labeled at its tail.
def hit (k bin x : Int) : Int := if x % k = bin then 1 else 0

def edgeMinusVertex (k bin start : Int) : List Int → Int
  | [] => 0
  | jump :: rest =>
    hit k bin (start + jump) - hit k bin start +
      edgeMinusVertex k bin (start + jump) rest

theorem pathHistogram (k bin start : Int) (jumps : List Int) :
    edgeMinusVertex k bin start jumps =
    hit k bin (start + jumps.sum) - hit k bin start := by
  induction jumps generalizing start with
  | nil => simp [edgeMinusVertex]
  | cons j js ih =>
    simp only [edgeMinusVertex, List.sum_cons, ih, Int.add_assoc]
    omega

def weightHits (k bin : Int) : List Int → List Int → Int
  | x :: xs, y :: ys => hit k bin (x + (y - x)) + weightHits k bin xs ys
  | _, _ => 0

theorem pairedHistogram (k bin : Int) (xs ys : List Int) (h : xs.length = ys.length) :
    weightHits k bin xs ys = (ys.map (hit k bin)).sum := by
  induction xs generalizing ys with
  | nil => cases ys <;> simp_all [weightHits]
  | cons x xs ih =>
    cases ys with
    | nil => simp at h
    | cons y ys =>
      simp only [List.length_cons, Nat.succ.injEq] at h
      have eq : x + (y - x) = y := by omega
      simp [weightHits, eq, ih ys h]

theorem reversalHistogram (k bin : Int) (xs : List Int) :
    weightHits k bin xs xs.reverse = (xs.map (hit k bin)).sum := by
  rw [pairedHistogram k bin xs xs.reverse (by simp)]
  simp [List.map_reverse, List.sum_reverse]

end LeafRoutes
