import Std

namespace Cordial.Dyadic

/-- Mass and ordinary first moment of a consecutive integer list. -/
def stats : List Int → Int × Int
  | [] => (0, 0)
  | x :: xs => let (s, m) := stats xs; (x + s, m + s)

theorem shift_right (v : List Int) :
    stats (0 :: v) = ((stats v).1, (stats v).2 + (stats v).1) := by
  simp [stats]

/-- Reconstruct the ordinary mass and moment from two parity fibers. -/
def interleave : List (Int × Int) → List Int
  | [] => []
  | (a,b) :: tail => a :: b :: interleave tail

theorem parity_stats (v : List (Int × Int)) :
    let e := stats (v.map Prod.fst)
    let o := stats (v.map Prod.snd)
    stats (interleave v) = (e.1 + o.1, 2*(e.2 + o.2) + o.1) := by
  induction v with
  | nil => decide
  | cons pair tail ih =>
    rcases pair with ⟨a,b⟩
    simp only [List.map_cons, interleave, stats, ih]
    apply Prod.ext <;> simp <;> omega

/-- The even differential contributes the even flow's moment minus the odd
    flow's shifted moment. A mass-zero correction of that remaining moment
    also fixes the odd fiber, with signed integer floor division. -/
theorem constrained_split (e o E O A B : Int)
    (mass : e+o=0) (moment : 2*(E+O)+o=0) :
    let a := (-e)/2
    let b := (-o)/2
    let z := -(E+A-(B+b))
    a+b=0 ∧ e+a-b=0 ∧ o+b-a=0 ∧
      E+(A+z)-(B+b)=0 ∧ O+B-(A+z)=0 := by
  dsimp
  omega

theorem free_split (e o : Int) (mass : e+o=0) :
    let a := (-e)/2
    let b := (-o)/2
    e+a-b=0 ∧ o+b-a=0 := by
  dsimp
  omega

end Cordial.Dyadic
