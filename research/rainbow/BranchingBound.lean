import Std

namespace Cordial.BranchingBound

/-- Extend a component up its connector by single vertices. Every intermediate
    order occurs at an edge cut, so a forbidden multiple cannot be crossed. -/
theorem connector (start extra target : Nat) (small : start < target)
    (cuts : ∀ r ≤ extra, start + r ≠ target) : start + extra < target := by
  by_cases h : start+extra < target
  · exact h
  have bad := cuts (target-start) (by omega)
  omega

/-- Sum the orders below all child connectors against their branching counts. -/
theorem children (k : Nat) (segments : List (Nat × Nat))
    (bounds : ∀ v ∈ segments, v.2 ≤ v.1*k) :
    (segments.map Prod.snd).sum ≤ (segments.map Prod.fst).sum*k := by
  induction segments with
  | nil => simp
  | cons v vs ih =>
    have hv := bounds v (by simp)
    have hs := ih (fun w hw => bounds w (by simp [hw]))
    simp only [List.map_cons, List.sum_cons, Nat.add_mul]
    omega

/-- At a branching root the terminal paths and the root itself use at most t
    vertices. The child components contain b other branching vertices. -/
theorem order (k m t b n : Nat) (order_eq : n = m*k+1+t)
    (bound : n ≤ b*k+t) (remainder : t < k) : m < b ∧ n ≤ b*k := by
  have hm : m < b := by
    by_cases h : b ≤ m
    · have := Nat.mul_le_mul_right k h
      omega
    omega
  have hs : m+1 ≤ b := hm
  have h := Nat.mul_le_mul_right k hs
  rw [Nat.succ_mul] at h
  omega

theorem twentySix (m s b leaves n : Nat) (order_eq : n = 26*m+s)
    (residue : s ≤ 26) (branches : m+2 ≤ b) (degree_sum : b+2 ≤ leaves)
    (leaf_bound : leaves+2 ≤ s) : n ≤ 546 := by omega

end Cordial.BranchingBound
