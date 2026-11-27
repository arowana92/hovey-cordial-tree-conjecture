import Std

namespace Cordial.MixedArms

/-- Relabeling the intermediate vertex fills the vacancy and recovers the old
    entering weight as the new internal weight, modulo the modulus. -/
theorem switch (k start y : Int) : (k-start)+(start+y) = k+y := by omega

/-- The vacancy lies beyond all tips and below the negative centers. -/
theorem vacancy (k b h p : Int) (half : b = 2*h+p)
    (parity : p = 0 ∨ p = 1) (space : 2*b < k)
    (allowed : p = 1 ∨ 2*b+2 < k) :
    h+1+(1-p)+b-1 < k-(h+1) ∧ k-(h+1) < k-h := by omega

/-- Once the small-hole and gap cases are exhausted, there is room to place
    an interval of tips containing the specified label, except at a full period. -/
theorem outer (k b y : Int) (length : 0 ≤ b ∧ 2*b+2 ≤ k)
    (positive : 1 ≤ y ∧ 2*y ≤ k)
    (gap : k-b/2-b ≤ y) :
    (b+1)/2 < y ∧ y < k-(b+1)/2 ∧
    (b+1 ≤ k-2*((b+1)/2)-1 ∨ (k = 2*(b+1) ∧ b%2 = 1)) := by omega

/-- Place the first tip as far left as the center band and the desired tip allow. -/
theorem placement (k q t y : Int) (positive : 1 ≤ q)
    (clearance : t < y ∧ y < k-t) (space : q ≤ k-2*t-1) :
    let first := max (t+1) (y-q+1)
    t < first ∧ first ≤ y ∧ y < first+q ∧ first+q ≤ k-t := by
  dsimp
  omega

end Cordial.MixedArms
