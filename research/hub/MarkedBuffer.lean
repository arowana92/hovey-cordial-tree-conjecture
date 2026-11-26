import Std

namespace Cordial.MarkedBuffer

/-- The incoming weight for each new vertex. The old middle weight is restored separately. -/
def weight (x L start : Int) (f : Int → Int) (v : Int) : Int :=
  if v = x then L else if v < start then v else f v

def newVertex (x L U top v : Int) : Prop :=
  (x ≤ v ∧ v < L) ∨ (U < v ∧ v ≤ top)

def newWeight (x L U top w : Int) : Prop :=
  (x < w ∧ w ≤ L) ∨ (U < w ∧ w ≤ top)

/-- Every lower filler, upper filler, and row of the upper insertion block together
    give one copy of precisely each missing weight. -/
theorem bandBijection (x L U start top : Int) (f : Int → Int)
    (order : x < L ∧ L ≤ U ∧ U < start ∧ start ≤ top)
    (maps : ∀ z, start ≤ z → z ≤ top → start ≤ f z ∧ f z ≤ top)
    (onto : ∀ w, start ≤ w → w ≤ top → ∃ z, start ≤ z ∧ z ≤ top ∧ f z = w)
    (inj : ∀ z v, start ≤ z → z ≤ top → start ≤ v → v ≤ top → f z = f v → z = v) :
    (∀ z, newVertex x L U top z → newWeight x L U top (weight x L start f z)) ∧
    (∀ w, newWeight x L U top w →
        ∃ z, newVertex x L U top z ∧ weight x L start f z = w) ∧
    (∀ z v, newVertex x L U top z → newVertex x L U top v →
        weight x L start f z = weight x L start f v → z = v) := by
  refine ⟨?_, ?_, ?_⟩
  · intro z hz
    by_cases h : start ≤ z
    · have htop : z ≤ top := by unfold newVertex at hz; omega
      have hf := maps z h htop
      simp only [newWeight, weight, show z ≠ x by omega, show ¬z < start by omega, ite_false]
      omega
    · unfold newVertex at hz
      unfold newWeight weight
      split <;> simp_all <;> omega
  · intro w hw
    unfold newWeight at hw
    by_cases hi : start ≤ w
    · obtain ⟨z, hz, ht, he⟩ := onto w hi (by omega)
      refine ⟨z, Or.inr ⟨by omega, ht⟩, ?_⟩
      simp [weight, show z ≠ x by omega, show ¬z < start by omega, he]
    · by_cases h : w = L
      · exact ⟨x, Or.inl ⟨by omega, by omega⟩, by simp [weight, h]⟩
      · exact ⟨w, by unfold newVertex; omega, by simp [weight, show w ≠ x by omega, show w < start by omega]⟩
  · intro z v hz hv he
    unfold newVertex at hz hv
    have ztop : z ≤ top := by omega
    have vtop : v ≤ top := by omega
    by_cases za : start ≤ z <;> by_cases va : start ≤ v
    · apply inj z v za ztop va vtop
      simpa [weight, show z ≠ x by omega, show v ≠ x by omega,
        show ¬z < start by omega, show ¬v < start by omega] using he
    · have hz' := maps z za ztop
      unfold weight at he
      simp only [show z ≠ x by omega, show ¬z < start by omega, show v < start by omega, ite_false, ite_true] at he
      split at he <;> omega
    · have hv' := maps v va vtop
      unfold weight at he
      simp only [show v ≠ x by omega, show ¬v < start by omega, show z < start by omega, ite_false, ite_true] at he
      split at he <;> omega
    · simp only [weight, show z < start by omega, show v < start by omega, ite_true] at he
      split at he <;> split at he <;> omega

/-- The middle edge restores its original sum. The next block fits and doubles
    its positive endpoint, retaining the same negative attachment label. -/
theorem recurs (p q x b i : Int) (hp : 0 < p) (hq : q < 0)
    (slot : 0 ≤ i ∧ i < b) (low : x ≤ q-b-2) :
    let y := p+q-x
    let nextX := x-y
    let nextY := y+q-nextX
    x+y = p+q ∧ nextX+y = x ∧ nextX+nextY = y+q ∧
      nextX ≤ q-b-2 ∧ 2*y < nextY ∧ y+(b-1-i) < nextY-i ∧ y ≤ -nextX := by
  dsimp
  omega

end Cordial.MarkedBuffer
