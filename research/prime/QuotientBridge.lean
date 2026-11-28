import Std

namespace Cordial.QuotientBridge

/-- Low vertex sets must be disjoint. The low edge sets may meet only
    at the bridge, which must fill at least one of their holes. -/
def Accept {A : Type} (v₀ v₁ e₀ e₁ : A → Prop) (bridge : A) : Prop :=
  (∀ x, v₀ x → v₁ x → False) ∧
  (e₀ bridge ∨ e₁ bridge) ∧
  ∀ x, e₀ x → e₁ x → x = bridge

def Project {A B : Type} (π : A → B) (p : A → Prop) (y : B) : Prop :=
  ∃ x, p x ∧ π x = y

/-- Only the piece's edge holes have to project injectively. When both
    sides have a hole over the proposed bridge, anchor on the piece. -/
theorem lift {A B : Type} {π : A → B} {v₀ v₁ e₀ e₁ : A → Prop} {b : A}
    (accepted : Accept (Project π v₀) (Project π v₁)
      (Project π e₀) (Project π e₁) (π b))
    (unique : ∀ x y, e₁ x → e₁ y → π x = π y → x = y)
    (anchorPiece : Project π e₁ (π b) → e₁ b)
    (anchorOld : ¬ Project π e₁ (π b) → Project π e₀ (π b) → e₀ b) :
    Accept v₀ v₁ e₀ e₁ b := by
  obtain ⟨vertices, filled, edges⟩ := accepted
  refine ⟨fun x h j => vertices (π x) ⟨x,h,rfl⟩ ⟨x,j,rfl⟩, ?_, ?_⟩
  · by_cases h : Project π e₁ (π b)
    · exact Or.inr (anchorPiece h)
    · exact Or.inl (anchorOld h (filled.resolve_right h))
  · intro x old piece
    have same := edges (π x) ⟨x,old,rfl⟩ ⟨x,piece,rfl⟩
    exact unique x b piece (anchorPiece ⟨x,piece,same⟩) same

/-- The two anchor translations solve the edge equation before reduction. -/
theorem anchor_shifts (u b j z : Int) :
    u*b + u*(b-j) = u*j + 2*(u*(b-j)) ∧ u*b + (z-u*b) = z := by
  rw [Int.mul_sub]
  omega

end Cordial.QuotientBridge
