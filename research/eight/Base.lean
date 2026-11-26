import research.Reduction

namespace Cordial.Eight

private abbrev Color := Fin 8

-- Only the first seven entries of the parent function enter an order-eight tree.
private def parents (a : Fin 1) (b : Fin 2) (c : Fin 3) (d : Fin 4)
    (e : Fin 5) (f : Fin 6) (g : Fin 7) (i : Nat) : Nat :=
  #[a.val,b.val,c.val,d.val,e.val,f.val,g.val][i]?.getD 0

-- Try fresh labels at one new child, checking the actual edge to its parent.
private def search (p : Nat → Nat) :
    Nat → Array Color → List Color → Option (Array Color)
  | 0, labels, _ => some labels
  | fuel+1, labels, used =>
    (List.finRange 8).findSome? fun x =>
      let w := x + labels[p (labels.size-1)]!
      if labels.contains x || used.contains w then none
      else search p fuel (labels.push x) (w::used)

private def witness (p : Nat → Nat) : (Nat → Color) × Color :=
  let labels := (search p 7 #[0] []).getD #[]
  let values := fun i => labels[i]?.getD 0
  let missing := ((List.finRange 8).find? fun a => tally (weight p values) 0 7 a == 0).getD 0
  (values, missing)

private def check (p : Nat → Nat) : Bool :=
  let (values,missing) := witness p
  decide ((∀ x, tally values 0 8 x = 1) ∧
    (∀ x, tally (weight p values) 0 7 x = bump missing x))

private theorem checked : ∀ (a : Fin 1) (b : Fin 2) (c : Fin 3) (d : Fin 4)
    (e : Fin 5) (f : Fin 6) (g : Fin 7), check (parents a b c d e f g) = true := by
  native_decide

private theorem prefixTally (f g : Nat → Color) (n : Nat)
    (h : ∀ i < n, f i = g i) (a : Color) : tally f 0 n a = tally g 0 n a := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp [tally, h n (by omega), ih (fun i hi => h i (by omega))]

/-- The rooted order-eight hypothesis, proved by a fresh executable search. -/
theorem base : BaseTest 8 := by
  intro p hp
  let atIndex (i : Nat) : Fin (i+1) := ⟨p i, Nat.lt_succ_of_le (hp i)⟩
  let q := parents (atIndex 0) (atIndex 1) (atIndex 2) (atIndex 3)
    (atIndex 4) (atIndex 5) (atIndex 6)
  have same (i : Nat) (hi : i < 7) : p i = q i := by
    have h : i=0 ∨ i=1 ∨ i=2 ∨ i=3 ∨ i=4 ∨ i=5 ∨ i=6 := by omega
    rcases h with h|h|h|h|h|h|h <;> subst i <;> rfl
  have result : check q = true := checked _ _ _ _ _ _ _
  let values := (witness q).1
  let gap := (witness q).2
  have valid : (∀ x, tally values 0 8 x = 1) ∧
      (∀ x, tally (weight q values) 0 7 x = bump gap x) := by
    simpa [check, values, gap] using result
  refine ⟨values, gap, valid.1, ?_⟩
  intro a
  have equiv := prefixTally (weight p values) (weight q values) 7
    (fun i hi => by simp [weight, same i hi]) a
  simpa using equiv.trans (valid.2 a)

/-- The formal induction at eight now requires only the attachment hypothesis. -/
theorem reduction (forest : ForestTest 8) (p : Nat → Nat)
    (hp : ∀ i, p i ≤ i) (n : Nat) : ∃ f : Nat → Fin 8, IsCordial p n f :=
  Cordial.reduction (by decide) base forest p hp n

end Cordial.Eight
