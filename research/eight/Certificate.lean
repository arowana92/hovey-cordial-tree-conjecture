import research.eight.Base
import research.eight.Representation
import research.eight.Data

namespace Cordial.Eight

private abbrev Color := Fin 8

private def size (r : Nat) := Data.sizes[r]?.getD 0
private def digit (data : ByteArray) (i : Nat) := (data[i]?.getD 0).toNat - 32

private def encode : Color ⊕ Nat → Nat
  | .inl a => a.val
  | .inr i => 8+i

private def decode (n : Nat) : Color ⊕ Nat :=
  if h : n < 8 then .inl ⟨n,h⟩ else .inr (n-8)

private theorem decode_encode (a : Color ⊕ Nat) : decode (encode a) = a := by
  cases a with
  | inl a => simp [decode,encode,a.isLt]
  | inr i => simp [decode,encode]

private def rowStart (r j : Nat) := Data.rowOffsets[r]?.getD 0 + j*(9*r)
private def parent (r j i : Nat) := decode (digit Data.rows (rowStart r j+i))
private def labels (r j : Nat) (d : Color) (i : Nat) : Color :=
  Fin.ofNat 8 (digit Data.rows (rowStart r j + (d.val+1)*r+i))

-- Count all residues in one pass. Vector indexing keeps the eight rows explicit.
private def histogram (f : Nat → Color) : Nat → Vector Nat 8
  | 0 => Vector.replicate 8 0
  | n+1 =>
    let h := histogram f n
    let a := f n
    h.set a.val (h[a.val]+1)

private theorem histogram_eq (f : Nat → Color) (n : Nat) (a : Color) :
    (histogram f n)[a.val] = tally f 0 n a := by
  induction n with
  | zero => simp [histogram,tally]
  | succ n ih =>
    by_cases same : f n = a
    · simp [histogram,tally,same,ih]
    · have ne : (f n).val ≠ a.val := fun h => same (Fin.ext h)
      simp [histogram,tally,same,ne,ih]

private def hasWitness (r j : Nat) (d : Color) : Bool :=
  let g := labels r j d
  let v := histogram g r
  let e := histogram (localWeight (parent r j) g) r
  let next := ((List.finRange 8).find? (fun a => bump d a + e[a.val] == 1)).getD 0
  decide ((∀ a : Color, v[a.val] ≤ 1) ∧
    (∀ a : Color, 1 ≤ bump d a + e[a.val] ∧ bump d a + e[a.val] ≤ 2) ∧
    (r = 8 → (∀ a : Color, v[a.val] = 1) ∧
             (∀ a : Color, bump d a + e[a.val] = 1 + bump next a)))

private theorem witness_ok {r j : Nat} {d : Color} (checked : hasWitness r j d = true) :
    Fits (parent r j) (labels r j d) r d := by
  simp only [hasWitness, decide_eq_true_eq, histogram_eq] at checked
  exact ⟨checked.1,checked.2.1, fun hr => ⟨_,checked.2.2 hr⟩⟩

private def transitionStart (r j a : Nat) :=
  Data.stepOffsets[r]?.getD 0 + (j*(8+r)+a)*(4+r)
private def target (r j a : Nat) :=
  let i := transitionStart r j a
  digit Data.steps i + 64*digit Data.steps (i+1) + 4096*digit Data.steps (i+2)
private def renumber (r j a i : Nat) := digit Data.steps (transitionStart r j a+3+i)

private def validStep (r j a : Nat) : Bool :=
  let k := target r j a
  let ren := renumber r j a
  let raw := appendParent (parent r j) r (decode a)
  decide (k < size (r+1) ∧ ((List.range (r+1)).map ren).Perm (List.range (r+1)) ∧
    ∀ i : Fin (r+1), parent (r+1) k (ren i.val) = (raw i.val).map id ren)

private def every (n : Nat) (check : Nat → Bool) := (List.range n).all check
private theorem every_ok {n : Nat} {check : Nat → Bool} (h : every n check = true)
    {i : Nat} (hi : i < n) : check i = true := by
  exact (List.all_eq_true.mp h) i (List.mem_range.mpr hi)

private theorem witnessesChecked :
    every 8 (fun t => every (size (t+1)) (fun j =>
      (List.finRange 8).all (hasWitness (t+1) j))) = true := by native_decide

private theorem stepsChecked :
    every 8 (fun r => every (size r) (fun j => every (8+r) (validStep r j))) = true := by
  native_decide

private theorem findRow (r : Nat) (hr : r ≤ 8) (p : ForestParent)
    (hp : ∀ j < r, ∀ i, p j = .inr i → i < j) :
    ∃ j, j < size r ∧ Nonempty (Reindex r p (parent r j)) := by
  induction r with
  | zero =>
    exact ⟨0,by decide,⟨⟨id,by simp,by omega⟩⟩⟩
  | succ r ih =>
    have lt : r < 8 := by omega
    obtain ⟨j,hj,⟨m⟩⟩ := ih (by omega) (fun i hi => hp i (by omega))
    let a := (p r).map id m.ren
    have good : encode a < 8+r := by
      cases h : p r with
      | inl c => have := c.isLt; simp [a,h,encode,Sum.map]; omega
      | inr i =>
        have hi := m.lt (hp r (by omega) i h)
        simp [a,h,encode,Sum.map,hi]
    have certified := every_ok (every_ok (every_ok stepsChecked lt) hj) good
    simp only [validStep,decide_eq_true_eq,decode_encode] at certified
    let ren := renumber r j (encode a)
    let k := target r j (encode a)
    have step : Reindex (r+1) (appendParent (parent r j) r a) (parent (r+1) k) :=
      ⟨ren,certified.2.1,fun i hi => certified.2.2 ⟨i,hi⟩⟩
    exact ⟨k,certified.1,⟨(m.grow hp).comp step⟩⟩

/-- All colored attachments and all eight deficient edge residues. -/
theorem forest : ForestTest 8 := by
  intro r positive small p hp d
  obtain ⟨j,hj,⟨m⟩⟩ := findRow r small p hp
  obtain ⟨t,rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt positive)
  have records := every_ok (every_ok witnessesChecked (show t < 8 by omega)) hj
  have row := List.all_eq_true.mp records d (List.mem_finRange d)
  exact ⟨_,m.fits _ _ (witness_ok row)⟩

/-- Every finite parent-array tree is eight-cordial, with no certificate hypothesis. -/
theorem allTrees (p : Nat → Nat) (hp : ∀ i, p i ≤ i) (n : Nat) :
    ∃ f : Nat → Fin 8, IsCordial p n f := reduction forest p hp n

end Cordial.Eight

#print axioms Cordial.Eight.allTrees
