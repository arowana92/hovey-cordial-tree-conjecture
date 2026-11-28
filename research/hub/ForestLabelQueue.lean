import Std

namespace Cordial.ForestLabelQueue

/-- A waiting subtree is recorded by its parent rank and its remaining order. -/
abbrev Job := Nat × Nat

def below : List Job → Nat → Nat
  | [], _ => 0
  | (p, n) :: tail, u => (if p ≤ u then n else 0) + below tail u

def demands : List Nat → Nat → Nat
  | [], _ => 0
  | x :: xs, u => (if x ≤ u then 1 else 0) + demands xs u

def dominates (q : List Job) (xs : List Nat) : Prop :=
  ∀ u, demands xs u ≤ below q u

theorem rotated_prefix (k m j : Nat) (P : Nat → Int) (hm : m ≤ k) (hj : j ≤ k)
    (endpoints : P k = P 0) (least : ∀ i ≤ k, P m ≤ P i) :
    0 ≤ (if m + j ≤ k then P (m+j) - P m
         else P k - P m + P (m+j-k) - P 0) := by
  split
  next h => have := least _ h; omega
  next _ => have := least (m+j-k) (by omega); omega

theorem has_ready (q : List Job) (u : Nat) (h : 0 < below q u) :
    ∃ j ∈ q, j.1 ≤ u := by
  induction q with
  | nil => simp [below] at h
  | cons j js ih =>
    obtain ⟨p,n⟩ := j
    by_cases hp : p ≤ u
    · exact ⟨(p,n), by simp, hp⟩
    · simp [below, hp] at h
      obtain ⟨w,hw,hr⟩ := ih h
      exact ⟨w, by simp [hw], hr⟩

theorem first_ready (q : List Job) (x : Nat) (xs : List Nat)
    (h : dominates q (x::xs)) : ∃ j ∈ q, j.1 ≤ x := by
  have := h x
  simp [demands] at this
  apply has_ready
  omega

theorem below_children (sizes : List Nat) (q : List Job) (x u : Nat) (h : x ≤ u) :
    below (sizes.map (fun n => (x,n)) ++ q) u = sizes.sum + below q u := by
  induction sizes with
  | nil => simp
  | cons n ns ih => simp [below, h, ih, Nat.add_assoc]

theorem no_demands_before (xs : List Nat) (x u : Nat)
    (h : u < x) (ordered : ∀ y ∈ xs, x ≤ y) : demands xs u = 0 := by
  induction xs with
  | nil => rfl
  | cons y ys ih =>
    have hxy := ordered y (by simp)
    have hrest := ih (fun z hz => ordered z (by simp [hz]))
    simp [demands, show ¬ y ≤ u by omega, hrest]

/-- Replacing a ready root by its children preserves all future prefix capacities.
    The chosen job is displayed first; the other waiting jobs may be in any order. -/
theorem step (p x n : Nat) (sizes xs : List Nat) (q : List Job)
    (ready : p ≤ x) (mass : n = sizes.sum + 1) (ordered : ∀ y ∈ xs, x ≤ y)
    (h : dominates ((p,n)::q) (x::xs)) :
    dominates (sizes.map (fun s => (x,s)) ++ q) xs := by
  intro u
  by_cases hx : x ≤ u
  · have hp : p ≤ u := Nat.le_trans ready hx
    have prior := h u
    simp [demands, below, hx, hp] at prior
    rw [below_children sizes q x u hx]
    omega
  · rw [no_demands_before xs x u (by omega) ordered]
    exact Nat.zero_le _

private theorem two_representatives (v k : Nat) (hv : v < k+k) :
    v = v % k ∨ v = v % k + k := by
  by_cases h : v < k
  · exact Or.inl (Nat.mod_eq_of_lt h).symm
  · right
    rw [Nat.mod_eq_sub_mod (by omega : v ≥ k), Nat.mod_eq_of_lt (by omega : v-k < k)]
    omega

theorem no_three_equal_weights (k a b c : Nat)
    (hab : a < b) (hbc : b < c) (hc : c < k+k)
    (equal₁ : a % k = b % k) (equal₂ : b % k = c % k) : False := by
  have ha := two_representatives a k (by omega)
  have hb := two_representatives b k (by omega)
  have hh := two_representatives c k hc
  omega

end Cordial.ForestLabelQueue
