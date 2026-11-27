import Std

namespace Cordial.EndpointSlopes

/-- Coefficient of the varied scale in each arrival of a seven-step transfer. -/
def gap (p s t : Int) := [t, -p-2*t, p+t, s+t, -t, -p-t, p+s+2*t]

/-- The exceptional +1 at an actual zero parent has zero coefficient. -/
def arm (p z : Int) (long : Bool) : List Int :=
  let a := z
  let b := z+p
  let c := a+b
  let d := b+c
  if long then [a,b,c,d] ++ gap d z (c+d)
  else [a,b,c] ++ gap c z d

def bridge (p q w z : Int) : List Int :=
  let diff := w - (arm p 0 false).getLastD 0 - (arm q 0 true).getLastD 0
  arm p (-3*diff+14*z) false ++ (arm q (2*diff-9*z) true).reverse

theorem rightMark : bridge 0 (-630) 0 1080 =
    [0,0,0,0,0,0,0,0,0,0,0,270,90,270,-270,360,-90,-180,90,-270,360] := by decide

theorem leftMark : bridge (-630) 0 0 700 =
    [350,-280,70,-210,350,-140,140,210,140,0,0,0,0,0,0,0,0,0,0,0,0] := by decide

theorem boundsAndSum :
    let coeffs := bridge 0 (-630) 0 1080 ++ bridge (-630) 0 0 700
    coeffs.all (fun x => decide (-280 ≤ x ∧ x ≤ 360)) = true ∧
    coeffs.sum - 630 = 630 := by decide

/-- While both signs are available, take one opposite the current displacement. -/
theorem mixedStep (v a neg pos : Int) (hv : -neg ≤ v ∧ v ≤ pos)
    (ha : -neg ≤ a ∧ a ≤ pos) (sign : (v ≤ 0 ∧ 0 ≤ a) ∨ (0 < v ∧ a ≤ 0)) :
    -neg ≤ v+a ∧ v+a ≤ pos := by omega

end Cordial.EndpointSlopes
