import Std
namespace Cordial.PathWindow
/-- Usable endpoint rank on a path of this many vertices. -/
def usable (n x : Int) : Prop :=
  0 ≤ x ∧ 2*x < n ∧ (x = 0 ∨ n ≠ 4*x+1)
def before (a b x : Int) : Prop :=
  usable (a+1) x ∧ usable b (a/2-x)
def afterCut (a b x : Int) : Prop :=
  usable a (x-a/2) ∧ usable (b+1) (x-a/2)
def reversedBlock (a b x m : Int) : Prop :=
  a < m ∧ (m-1-a)/2 = x ∧ usable (a+b+1-m) ((m-1)/2)
def built (a b x : Int) : Prop :=
  before a b x ∨ before b a x ∨ afterCut a b x ∨ ∃ m, reversedBlock a b x m

/-- The four explicit joins in the path construction cover at least one of
    the two consecutive ranks at every position in the indicated range. -/
theorem window (a b h : Int) (ha : 0 ≤ a) (hab : a ≤ b) (hh : 1 ≤ h)
    (hn : 6*h+2 ≤ a+b+1) (even : (a+b+1)%2=0) :
    built a b h ∨ built a b (h-1) := by
  by_cases short : a ≤ h+1
  · right
    refine Or.inr (Or.inr (Or.inr ⟨2*(a/2)+2*h, ?_⟩))
    dsimp [reversedBlock,usable]
    omega
  by_cases low : h ≤ a/2
  · by_cases first : before a b h
    · exact Or.inl (Or.inl first)
    by_cases second : before a b (h-1)
    · exact Or.inr (Or.inl second)
    have special : a=4*h ∧ b=4*h+5 := by
      simp only [before,usable] at first second
      omega
    by_cases small : h ≤ 2
    · by_cases one : h=1
      · right
        refine Or.inr (Or.inr (Or.inr ⟨6,?_⟩))
        dsimp [reversedBlock,usable]
        omega
      · right
        refine Or.inr (Or.inr (Or.inr ⟨11,?_⟩))
        dsimp [reversedBlock,usable]
        omega
    · left
      refine Or.inr (Or.inl ?_)
      dsimp [before,usable]
      omega
  · by_cases first : afterCut a b h
    · exact Or.inl (Or.inr (Or.inr (Or.inl first)))
    right
    refine Or.inr (Or.inr (Or.inl ?_))
    dsimp [afterCut,usable] at first ⊢
    omega
/-- Odd orders have complementary parities on the two blocks, so at most one
    endpoint rank is exceptional. The nine-vertex midpoint admits rank zero
    by the independent marked-path construction. -/
theorem oddWindow (a b h : Int) (ha : 0 ≤ a) (hab : a ≤ b) (hh : 1 ≤ h)
    (hn : 6*h-1 ≤ a+b+1) (odd : (a+b+1)%2=1) :
    built a b h ∨ built a b (h-1) ∨ (a=4 ∧ b=4 ∧ h=1) := by
  by_cases short : a < h
  · right; left
    refine Or.inr (Or.inr (Or.inr ⟨2*((a+1)/2)+2*h-1,?_⟩))
    dsimp [reversedBlock,usable]
    omega
  by_cases low : h ≤ a/2
  · by_cases first : before a b h
    · exact Or.inl (Or.inl first)
    by_cases second : before a b (h-1)
    · exact Or.inr (Or.inl (Or.inl second))
    right; right
    dsimp [before,usable] at first second
    omega
  · by_cases first : afterCut a b h
    · exact Or.inl (Or.inr (Or.inr (Or.inl first)))
    right; left
    refine Or.inr (Or.inr (Or.inl ?_))
    dsimp [afterCut,usable] at first ⊢
    omega
theorem halfTip (b : Int) (hb : 3 ≤ b) (odd : b%2=1) (exc : b≠5) :
    usable b ((b-3)/2) := by
  dsimp [usable]
  omega

theorem quarterCut (d a : Int) (hd : 0 < d) (ha : 0 ≤ a) (hs : a < 2*d-1) :
    let m := d+a/2
    let s := 4*d-1-m
    let diff := (s+1)/2-(m+1)/2
    a < m ∧ m < s ∧
      (usable s diff ∨ usable s (diff-1)) ∧ (usable s diff ∨ usable s (diff+1)) := by
  dsimp [usable]
  omega

end Cordial.PathWindow
