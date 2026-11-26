import Std

namespace Cordial.PartialRotation

/-- The complement consists of the rises of this integer staircase. -/
def rise (n m ρ x : Int) : Prop :=
  (m*x + ρ)/n < (m*(x+1) + ρ)/n

theorem rotate_phase (n m ρ x a j : Int) (hn : 0 < n) :
    rise n m (ρ - m*a + j*n) (x+a) ↔ rise n m ρ x := by
  have step (z : Int) :
      (m*(z+a) + (ρ - m*a + j*n))/n = (m*z+ρ)/n + j := by
    rw [show m*(z+a) + (ρ - m*a + j*n) = (m*z+ρ) + j*n by
      rw [Int.mul_add]; omega, Int.add_mul_ediv_right _ _ (by omega)]
  unfold rise
  rw [show x+a+1 = x+1+a by omega, step, step]
  omega

/-- floor((nz-ρ-1)/m) is the position of rise number z. -/
def position (nz ρ m : Int) : Int := (nz-ρ-1)/m

theorem position_le (nz ρ σ m k : Int) (hm : 0 < m) (h : ρ-σ ≤ k*m) :
    position nz σ m ≤ position nz ρ m + k := by
  unfold position
  rw [← Int.add_mul_ediv_right _ _ (by omega : m ≠ 0)]
  apply Int.ediv_le_ediv hm
  omega

theorem upper_displacements (nz ρ σ n m : Int) (hm : 0 < m) (size : n ≤ 2*m)
    (short₁ : 2*(ρ-σ) ≤ n) (short₂ : 2*(σ-ρ) ≤ n) :
    -1 ≤ position nz σ m - position nz ρ m ∧
      position nz σ m - position nz ρ m ≤ 1 := by
  have f := position_le nz ρ σ m 1 hm (by omega)
  have g := position_le nz σ ρ m 1 hm (by omega)
  omega

theorem lower_parent_labels (nz ρ σ n m : Int) (hm : 0 < m) (size : n ≤ 2*m)
    (forward : ρ ≤ σ) (phase : σ-ρ ≤ n) :
    -1 ≤ 1 + position nz σ m - position nz ρ m ∧
      1 + position nz σ m - position nz ρ m ≤ 1 := by
  have f := position_le nz ρ σ m 0 hm (by omega)
  have g := position_le nz σ ρ m 2 hm (by omega)
  omega

end Cordial.PartialRotation
