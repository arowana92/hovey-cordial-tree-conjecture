import Std

namespace Cordial.InvolutionArms

/-- The six actual weights on three arms, minus their desired values.
At modulus 2p every entry vanishes. The desired list omits L and includes 0. -/
theorem weightDifferences (p L t : Int) :
    [p + (p-L) - (-L), (p-L) + (p+L) - 0,
     p + (-L) - (p-L), (-L) + (t+L) - t,
     p + L - (p+L), L + t - (t+L)] =
    [2*p, 2*p, 0, 0, 0, 0] := by
  simp only [List.cons.injEq, and_true]
  omega

/-- Two real leaves have the histogram difference of one first-layer jump.
At modulus 2p, the jump from u to u-p is also a jump by p. -/
theorem virtualJump (p L u : Int) :
    [L+u, (-p-L)+(u+L)] = [u+L,u-p] ∧ (u+p)-(u-p)=2*p := by
  simp only [List.cons.injEq, and_true]
  omega

end Cordial.InvolutionArms
