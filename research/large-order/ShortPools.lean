import Std

namespace Cordial.ShortPools

/-- If a block of stride w fits nowhere, each residual run contains at most
    w vertices, including the free buffer at the start of the run. -/
theorem residual (runs : List Nat) (w : Nat) (h : ∀ r ∈ runs, r ≤ w) :
    runs.sum ≤ runs.length*w := by
  induction runs with
  | nil => simp
  | cons x xs ih =>
    have hx := h x (by simp)
    have hr := ih (fun y hy => h y (by simp [hy]))
    simp only [List.sum_cons, List.length_cons, Nat.succ_mul]
    omega

/-- The six block lengths have been charged for all possible failure stages.
    u is the stride sum already used; b counts pins and R counts runs. -/
theorem failed (k b R u w n : Nat) (_hk : 1 ≤ k) (hb : b ≤ 2*k)
    (hr : R+1 = b) (size : n ≤ b+u+R*w)
    (stage :
      (w=20 ∧ u+20 ≤ 20*k) ∨ (w=10 ∧ u+10 ≤ 30*k) ∨
      (w=8 ∧ u+8 ≤ 46*k) ∨ (w=6 ∧ u+6 ≤ 52*k) ∨
      (w=4 ∧ u+4 ≤ 56*k+8)) : n ≤ 66*k := by
  rcases stage with ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ <;> omega

theorem minimumFailed (k b R u w n : Nat) (_hk : 5 ≤ k) (hb : b+2 ≤ 2*k)
    (hr : R+1 = b) (size : n ≤ b+u+R*w)
    (stage :
      (w=20 ∧ u+20 ≤ 20*k) ∨ (w=10 ∧ u+10 ≤ 30*k) ∨
      (w=8 ∧ u+8 ≤ 46*k) ∨ (w=6 ∧ u+6 ≤ 52*k) ∨
      (w=4 ∧ u+4 ≤ 56*k+8)) : n < 66*k := by
  rcases stage with ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ | ⟨rfl, h⟩ <;> omega

end Cordial.ShortPools
