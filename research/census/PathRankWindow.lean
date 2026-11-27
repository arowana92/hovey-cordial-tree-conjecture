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
end Cordial.PathWindow
