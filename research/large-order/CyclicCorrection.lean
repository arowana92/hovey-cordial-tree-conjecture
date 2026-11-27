import Std

namespace Cordial.LargeOrder

def total (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n+1 => total f n + f n

def moment (f : Nat → Int) (k : Nat) : Int :=
  total (fun i => (i : Int) * f i) k

theorem sum_prefix (f : Nat → Int) (k : Nat) :
    total (fun j => total f (j+1)) k = (k : Int) * total f k - moment f k := by
  induction k with
  | zero => simp [total, moment]
  | succ k ih =>
    have cast : ((k+1 : Nat) : Int) = (k : Int)+1 := by omega
    simp only [total, moment, cast, Int.add_mul, Int.mul_add, Int.one_mul] at ih ⊢
    omega

theorem sum_complement (f : Nat → Int) (c : Int) (k : Nat) :
    total (fun j => c-f j) k = (k : Int)*c-total f k := by
  induction k with
  | zero => simp [total]
  | succ k ih =>
    have cast : ((k+1 : Nat) : Int) = (k : Int)+1 := by omega
    simp only [total, cast, Int.add_mul, Int.one_mul] at ih ⊢
    omega

/-- Every zero-mass integer vector of zero moment modulo k is a cyclic
    difference of a zero-mass integer vector. -/
theorem correct (z : Nat → Int) (k : Nat) (hk : 0 < k)
    (zero : total z k = 0) (divides : (k : Int) ∣ moment z k) :
    ∃ h : Nat → Int, total h k = 0 ∧
      ∀ j < k, (if j = 0 then h (k-1) else h (j-1)) - h j = z j := by
  obtain ⟨t, ht⟩ := divides
  refine ⟨fun j => -t-total z (j+1), ?_, ?_⟩
  · rw [sum_complement, sum_prefix, zero, ht, Int.mul_neg, Int.mul_zero]
    omega
  · intro j hj
    cases j with
    | zero =>
      have hlast : k-1+1 = k := by omega
      simp only [ite_true, hlast, zero]
      simp [total] <;> omega
    | succ j =>
      simp [total] <;> omega

/-- On several equal-length cycles only the aggregate moment needs to vanish
modulo the length. The primitive is required to have zero total over all cycles. -/
theorem correct_cycles (z : Nat → Nat → Int) (g m : Nat) (hg : 0 < g) (hm : 0 < m)
    (zero : ∀ r < g, total (z r) m = 0)
    (divides : (m : Int) ∣ total (fun r => moment (z r) m) g) :
    ∃ h : Nat → Nat → Int, total (fun r => total (h r) m) g = 0 ∧
      ∀ r < g, ∀ j < m,
        (if j = 0 then h r (m-1) else h r (j-1)) - h r j = z r j := by
  obtain ⟨t, ht⟩ := divides
  let c : Nat → Int := fun r => if r = 0 then -t else 0
  let h : Nat → Nat → Int := fun r j => c r - total (z r) (j+1)
  have row (r : Nat) (hr : r < g) :
      total (h r) m = (m : Int) * c r + moment (z r) m := by
    simp [h, sum_complement, sum_prefix, zero r hr]
  have sums (n : Nat) (hn : n ≤ g) :
      total (fun r => total (h r) m) n = total (fun r => moment (z r) m) n +
        (if n = 0 then 0 else -(m : Int)*t) := by
    induction n with
    | zero => simp [total]
    | succ n ih =>
      have hr : n < g := by omega
      have prev := ih (by omega)
      simp only [total, Nat.succ_ne_zero, ite_false, row n hr, prev]
      cases n with
      | zero => simp [c, total, Int.mul_neg, Int.neg_mul, Int.add_comm]
      | succ n => simp [c, Int.add_comm, Int.add_left_comm]
  refine ⟨h, ?_, ?_⟩
  · rw [sums g (Nat.le_refl _), ht, ite_eq_right (Nat.ne_of_gt hg), Int.neg_mul]
    omega
  · intro r hr j hj
    cases j with
    | zero =>
      have last : m-1+1 = m := by omega
      simp only [h, ite_true, last, zero r hr]
      simp [total] <;> omega
    | succ j => simp [h, total] <;> omega

end Cordial.LargeOrder
