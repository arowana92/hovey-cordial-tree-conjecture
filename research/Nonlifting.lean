import Std

namespace Cordial.Lifts

/-- If the weighted sum of parent labels vanishes modulo s*k and the usual
    parent has label k*h, replacing it once forces the same parent label. -/
theorem one_exception (s k h b : Int) (hs : 0 < s) (hk : 0 < k)
    (lo : 0 ≤ k*h) (hi : k*h < s*k) (blo : 0 ≤ b) (bhi : b < s*k)
    (balance : s*k ∣ (s-1)*(k*h) + b) : b = k*h := by
  obtain ⟨t, ht⟩ := balance
  have eq : b - k*h = s*k * (t-h) := by
    rw [Int.sub_mul, Int.one_mul, ← Int.mul_assoc] at ht
    rw [Int.mul_sub]
    omega
  have pos : 0 < s*k := Int.mul_pos hs hk
  by_cases less : t < h
  · have hle : t - h ≤ -1 := by omega
    have bound := Int.mul_le_mul_of_nonneg_left hle (Int.le_of_lt pos)
    rw [Int.mul_neg, Int.mul_one] at bound
    omega
  by_cases more : h < t
  · have hle : 1 ≤ t - h := by omega
    have bound := Int.mul_le_mul_of_nonneg_left hle (Int.le_of_lt pos)
    rw [Int.mul_one] at bound
    omega
  have same : t-h = 0 := by omega
  simp [same] at eq
  omega

end Cordial.Lifts
