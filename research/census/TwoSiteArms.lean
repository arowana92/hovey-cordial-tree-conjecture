import Std

namespace Cordial.TwoSiteArms

/-- Directed displacement of doubling on an odd interval of slots. -/
def jump (h i : Int) : Int := if i ≤ h then i else i-(2*h+1)

theorem jump_range (h i : Int) (hi : 0 ≤ i ∧ i ≤ 2*h) :
    -h ≤ jump h i ∧ jump h i ≤ h := by
  unfold jump
  split <;> omega

theorem jump_inj (h i j : Int) (hi : 0 ≤ i ∧ i ≤ 2*h)
    (hj : 0 ≤ j ∧ j ≤ 2*h) (same : jump h i = jump h j) : i = j := by
  unfold jump at same
  split at same <;> split at same <;> omega

theorem jump_onto (h d : Int) (hd : -h ≤ d ∧ d ≤ h) :
    ∃ i, (0 ≤ i ∧ i ≤ 2*h) ∧ jump h i = d := by
  by_cases pos : 0 ≤ d
  · exact ⟨d, by omega, by simp [jump, hd.2]⟩
  · refine ⟨d+2*h+1, by omega, ?_⟩
    unfold jump
    split <;> omega

theorem image_onto (h y : Int) (hy : 0 ≤ y ∧ y ≤ 2*h) :
    ∃ i, (0 ≤ i ∧ i ≤ 2*h) ∧ i + jump h i = y := by
  by_cases even : y % 2 = 0
  · refine ⟨y/2, by omega, ?_⟩
    unfold jump
    split <;> omega
  · refine ⟨y/2+h+1, by omega, ?_⟩
    unfold jump
    split <;> omega

/-- The positive outer interval supplies the new tip labels and tip weights. -/
theorem shell (r s x : Int) (hr : 0 ≤ r) (hs : 0 ≤ s) :
    (-r-s ≤ x ∧ x ≤ r+3*s) ↔
    (-r ≤ x ∧ x ≤ r) ∨ (-r-s ≤ x ∧ x < -r) ∨
    (r < x ∧ x ≤ r+s) ∨ (r+s < x ∧ x ≤ r+3*s) := by omega

end Cordial.TwoSiteArms
