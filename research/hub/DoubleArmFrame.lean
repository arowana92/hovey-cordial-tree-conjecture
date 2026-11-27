import Std

namespace Cordial.DoubleArmFrame

/-- Across either choice of hub the two edge sums of an arm do not change. -/
theorem weights {u v w : Int} (hz : u+v+w = 0) (c : Int) :
    c+(2*w-c) = 2*w ∧ (2*w-c)+(2*u-1+c) = -1-2*v := by omega

/-- Within a triple the parent and tip at index z fill the same two positions
at either center, after cycling through the three rows. -/
theorem slots (z : Int) :
    [2*z-(1:Int), 2*z-1+1].Perm [2*z, 2*z-1] := by
  have h : 2*z-1+1 = 2*z := by omega
  rw [h]
  exact List.Perm.swap _ _ _

end Cordial.DoubleArmFrame
