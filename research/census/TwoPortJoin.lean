import Std

namespace Cordial.TwoPortJoin

/-- The forest labels and its holes have already been multiplied by the chosen unit. -/
theorem fillBoth (k p q a b u v : Int)
    (h : (p-q)%k = (u-v-a+b)%k) :
    let t := p+a-u
    (p+a+t)%k = (u+2*t)%k ∧ (q+b+t)%k = (v+2*t)%k := by
  dsimp only
  constructor
  · congr 1
    omega
  · have hr := h.symm
    rw [Int.emod_eq_emod_iff_emod_sub_eq_zero] at hr ⊢
    have e : q+b+(p+a-u)-(v+2*(p+a-u)) = (u-v-a+b)-(p-q) := by omega
    rw [e]
    exact hr

/-- One bridge takes the old deficit, the other a translated forest hole. -/
theorem fillAcross (k p q a b D v : Int)
    (h : (p+q-D)%k = (v-a-b)%k) :
    let t := D-p-a
    (p+a+t)%k = D%k ∧ (q+b+t)%k = (v+2*t)%k := by
  dsimp only
  constructor
  · congr 1
    omega
  · rw [Int.emod_eq_emod_iff_emod_sub_eq_zero] at h ⊢
    have e : q+b+(D-p-a)-(v+2*(D-p-a)) = (p+q-D)-(v-a-b) := by omega
    rw [e]
    exact h

/-- Per-residue accounting, with no distinctness required between the old
    and new deficits. The indicator counts may refer to the same residue. -/
theorem histograms (level oldHole firstHole secondHole : Int) :
    let before := level-oldHole + (1-firstHole-secondHole)
    before+firstHole+secondHole = level+1-oldHole ∧
    before+oldHole+secondHole = level+1-firstHole := by
  dsimp only
  omega

end Cordial.TwoPortJoin
