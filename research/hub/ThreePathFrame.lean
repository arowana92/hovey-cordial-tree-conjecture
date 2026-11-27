import Std

namespace Cordial.ThreePathFrame

/-- The same three labeled vertices form a path entering from either center. -/
theorem weights (u v : Int) :
    0+(3*u+1) = 1+3*u ∧
    (3*u+1)+(3*v+2) = 3*(u+v)+3 ∧
    (3*v+2)+3*u = 3*(u+v)+2 := by omega

/-- Attaching leaves at the two pinned centers fills either end of the intervals. -/
theorem leaves (l h : Int) : (0:Int)+(h+1) = h+1 ∧ 1+(l-1) = l := by omega

end Cordial.ThreePathFrame
