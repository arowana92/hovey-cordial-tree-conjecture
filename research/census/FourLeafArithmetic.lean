import Std

namespace Cordial.FourLeaves

/-- A sufficient endpoint condition for the path construction. -/
def Available (n h : Int) : Prop :=
  0 ≤ h ∧ 2*h+1 ≤ n ∧ (h = 0 ∨ n ≠ 4*h+1)

/-- The adjacent rank blocks leave exactly one sum for the bridge. -/
theorem bridge (a b x y : Int) :
    x + (b+y) = a+b-1 ↔ y = a-1-x := by omega

theorem twoEnded (a b h : Int) (hh : 1 ≤ h) (hab : a ≤ b) (ha : 4*h+5 ≤ a) :
    let u := 2*h+a%2
    let v := b%2
    let c := a-u
    let d := b-v
    c%2 = 0 ∧ d%2 = 0 ∧ Available c ((u+v)/2) ∧ Available d (c/2) := by
  dsimp [Available]
  omega

theorem oneEnded (a b h : Int) (hh : 1 ≤ h) (ha : 1 ≤ a) (hb : a+4*h+4 ≤ b) :
    let v := 2*h+b%2
    (b-v)%2 = 0 ∧ Available (b-v) ((a+v)/2) := by
  dsimp [Available]
  omega

theorem largePath (a b h : Int) (hn : 12*h+13 ≤ a+b+1) :
    4*h+5 ≤ a ∨ a+4*h+4 ≤ b := by omega

theorem rankOneLink (g : Int) (hg : 1 ≤ g) (hne : g ≠ 3) :
    g = 1 ∨ g = 2 ∨ g = 6 ∨ Available (g-1) 1 := by
  unfold Available
  omega

theorem shiftedLink (g : Int) (hg : 1 ≤ g) (h1 : g ≠ 1) (h4 : g ≠ 4) :
    1 ≤ g-1 ∧ g-1 ≠ 3 := by omega

theorem spiderRemainder (t : Int) (hp : 1 ≤ t) :
    t = 5 ∨ Available (t-5) 2 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨
    t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 ∨ t = 14 := by
  unfold Available
  omega

theorem doubleRemainder (c d : Int) (hc : 3 ≤ c) (hd : c ≤ d) :
    (Available c 1 ∧ Available d 2) ∨ (Available d 1 ∧ Available c 2) ∨
    (c = 3 ∧ d = 3) ∨ (c = 3 ∧ d = 4) ∨ (c = 3 ∧ d = 9) ∨
    (c = 4 ∧ d = 4) ∨ (c = 4 ∧ d = 9) ∨ (c = 5 ∧ d = 5) ∨
    (c = 9 ∧ d = 9) := by
  unfold Available
  omega

end Cordial.FourLeaves
