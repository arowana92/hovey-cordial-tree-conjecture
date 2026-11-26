import Std

namespace Cordial.RadiusTwo

/-- Integer coordinates within one parity class, centered at its chosen origin. -/
def stretch (d n x : Int) : Int :=
  if x ≤ -d then x - n else if d ≤ x then x + n else x

theorem stretch_injective (d n x z : Int) (hn : 0 ≤ n)
    (he : stretch d n x = stretch d n z) : x = z := by
  unfold stretch at he
  split at he <;> split at he <;> repeat first | split at he | omega

/-- The two omitted intervals each have length n, even if an outer part was empty. -/
theorem stretch_image (d n l u y : Int) (hd : 0 < d) (hn : 0 ≤ n)
    (hl : l ≤ 1-d) (hu : d-1 ≤ u) :
    (∃ x : Int, l ≤ x ∧ x ≤ u ∧ stretch d n x = y) ↔
      l-n ≤ y ∧ y ≤ u+n ∧ (y ≤ -d-n ∨ (-d < y ∧ y < d) ∨ d+n ≤ y) := by
  constructor
  · rintro ⟨x, hx, hxu, he⟩
    unfold stretch at he
    split at he
    · omega
    · split at he <;> omega
  · rintro ⟨hy, hyu, left | middle | right⟩
    · refine ⟨y+n, by omega, by omega, ?_⟩
      have h : y+n ≤ -d := by omega
      simp [stretch, h]
    · refine ⟨y, by omega, by omega, ?_⟩
      have h : ¬ y ≤ -d := by omega
      have k : ¬ d ≤ y := by omega
      simp [stretch, h, k]
    · refine ⟨y-n, by omega, by omega, ?_⟩
      have h : ¬ y-n ≤ -d := by omega
      have k : d ≤ y-n := by omega
      simp [stretch, h, k]

end Cordial.RadiusTwo
