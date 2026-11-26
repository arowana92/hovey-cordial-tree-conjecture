import Std

namespace UniversalHub

-- Vertex and edge multisets in the proof are listed in encounter order.
theorem pathForward (p l : Int) (hp : 0 < p) (hl : p < l) :
    [p + (-p-l), (-p-l) + l, l + (-l), (-l) + (-p)] =
    [-l, -p, 0, -p-l] ∧ -p-l < -l ∧ -l < -p ∧ -p < 0 ∧ 0 < l := by
  simp only [List.cons.injEq, and_true]
  omega

theorem pathReverse (p l : Int) (hp : 0 < p) (hl : p < l) :
    [p + (-p-l), (-p-l) + (-l), (-l) + l, l + (-p-2*l)] =
    [-l, -p-2*l, 0, -p-l] ∧ -p-2*l < -p-l ∧ -p-l < -l ∧ -l < 0 ∧ 0 < l := by
  simp only [List.cons.injEq, and_true]
  omega

theorem arms (p l : Int) (hp : 0 < p) (hl : p < l) :
    [p + (-p-l), (-p-l) + l, p + (-p), (-p) + (-l)] =
    [-l, -p, 0, -p-l] ∧ -p-l < -l ∧ -l < -p ∧ -p < 0 ∧ 0 < l := by
  simp only [List.cons.injEq, and_true]
  omega

theorem firstLeaf (g q l : Int) (hg : 0 < g) (hq : q ≤ -l) :
    l < g-q ∧ q+(g-q)=g := by omega

theorem subsequentLeaf (g q : Int) (hq : q < 0) :
    g < g-q ∧ q+(g-q)=g := by omega

theorem pairedLeaves (l top : Int) (hl : 0 < l) :
    top < top+1 ∧ top+1 < top+1+l ∧ l+(top+1)=top+1+l ∧
    (-l)+(top+1+l)=top+1 := by omega

end UniversalHub
