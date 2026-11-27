import Std

namespace Cordial.TwoCenterLayers

theorem parentBand (m r p : Int) (b : Int) (hb : b = 0 ∨ b = 1) :
    (m-r ≤ p ∧ p < m+r ∧ (m+r-1-b-p) % 2 = 0) ↔
    ∃ i : Int, 0 ≤ i ∧ i < r ∧ p = m+r-1-b-2*i := by
  constructor
  · intro hp
    exact ⟨(m+r-1-b-p)/2, by omega, by omega, by omega⟩
  · rintro ⟨i, hi, hir, hp⟩
    omega

theorem lower (l m r i : Int) :
    (l-r+i) + (m+r-1-2*i) = (l+m-r)+(r-1-i) := by omega

theorem upper (u m r i : Int) :
    (u+1+i) + (m+r-2-2*i) = (u+m)+(r-1-i) := by omega

theorem reversal {r i : Int} (hi : 0 ≤ i ∧ i < r) :
    0 ≤ r-1-i ∧ r-1-i < r ∧ r-1-(r-1-i) = i := by omega

end Cordial.TwoCenterLayers
