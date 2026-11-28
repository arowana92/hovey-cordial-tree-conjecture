import Std

namespace Cordial.SeparatedPins

/-- If no clean run has the requested length, their total is bounded. -/
private theorem sumBound (xs : List Nat) (cap : Nat)
    (h : ∀ x ∈ xs, x ≤ cap) : xs.sum ≤ xs.length * cap := by
  induction xs with
  | nil => simp
  | cons x rest ih =>
    have hx := h x (by simp)
    have hr := ih (fun y hy => h y (by simp [hy]))
    simp only [List.sum_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

/-- A segment with at most the permitted number of dirty vertices contains a
    long enough run for an aligned bridge. The nondivisible case may need k+2. -/
theorem cleanRun (k d c t : Nat) (runs : List Nat)
    (kinds : k = 8 ∨ k = 9)
    (far : 2*k*k-k+1 ≤ d) (lengths : runs.length = c+1)
    (partition : runs.sum+c+1 = d)
    (regime : (c ≤ k-1 ∧ t = k) ∨ (c ≤ k-2 ∧ t ≤ k+2)) :
    ∃ r ∈ runs, t+k-1 ≤ r := by
  apply Classical.byContradiction
  intro missing
  have bounded := sumBound runs (t+k-2) (fun x hx => by
    have small : ¬ t+k-1 ≤ x := fun big => missing ⟨x, hx, big⟩
    omega)
  rw [lengths] at bounded
  rcases kinds with rfl | rfl <;> rcases regime with h | h
  · obtain ⟨hc, rfl⟩ := h; omega
  · have scale := Nat.mul_le_mul (by omega : c+1 ≤ 7) (by omega : t+8-2 ≤ 16)
    omega
  · obtain ⟨hc, rfl⟩ := h; omega
  · have scale := Nat.mul_le_mul (by omega : c+1 ≤ 8) (by omega : t+9-2 ≤ 18)
    omega

/-- Select the first vertex of a bridge so the left component is divisible. -/
theorem aligned (k n t r : Int) (kinds : k = 8 ∨ k = 9)
    (long : t+k-1 ≤ r) :
    ∃ i : Int, 0 ≤ i ∧ i < k ∧ i+t ≤ r ∧ (n+i)%k = 0 := by
  rcases kinds with rfl | rfl
  · exact ⟨(-n)%8, by omega, by omega, by omega, by omega⟩
  · exact ⟨(-n)%9, by omega, by omega, by omega, by omega⟩

end Cordial.SeparatedPins
