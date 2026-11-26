import Std

namespace Cordial.MixedGuards

/-- Total derivative of the guard's open leaf jumps for three branches.
Each pair of arguments gives the two leaf populations on one branch. -/
def triple (l m u n v w : Int) := l+u-2*v+m+2*(n-1)-2*(w-1)

theorem positiveTriple (l m u n v w : Int) (a : 0 < m) (b : 0 < n) (_c : 0 < w) :
    0 < triple l m u n v w ∨ 0 < triple l m v w u n ∨
    0 < triple u n l m v w ∨ 0 < triple u n v w l m ∨
    0 < triple v w l m u n ∨ 0 < triple v w u n l m := by
  unfold triple
  omega

/-- Total when the two branches have a common zero boundary. -/
def pair (l m u n j : Int) := m+j*l+(-2*j-1)*u+(j+1)*(n-1)

theorem positivePair (l m u n : Int) (a : 0 < m) (b : 0 < n) :
    0 < pair l m u n 4 ∨ 0 < pair u n l m 4 ∨
    0 < pair l m u n (-4) ∨ 0 < pair u n l m (-4) := by
  unfold pair
  omega

end Cordial.MixedGuards
