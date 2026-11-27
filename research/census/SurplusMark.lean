import Std
namespace Cordial.SurplusMark

def usable (n x : Int) : Prop :=
  0 ≤ x ∧ 2*x < n ∧ (x = 0 ∨ n ≠ 4*x+1)
def before (a b x : Int) : Prop :=
  usable (a+1) x ∧ usable b (a/2-x)
def afterCut (a b x : Int) : Prop :=
  usable a (x-a/2) ∧ usable (b+1) (x-a/2)
def reverseAt (a b x l : Int) : Prop :=
  a < l ∧ (l-1-a)/2=x ∧ usable (a+b+1-l) ((l-1)/2)
def joins (a b x : Int) : Prop :=
  before a b x ∨ before b a x ∨ afterCut a b x ∨
  reverseAt a b x (a+2*x+1) ∨ reverseAt a b x (a+2*x+2)

theorem three (a b h : Int) (ha : 0 ≤ a) (hab : a ≤ b) (hh : 1 ≤ h)
    (total : a+b=6*h+3) :
    joins a b h ∨ (h%3=0 ∧ 3*a=4*h+3) := by
  by_cases small : a ≤ h+1
  · left
    right; right; right
    dsimp [reverseAt,usable]
    omega
  by_cases big : 2*h ≤ a
  · left
    by_cases first : before a b h
    · exact Or.inl first
    · right; left
      dsimp [before,usable] at first ⊢
      omega
  by_cases mid : afterCut a b h
  · exact Or.inl (Or.inr (Or.inr (Or.inl mid)))
  · right
    dsimp [afterCut,usable] at mid
    omega

theorem five (a b h : Int) (ha : 0 ≤ a) (hab : a ≤ b) (hh : 1 ≤ h)
    (total : a+b=10*h+5) :
    joins a b h ∨ joins a b (2*h+1) := by
  by_cases small : a < 2*h
  · left
    right; right; right
    dsimp [reverseAt,usable]
    omega
  by_cases first : before a b h
  · exact Or.inl (Or.inl first)
  by_cases second : before b a h
  · exact Or.inl (Or.inr (Or.inl second))
  right; right; right; left
  dsimp [before,usable] at first second
  dsimp [afterCut,usable]
  omega
theorem sevenSmall (a b h : Int) (ha : 0 ≤ a) (hab : a ≤ b) (hh : h=1 ∨ h=2)
    (total : a+b=14*h+7) : joins a b h ∨ joins a b (2*h+1) := by
  have hb : b=14*h+7-a := by omega
  subst b
  rcases hh with eq | eq
  · subst h
    have cases : a=0 ∨ a=1 ∨ a=2 ∨ a=3 ∨ a=4 ∨ a=5 ∨ a=6 ∨ a=7 ∨ a=8 ∨ a=9 ∨ a=10 := by omega
    rcases cases with eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq <;> subst a <;>
      simp +decide [joins,before,afterCut,reverseAt,usable]
  · subst h
    have cases : a=0 ∨ a=1 ∨ a=2 ∨ a=3 ∨ a=4 ∨ a=5 ∨ a=6 ∨ a=7 ∨ a=8 ∨ a=9 ∨ a=10 ∨ a=11 ∨ a=12 ∨ a=13 ∨ a=14 ∨ a=15 ∨ a=16 ∨ a=17 := by omega
    rcases cases with eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq | eq <;> subst a <;>
      simp +decide [joins,before,afterCut,reverseAt,usable]
end Cordial.SurplusMark
