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

/-- Bound all ordinary path positions by groups of thirteen. -/
theorem arbitraryOrder (d r h groups positions n : Nat) (hd : r+2 ≤ d)
    (hh : h ≤ 12) (hg : groups ≤ 1)
    (hp : positions ≤ 12*(d+r-1)+13*groups)
    (order : n = d+2*(positions+r+h)) : n+26 ≤ 51*d := by omega

/-- Up to three groups suffice at a centroid when there are at most 2H+1 tips. -/
theorem threeGroups (H d h pairs q : Nat) (hH : 1 ≤ H) (cap : H+h ≤ 12)
    (tips : d ≤ 2*H+1) (bound : pairs ≤ 3*(12-H-h)+1+h)
    (order : 2*pairs+d+H = 26*q) : q ≤ 2 := by omega

theorem sixTips (h groups pairs q : Nat) (hh : h ≤ 10)
    (groups_le : groups ≤ h/7)
    (bound : pairs ≤ 3*(10-h)+2+12+13*groups+h)
    (order : 2*pairs+8 = 26*q) : q ≤ 3 := by omega

theorem fiveTips (pairs q : Nat) (bound : pairs < 62)
    (order : 2*pairs+6 = 26*q) : q ≤ 4 := by omega

end Cordial.ExposureHull
