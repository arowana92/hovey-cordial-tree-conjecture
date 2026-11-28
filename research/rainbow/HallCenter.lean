import Std

namespace Cordial.HallCenter

/-- Choose sources for a multiset of shifts from an available list of rows. -/
private theorem selectRows {α β : Type} [DecidableEq β] (shift : α → β)
    (rows : List α) (need : List β)
    (enough : ∀ g, need.count g ≤ (rows.map shift).count g) :
    ∃ picked : List α, picked.Sublist rows ∧ (picked.map shift).Perm need := by
  induction rows generalizing need with
  | nil =>
    cases need with
    | nil => exact ⟨[], .slnil, .nil⟩
    | cons b bs =>
      have h := enough b
      simp at h
  | cons z zs ih =>
    by_cases hz : shift z ∈ need
    · have cap (g : β) : (need.erase (shift z)).count g ≤ (zs.map shift).count g := by
        have h := enough g
        by_cases eq : shift z = g
        · subst g
          simp at h ⊢
          omega
        · simpa [List.count_erase, List.count_cons, eq, Ne.symm eq] using h
      obtain ⟨take, sub, perm⟩ := ih _ cap
      exact ⟨z :: take, sub.cons_cons z, (perm.cons _).trans (List.perm_cons_erase hz).symm⟩
    · have cap (g : β) : need.count g ≤ (zs.map shift).count g := by
        by_cases eq : shift z = g
        · subst g
          simp [List.count_eq_zero.mpr hz]
        · simpa [List.count_cons,eq] using enough g
      obtain ⟨take, sub, perm⟩ := ih _ cap
      exact ⟨take, sub.cons z, perm⟩

/-- Any injective displacement of too many center sources misses the blocked set. -/
private theorem chooseCenter {α : Type} (centers blocked : List α) (f : α → α)
    (inj : ∀ u v, f u = f v → u = v) (distinct : centers.Nodup)
    (more : blocked.length < centers.length) :
    ∃ s ∈ centers, f s ∉ blocked := by
  classical
  apply Classical.byContradiction
  intro no
  have sub : centers.map f ⊆ blocked := by
    intro v hv
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hv
    exact Classical.byContradiction (fun miss => no ⟨s,hs,miss⟩)
  have unique : (centers.map f).Nodup :=
    List.Pairwise.map f (fun u v ne h => ne (inj u v h)) distinct
  have bound := unique.length_le_of_subset sub
  simp at bound
  omega

/-- In the Hall permutation, keep the center, discard its displaced forbidden
source, and realize every remaining requested shift with distinct other rows. -/
theorem realizePinnedRows {α β : Type} [DecidableEq α] [DecidableEq β]
    (rows centers blocked : List α) (shift : α → β) (forbidden : α → α)
    (entering : β) (leaves : List β)
    (table : rows.Nodup) (choices : centers.Nodup)
    (candidate : ∀ s ∈ centers, s ∈ rows ∧ shift s = entering ∧
      forbidden s ∈ rows ∧ forbidden s ≠ s)
    (injective : ∀ u v, forbidden u = forbidden v → u = v)
    (more : blocked.length < centers.length)
    (capacity : ∀ g, (entering :: leaves).count g ≤ (rows.map shift).count g)
    (spare : ∀ z ∈ rows, z ∉ blocked →
      (entering :: leaves).count (shift z) < (rows.map shift).count (shift z)) :
    ∃ s ∈ centers, ∃ selected : List α,
      selected.Sublist ((rows.erase s).erase (forbidden s)) ∧
      (selected.map shift).Perm leaves ∧ (s :: selected).Nodup ∧ forbidden s ∉ selected := by
  obtain ⟨s, hs, free⟩ := chooseCenter centers blocked forbidden injective choices more
  obtain ⟨old, color, valid, different⟩ := candidate s hs
  let z := forbidden s
  have member : z ∈ rows.erase s := (List.mem_erase_of_ne different).mpr valid
  have first := (List.perm_cons_erase old).map shift
  have second := (List.perm_cons_erase member).map shift
  have cap (g : β) : leaves.count g ≤ (((rows.erase s).erase z).map shift).count g := by
    have h := capacity g
    have p := first.count_eq g
    have q := second.count_eq g
    by_cases eq : shift z = g
    · subst g
      have extra := spare z valid free
      simp only [List.map_cons, List.count_cons, color] at p q
      simp only [List.count_cons] at extra
      simp at q
      omega
    · simp only [List.map_cons, List.count_cons, color, beq_iff_eq, eq, ite_false] at p q
      simp only [List.count_cons, beq_iff_eq] at h
      omega
  obtain ⟨selected, sub, perm⟩ := selectRows shift _ leaves cap
  have sub' := sub.trans (List.erase_sublist (a := z))
  have kept : s ∉ selected := fun h => table.not_mem_erase (sub'.subset h)
  have absent : z ∉ selected := fun h => (table.erase s).not_mem_erase (sub.subset h)
  exact ⟨s,hs,selected,sub,perm,List.nodup_cons.mpr ⟨kept,(table.erase s).sublist sub'⟩,absent⟩

/-- The two possible forbidden-source displacements are injective modulo k. -/
theorem shiftInjective {k : Nat} [NeZero k] (x : Fin k) :
    (∀ u v : Fin k, u+x = v+x → u=v) ∧ (∀ u v : Fin k, u-x = v-x → u=v) := by
  constructor <;> intro u v h <;> grind

/-- Both translations preserve all ordinary leaf destinations. The second one
puts the formal center at zero with shift a+x, before assigning it the actual x. -/
theorem placements {k : Nat} [NeZero k] (s x a : Fin k) (nonzero : x ≠ 0) :
    (∀ y g t : Fin k, (y+g)+t = (y+t)+g) ∧
    s+(x-s) = x ∧ (s+a)+(x-s) = x+a ∧ s-x ≠ s ∧
      (∀ y : Fin k, y+(x-s)=0 ↔ y=s-x) ∧
    s-s = 0 ∧ (s+(a+x))-s = x+a ∧ s+x ≠ s ∧
      (∀ y : Fin k, y-s=x ↔ y=s+x) := by
  grind

end Cordial.HallCenter
