import research.Reduction

namespace Cordial.Eight

abbrev ForestParent := Nat → Fin 8 ⊕ Nat

/-- A reindexing preserves both the new endpoints and all original boundary colors. -/
structure Reindex (r : Nat) (p q : ForestParent) where
  ren : Nat → Nat
  perm : ((List.range r).map ren).Perm (List.range r)
  edge : ∀ i < r, q (ren i) = (p i).map id ren

private theorem tally_count (g : Nat → Fin 8) (n : Nat) (a : Fin 8) :
    tally g 0 n a = ((List.range n).map g).count a := by
  induction n with
  | zero => simp [tally]
  | succ n ih =>
    by_cases h : g n = a
    · simp [tally, List.range_succ, ih, List.count_append, h]
    · simp [tally, List.range_succ, ih, List.count_append, h]

theorem Reindex.lt {r p q} (m : Reindex r p q) {i : Nat} (hi : i < r) : m.ren i < r := by
  apply List.mem_range.mp
  apply m.perm.mem_iff.mp
  exact List.mem_map.mpr ⟨i,List.mem_range.mpr hi,rfl⟩

def Reindex.comp {r p q s} (u : Reindex r p q) (v : Reindex r q s) : Reindex r p s where
  ren := v.ren ∘ u.ren
  perm := by simpa [List.map_map] using (u.perm.map v.ren).trans v.perm
  edge := by
    intro i hi
    simp only [Function.comp_apply, v.edge _ (u.lt hi), u.edge _ hi]
    cases p i <;> rfl

private theorem reindex_tally {r p q} (m : Reindex r p q) (g : Nat → Fin 8) (a : Fin 8) :
    tally (g ∘ m.ren) 0 r a = tally g 0 r a := by
  simpa [tally_count, List.map_map] using (m.perm.map g).count_eq a

theorem Reindex.fits {r p q} (m : Reindex r p q) (g : Nat → Fin 8) (d : Fin 8)
    (h : Fits q g r d) : Fits p (g ∘ m.ren) r d := by
  have weights (a : Fin 8) :
      tally (localWeight p (g ∘ m.ren)) 0 r a = tally (localWeight q g) 0 r a := by
    rw [← reindex_tally m (localWeight q g) a, tally_count, tally_count]
    congr 1
    apply List.map_congr_left
    intro i hi
    simp only [Function.comp_apply, localWeight, m.edge i (List.mem_range.mp hi)]
    cases p i <;> rfl
  simpa only [Fits, reindex_tally m g, weights] using h

def appendParent (q : ForestParent) (r : Nat) (a : Fin 8 ⊕ Nat) : ForestParent :=
  fun i => if i = r then a else q i

/-- Add the same new leaf, expressed at the reindexed parent of the old row. -/
def Reindex.grow {r p q} (m : Reindex r p q)
    (valid : ∀ j < r+1, ∀ i, p j = .inr i → i < j) :
    Reindex (r+1) p (appendParent q r ((p r).map id m.ren)) := by
  let next := fun i => if i=r then r else m.ren i
  refine ⟨next, ?_, ?_⟩
  · have old : (List.range r).map next = (List.range r).map m.ren := by
      apply List.map_congr_left
      intro i hi
      simp [next, Nat.ne_of_lt (List.mem_range.mp hi)]
    simpa [List.range_succ, List.map_append, old, next] using
      m.perm.append_right [r]
  · intro i hi
    by_cases last : i=r
    · subst i
      simp only [next, ite_eq_left rfl, appendParent]
      cases hp : p r with
      | inl a => rfl
      | inr j =>
        have hn := Nat.ne_of_lt (valid r (by omega) j hp)
        simp [Sum.map, hn]
    · have less : i < r := by omega
      have before := Nat.ne_of_lt (m.lt less)
      simp only [next, ite_eq_right last, appendParent, ite_eq_right before, m.edge i less]
      cases hp : p i with
      | inl a => rfl
      | inr j =>
        have hj := valid i hi j hp
        have hn : j ≠ r := by omega
        simp [Sum.map, hn]

end Cordial.Eight
