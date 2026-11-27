import Std

namespace Cordial.WeightTransfer

inductive Walk {α : Type} (edge : α → α → Prop) (start : α) : α → Prop where
  | nil : Walk edge start start
  | snoc {u v : α} : Walk edge start u → edge u v → Walk edge start v

/-- Along any walk from a low bin to a high bin, one step crosses the cut. -/
theorem crosses {α : Type} {edge : α → α → Prop} (high : α → Prop)
    {s t : α} (walk : Walk edge s t) (hs : ¬ high s) (ht : high t) :
    ∃ d g, edge d g ∧ ¬ high d ∧ high g := by
  induction walk with
  | nil => exact False.elim (hs ht)
  | @snoc u v _ step ih =>
    by_cases hu : high u
    · exact ih hu
    · exact ⟨u, v, step, hu, ht⟩

/-- Adding a whole period, doubling a low bin and omitting a high bin,
    leaves every count in the two new adjacent levels. -/
theorem balancedTransfer {α : Type} [DecidableEq α] (count : α → Int)
    (q : Int) (levels : ∀ x, q ≤ count x ∧ count x ≤ q + 1)
    (d g : α) (hd : count d = q) (hg : count g = q + 1) (x : α) :
    let result := count x + 1 + (if x = d then 1 else 0) - (if x = g then 1 else 0)
    q + 1 ≤ result ∧ result ≤ q + 2 := by
  have hx := levels x
  dsimp only
  split <;> split <;> (subst_vars; omega)

end Cordial.WeightTransfer
