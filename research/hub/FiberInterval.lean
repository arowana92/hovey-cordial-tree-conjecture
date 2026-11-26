import Std

namespace Cordial.FiberInterval

/-- Digits are measured from the omitted weight. Digits below the occupied
vertex digit advance by one, and those above it stay in place. -/
def target (occupied digit : Nat) : Nat :=
  if digit < occupied then digit + 1 else digit

theorem exact {d occupied : Nat} (h : occupied < d) (weight : Nat) :
    (0 < weight ∧ weight < d) ↔
    ∃ digit, (digit < d ∧ digit ≠ occupied ∧ target occupied digit = weight) ∧
      ∀ other, other < d → other ≠ occupied → target occupied other = weight →
        other = digit := by
  constructor
  · intro hw
    by_cases left : weight ≤ occupied
    · refine ⟨weight - 1, ⟨by omega, by omega, ?_⟩, ?_⟩
      · simp only [target]
        split <;> omega
      · intro other ho hn hm
        simp only [target] at hm
        split at hm <;> omega
    · refine ⟨weight, ⟨hw.2, by omega, ?_⟩, ?_⟩
      · simp only [target]
        split <;> omega
      · intro other ho hn hm
        simp only [target] at hm
        split at hm <;> omega
  · rintro ⟨digit, ⟨hd, hn, hm⟩, _⟩
    simp only [target] at hm
    split at hm <;> omega

end Cordial.FiberInterval
