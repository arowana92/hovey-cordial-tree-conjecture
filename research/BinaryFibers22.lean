import Std

namespace Cordial.BinaryFibers22

/-- The high-bit change of the two chord sums at midpoint a in Z/11. -/
def equation (x a : Nat) : Nat :=
  let bit (i : Nat) := x.testBit (i % 11)
  ((bit (a+10) ^^ bit (a+1)) ^^ (bit (a+8) ^^ bit (a+3))).toNat

/-- The second chord at midpoint zero is omitted. Fix the highest vertex bit at zero. -/
def syndrome (x : Nat) : Nat :=
  (List.range 10).foldl (fun z i => z + equation x (i+1) * 2^i) 0

-- Every possible ten-bit right hand side has a witness.
theorem covers :
    ((List.range 1024).map syndrome).mergeSort = List.range 1024 := by native_decide

theorem exists_flip (b : Nat) (hb : b < 1024) : ∃ x < 1024, syndrome x = b := by
  have h : b ∈ List.range 1024 := List.mem_range.mpr hb
  rw [← covers] at h
  have hp := List.mergeSort_perm ((List.range 1024).map syndrome) (fun a b => decide (a ≤ b))
  have hm := hp.mem_iff.mp h
  obtain ⟨x, hx, he⟩ := List.mem_map.mp hm
  exact ⟨x, List.mem_range.mp hx, he⟩

end Cordial.BinaryFibers22
