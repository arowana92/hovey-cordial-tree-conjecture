import Std

namespace Cordial.ExposureHull

/-- At three exposures a shortest pair of arms leaves twelve pairs outside
    its path at every critical order beyond 51. -/
theorem threeLarge (q a b c s : Nat) (hq : 3 ≤ q)
    (h : a+b+c+s+3 = 13*q) (ha : a ≤ c) (hb : b ≤ c) :
    12 ≤ c+s := by omega

/-- The geometry of the unresolved tripod at order 51. -/
theorem threeSmall (a b c s : Nat) (h : a+b+c+s = 23)
    (ha : a+s ≤ 11) (hb : b+s ≤ 11) (hc : c+s ≤ 11) :
    s ≤ 5 ∧ 12 ≤ a+b ∧ s+1 ≤ a := by omega

/-- At four or more exposures the four-leaf tour bounds the closest pair. -/
theorem fourTour (q H j h : Nat) (hq : 2 ≤ q) (hH : 2 ≤ H)
    (hn : j+H+1 = 13*q) (ht : 2*h ≤ j+1) :
    h+14 ≤ 13*q := by omega

end Cordial.ExposureHull
