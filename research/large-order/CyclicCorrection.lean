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
      simp only [if_true, hlast, zero]
      simp [total] <;> omega
    | succ j =>
      simp [total] <;> omega

end Cordial.LargeOrder
