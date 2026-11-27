import Std

namespace Cordial.MatchedArms

/-- Index of the arm whose joining edge must weigh 2*t. -/
def arm (h t : Int) : Int :=
  if t ≤ h + h / 2 then h + 2 * (t - h)
  else if t ≤ 2 * h then h - (2 * (2 * h + 1 - t) - 1)
  else if t ≤ 2 * h + (h + 1) / 2 then h + (2 * (t - 2 * h) - 1)
  else h - 2 * (3 * h + 1 - t)

/-- Number of upper endpoints on the joining edge. -/
def level (h t : Int) : Int :=
  if t ≤ h + h / 2 then 0
  else if t ≤ 2 * h + (h + 1) / 2 then 1
  else 2

theorem slot {h t : Int} (ht : h < t ∧ t ≤ 3 * h) :
    0 ≤ arm h t ∧ arm h t ≤ 2 * h ∧ arm h t ≠ h ∧
    0 ≤ level h t ∧ level h t ≤ 2 ∧
    h + arm h t + (2*h+1) * level h t = 2*t := by
  unfold arm level
  repeat' split
  all_goals omega

theorem distinct {h s t : Int}
    (hs : h < s ∧ s ≤ 3 * h) (ht : h < t ∧ t ≤ 3 * h)
    (he : arm h s = arm h t) : s = t := by
  unfold arm at he
  repeat' split at he
  all_goals omega

theorem forcedLow {h t : Int} (ht : h < t ∧ t ≤ 3 * h) :
    level h t = 0 ↔ 1 ≤ t - h ∧ t - h ≤ h / 2 := by
  unfold level
  split <;> (try split) <;> omega

theorem forcedHigh {h t : Int} (ht : h < t ∧ t ≤ 3 * h) :
    level h t = 2 ↔ 1 ≤ 3 * h + 1 - t ∧ 3 * h + 1 - t ≤ h / 2 := by
  unfold level
  split <;> (try split) <;> omega

end Cordial.MatchedArms
