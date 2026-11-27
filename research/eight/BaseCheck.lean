import research.Reduction

namespace Cordial.Eight.Kernel

def factorial : Nat → Nat
  | 0 => 1
  | n+1 => (n+1)*factorial n

def parent (idx i : Nat) := (idx / factorial i) % (i+1)
def digit (word i : Nat) : Fin 8 := Fin.ofNat 8 (word >>> (3*i))

/-- The ninth packed digit is the promised missing weight. -/
def ok (row : Nat → Nat) (idx : Nat) : Bool :=
  let f := digit (row idx)
  decide ((∀ x, tally f 0 8 x = 1) ∧
    (∀ x, tally (weight (parent idx) f) 0 7 x = bump (f 8) x))

def batch (row : Nat → Nat) (lo : Nat) : Nat → Bool
  | 0 => true
  | n+1 => batch row lo n && ok row (lo+n)

theorem member {row lo n} (checked : batch row lo n = true) :
    ∀ i, lo ≤ i → i < lo+n → ok row i = true := by
  induction n with
  | zero => omega
  | succ n ih =>
    simp only [batch, Bool.and_eq_true] at checked
    intro i hlo hi
    by_cases last : i=lo+n
    · simpa [last] using checked.2
    · exact ih checked.1 i hlo (by omega)

theorem ranges {row lo mid hi}
    (l : ∀ i, lo ≤ i → i < mid → ok row i = true)
    (r : ∀ i, mid ≤ i → i < hi → ok row i = true) :
    ∀ i, lo ≤ i → i < hi → ok row i = true := by
  intro i hlo hhi
  by_cases h : i < mid
  · exact l i hlo h
  · exact r i (by omega) hhi

private theorem tally_congr {f g : Nat → Fin 8} (n : Nat)
    (h : ∀ i < n, f i = g i) (a : Fin 8) : tally f 0 n a = tally g 0 n a := by
  induction n with
  | zero => rfl
  | succ n ih => simp [tally,h n (by omega),ih (fun i hi => h i (by omega))]

theorem ofRows (row : Nat → Nat) (checked : ∀ i, i < 5040 → ok row i = true) :
    BaseTest 8 := by
  intro p hp
  let idx := p 1 + 2*p 2 + 6*p 3 + 24*p 4 + 120*p 5 + 720*p 6
  have h0 := hp 0
  have h1 := hp 1
  have h2 := hp 2
  have h3 := hp 3
  have h4 := hp 4
  have h5 := hp 5
  have h6 := hp 6
  have bound : idx < 5040 := by dsimp [idx]; omega
  have eqp (i : Nat) (hi : i < 7) : p i = parent idx i := by
    have cases : i=0 ∨ i=1 ∨ i=2 ∨ i=3 ∨ i=4 ∨ i=5 ∨ i=6 := by omega
    rcases cases with h|h|h|h|h|h|h <;> subst i <;>
      simp [parent,factorial,idx] <;> omega
  let f := digit (row idx)
  have valid := of_decide_eq_true (checked idx bound)
  change (∀ x, tally f 0 8 x = 1) ∧
    (∀ x, tally (weight (parent idx) f) 0 7 x = bump (f 8) x) at valid
  refine ⟨f,f 8,valid.1,?_⟩
  intro x
  have same := tally_congr (f:=weight p f) (g:=weight (parent idx) f) 7
    (fun i hi => by simp [weight,eqp i hi]) x
  simpa using same.trans (valid.2 x)

end Cordial.Eight.Kernel
