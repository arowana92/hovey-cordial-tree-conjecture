import Std

namespace Cordial.PathBridge

def first (p x : Int) : Int := if p = 0 then x + 1 else x
def second (p x : Int) : Int := x + p

/-- The first ordinary edge starts the discrepancy from x to the second arrival. -/
theorem firstStep (p x : Int) :
    [p + first p x, x].Perm [first p x, second p x] := by
  by_cases h : p = 0
  · simp [first, second, h]
  · have e : p + x = x + p := by omega
    simp only [first, second, ite_eq_right h, e]
    exact List.Perm.swap _ _ _

def endpoint (last x terminal : Int) : Int := last + x + 2*terminal

/-- Final arrival of the seven-edge transfer after three ordinary vertices. -/
def endTen (p x : Int) : Int :=
  let a := first p x
  let b := second p x
  endpoint (a+b) x (a+2*b)

/-- Final arrival after four ordinary vertices followed by the same transfer. -/
def endEleven (p x : Int) : Int :=
  let a := first p x
  let b := second p x
  endpoint (a+2*b) x (2*a+3*b)

theorem tenSlope (p x : Int) : endTen p x = endTen p 0 + 9*x := by
  simp only [endTen, first, second, endpoint]
  split <;> omega

theorem elevenSlope (p x : Int) : endEleven p x = endEleven p 0 + 14*x := by
  simp only [endEleven, first, second, endpoint]
  split <;> omega

/-- The two terminal vertices across the joining edge give its prescribed sum. -/
theorem bridgeWeight (p q w z : Int) :
    let d := w - endTen p 0 - endEleven q 0
    endTen p (-3*d + 14*z) + endEleven q (2*d - 9*z) = w := by
  dsimp only
  rw [tenSlope p (-3*_ + 14*z), elevenSlope q (2*_ - 9*z)]
  omega

end Cordial.PathBridge
