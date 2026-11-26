import Std.Tactic

namespace HubBarePath

/-- Vertex labels have been multiplied by six. The old component labels
are then divisible by three, while every internal path label avoids zero
modulo three. The equations are the seven endpoint-sum checks in path order. -/
theorem reconnect (p q w : Int) (hp : q < p) (hq : 0 < q) (hw : p ≤ w)
    (hr : p % 3 ≠ q % 3) :
    let a := -4*p-2*q
    let b := 2*(p-q)
    let c := q-p+3*w
    let d := p-q+3*w
    let e := 2*(q-p)
    let f := -2*p-4*q
    (6*p+a = b ∧ a+b = f ∧ b+c = d ∧ c+d = 6*w ∧
     d+e = c ∧ e+f = a ∧ f+6*q = e) ∧
    (a < f ∧ f < e ∧ e < 0 ∧ 0 < b ∧ b < c ∧ c < d) ∧
    (a % 3 ≠ 0 ∧ b % 3 ≠ 0 ∧ c % 3 ≠ 0 ∧ d % 3 ≠ 0 ∧
     e % 3 ≠ 0 ∧ f % 3 ≠ 0) := by
  dsimp
  repeat' apply And.intro
  all_goals omega

end HubBarePath
