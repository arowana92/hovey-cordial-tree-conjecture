import Std

namespace MarkedLeafBlocks

/-- The upper triple, lower triple, lower pair and upper singleton use every reserve. -/
theorem exact_reserve (E B a b c : Int) (hB : 8 * (E + 1) ≤ B)
    (ha : B - E ≤ a ∧ a ≤ B) (hb : B - E ≤ b ∧ b ≤ B)
    (hc : B - E ≤ c ∧ c ≤ B) :
    ∃ x y z w : Int, 0 ≤ x ∧ 0 ≤ y ∧ 0 ≤ z ∧ 0 ≤ w ∧
      2*x+y = a ∧ z+w = b ∧ x+2*y+z = c := by
  let x := (2*a-c+2)/3
  let y := a-2*x
  let z := c-2*a+3*x
  refine ⟨x, y, z, b-z, ?_⟩
  dsimp [x, y, z]
  omega

/-- In either ordering of three parents, both moment slacks control the smaller masses. -/
theorem ordered_moment (A B C : Int) (h₁ : C ≤ B) (h₂ : B ≤ A) (h₃ : 0 ≤ C) :
    let W := if 3*B ≤ 2*A then 2*B-C else 2*B-A
    B+C ≤ 4*W ∧ B+C ≤ 4*(A+B+C-W) := by
  dsimp
  split <;> omega

end MarkedLeafBlocks
