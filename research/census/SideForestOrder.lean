import Std

namespace Cordial.SideForestOrder

/-- Two bounded corridor segments realize every size between the endpoints. -/
theorem splitCorridors (base k e g : Int) (he : 0 ≤ e) (hg : 0 ≤ g)
    (low : base ≤ k) (high : k ≤ base + e + g) :
    ∃ i j : Int, 0 ≤ i ∧ i ≤ e ∧ 0 ≤ j ∧ j ≤ g ∧ base + i + j = k := by
  by_cases fits : k - base ≤ e
  · exact ⟨k - base, 0, by omega, by omega, by omega, by omega, by omega⟩
  · exact ⟨e, k - base - e, by omega, by omega, by omega, by omega, by omega⟩

/-- The explicit two-joint exclusion and the cumulative child tables agree. -/
theorem allowedChild (k w f g e h : Int) :
    ¬ (2+w+g+f ≤ k ∧ k ≤ 2+w+g+f+e+h ∧ w+f+3 ≤ k) ↔
      min (k-2-g-w) (k-3-w) < f ∨ f+h < k-2-g-w-e := by
  by_cases smaller : k-2-g-w ≤ k-3-w
  · rw [Int.min_eq_left smaller]
    omega
  · rw [Int.min_eq_right (by omega : k-3-w ≤ k-2-g-w)]
    omega

/-- Exact threshold for a padded side to follow at most three boundary runs. -/
theorem paddingThreshold (k t a : Int) :
    t-a+3 ≤ a+(k-1-t) ↔ t+2-k/2 ≤ a := by
  omega

end Cordial.SideForestOrder
