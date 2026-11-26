import Std

namespace Primitive

-- Coefficients at five consecutive positions at stride s.
theorem regroup (a b c : Int) (v0 v1 v2 v3 v4 : Int) :
    (a - (v0+2*v1+v2)) - 2*(b - (v1+2*v2+v3)) + (c - (v2+2*v3+v4))
    + (v0-2*v2+v4) = a-2*b+c := by omega

-- Numerator of the real difference after putting both terms over 4s².
theorem kernel (left middle right : Int) :
    4*middle-(left+2*middle+right) = -(left-2*middle+right) := by omega

theorem roundingBudget (a b c d : Int)
    (ha : -1 ≤ a ∧ a ≤ 1) (hb : -1 ≤ b ∧ b ≤ 1)
    (hc : -1 ≤ c ∧ c ≤ 1) (hd : -1 ≤ d ∧ d ≤ 1) :
    -5 ≤ a-b-2*c-d ∧ a-b-2*c-d ≤ 5 := by omega

end Primitive
