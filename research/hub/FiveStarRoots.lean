import Std

namespace Cordial.FiveStarRoots

/-- The five edges at the common parent, followed by four edges to children.
The right side permutes precisely the five roots and four child labels. -/
theorem nineWeights (p d : Int) :
    let a := d
    let b := d+p
    let c := d-p
    let e := -d-3*p
    let f := -d-2*p
    let u := -2*d-4*p
    let v := d+2*p
    let w := -d-p
    let y := 2*d+p
    [p+a, p+b, p+c, p+e, p+f, b+u, c+v, e+w, f+y] =
    [b, v, a, f, w, e, y, u, c] := by
  dsimp only
  simp only [List.cons.injEq, and_true]
  omega

/-- The three distinguished leaves concatenate without dividing by their arity. -/
theorem primaryWeights (s t a b : Int) :
    [t+a,(t+a)+b,(t+a+b)+(s-t-a-b)] = [t+a,t+a+b,s] := by
  simp only [List.cons.injEq, and_true, true_and]
  omega

end Cordial.FiveStarRoots
