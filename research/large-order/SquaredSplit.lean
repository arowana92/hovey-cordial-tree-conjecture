import Std

namespace SquaredSplit

-- Pick an odd-fiber mass in the required parity class, within one of n/4.
theorem roundedParityMass (n parity : Int) :
    let h := parity + 2*((n-4*parity+4)/8)
    (h-parity)%2=0 ∧ -4 ≤ 4*h-n ∧ 4*h-n ≤ 4 := by
  dsimp
  omega

-- This is the exact first-moment constraint after the integer total choices.
theorem localMoments (half me ho no : Int) (h : (ho-(half-me))%2=0) :
    let he := ho+half
    let ne := no+(me-he+2*ho)/2
    2*(he-ho)=2*half ∧ 2*(ne-no)+he-2*ho=me := by
  dsimp
  omega

theorem transferBudget (u : Nat) (h : 2 ≤ u) : 2*u+2 ≤ 6*(u-1) := by omega

end SquaredSplit
