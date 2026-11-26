import Std

namespace Cordial.OrderedCut

/-- The outermost group comes first. Inside a group all roots have one parent. -/
abbrev Groups := List (List Nat)

def mass : Groups → Nat
  | [] => 0
  | g :: rest => g.sum + mass rest

/-- A preorder cut either stops at a vertex, or lies inside one child.
    'done' counts vertices of completed sibling subtrees. -/
inductive Trace : Nat → Groups → Prop where
  | stop (done : Nat) (g : List Nat) (positive : ∀ s ∈ g, 0 < s) :
      Trace (1 + done + g.sum) [g]
  | ascend {size : Nat} {inner : Groups} (child : Trace size inner)
      (done : Nat) (g : List Nat) (ordered : ∀ s ∈ g, size ≤ s) :
      Trace (1 + done + size + g.sum) (g :: inner)

def separated : Groups → Prop
  | [] => True
  | g :: inner => (∀ s ∈ g, mass inner < s) ∧ separated inner

theorem trace_separated {size : Nat} {groups : Groups} (h : Trace size groups) :
    mass groups < size ∧ separated groups := by
  induction h with
  | stop done g hp =>
    simp [mass, separated]
    exact ⟨by omega, hp⟩
  | ascend child done g ordered ih =>
    obtain ⟨bound, sep⟩ := ih
    exact ⟨by simp only [mass]; omega,
      fun s hs => Nat.lt_of_lt_of_le bound (ordered s hs), sep⟩

def occupied : Groups → Nat
  | [] => 0
  | [] :: gs => occupied gs
  | (_ :: _) :: gs => occupied gs + 1

/-- Every occupied boundary parent on the cut path is itself in the prefix. -/
theorem trace_room {size : Nat} {groups : Groups} (h : Trace size groups) :
    mass groups + occupied groups ≤ size := by
  induction h with
  | stop done g hp =>
    cases g <;> simp [mass, occupied] <;> omega
  | ascend child done g ordered ih =>
    cases g <;> simp only [mass, occupied, List.sum_nil, Nat.zero_add] <;> omega

def exactSeparation : Groups → Prop
  | [] => True
  | g :: inner => (∀ s ∈ g, mass inner + occupied inner ≤ s) ∧ exactSeparation inner

theorem trace_exact {size : Nat} {groups : Groups} (h : Trace size groups) :
    exactSeparation groups := by
  induction h with
  | stop done g hp => simp [exactSeparation, mass, occupied]
  | ascend child done g ordered ih =>
    exact ⟨fun s hs => Nat.le_trans (trace_room child) (ordered s hs), ih⟩

theorem group_bound (groups : Groups) (h : separated groups) :
    2 ^ occupied groups ≤ mass groups + 1 := by
  induction groups with
  | nil => decide
  | cons g inner ih =>
    obtain ⟨larger, sub⟩ := h
    have old := ih sub
    cases g with
    | nil => simpa [occupied, mass] using old
    | cons s rest =>
      have head := larger s (by simp)
      simp only [occupied, Nat.pow_succ, mass, List.sum_cons]
      omega

end Cordial.OrderedCut
