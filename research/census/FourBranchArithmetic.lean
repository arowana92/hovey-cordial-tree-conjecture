import Std

namespace Cordial.FourBranch

/-- Positions on the original rotation interval, with upper bound exclusive. -/
theorem rotation_bounds (a b p : Int) (ha : 1 ≤ a) (hab : a ≤ b) (hp : 0 ≤ p) :
    let c := a+b
    let n := 3*c+4+p
    let lo := a+1
    let length := 2*c+a
    lo+length ≤ n ∧ lo ≤ c+a ∧ c+a < lo+c ∧ lo+c+a ≤ n-c ∧
    (n-c < lo+length ↔ p+4 ≤ 2*a) ∧
    (c+a+c = n-c ↔ a = p+4) ∧
    (c+a+(c+a) = n-c ↔ 2*a = p+4) := by
  dsimp
  omega

/-- The gap between the two moving intervals holds the remaining center. -/
theorem split_intervals (a b p : Int) (ha : 1 ≤ a) (_hb : 1 ≤ b) (hp : 0 ≤ p) :
    let t := a+b
    let start := b+3+p
    let n := 2*a+3*b+4+p
    b+1 < start ∧ start+t = n-(t+1) ∧ start+t+1+b ≤ n := by
  dsimp
  omega

end Cordial.FourBranch
