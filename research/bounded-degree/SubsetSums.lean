import Std

/- The sums of t distinct integers in [1,t+w] cover every integer between
   their possible minimum and maximum, including both endpoints. -/
namespace Cordial.Projection

def total (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | t + 1 => total f t + f t

private theorem total_congr (f g : Nat → Nat) (t : Nat)
    (h : ∀ i < t, f i = g i) : total f t = total g t := by
  induction t with
  | zero => rfl
  | succ t ih =>
    simp only [total, ih (fun i hi => h i (by omega)), h t (by omega)]

private theorem total_zero (t : Nat) : total (fun _ => 0) t = 0 := by
  induction t with
  | zero => rfl
  | succ t ih => simp [total, ih]

private theorem offsets (t w h : Nat) (bound : h ≤ t * w) :
    ∃ f : Nat → Nat, (∀ i < t, f i ≤ w) ∧
      (∀ i j, i ≤ j → j < t → f i ≤ f j) ∧ total f t = h := by
  induction t generalizing h with
  | zero =>
    simp at bound
    exact ⟨fun _ => 0, by omega, by omega, by simp [total, bound]⟩
  | succ t ih =>
    rw [Nat.succ_mul] at bound
    by_cases small : h ≤ w
    · let f := fun i => if i < t then 0 else h
      refine ⟨f, ?_, ?_, ?_⟩
      · intro i _
        simp only [f]
        split <;> omega
      · intro i j hij hj
        simp only [f]
        split <;> split <;> omega
      · have eq := total_congr f (fun _ => 0) t (fun i hi => by simp [f, hi])
        simp [total, eq, total_zero, f]
    · obtain ⟨g, gb, gm, gs⟩ := ih (h - w) (by omega)
      let f := fun i => if i < t then g i else w
      refine ⟨f, ?_, ?_, ?_⟩
      · intro i _
        by_cases hi : i < t <;> simp [f, hi, gb]
      · intro i j hij hj
        by_cases hj' : j < t
        · have hi : i < t := by omega
          simpa [f, hi, hj'] using gm i j hij hj'
        · by_cases hi : i < t <;> simp [f, hi, hj', gb]
      · have eq := total_congr f g t (fun i hi => by simp [f, hi])
        simp [total, eq, gs, f]
        omega

private theorem total_add (f g : Nat → Nat) (t : Nat) :
    total (fun i => f i + g i) t = total f t + total g t := by
  induction t with
  | zero => rfl
  | succ t ih => simp only [total, ih]; omega

theorem interval_subset_sums (t w h : Nat) (bound : h ≤ t * w) :
    ∃ a : Nat → Nat, (∀ i < t, 1 ≤ a i ∧ a i ≤ t + w) ∧
      (∀ i j, i < j → j < t → a i < a j) ∧
      total a t = total (fun i => i + 1) t + h := by
  obtain ⟨f, fb, fm, fs⟩ := offsets t w h bound
  refine ⟨fun i => (i + 1) + f i, ?_, ?_, ?_⟩
  · intro i hi
    change 1 ≤ i + 1 + f i ∧ i + 1 + f i ≤ t + w
    have := fb i hi
    omega
  · intro i j hij hj
    change i + 1 + f i < j + 1 + f j
    have := fm i j (by omega) hj
    omega
  · rw [total_add (fun i => i + 1) f t, fs]

end Cordial.Projection
