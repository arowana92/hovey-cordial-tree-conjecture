import Std

namespace Cordial.DivisibleCut

/-- A tree or a nonempty list of children. The two natural indices are
    order and number of terminal vertices. Each child has nondivisible order. -/
inductive Assembly (k : Nat) : Bool → Nat → Nat → Prop where
  | leaf : Assembly k true 1 1
  | node : Assembly k false n l → Assembly k true (n+1) l
  | single : Assembly k true n l → ¬ k ∣ n → Assembly k false n l
  | cons : Assembly k true n l → ¬ k ∣ n → Assembly k false m t →
      Assembly k false (n+m) (l+t)

theorem size (k : Nat) (positive : 0 < k) (tree : Assembly k b n l) :
    if b then n ≤ k*l else n < k*l := by
  induction tree with
  | leaf => simp; omega
  | node _ ih => simp_all; omega
  | @single n l _ indiv ih =>
    simp at ih ⊢
    exact Nat.lt_of_le_of_ne ih (fun eq => indiv ⟨l,eq⟩)
  | cons _ _ _ ih rest =>
    simp_all [Nat.mul_add]
    omega

/-- At a leaf-rooted tree of at least two vertices, there is one fewer
    terminal than original leaves. Hall deletion gives L+2 ≤ s. -/
theorem bound (k n l s m : Nat) (positive : 0 < k) (leaves : 2 ≤ l)
    (tree : Assembly k true n (l-1)) (order : n = m*k+s)
    (_residue : 0 < s) (upper : s ≤ k) (hall : l+2 ≤ s) :
    m+2 ≤ l ∧ n ≤ k*(k-3) := by
  have h : n ≤ k*(l-1) := size k positive tree
  constructor
  · by_cases done : m+2 ≤ l
    · exact done
    · exfalso
      have big : l-1 ≤ m := by omega
      have := Nat.mul_le_mul_left k big
      rw [Nat.mul_comm k m] at this
      omega
  · exact Nat.le_trans h (Nat.mul_le_mul_left k (by omega))
end Cordial.DivisibleCut
