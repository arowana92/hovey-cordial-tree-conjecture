import Std

namespace Cordial.TwoHubGaps

/-- The parent label is zero below the blocked weight and one above it. -/
def weight (w x : Int) : Int := if x < w then x else x + 1

theorem injective (w x z : Int) (h : weight w x = weight w z) : x = z := by
  unfold weight at h
  split at h <;> split at h <;> omega

theorem fills_gap (l w u y : Int) (hl : l < w) (hu : w ≤ u) :
    (∃ x : Int, l < x ∧ x < u ∧ weight w x = y) ↔ l < y ∧ y ≤ u ∧ y ≠ w := by
  constructor
  · rintro ⟨x, hx, hxu, he⟩
    unfold weight at he
    split at he <;> omega
  · rintro ⟨hy, hyu, hn⟩
    by_cases h : y < w
    · exact ⟨y, hy, by omega, by simp [weight, h]⟩
    · refine ⟨y-1, by omega, by omega, ?_⟩
      have he : ¬ y-1 < w := by omega
      simp [weight, he]

end Cordial.TwoHubGaps
