import Std

namespace Cordial.RankedHulls

private theorem countSubset {α : Type} (p q : α → Bool) (xs : List α)
    (h : ∀ a ∈ xs, p a = true → q a = true) :
    xs.countP p ≤ xs.countP q := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
    have ht := ih (fun b hb => h b (by simp [hb]))
    have head := h a (by simp)
    simp only [List.countP_cons]
    cases hp : p a <;> cases hq : q a <;> simp_all <;> omega

/-- For two nondecreasing lists on the same index set, the largest
multiplicity in the child list bounds every sum multiplicity. -/
theorem sumCount (parent child : Nat → Int) (rows : List Nat)
    (hp : ∀ i ∈ rows, ∀ j ∈ rows, i ≤ j → parent i ≤ parent j)
    (hc : ∀ i ∈ rows, ∀ j ∈ rows, i ≤ j → child i ≤ child j)
    (cap : Nat) (bound : ∀ z, rows.countP (fun i => decide (child i = z)) ≤ cap)
    (weight : Int) :
    rows.countP (fun i => decide (parent i + child i = weight)) ≤ cap := by
  by_cases ex : ∃ i ∈ rows, parent i + child i = weight
  · obtain ⟨i, hi, he⟩ := ex
    apply Nat.le_trans _ (bound (child i))
    apply countSubset
    intro j hj coincides
    simp only [decide_eq_true_eq] at coincides ⊢
    rcases Nat.le_total i j with hij | hji
    · have := hp i hi j hj hij
      have := hc i hi j hj hij
      omega
    · have := hp j hj i hi hji
      have := hc j hj i hi hji
      omega
  · have zero : rows.countP (fun i => decide (parent i + child i = weight)) = 0 := by
      apply List.countP_eq_zero.mpr
      intro i hi h
      exact ex ⟨i,hi,of_decide_eq_true h⟩
    omega

/-- A nonzero observation cannot belong to two occupied scale bands
whose dyadic indices differ by twelve or more. -/
theorem separatedScales (s b a : Nat) (hs : 0 < s)
    (hsep : 4096*s ≤ b) (hlo : b ≤ 512*a) (hhi : a ≤ 4*s) : False := by
  omega

/-- Two arbitrary signs in the distinct free bands still give a large edge. -/
theorem freeEdge (t x y : Int)
    (hx : 4*t ≤ x ∧ x < 8*t ∨ 4*t ≤ -x ∧ -x < 8*t)
    (hy : 16*t ≤ y ∧ y < 24*t ∨ 16*t ≤ -y ∧ -y < 24*t) :
    x+y ≥ 8*t ∨ -(x+y) ≥ 8*t := by
  omega

/-- The two rank sums, leading sites, high-rank tail and nonleaves together
fit below the stated coefficient of k. -/
theorem explicitOrderCoefficient :
    2*8192*(2:Nat)^62 + 254*13001 + 2^17*(2^28)^2 + 2^28 < 2^80 := by
  decide

#print axioms sumCount
end Cordial.RankedHulls
