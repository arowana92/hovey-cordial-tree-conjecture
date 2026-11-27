import Std

namespace Cordial.CaterpillarGap

def bump (t x : Int) : Int := if x < t then 0 else 1

/-- Every representative in one full period places the bridge in the outside hole. -/
theorem bridgeChoices (a b r c : Int) (_hr : 0 ≤ r ∧ r < a)
    (hc : -b-r-1 ≤ c ∧ c ≤ a-r-1) :
    (∃ t : Int, 0 ≤ t ∧ t ≤ a ∧ c = a-r-t-bump t r) ∨
    (∃ t : Int, 0 ≤ t ∧ t ≤ b ∧ c = -1-r-t) := by
  by_cases h : -r ≤ c
  · left
    by_cases high : a-2*r-1 ≤ c
    · refine ⟨a-r-c-1, by omega, by omega, ?_⟩
      unfold bump
      split <;> omega
    · refine ⟨a-r-c, by omega, by omega, ?_⟩
      unfold bump
      split <;> omega
  · right
    exact ⟨-1-r-c, by omega, by omega, by omega⟩

/-- Skipping a rank preserves strict increase along the staircase. -/
theorem strictGap (i j i' j' t : Int) (h : i+j < i'+j') (hi : i ≤ i') :
    i+j+bump t i < i'+j'+bump t i' := by
  unfold bump
  (repeat' split) <;> omega

/-- Low free class containing the joint before deletion: all boundary sums
    precede the free staircase, in a single interval of length k. -/
theorem jointFirst (a k d t i j z : Int) (hz : 0 ≤ z ∧ z < d)
    (hs : d-1 ≤ i+j ∧ i+j ≤ k-3) :
    a-1 ≤ a-1+z ∧ a-1+z < a+i+j+bump t i ∧ a+i+j+bump t i ≤ a+k-2 := by
  unfold bump
  split <;> omega

/-- Low class opposite the joint: the last boundary column may be bumped
    only when every subsequent column is bumped as well. -/
theorem jointSecond (b k d t i j z : Int) (hz : 0 ≤ z ∧ z < d)
    (hj : d-1 ≤ j) (hs : d-1 ≤ i+j ∧ i+j ≤ k-3) :
    b ≤ b+z+bump t z ∧ b+z+bump t z < b+1+i+j+bump t j ∧
    b+1+i+j+bump t j ≤ b+k-1 := by
  unfold bump
  (repeat' split) <;> omega

/-- If neither reduced arm can come before a marked leaf in a k-prefix,
    the only configuration without another central leaf is divisible. -/
theorem twoArms (k l r p : Int) (hl : l < k ∧ k < l+2)
    (hr : r < k ∧ k < r+2) (hp : 1 ≤ p) :
    l = k-1 ∧ r = k-1 ∧ (l+r+p+1 = 2*k ∨ 2 ≤ p) := by omega

end Cordial.CaterpillarGap
