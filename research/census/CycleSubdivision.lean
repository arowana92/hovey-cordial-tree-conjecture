import Std

namespace Cordial.CycleSubdivision

def stretch (r x : Int) := if x < r then x+2 else x+6

theorem cross_sum (r x y : Int) (low : x < r) (high : r ≤ y) :
    stretch r x + stretch r y = x+y+8 := by
  simp [stretch,low,Int.not_lt.mpr high]
  omega

theorem high_sum (r x y : Int) (hx : r ≤ x) (hy : r ≤ y) :
    stretch r x + stretch r y = x+y+12 := by
  simp [stretch,Int.not_lt.mpr hx,Int.not_lt.mpr hy]
  omega

def cross (r w : Int) : Prop := 2*r-1 ≤ w ∧ w ≤ 3*r-3 ∧ w ≠ 2*r

/-- The four appended cross edges fill exactly the gap in the new profile. -/
theorem grow_cross (r w : Int) (hr : 6 ≤ r) :
    cross (r+4) w ↔ cross r (w-8) ∨ (3*r+6 ≤ w ∧ w ≤ 3*r+9) := by
  unfold cross
  omega

theorem grow_high (r w : Int) :
    (w = 3*(r+4)-2 ∨ w = 3*(r+4)) ↔ (w-12 = 3*r-2 ∨ w-12 = 3*r) := by omega

/-- For two insertions an orientation meets the deficit and has distinct free labels. -/
theorem two_slots (k u v d : Int) (distinct : (2*(u-v))%k ≠ 0) :
    (2*(d-u)-(u+v))%k ≠ 0 ∨ (2*(d-v)-(u+v))%k ≠ 0 := by
  by_cases h : (2*(d-u)-(u+v))%k = 0
  · right
    intro h'
    have eqn : 2*(u-v) = (2*(d-v)-(u+v))-(2*(d-u)-(u+v)) := by omega
    rw [eqn,Int.sub_emod,h,h'] at distinct
    simp at distinct
  · exact Or.inl h

/-- A change of vertex surplus cannot double to half the modulus if it is odd. -/
theorem parity_obstruction (h j y z : Int) (hh : h%2 = 1) (hj : j%2 = 1) :
    ¬ ∃ q : Int, 2*(z-y) = j*h+2*h*q := by
  rintro ⟨q,e⟩
  have he := congrArg (fun x : Int => x%2) e
  simp [Int.add_emod,Int.mul_emod,hh,hj] at he

end Cordial.CycleSubdivision
