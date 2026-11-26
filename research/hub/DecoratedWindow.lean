import Std

namespace Cordial.DecoratedWindow

/-- Truncate the final column and omit the first row of the 40 translated
forward/reverse bridge vectors. The rows have zero sum before truncation. -/
def slopes : Array Int :=
  #[14,14,28,42,-112,70,56,-42,-70,126,-126,72,45,-54,-72,117,-45,-27,-18,-9,-9]

abbrev I := Fin 39

def windowEntry (row col : Nat) : Int :=
  let start := row / 2
  if col < start || col ≥ start + 21 then 0 else
    let pos := col - start
    slopes[if row % 2 = 0 then pos else 20 - pos]!

def entry (i j : I) := windowEntry (i.val + 1) j.val

def indices := List.finRange 39

/-- Build integer linear combinations by eliminating the left half of [M | I].
Correctness uses direct multiplication back into M below. -/
def diagonalize : Array (Array Int) := Id.run do
  let mut a := indices.toArray.map fun i =>
    (indices.toArray.map (entry i)) ++ indices.toArray.map (fun j => if i = j then 1 else 0)
  for i in [:39] do
    let some p := (List.range 39).find? (fun j => j ≥ i && a[j]![i]! != 0) | return #[]
    a := a.swapIfInBounds i p
    let pivot := a[i]!
    for j in [:39] do
      let b := a[j]![i]!
      if j != i && b != 0 then
        let row := a[j]!.zipWith (fun u v => pivot[i]! * u - b * v) pivot
        let divisor := row.foldl (fun g u => Nat.gcd g u.natAbs) 0
        a := a.set! j (row.map (fun u => u / (divisor : Int)))
  return a

def certificate := diagonalize

def eval {α : Type} : List α → (α → Int) → (α → Int) → Int
  | [], _, _ => 0
  | i :: rest, f, x => f i * x i + eval rest f x

def coefficient (i j : I) := certificate[i.val]![39+j.val]!
def diagonal (i : I) := certificate[i.val]![i.val]!

theorem sumsZero : slopes.toList.sum = 0 := by decide

theorem checkedInverse :
    (∀ i : I, diagonal i ≠ 0) ∧
    (∀ i j : I, eval indices (coefficient i) (fun r => entry r j) =
      if j = i then diagonal i else 0) := by native_decide

private theorem evalZero {α} (js : List α) (x : α → Int) :
    eval js (fun _ => 0) x = 0 := by
  induction js with
  | nil => rfl
  | cons j rest ih => simp [eval, ih]

private theorem evalAddMul {α} (js : List α) (f g x : α → Int) (c : Int) :
    eval js (fun j => c*f j + g j) x = c * eval js f x + eval js g x := by
  induction js with
  | nil => simp [eval]
  | cons j rest ih =>
    simp only [eval, ih, Int.add_mul, Int.mul_add, Int.mul_assoc]
    omega

private theorem evalCombination (rs : List I) (f x : I → Int)
    (h : ∀ r, eval indices (entry r) x = 0) :
    eval indices (fun j => eval rs f (fun r => entry r j)) x = 0 := by
  induction rs with
  | nil => exact evalZero indices x
  | cons r rest ih =>
    change eval indices (fun j => f r * entry r j + eval rest f (fun s => entry s j)) x = 0
    rw [evalAddMul, h, ih]
    simp

private theorem evalPoint (js : List I) (i : I) (v : Int) (x : I → Int) (h : js.Nodup) :
    eval js (fun j => if j = i then v else 0) x = if i ∈ js then v*x i else 0 := by
  induction js with
  | nil => simp [eval]
  | cons j rest ih =>
    obtain ⟨hne, ht⟩ := List.nodup_cons.mp h
    by_cases eq : j = i
    · subst j
      simp [eval, ih ht, hne]
    · simp [eval, ih ht, eq, Ne.symm eq]

/-- The square integer minor has trivial kernel for arbitrary integer data. -/
theorem trivialKernel (x : I → Int) (h : ∀ r, eval indices (entry r) x = 0) (i : I) :
    x i = 0 := by
  have hi := evalCombination indices (coefficient i) x h
  have eq : (fun j => eval indices (coefficient i) (fun r => entry r j)) =
      (fun j => if j = i then diagonal i else 0) := funext (checkedInverse.2 i)
  rw [eq] at hi
  have nodup : indices.Nodup := by decide
  have mem : i ∈ indices := (by decide : ∀ t : I, t ∈ indices) i
  rw [evalPoint indices i (diagonal i) x nodup, ite_eq_left mem] at hi
  exact (Int.mul_eq_zero.mp hi).resolve_left (checkedInverse.1 i)

private theorem evalDiff (js : List I) (f x : I → Int) (z : Int) :
    eval js f (fun j => x j-z) = eval js f x - eval js f (fun _ => 1) * z := by
  induction js with
  | nil => simp [eval]
  | cons j rest ih =>
    simp only [eval, ih, Int.mul_sub, Int.add_mul, Int.mul_one]
    omega

theorem rowSums : ∀ r : I, eval indices (entry r) (fun _ => 1) =
    -windowEntry (r.val+1) 39 := by native_decide

/-- If all the forward and reverse windows vanish, each of the first
39 counts equals the last count. Even the first window equation is redundant. -/
theorem constantCounts (x : I → Int) (last : Int)
    (h : ∀ r, eval indices (entry r) x + windowEntry (r.val+1) 39 * last = 0)
    (i : I) : x i = last := by
  have eq : ∀ r, eval indices (entry r) (fun j => x j-last) = 0 := by
    intro r
    rw [evalDiff, rowSums, Int.neg_mul]
    have := h r
    omega
  have := trivialKernel (fun j => x j-last) eq i
  omega

theorem oppositeRoots (j d : Int) : [j+d, -j+(d+j)] = [d+j,d] := by
  simp only [List.cons.injEq, and_true]
  omega

end Cordial.DecoratedWindow
