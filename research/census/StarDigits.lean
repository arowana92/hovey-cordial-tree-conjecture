import Std

namespace Cordial.StarDigits

/-- Opposite sides of a spoke use i and i+t reduced modulo 2t+1. -/
def other (t i : Nat) : Nat := if i ≤ t then i+t else i-t-1

theorem spoke_bounds (t i : Nat) (hi : i ≤ 2*t) :
    t ≤ i+other t i ∧ i+other t i ≤ 3*t := by
  simp only [other]
  split <;> omega

theorem spoke_unique (t i j : Nat)
    (h : i+other t i = j+other t j) : i=j := by
  unfold other at h
  split at h <;> split at h <;> omega

theorem spoke_covers (t y : Nat) (hlo : t ≤ y) (hhi : y ≤ 3*t) :
    ∃ i ≤ 2*t, i+other t i=y := by
  by_cases even : (y-t)%2=0
  · refine ⟨(y-t)/2, by omega, ?_⟩
    unfold other
    split <;> omega
  · refine ⟨t+1+(y-t-1)/2, by omega, ?_⟩
    unfold other
    split <;> omega

/-- Two edge carries sharing an endpoint differ by at most one. -/
theorem shared_carry (q x z a c d r s : Int)
    (hq : 0 < q) (hx : 0 ≤ x ∧ x < q) (hz : 0 ≤ z ∧ z < q)
    (hr : 0 ≤ r ∧ r < q) (hs : 0 ≤ s ∧ s < q)
    (h₁ : x+a=q*c+r) (h₂ : z+a=q*d+s) :
    c ≤ d+1 ∧ d ≤ c+1 := by
  constructor
  · apply Int.le_of_not_gt
    intro h
    have he : 2 ≤ c-d := by omega
    have hm := Int.mul_le_mul_of_nonneg_left he (Int.le_of_lt hq)
    rw [Int.mul_sub] at hm
    omega
  · apply Int.le_of_not_gt
    intro h
    have he : 2 ≤ d-c := by omega
    have hm := Int.mul_le_mul_of_nonneg_left he (Int.le_of_lt hq)
    rw [Int.mul_sub] at hm
    omega

end Cordial.StarDigits
