import Std

namespace Cordial.PairedStarRoots

/-- The right side lists each assigned root or tip exactly once. Two roots have
boundary q, and the other three boundary labels are independent. -/
theorem nineWeights (a q c h d : Int) :
    let r := d
    let b := d+a
    let e := d-c
    let f := -d-a-h-q
    let j := -d-a-q
    let u := -2*d-2*a-h-q
    let v := d+a+q
    let w := -d-a
    let y := 2*d+a+q-c
    [a+r,q+b,c+e,h+f,q+j,b+u,e+v,f+w,j+y] =
    [b,v,r,j,w,f,y,u,e] := by
  dsimp only
  simp only [List.cons.injEq, and_true]
  omega

/-- Include the auxiliary root walk between the second and third jumps. -/
theorem terminal (s t total a b c : Int) :
    t+a+b+total+c+(s-t-total-a-b-c) = s := by omega

end Cordial.PairedStarRoots
