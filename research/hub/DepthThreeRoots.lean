import Std

namespace Cordial.DepthThreeRoots

theorem threeBoundaries (a b c d : Int) :
    let x := d-a
    let y := d
    let u := d-a-b
    let v := 2*d-a
    let w := -4*d+2*a-c
    let f := -2*d+a-c
    let h := -2*d+a
    let j := 3*d-2*a-b
    [a+x,x+y,b+u,u+v,v+w,c+f,f+h,h+j] = [y,v,x,j,f,h,w,u] := by
  dsimp only
  simp only [List.cons.injEq, and_true]
  omega

theorem zeroBoundary (x d : Int) :
    [0+x,x+d,0+(-2*x-d),(-2*x-d)+(x+d),(x+d)+(-x)] =
    [x,x+d,-2*x-d,-x,d] := by
  simp only [List.cons.injEq, and_true, true_and]
  omega

end Cordial.DepthThreeRoots
