import Std

namespace Cordial.HistogramLift

/-- Assign each occurrence in one residue class to a slot among its r lifts. -/
def slots (r h : Nat) : List Nat :=
  List.range (min h r) ++ List.replicate (h-r) 0

theorem slotsLength (r h : Nat) : (slots r h).length = h := by
  simp [slots]
  omega

/-- The occupied slots form one initial interval, even when the bin is overfull. -/
theorem occupied {r h i : Nat} (hr : 0 < r) :
    i ∈ slots r h ↔ i < min h r := by
  simp only [slots, List.mem_append, List.mem_range, List.mem_replicate]
  constructor
  · rintro (h1 | ⟨h1, h2⟩)
    · exact h1
    · omega
  · exact Or.inl

theorem omittedSlots {r h i : Nat} (hr : 0 < r) (hi : i < r) :
    i ∉ slots r h ↔ h ≤ i := by
  rw [occupied hr]
  omega

theorem slotResidue {k x : Nat} (hx : x < k) (i : Nat) :
    (x+k*i)%k = x := by
  simp [Nat.add_mod, Nat.mod_eq_of_lt hx]

theorem slotUnique {k x y i j : Nat} (hx : x < k) (hy : y < k)
    (eq : x+k*i = y+k*j) : x = y ∧ i = j := by
  have same := congrArg (fun a => a % k) eq
  change (x+k*i)%k = (y+k*j)%k at same
  rw [slotResidue hx, slotResidue hy] at same
  subst y
  have prod : k*i = k*j := Nat.add_left_cancel eq
  exact ⟨rfl, Nat.eq_of_mul_eq_mul_left (by omega) prod⟩

/-- A switch adds its increment to the true vertex label and to the temporary
offset at each incident edge. This identity applies before modular reduction. -/
theorem switchedEdge (x y u v bias : Int) :
    (x+u)+(y+v)+bias = x+y+(bias+u+v) := by omega

/-- The first coordinate is degree, and the second is actual minus temporary label. -/
def shiftMoment (j : Int) (switches : List (Int × Int)) : Int :=
  (switches.map (fun (d,e) => (d-j)*e)).sum

theorem shiftedMoment (j : Int) (switches : List (Int × Int)) :
    shiftMoment j switches =
      shiftMoment 0 switches - j * (switches.map Prod.snd).sum := by
  induction switches with
  | nil => simp [shiftMoment]
  | cons s tail ih =>
    obtain ⟨d,e⟩ := s
    simp only [shiftMoment, List.map_cons, List.sum_cons, Int.sub_zero] at ih ⊢
    rw [ih, Int.sub_mul, Int.mul_add]
    omega

end Cordial.HistogramLift
