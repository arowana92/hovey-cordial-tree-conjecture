import Std

namespace Cordial.DeficitIntervals

/-- The residue x is a multiple of the step, with multiplier in [lo,hi]. -/
def Near (modulus step x lo hi : Int) : Prop :=
  ∃ i : Int, lo ≤ i ∧ i ≤ hi ∧ modulus ∣ x-step*i

private theorem difference
    (u : Near n step x l r) (v : Near n step y s t) :
    Near n step (y-x) (s-r) (t-l) := by
  obtain ⟨i,il,ir,di⟩ := u
  obtain ⟨j,jl,jr,dj⟩ := v
  refine ⟨j-i, by omega, by omega, ?_⟩
  have eq : (y-x)-step*(j-i) = (y-step*j)-(x-step*i) := by
    rw [Int.mul_sub]; omega
  rw [eq]
  exact Int.dvd_sub dj di

private theorem disjoint
    (period : ∀ j : Int, 0 < j → j ≤ cap → ¬ n ∣ step*j)
    (a : Near n step x l r) (b : Near n step x s t)
    (sep : r < s) (width : t-l ≤ cap) : False := by
  obtain ⟨i,il,ir,di⟩ := a
  obtain ⟨j,jl,jr,dj⟩ := b
  apply period (j-i) (by omega) (by omega)
  have eq : step*(j-i) = (x-step*i)-(x-step*j) := by
    rw [Int.mul_sub]; omega
  rw [eq]
  exact Int.dvd_sub di dj

/-- Three failed bridge placements force the step to have order at most 3h
    after quotienting out their three small directions. -/
theorem three_placements (n step h x y : Int) (positive : 1 ≤ h)
    (first : Near n step x (1-h) 0 ∨ Near n step y (-h) (-1))
    (last : Near n step x 1 h ∨ Near n step y (h+1) (2*h))
    (low : Near n step (y-x) 0 (h-1) ∨ Near n step y 0 h) :
    ∃ j : Int, 0 < j ∧ j ≤ 3*h ∧ n ∣ step*j := by
  apply Classical.byContradiction
  intro no
  have period : ∀ j : Int, 0 < j → j ≤ 3*h → ¬ n ∣ step*j :=
    fun j hj bound div => no ⟨j,hj,bound,div⟩
  rcases first with a | a <;> rcases last with b | b
  · exact disjoint period a b (by omega) (by omega)
  · rcases low with c | c
    · exact disjoint period c (difference a b) (by omega) (by omega)
    · exact disjoint period c b (by omega) (by omega)
  · rcases low with c | c
    · exact disjoint period (difference b a) c (by omega) (by omega)
    · exact disjoint period a c (by omega) (by omega)
  · exact disjoint period a b (by omega) (by omega)

end Cordial.DeficitIntervals
