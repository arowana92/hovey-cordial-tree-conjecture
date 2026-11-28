import Std

namespace Cordial.CycleBlocks

def step (t i : Int) : Int :=
  if i < t then 2*t+1 else 2*(2*t+1)

def following (t i : Int) : Int :=
  if i = 2*t then 0 else i+1

def recipient (t i : Int) : Int :=
  if i < t then i+t+1 else i-t

/-- The bridge out of each block equals the missing wrap edge of its recipient. -/
theorem bridge (t i : Int) (_ht : 0 < t) (lo : 0 ≤ i) (hi : i ≤ 2*t) :
    i - step t i + following t i = 2 * recipient t i - step t (recipient t i) := by
  unfold following step recipient
  split <;> split <;> split <;> omega

/-- Every block gets precisely one such bridge, including the final wrap. -/
theorem recipient_bijection (t j : Int) (_ht : 0 < t) (lo : 0 ≤ j) (hi : j ≤ 2*t) :
    ∃ i, 0 ≤ i ∧ i ≤ 2*t ∧ recipient t i = j ∧
      ∀ x, 0 ≤ x → x ≤ 2*t → recipient t x = j → x = i := by
  by_cases h : j ≤ t
  · refine ⟨j+t, by omega, by omega, ?_, ?_⟩
    · unfold recipient
      split <;> omega
    · intro x hx hx' he
      unfold recipient at he
      split at he <;> omega
  · refine ⟨j-t-1, by omega, by omega, ?_, ?_⟩
    · unfold recipient
      split <;> omega
    · intro x hx hx' he
      unfold recipient at he
      split at he <;> omega

end Cordial.CycleBlocks
